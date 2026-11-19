#!/usr/bin/env python3
"""Build, check, and render Beamer decks.

  build DECK.tex    compile with an available engine, then print the check report
  check DECK.tex    report errors and layout warnings by PDF page from the last build
  render FILE.pdf   render pages to PNG, optionally as contact sheets or with a point grid

Standard library only. `render` needs Poppler's pdftoppm and pdfinfo; `--sheet` and
`--grid` also need Pillow.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ENGINES = ("xelatex", "lualatex", "pdflatex", "tectonic")
UNICODE_CLASSES = {"ctexbeamer", "ctexart", "ctexrep", "ctexbook"}
UNICODE_PACKAGES = {"fontspec", "xeCJK", "ctex", "unicode-math", "luatexja", "luatexja-fontspec"}
THEME_PREFIXES = {
    "usetheme": "beamertheme", "usecolortheme": "beamercolortheme",
    "usefonttheme": "beamerfonttheme", "useinnertheme": "beamerinnertheme",
    "useoutertheme": "beameroutertheme",
}
OPTIONAL = r"(?:\[[^\]]*\])?"
INCLUDE = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
NOTES_WRAPPER = """% Presenter version: the same deck with speaker notes on a second screen.
\\def\\presenternotes{{}}
\\input{{{stem}}}
"""


def strip_comments(text):
    return re.sub(r"(?<!\\)%.*", "", text)


def read(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def deck_sources(tex):
    """The main file and the .tex files it inputs, in reading order."""
    seen, order, pending = set(), [], [tex]
    while pending:
        path = pending.pop(0)
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        order.append(path)
        for name in INCLUDE.findall(strip_comments(read(path))):
            child = tex.parent / name.strip()
            pending.append(child if child.suffix == ".tex" else child.with_name(child.name + ".tex"))
    return order


def requirements(text):
    """Return (files to look up with kpsewhich, whether a Unicode engine is needed)."""
    body = strip_comments(text)
    files, packages = [], set()
    cls = re.search(r"\\documentclass\s*" + OPTIONAL + r"\s*\{([^}]+)\}", body)
    cls = cls.group(1).strip() if cls else ""
    if cls:
        files.append(cls + ".cls")
    for match in re.finditer(r"\\(?:usepackage|RequirePackage)\s*" + OPTIONAL + r"\s*\{([^}]+)\}", body):
        packages.update(p.strip() for p in match.group(1).split(",") if p.strip())
    files += sorted(p + ".sty" for p in packages)
    for command, prefix in THEME_PREFIXES.items():
        for match in re.finditer("\\\\" + command + r"\s*" + OPTIONAL + r"\s*\{([^}]+)\}", body):
            files += [prefix + t.strip() + ".sty" for t in match.group(1).split(",") if t.strip()]
    cjk = re.search(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\uff00-\uffef]", body)
    unicode = cls in UNICODE_CLASSES or bool(packages & UNICODE_PACKAGES) or bool(cjk)
    return files, unicode


def missing_tex_files(files, folder):
    if not shutil.which("kpsewhich"):
        return files
    missing = []
    for name in files:
        found = subprocess.run(["kpsewhich", name], cwd=folder, capture_output=True, text=True)
        if not found.stdout.strip():
            missing.append(name)
    return missing


def choose_engine(tex, requested):
    if requested != "auto":
        if not shutil.which(requested):
            sys.exit(f"{requested} is not installed")
        return requested, "requested"
    sources = deck_sources(tex)
    text = "\n".join(read(path) for path in sources)
    files, unicode = requirements(text)
    candidates = ["xelatex", "lualatex"] if unicode else ["pdflatex", "xelatex", "lualatex"]
    notes = []
    for path in sources:
        head = "\n".join(read(path).splitlines()[:30])
        magic = re.search(r"%\s*!\s*TE?X\s+(?:TS-)?program\s*=\s*(\w+)", head, re.IGNORECASE)
        if magic:
            wanted = magic.group(1).lower()
            if wanted in candidates and shutil.which(wanted):
                candidates.remove(wanted)
                candidates.insert(0, wanted)
            elif wanted in ENGINES:
                notes.append(f"magic comment asks for {wanted}, which is not installed or not suitable")
            break
    installed = [engine for engine in candidates if shutil.which(engine)]
    missing = missing_tex_files(files, tex.parent) if installed else []
    if installed and not missing:
        notes.insert(0, "Unicode source" if unicode else "pdfLaTeX-compatible source")
        return installed[0], "; ".join(notes)
    if shutil.which("tectonic"):
        notes.insert(0, f"local TeX lacks {', '.join(missing)}" if missing else "no suitable TeX engine")
        return "tectonic", "; ".join(notes)
    if installed:
        sys.exit(f"Missing TeX files: {', '.join(missing)}. Install them or Tectonic.")
    sys.exit("No usable engine: install TeX Live/MiKTeX (xelatex or lualatex for Unicode) or Tectonic.")


def run(cmd, folder, timeout, env):
    try:
        return subprocess.run(cmd, cwd=folder, capture_output=True, text=True,
                              errors="replace", timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        sys.exit(f"Timed out after {timeout}s: {' '.join(cmd)}")


def build(tex, engine, timeout):
    folder, name, stem = tex.parent, tex.name, tex.stem
    # Wide log lines keep warnings on one line for TeX Live engines.
    env = dict(os.environ, max_print_line="1000", error_line="254", half_error_line="238")
    if engine == "tectonic":
        return run(["tectonic", "--keep-logs", "--keep-intermediates", name], folder, timeout, env)
    base = [engine, "-interaction=nonstopmode", "-file-line-error"]
    if shutil.which("latexmk"):
        flag = {"pdflatex": "-pdf", "xelatex": "-pdfxe", "lualatex": "-pdflua"}[engine]
        return run(["latexmk", flag] + base[1:] + [name], folder, timeout, env)
    result = run(base + [name], folder, timeout, env)
    if (folder / f"{stem}.bcf").exists() and shutil.which("biber"):
        run(["biber", stem], folder, timeout, env)
    elif "\\bibdata" in read(folder / f"{stem}.aux") and shutil.which("bibtex"):
        run(["bibtex", stem], folder, timeout, env)
    for _ in range(2):
        result = run(base + [name], folder, timeout, env)
        if not re.search(r"Rerun to get|may have changed", read(folder / f"{stem}.log")):
            break
    return result


def unwrap(log):
    """Join lines that TeX wrapped at its default 79-column limit."""
    lines, buffer = [], ""
    for line in log.split("\n"):
        buffer += line
        if len(line) != 79 and len(line.encode("utf-8")) != 79:
            lines.append(buffer)
            buffer = ""
    lines.append(buffer)
    return "\n".join(lines)


def shipouts(log):
    """(offset, page) where pages are shipped. Numbers must increase by one, or by two when
    a marker is missing, as with pgfpages, which does not print the first one."""
    marks = []
    for match in re.finditer(r"\[(\d+)(?=[\s\]<{(]|$)", log):
        number, last = int(match.group(1)), marks[-1][1] if marks else 0
        if last < number <= last + 2:
            marks.append((match.start(), number))
    return marks


def open_files(log, folder):
    """Checkpoints (offset, innermost open source file) from TeX's parenthesized file trace."""
    stack, points, offset = [], [], 0
    skip_next = False
    for line in log.split("\n"):
        # Box dumps and error context echo document text, whose parentheses are not file marks.
        skip = skip_next or line.startswith("[]") or re.match(r"\\[A-Z0-9]+/|l\.\d+ ", line)
        skip_next = bool(re.match(r"l\.\d+ ", line))
        if not skip:
            for match in re.finditer(r"\(([^\s()]+)|[()]", line):
                token = match.group(0)
                if token == ")":
                    if stack:
                        stack.pop()
                elif token == "(":
                    stack.append(None)
                else:
                    stack.append(source_file(match.group(1), folder))
                points.append((offset + match.start(), next((f for f in reversed(stack) if f), None)))
        offset += len(line) + 1
    return points


