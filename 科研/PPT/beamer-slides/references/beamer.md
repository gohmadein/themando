# Beamer Reference

LaTeX patterns and fixes for writing decks. The bundled starter is [`assets/template.tex`](../assets/template.tex), its theme is [`assets/beamerthemetealnav.sty`](../assets/beamerthemetealnav.sty), and [`assets/example.tex`](../assets/example.tex) uses every layout the theme provides.

## Engines

- `slides.py build` reads the main file and the files it inputs. It honors a `% !TEX program = ...` magic comment when that engine is installed and suitable, and otherwise picks XeLaTeX or LuaLaTeX for Unicode sources (fontspec, ctex, CJK text) and pdfLaTeX for the rest. It falls back to Tectonic when the local TeX installation lacks a class, package, or theme the deck loads, and says why.
- The theme works with every engine: under XeLaTeX, LuaLaTeX, or Tectonic it selects fonts through fontspec, and under pdfLaTeX it loads the Type 1 versions of Linux Biolinum and DejaVu Sans Mono. Chinese decks need XeLaTeX, LuaLaTeX, or Tectonic.
- Tectonic downloads missing packages on first use, which needs network access and then stays cached. It finds system fonts by name through fontconfig, stops at the first error, and its bundle may lag behind CTAN.
- On Overleaf, set the compiler to XeLaTeX or LuaLaTeX in the project menu.
- The check reads the `.log` and `.nav` files from the last build. Remove auxiliary files with `latexmk -c` when the user wants a clean folder.

## The tealnav theme

- **Colors:** `tealnavDark` (text, top bar, standout frames), `tealnavOrange` (alerts, rules, progress), `tealnavPaper` (background), and title-band tints `tealnavGrey`, `tealnavBlue`, `tealnavPeach`, `tealnavLavender`. Redefine `\tealnavtints` to change the order in which sections cycle through the tints.
- **Fonts:** Linux Biolinum for Latin text, then the first installed of PingFang SC, Noto Sans CJK SC, Source Han Sans SC, or Microsoft YaHei for Chinese, and Menlo, DejaVu Sans Mono, or Consolas for code. Override any of them after `\usetheme{tealnav}`. Math stays in Computer Modern through `professionalfonts`.
- **Top bar:** lists every section's short title, so keep section titles short and give long ones a short form with `\section[Short]{Full title}`. Five or six sections fit comfortably.
- **Section pages:** each `\section` adds an unnumbered section page with a progress bar. `\AtBeginSection{}` after `\usetheme` turns them off.
- **Outline:** `\tableofcontents` in a `[plain]` frame draws numbered rows. `\sectionaside{...}` inside a section title adds a right-aligned note on the outline only, such as an English name. About six rows fit; reduce `\tealnavtocskip` for more.
- **Title page:** an optional `\titlegraphic{...}` sits at the top left.
- **Blocks:** `block` has a grey title band, `exampleblock` a blue one, and `alertblock` a pink band with orange title; bodies have no background.
- **Code boxes:** `codeexample` shows LaTeX source above its typeset result and `codeside` places them side by side. Both are listings, so the frame needs `[fragile]`; adjust them with `\tcbset{tealnav/.append style={...}}`.
- **Standout frames:** `\begin{frame}[standout]` gives a dark closing or emphasis frame with large centered text.
- **Backup frames:** frames after `\appendix` are numbered from 1 again, and section progress bars count only the main part; no extra package is needed.
- **Presenter builds:** the theme styles the note page and restores the text color per slide, which XeTeX otherwise loses with pgfpages.

With a user or institutional template, keep that template's look and add only the packages the content needs.

Other themes are fine when the user wants them: the stock themes are always available but look dated; `metropolis` is in TeX Live but unmaintained and wants Fira fonts under XeLaTeX or LuaLaTeX; `moloch` is its maintained fork on CTAN since 2024, so older installations may lack it.

## Chinese

