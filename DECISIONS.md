# DECISIONS.md

One standing decision per block. Read the one that covers an area before changing it. To reverse a decision, add a new block that supersedes it. Do not edit the old block.

## D-001: {ai} Engineering governs this repo

Status: Accepted · Date: 2026-09-28

### Context

A repo with no contract leaves every agent to invent its own rules.

### Decision

{ai} Engineering 2.4.0 is installed: global skill canon, local receipts, git floor on.

### Consequences

- Init, doctor, and the chain are the contract.

### Alternatives considered

- **Per-repo copies of the skills:** they drift. Rejected.

## D-002: The ASCII portrait is regenerated with ascii-image-converter

Status: Accepted · Date: 2026-09-29

### Context

The profile card shows the photo as ASCII with an empty background, like
Andrew6rant's card. A luminance-only conversion printed the wall and the
shutter as noise.

### Decision

1. Segment the person from the background (macOS Vision,
   `VNGeneratePersonSegmentationRequest`, person mask over the photo). A photo
   that already ships with a transparent background skips this step.
2. Composite onto white in grayscale: `subject_light = gray·mask ⊕ 255`.
   The dark theme uses the negated subject on white:
   `subject_dark = invert(gray)·mask ⊕ 255`, so the background is empty in
   both themes and each theme inks the opposite half of the tones.
3. Convert with the installed tool at the fixed canvas size:

```bash
ascii-image-converter subject_light.png -d 39,25 -g -m '@%#MWmnhrxaexs:-.,;'"'"'` '
ascii-image-converter subject_dark.png  -d 39,25 -g -m '@%#MWmnhrxaexs:-.,;'"'"'` '
```

4. Replace the 25 `<tspan>` rows inside `<text x="15" y="30" class="ascii">`
   in `light_mode.svg` / `dark_mode.svg`. 39 cols × 25 rows keeps the art at
   `x=15…390`, clear of the info panel.

### Consequences

- The map is ordered darkest → lightest, so the same map works for both
  themes; only the source image flips.
- Every panel line must stay ≤ 60 characters wide (Menlo 0.6 em at 16 px) or
  it clips the 985 px canvas.

### Alternatives considered

- **Keeping the background in the art:** the user asked for the figure only.
  Rejected.
- **A committed generator script:** the pipeline is three commands; a script
  would rot when the photo changes. Rejected.

## D-003: The card is 1430×870 with a 64×41 portrait

Status: Accepted · Date: 2026-09-29 · Supersedes the canvas numbers in D-002
(39×25 art at `x=15…390`, 985×530 canvas, 16 px panel). D-002's pipeline and
map still stand.

### Context

At 39×25 the portrait was too coarse to read like full-width
`ascii-image-converter` output, and the info panel had no room to grow
beside a bigger illustration.

### Decision

1. Canvas: 1430×870. Portrait: 64×41 at font 16 (cell 9.6×20 px), `x=20`,
   rows `y=30…830`, regenerated through the D-002 pipeline with
   `-d 64,41`.
2. Panel: `x=680`, font 20 (cell 12×25 px), 33 rows `y=30…830` so the last
   info row lands on the last portrait row. Every value right-aligns to
   column 60 (`x=1400`); section rules reach the same edge and no glyph is
   wider than one cell, so the rule length is `60 − prefix − 1` cells.
3. Sections: header, `- About`, `- Languages`, `- Hobbies`, `- Contact`,
   `- GitHub Stats`. Two facts added from soydachi.com: Newsletter
   (Entre código y personas) and Events (Commit Conf, Codemotion).
4. `today.py` is untouched: the stats rows keep their ids, their structure,
   and their justification widths (the 60-column budget is unchanged).

### Consequences

- GitHub scales the card to the profile width, so glyphs render ~13 px:
  more detail per illustration at a slightly smaller character.
- Panel lines stay ≤ 60 characters = 720 px at font 20, inside the 1430 px
  canvas with a 30 px right margin.

### Alternatives considered

- **Scaling the old card without regenerating the art:** same chunky 39×25
  portrait, larger cells. Rejected — the ask was detail, not zoom.
- **A taller panel font-only or a two-row layout:** keeps the side-by-side
  terminal card the user knows. Rejected.