def source_file(name, folder):
    """Resolve a file name from the log to a deck source (.tex or .vrb), else None."""
    path = Path(name) if Path(name).is_absolute() else folder / name
    for candidate in (path, path.with_name(path.name + ".tex")):
        if candidate.suffix in (".tex", ".vrb") and candidate.is_file():
            return candidate.resolve()
    return None


def file_at(points, position):
    current = None
    for offset, path in points:
        if offset > position:
            break
        current = path
    return current


def frame_titles(path):
    """Line spans of the frames in one source file, with their titles."""
    text = read(path)
    spans = []
    for match in re.finditer(r"\\begin\{frame\}(.*?)\\end\{frame\}", text, re.DOTALL):
        start = text.count("\n", 0, match.start()) + 1
        end = text.count("\n", 0, match.end()) + 1
        inner = match.group(1)
        title = re.match(r"\s*(?:<[^>]*>)?\s*(?:\[[^\]]*\])?\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", inner)
        title = title or re.search(r"\\frametitle\s*(?:<[^>]*>)?\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", inner)
        spans.append((start, end, " ".join(title.group(1).split()) if title else ""))
    return spans


def source_notes(sources):
    notes = []
    for path in sources:
        prefix = "" if path == sources[0] else f"{path.name} "
        for number, line in enumerate(read(path).splitlines(), 1):
            line = strip_comments(line)
            options = re.search(r"\\begin\{frame\}\s*(?:<[^>]*>)?\s*\[([^\]]*)\]", line)
            if options:
                for option in ("shrink", "allowframebreaks"):
                    if option in options.group(1):
                        notes.append(f"{prefix}line {number}: frame option {option}")
            if "\\tiny" in line:
                notes.append(f"{prefix}line {number}: \\tiny")
    return notes