- Use `\documentclass[aspectratio=169,11pt,fontset=fandol]{ctexbeamer}` with XeLaTeX, LuaLaTeX, or Tectonic; pdfLaTeX cannot typeset Chinese with fontspec fonts. `fontset=fandol` always resolves; the theme then switches to PingFang SC, Noto Sans CJK SC, Source Han Sans SC, or Microsoft YaHei when installed.
- Fandol fonts cover common characters only. Check the report's missing-glyph list after building with them.
- Chinese fonts have no italic. `\emph` and `\textit` on Chinese text fall back to upright and show up as a font substitution; use `\alert` or `\textbf` for emphasis.
- Symbols such as circled numbers go to the Latin font, which often lacks them. Under XeLaTeX or Tectonic, `\xeCJKDeclareCharClass{CJK}{"2460 -> "2473}` in the preamble sends ①–⑳ to the CJK font; arrows read better as math (`$\to$`).
- Noto CJK fonts ship as TTC collections whose embedded name reads `jp` in `pdffonts` even when the SC face is selected. Judge the face from rendered glyphs, not from the font name.
- The Latin font comes from `\setsansfont`, so Chinese and English text use separately chosen fonts. Write Chinese punctuation in full width; ctex handles spacing and compression.

## Layout patterns

Two columns, top-aligned, with a figure bounded in both dimensions:

```latex
\begin{frame}{Frame title}
  \begin{columns}[T]
    \column{0.45\textwidth}
    \begin{itemize}
      \item ...
    \end{itemize}
    \column{0.52\textwidth}
    \centering
    \includegraphics[width=\linewidth,height=0.62\textheight,keepaspectratio]{figure-name}
  \end{columns}
\end{frame}
```

Figure on top, points below:

```latex
\begin{frame}{Frame title}
  \begin{center}
    \includegraphics[width=0.9\linewidth,height=0.5\textheight,keepaspectratio]{figure-name}
  \end{center}
  \begin{itemize}
    \item ...
  \end{itemize}
\end{frame}
```

- Keep column widths summing to slightly under `\textwidth`. `[T]` aligns the first lines; `[c]` centers columns vertically.
- With the tealnav theme, a figure alone under a one-line title fits within about `0.8\textheight`; with one line of text and a source line, about `0.7`. Leave less for each further line, and less again when the title wraps.
- Crop a figure with `trim=left bottom right top,clip`, and pick a page of a multi-page PDF with `page=N`. Both keep vector quality.
- `\centering` applies until the end of the frame or group. Wrap centered material in a `center` environment or a group so later text stays left-aligned, and end a paragraph with `\par` before switching alignment.
- Frames are vertically centered by default. Use `\begin{frame}[t]` for build-up sequences so content does not jump between steps.
- `\vfill` pushes content apart; `\medskip` and `\bigskip` add fixed gaps. Adjust item spacing locally with `\setlength{\itemsep}{0.5em}` inside the list.

Annotate a region of an image with coordinates relative to the image:

```latex
\begin{tikzpicture}
  \node[anchor=south west,inner sep=0] (img)
    {\includegraphics[width=0.8\linewidth,height=0.6\textheight,keepaspectratio]{figure-name}};
  \begin{scope}[x={(img.south east)},y={(img.north west)}]
    \draw[tealnavOrange,very thick,rounded corners] (0.60,0.30) rectangle (0.95,0.80);
  \end{scope}
\end{tikzpicture}
```

Render the frame to place such boxes; coordinates guessed from the source often land on the wrong panel. Define TikZ styles that take parameters with `\tikzset` in the preamble, since `#1` inside a frame body raises "Illegal parameter number".

