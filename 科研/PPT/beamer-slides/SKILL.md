---
name: beamer-slides
description: Create, revise, and check LaTeX Beamer presentations that compile to PDF, from papers, notes, outlines, or an existing deck, in English or Chinese. Plans the talk, writes frames with a bundled 16:9 theme (teal section bar, section-tinted titles, code/result boxes) or the user's own, compiles with an available engine (XeLaTeX, LuaLaTeX, pdfLaTeX, or Tectonic), maps overflow warnings to pages, and reviews rendered pages. Use for requests such as “用 LaTeX/Beamer 做 PPT”, 组会汇报, 论文讲解, lecture slides, or fixing layout and compile problems in a Beamer deck. Editable PowerPoint files need a different tool.
compatibility: Needs Python 3.9+, a TeX distribution with Beamer (TeX Live or MiKTeX) or Tectonic, and Poppler (pdftoppm, pdfinfo) for page rendering; contact sheets use Pillow. Chinese decks need XeLaTeX, LuaLaTeX, or Tectonic with the ctex bundle.
---

# Beamer Slides

Produce a Beamer source deck and its compiled PDF. Keep the user's language, template, theme, and file layout; the bundled template is the default only for a new deck without one. Resolve bundled paths from this skill's directory and work in the user's project, never in the installed skill.

## Establish the brief

Read the supplied material before asking anything: paper source or PDF, parsed Markdown, notes, an existing deck, or the user's template. Parsed Markdown can drop footnotes, figure text, and table details, so check numbers that go on slides against the PDF or source. Identify the audience, occasion, time budget, language, and any required template or venue format. Infer routine choices from context. Ask only when an unresolved choice would produce a substantially different deck, such as a conference talk versus a detailed group-meeting walkthrough of the same paper.

## Plan the talk

Outline the deck before writing LaTeX. For each frame, note the point it makes, the evidence that carries it (figure, table, equation, diagram, or example), and where that evidence comes from in the source. Read [talk design](references/design.md) for structure by occasion, frame count against time, and how to handle figures, tables, and math.

Show the outline first when the deck is long, the story has real alternatives, or the user wants to steer; otherwise proceed and summarize the structure with the draft. Numbers, claims, figures, and citations come from the source material. Mark anything inferred or unverified instead of filling gaps.

## Write the deck

For a new deck, copy [the template](assets/template.tex) and [the theme](assets/beamerthemetealnav.sty) into the project, for example `slides/<name>.tex` with the theme file and a `figures/` folder beside it, and fill in the title block. The title page shows [the bundled logo](assets/logo.png), which is Southeast University's: copy it to `figures/logo.png` only for decks that should carry it, and otherwise use the user's own logo or delete the `\titlegraphic` line. A Chinese deck switches the class line as the template comment describes. [The example deck](assets/example.tex), compiled as [example.pdf](assets/example.pdf), shows each layout the theme provides and a tips section of presentation techniques (previewed lists, annotated equations, stepwise diagrams, magnifiers, panel walkthroughs, result tables, backup links, cards, contact frames); read it for patterns, not as content to copy. For an existing deck or a user-supplied template, edit within its conventions rather than merging in the bundled style.

Read [Beamer reference](references/beamer.md) for layout patterns, Chinese fonts, overlays, presentation techniques, speaker notes, figure extraction, and common errors. Copy figures into `figures/` with stable names; prefer the original vector files when the paper source has them, and crop to the part the frame discusses. `slides.py render paper.pdf --pages N --grid` overlays a point grid on a source page for choosing crop values. Keep the source easy to edit: one frame per idea, and a short comment with the source location where it helps later checking.

## Build and check

```text
python3 <skill-dir>/scripts/slides.py build path/to/deck.tex
```

The build reads the deck and the files it inputs, then picks an engine: the magic comment's engine when usable, otherwise XeLaTeX or LuaLaTeX for Unicode sources and pdfLaTeX for the rest, and Tectonic when the local TeX installation lacks a needed class, package, or theme. `--engine` overrides the choice, and `--notes` builds the presenter version with speaker notes from the same source. After compiling, the script reports errors, overfull boxes above 2pt by PDF page with their size, shrunk frames, missing glyphs, undefined references, font substitutions, and uses of `shrink`, `allowframebreaks`, or `\tiny`. Rerun only the report with `slides.py check deck.tex`.

Fix the first error before later ones, since one mistake often causes several messages. Treat overflow as content pressure: cut, split, or rearrange first, then adjust spacing or sizes. Frame shrinking, `\tiny` body text, and scaled text boxes hide overflow by making text unreadable; use them only for content meant as fine print. A clean report does not establish a good slide, because crowding against the footline, cramped columns, and unreadable figure text produce no warnings.

## Review rendered pages

```text
python3 <skill-dir>/scripts/slides.py render path/to/deck.pdf --sheet
python3 <skill-dir>/scripts/slides.py render path/to/deck.pdf --pages 4,7-8 --dpi 160
```

Rendering writes PNGs to a temporary folder per PDF unless `--out` is given. Look at the contact sheets for deck-level consistency and pacing, and at full-size pages for frames the report flagged, dense frames, and figures with small text. Check for clipped or overlapping content, content touching the footline or margins, figure text too small to read when projected, unbalanced columns, near-empty frames, inconsistent colors or terminology, and overlay steps that jump or leave the final step incomplete.

After edits, rebuild and render again at the same dpi; when the page count is unchanged, the script lists the pages whose images changed, so only those need another look. Stop iterating when the remaining issues are judgment calls, and report them instead of churning the layout.

## Deliver

Report the `.tex` and `.pdf` paths, frame and page counts, the engine used, what was checked (the compile report and which pages were viewed), and any remaining issues or unverified content. Leave auxiliary files in place unless the user asks for a cleanup. Speaker notes, a presenter PDF, or a handout version are produced on request; when the deck has notes, build the presenter version too, since notes are typeset only there. This workflow produces PDF slides; if the user needs an editable PowerPoint file, say so rather than presenting the PDF as one.