def check(tex, min_pt):
    stem, folder = tex.stem, tex.parent
    raw = read(folder / f"{stem}.log")
    pdf = folder / f"{stem}.pdf"
    if not raw:
        print(f"No log at {folder / (stem + '.log')}; build the deck first.")
        return 1
    log = unwrap(raw)
    offsets = shipouts(log)
    files = open_files(log, folder)
    frames = [(int(a), int(b)) for a, b in
              re.findall(r"\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}", read(folder / f"{stem}.nav"))]
    pages = frames[-1][1] if frames else (offsets[-1][1] if offsets else 0)
    sources = deck_sources(tex)
    titles = {}

    def frame_of(page):
        for index, (first, last) in enumerate(frames, 1):
            if first <= page <= last:
                return index
        return None

    def where(position, line=None):
        page = page_at(offsets, position)
        frame = frame_of(page)
        label = f"p.{page}" + (f" (frame {frame})" if frame and len(frames) != pages else "")
        if not line:
            return page, label
        source = file_at(files, position) or tex
        if source.suffix == ".vrb":
            return page, f"{label} fragile frame, line {line} of {source.name}"
        if source not in titles:
            titles[source] = frame_titles(source)
        title = next((t for start, end, t in titles[source] if start <= line <= end), "")
        place = f"line {line}" if source == tex else f"line {line} of {source.relative_to(folder) if source.is_relative_to(folder) else source}"
        return page, f"{label} {place}" + (f' "{title}"' if title else "")

    errors = []
    for match in re.finditer(r"^(?:! (.+)|(?:\./)?[^\s:]+\.(?:tex|sty|cls|def|vrb):(\d+): (.+))$", log, re.MULTILINE):
        message = match.group(1) or match.group(3)
        line = int(match.group(2)) if match.group(2) else None
        if line is None:
            follow = re.search(r"^l\.(\d+)", log[match.end():match.end() + 2000], re.MULTILINE)
            line = int(follow.group(1)) if follow else None
        entry = f"{where(match.start(), line)[1]}: {message.strip()}"
        if entry not in errors:
            errors.append(entry)

    overflow, small = {}, 0
    pattern = (r"Overfull \\([hv])box \(([\d.]+)pt too (?:wide|high)\) "
               r"(?:in (?:paragraph|alignment) at lines (\d+)--\d+|detected at line (\d+)|has occurred while)")
    for match in re.finditer(pattern, log):
        amount = float(match.group(2))
        if amount < min_pt:
            small += 1
            continue
        line = int(match.group(3) or match.group(4) or 0) or None
        page, label = where(match.start(), line)
        kind = "too wide" if match.group(1) == "h" else "too high"
        key = (frame_of(page) or page, match.group(1), label.split(" ", 1)[-1])
        if key not in overflow or amount > overflow[key][1]:
            overflow[key] = (page, amount, f"{label}: {amount:.1f}pt {kind}")

    shrunk = [f"{where(m.start())[1]}: shrunk by {m.group(1)}%"
              for m in re.finditer(r"Frame text is shrunk by a factor of\s+([\d.]+)", log)]
    glyphs = sorted({f"{m.group(1).strip()} in {re.split(r'[/:]', m.group(2))[0]}"
                     for m in re.finditer(r"Missing character: There is no (.+?) in font (.+?)!", log)})
    undefined = sorted(set(re.findall(r"LaTeX Warning: ((?:Citation|Reference) [`'].+?' on page \d+) undefined", log)))
    shapes = sorted(set(re.findall(r"Font shape [`']([^']+)' undefined", log)))

    if pdf.exists():
        print(f"{pdf.name}: {pages} pages" + (f", {len(frames)} frames" if frames and len(frames) != pages else ""))
    else:
        print(f"{pdf.name}: not produced")
    sections = [
        ("Errors", errors[:15]),
        (f"Overflow >= {min_pt:g}pt" + (f" ({small} smaller ignored)" if small else ""),
         [text for _, _, text in sorted(overflow.values())]),
        ("Shrunk frames", shrunk),
        ("Missing glyphs", glyphs),
        ("Undefined", undefined),
        ("Font substitutions", shapes),
        ("Source notes", source_notes(sources)),
    ]
    for heading, items in sections:
        print(f"{heading}: {'none' if not items else ''}")
        for item in items:
            print(f"  {item}")
    flagged = sorted({page for page, _, _ in overflow.values()})
    if flagged:
        print(f"Render to inspect: --pages {','.join(map(str, flagged))}")
    return 1 if errors or not pdf.exists() else 0