Tables use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`). `\small` is usually the smallest readable table size; scaling a whole table with `\resizebox` makes its text unreadable once the factor drops much below one, so cut columns instead. Row shading with `\rowcolor` needs `\usepackage{colortbl}`.

A short source line at the bottom of a frame:

```latex
\par\vfill
{\raggedright\footnotesize\color{tealnavDark!70} Source: Author et al., Venue Year, Table 2.\par}
```

Section opener frames come from `\AtBeginSection{\begin{frame}[plain]\sectionpage\end{frame}}`. These frames do not appear in the source, which shifts frame numbers relative to `\begin{frame}` counts.

## Overlays

- `\pause`; `\item<2->`; `\begin{itemize}[<+->]` reveals items one by one; `\uncover<2->{...}` reserves space before showing; `\only<2>{...}` takes no space when hidden, so the layout can jump; `\alert<2>{...}` highlights on one step.
- Each step is a PDF page. The check report lists frames and pages when they differ, and overflow is attributed to the frame.
- `\documentclass[handout]{beamer}` collapses steps into one page per frame for a printable version.

## Techniques

The tips section of [`assets/example.tex`](../assets/example.tex) shows each of these on its own frame, in this order. Use them where they help the audience follow the argument, not as decoration.

- **Previewed lists:** `\setbeamercovered{transparent}` inside the frame plus `\begin{itemize}[<+-| alert@+>]` shows upcoming items faded and colors the current one.
- **Emphasis:** `\alert` for the one point of a frame, `\textbf` for terms, and `\colorbox` for a highlighter look. For Chinese, `xeCJKfntef` adds `\CJKunderdot`, `\CJKunderwave`, and `\CJKsout`; it needs XeLaTeX.
- **Annotated equations:** `\tikzmarknode[fill=...]{name}{term}` from the TikZ `tikzmark` library colors a term and names it; a `remember picture,overlay` picture then draws labels to `name.south` or `name.north`. The marks resolve on the second compile, which the build script runs. The `annotate-equations` package wraps the same idea but is missing from older distributions.
- **Stepwise diagrams:** the TikZ library `overlay-beamer-styles` adds `visible on=<2->`, which reserves space so the picture does not jump, and `alt=<2>{style A}{style B}` for highlighting the current step.
- **Switching figures in place:** wrap the alternatives in `\begin{overlayarea}{\linewidth}{height}` and select them with `\only<n>`; `\alt<n>{...}{...}` changes matching text.
- **Magnifier:** the TikZ `spy` library (`spy using outlines={circle,magnification=3,...}`, then `\spy on (point) in node at (place)`) zooms into a detail. Inside a pgfplots axis, define the two points with `\coordinate` in `axis cs`. It fails with ctex under LuaLaTeX; use XeLaTeX.
- **Panel walkthrough:** place the figure in a node anchored `south west` at the origin, set `x={(fig.south east)},y={(fig.north west)}` so coordinates run from 0 to 1 across the image, and draw a translucent `even odd rule` mask with a hole over the current panel on each step. The original figure stays uncropped.
- **Stamps and badges:** a `remember picture,overlay` node at `current page.north east` places content at a fixed page position.
- **Result tables:** `tabularray` sets styles by key, such as `row{Z}={bg=...}` for the last row and `cell{Z}{2,3}={font=\bfseries}`. With `\UseTblrLibrary{siunitx}`, `Q[si={table-format=2.1}]` aligns decimals; text cells in those columns need triple braces `{{{...}}}` in older tabularray versions (newer ones also accept `guard`), and `\sisetup{mode=text}` keeps numbers in the slide font.
- **Jumping to backup frames:** label the target with `\begin{frame}[label=name]`, link to it with `\hyperlink{name}{\beamergotobutton{...}}`, and link back with `\beamerreturnbutton`. The `beamerappendixnote` package automates such note frames with `\appxnote`.
- **Cards:** the tcolorbox `raster` library (`\begin{tcbitemize}[raster columns=3,raster equal height]`) lays out equal-height boxes; `fontawesome5` supplies icons such as `\faCogs`.
- **Contact frames:** `qrcode` draws QR codes without image files; `academicons` provides `\aiGoogleScholar` and `\aiOrcid`. Put an icon used as an item label in braces, as in `\item[{\aiOrcid}]`.
- **Presenting:** the `pdfpc` package stores talk duration and notes in the PDF for the pdfpc presenter console. The `animate` package plays animations only in Adobe Acrobat, so prefer overlays for steps.

## Code and verbatim

Frames containing `verbatim`, `lstlisting`, or `\verb` need `\begin{frame}[fragile]`. Beamer typesets such frames from a `.vrb` copy, so overflow inside a listing is reported with a line number of that copy; the report marks these. Prefer `listings` over `minted`, which requires `-shell-escape`; the build script does not enable it.

## Speaker notes

Put `\note{...}` inside or right after a frame. `slides.py build deck.tex --notes` writes `deck-notes.tex`, a wrapper that defines `\presenternotes` and inputs the deck, then builds `deck-notes.pdf` with notes on a second screen at double page width. The deck needs the template's `\ifdefined\presenternotes` block; with another theme, also restore the text color per slide as the tealnav theme does, since XeTeX loses it with pgfpages. Notes are typeset only in the presenter build, so build it to catch errors in note text. Present with pdfpc or pympress.

## Silent problems

These produce no error and sometimes no warning; look for them on rendered pages.

- A brace group right after the frame title, such as `\begin{frame}{Title}` followed by `{\color{...} ...}`, becomes the frame subtitle. Start the body with something else, for example `\par` or a command.
- `\mathbb` covers capital letters only; `\mathbb{1}` prints a wrong glyph. Use `\mathbf{1}`, or `\mathds{1}` from `dsfont`.
- Text pressed against the footline, figures with tiny labels, and cramped columns fit the frame and raise no overflow warning.

## Common errors

| Message | Usual cause | Fix |
| --- | --- | --- |
| `Misplaced alignment tab character &` | `&` in a title or text | Write `\&`. |
| `Missing $ inserted` | `_` or `^` outside math, often in identifiers | Escape as `\_`, or use math or `\texttt`. |
| `Undefined control sequence` | Typo or missing package | Check the command at the reported line; load the package. |
| `File ended while scanning use of \frame` or `\beamer@collect@@body` | Unbalanced braces, missing `\end{frame}`, or verbatim without `[fragile]` | Balance the frame; add `[fragile]`. |
| ``LaTeX Error: File `x' not found`` | Path not relative to the `.tex` folder or `\graphicspath` | Fix the path; avoid spaces and special characters in file names. |
| `Unable to load picture or PDF file` | Damaged or unusual PDF, often from a page-splitting tool | Re-extract the page with `pdftocairo -pdf`. |
| `Package fontspec Error: The font "X" cannot be found` | Font not installed for this engine | Use an installed font or the theme's fallback lists. |
| `Paragraph ended before ... was complete` | Blank line inside a command argument | Remove the blank line or use `\par` where allowed. |
| `Illegal parameter number in definition of ...` | `#1` inside a frame, often in a TikZ style | Move the definition to the preamble. |
| `Unicode character ... not set up for use with LaTeX` | Non-Latin text under pdfLaTeX | Switch to XeLaTeX, LuaLaTeX, or Tectonic. |
| `Missing character: There is no X in font Y` | Glyph absent from the font | Choose a font that has it, or use a LaTeX command for the symbol. |
| `Dimension too large` | TikZ or pgfplots coordinates out of range | Rescale the data or axis. |

## Figures from PDFs

- Prefer vector figures from the paper source when available.
- Raster figures embedded in a PDF can be extracted at their original resolution: `pdfimages -list paper.pdf` shows sizes per page, and `pdfimages -png -f N -l N paper.pdf figures/pN` writes them. Images from parsed PDFs, such as MinerU output, are often downsampled; check their pixel size against the displayed width.
- For vector figures, extract the page with `pdftocairo -pdf -f N -l N paper.pdf figures/paper-pN.pdf` and crop it with `trim`/`clip`. Pages split by other tools can keep the whole document's resources or fail to load in Tectonic.
- To choose the crop, render the page with `slides.py render paper.pdf --pages N --grid`. The grid is labeled in PDF points from the top-left corner, and the command prints how to turn a box read from it into `trim` values.
