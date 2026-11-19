# Talk Design

Defaults and patterns for deciding what goes on the slides. Adapt them to the user's material, field conventions, and explicit preferences.

## Fit the occasion

- **Conference or invited talk:** one main message. Motivate the problem quickly, give the key idea with intuition, show the strongest evidence, and leave proofs, hyperparameters, and secondary experiments for backup frames.
- **Group meeting or paper reading (组会论文分享):** the audience wants to understand and judge the paper. Cover the problem setting, enough of the method to reimplement its core, the experimental setup, results read critically, limitations, and what is relevant or questionable for the group's own work. Discussion questions fit at the end.
- **Lecture or tutorial:** build from intuition and a concrete example toward the formal statement. One concept per frame, with a worked example, a recap, and exercises when they help.
- **Progress report, proposal, or defense:** context, contributions or status, evidence, plan, and risks, with clear statements of what is done and what is not.

## Time and frame count

A content frame usually takes one to two minutes; dense math or results frames take longer, and title or section frames take seconds. Use this to check the outline against the time budget rather than as a quota. With overlays, count frames, not PDF pages.

## Story

A talk leads with the problem and the idea, not with the paper's section order. A common arc runs from the problem, through why it matters and why it is hard, to the key idea, how it works, the evidence, and the limits and takeaways. Related work earns space only where it positions the contribution.

Each section should set up the next one. End with what the audience should remember, then backup frames for questions you can anticipate. A closing frame that only thanks the audience wastes the most-viewed slide of the talk.

## Frames

- One point per frame. When the frame supports a claim, the title can state it; topic titles fit agendas, definitions, and section openers.
- Let the evidence carry the frame: a figure, table, equation, diagram, or example. Bullets add what the visual cannot say. Fragments work for points the speaker will expand; claims and definitions that must be read precisely deserve full sentences.
- Judge density by whether the audience can read the frame while listening, in the time it is on screen. Two clear frames usually beat one dense frame. Avoid near-empty frames unless the emptiness is deliberate.
- Use emphasis for the one thing to notice, and keep semantic colors stable across the deck, for example the same color for the proposed method on every chart and table.

## Figures

- Reuse the original figures. Crop to the panels the frame discusses, and show them large enough that axis labels and legends are legible when projected. If a figure's text stays too small, crop further, split panels across frames, or annotate the takeaway.
- Annotate what to look at: a highlight box, an arrow, or a one-line caption stating the observation.
- Never redraw a quantitative plot from estimated values; regenerate it only from the actual data. Schematic diagrams can be redrawn in TikZ to simplify them, provided the structure stays faithful.
- Raster figures need enough pixels for their displayed width; low-resolution crops from a rendered PDF page look blurry on a projector.

## Tables

Reduce a results table to the rows and columns that support the point, and highlight the comparison that matters. Keep units and decimal places consistent. Move the full table to a backup frame. A table that cannot be read at slide size is usually better as a chart or split into parts.

## Math

Introduce symbols before or alongside the equation, and explain its terms in words; color-coding terms helps when the same quantities recur. Keep the equations the argument depends on and move derivations to backup frames or reveal them step by step.

## Overlays

Static frames are the default: the PDF stays readable without presenting and works as a handout. Stepwise reveal earns its place when the order carries meaning, such as building a diagram, walking through a derivation, or holding back an answer. The final step must show the complete frame.

## Speaker notes

When notes are requested, write a `\note` for each frame with what to say, the key numbers, and the transition to the next frame. Notes let slide text stay short; avoid duplicating the full script on the slide.

## Faithfulness

Trace every number, claim, and citation to the source, and keep a source comment in the `.tex` where checking later would otherwise be hard. Do not invent author affiliations, venues, dates, or results; leave a visible placeholder and report it when information is missing.