def page_at(marks, position):
    return max((page for offset, page in marks if offset < position), default=0) + 1


def page_list(spec, total):
    if not spec:
        return list(range(1, total + 1))
    pages = []
    for part in spec.split(","):
        first, _, last = part.strip().partition("-")
        pages += range(int(first), int(last or first) + 1)
    return [p for p in dict.fromkeys(pages) if 1 <= p <= total]


def pdf_info(pdf, page=None):
    cmd = ["pdfinfo"] + (["-f", str(page), "-l", str(page)] if page else []) + [str(pdf)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def render(pdf, spec, dpi, out, sheet, grid):
    if not (shutil.which("pdftoppm") and shutil.which("pdfinfo")):
        sys.exit("pdftoppm and pdfinfo (Poppler) are required for rendering")
    count = re.search(r"^Pages:\s+(\d+)", pdf_info(pdf), re.MULTILINE)
    if not count:
        sys.exit(f"Cannot read page count of {pdf}")
    total = int(count.group(1))
    pages = page_list(spec, total)
    if out is None:
        key = hashlib.sha1(str(pdf.resolve()).encode()).hexdigest()[:8]
        out = Path(tempfile.gettempdir()) / f"beamer-slides-{pdf.stem}-{key}"
    out.mkdir(parents=True, exist_ok=True)
    meta_path = out / "render.json"
    try:
        previous = json.loads(meta_path.read_text())
    except (OSError, ValueError):
        previous = {}
    current = {"pdf": str(pdf.resolve()), "pages": total, "dpi": dpi}
    comparable = previous == current
    paths, changed = [], []
    for page in pages:
        target = out / f"page-{page:03d}"
        before = digest(target.with_suffix(".png"))
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page),
                        "-singlefile", str(pdf), str(target)], check=True)
        paths.append(target.with_suffix(".png"))
        if comparable and before and before != digest(paths[-1]):
            changed.append(page)
    meta_path.write_text(json.dumps(current))
    print(f"Rendered {len(paths)} page(s) at {dpi} dpi to {out}")
    if comparable:
        print(f"Changed since the previous render: {','.join(map(str, changed)) or 'none'}")
    elif previous:
        print("Page count, dpi, or PDF differ from the previous render; changes not compared")
    if grid:
        paths = [grid_overlay(pdf, path, page, dpi) for path, page in zip(paths, pages)]
    if sheet:
        for old in out.glob("sheet-*.png"):
            old.unlink()
        paths = contact_sheets(paths, pages, out)
    for path in paths:
        print(path)


def pillow():
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("--sheet and --grid need Pillow; view the page PNGs instead")
    return Image, ImageDraw


def grid_overlay(pdf, path, page, dpi, step=50):
    """Draw lines every `step` pt, labelled from the top-left corner, for choosing trim values."""
    Image, ImageDraw = pillow()
    size = re.search(r"Page\s+\d+\s+size:\s+([\d.]+) x ([\d.]+)", pdf_info(pdf, page))
    width, height = (float(size.group(1)), float(size.group(2))) if size else (None, None)
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    scale = dpi / 72
    for value in range(0, int(max(image.size) / scale) + 1, step):
        color = (220, 40, 40) if value % (2 * step) == 0 else (240, 150, 150)
        draw.line([(value * scale, 0), (value * scale, image.height)], fill=color, width=1)
        draw.line([(0, value * scale), (image.width, value * scale)], fill=color, width=1)
        if value % (2 * step) == 0:
            draw.text((value * scale + 2, 2), str(value), fill=(200, 0, 0))
            draw.text((2, value * scale + 2), str(value), fill=(200, 0, 0))
    target = path.with_name(path.stem.replace("page", "grid") + ".png")
    image.save(target)
    if width:
        print(f"p.{page}: {width:g} x {height:g} pt; for a box x0..x1, y0..y1 read from the grid, "
              f"trim = x0 {height:g}-y1 {width:g}-x1 y0")
    return target


def contact_sheets(paths, pages, out, columns=3, rows=3, width=520):
    Image, ImageDraw = pillow()
    sheets, per_sheet = [], columns * rows
    for start in range(0, len(paths), per_sheet):
        batch = list(zip(paths[start:start + per_sheet], pages[start:start + per_sheet]))
        images = [Image.open(path).convert("RGB") for path, _ in batch]
        height = round(width * images[0].height / images[0].width)
        label, gap = 22, 12
        count_rows = (len(images) + columns - 1) // columns
        canvas = Image.new("RGB", (columns * (width + gap) + gap, count_rows * (height + label + gap) + gap), "#808080")
        draw = ImageDraw.Draw(canvas)
        for index, (image, (_, page)) in enumerate(zip(images, batch)):
            x = gap + (index % columns) * (width + gap)
            y = gap + (index // columns) * (height + label + gap)
            draw.text((x, y + 4), f"p.{page}", fill="white")
            canvas.paste(image.resize((width, round(width * image.height / image.width))), (x, y + label))
        target = out / f"sheet-{batch[0][1]:03d}-{batch[-1][1]:03d}.png"
        canvas.save(target)
        sheets.append(target)
    return sheets


def notes_wrapper(tex):
    if "presenternotes" not in strip_comments(read(tex)):
        sys.exit("The deck has no \\ifdefined\\presenternotes block; copy the one from the template's "
                 "speaker-notes section into the preamble first.")
    wrapper = tex.with_name(f"{tex.stem}-notes.tex")
    if not wrapper.exists():
        wrapper.write_text(NOTES_WRAPPER.format(stem=tex.stem), encoding="utf-8")
    return wrapper


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    build_cmd = commands.add_parser("build", help="compile and report")
    build_cmd.add_argument("tex", type=Path)
    build_cmd.add_argument("--engine", choices=("auto",) + ENGINES, default="auto")
    build_cmd.add_argument("--notes", action="store_true",
                           help="build the presenter version DECK-notes.pdf with speaker notes")
    build_cmd.add_argument("--timeout", type=int, default=900, help="seconds per compiler call")
    build_cmd.add_argument("--min-pt", type=float, default=2.0, help="ignore smaller overfull boxes")
    check_cmd = commands.add_parser("check", help="report on the last build")
    check_cmd.add_argument("tex", type=Path)
    check_cmd.add_argument("--min-pt", type=float, default=2.0, help="ignore smaller overfull boxes")
    render_cmd = commands.add_parser("render", help="render pages to PNG")
    render_cmd.add_argument("pdf", type=Path)
    render_cmd.add_argument("--pages", help="e.g. 1,4-6 (default: all)")
    render_cmd.add_argument("--dpi", type=int, default=120)
    render_cmd.add_argument("--out", type=Path, help="output folder (default: a temp folder per PDF)")
    render_cmd.add_argument("--sheet", action="store_true", help="tile pages into 3x3 contact sheets")
    render_cmd.add_argument("--grid", action="store_true", help="overlay a grid in PDF points for cropping")
    args = parser.parse_args()

    if args.command == "render":
        if not args.pdf.is_file():
            sys.exit(f"No such PDF: {args.pdf}")
        render(args.pdf, args.pages, args.dpi, args.out, args.sheet, args.grid)
        return 0
    tex = args.tex.resolve()
    if not tex.is_file():
        sys.exit(f"No such file: {tex}")
    if args.command == "build":
        engine, reason = choose_engine(tex, args.engine)
        print(f"Engine: {engine} ({reason})")
        if args.notes:
            tex = notes_wrapper(tex)
            print(f"Presenter version: {tex.name}")
        log = tex.parent / f"{tex.stem}.log"
        before = log.stat().st_mtime_ns if log.exists() else None
        result = build(tex, engine, args.timeout)
        if not log.exists() or log.stat().st_mtime_ns == before:
            output = (result.stdout + result.stderr).strip().splitlines()
            print(f"{engine} exited with status {result.returncode} without writing a new log:")
            print("\n".join(output[-20:]))
            return 1
    return check(tex, args.min_pt)


if __name__ == "__main__":
    sys.exit(main())
