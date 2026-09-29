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
2. Crop to the card aspect (3:4, centred on the subject). The dark source is
   the same crop with negated RGB and the original alpha, so the background
   stays empty in both themes.
3. Convert both sources with the tool's complex charset at the card's fixed
   canvas size:

```bash
ascii-image-converter crop.png     -d 76,49 -g -c
ascii-image-converter crop_neg.png -d 76,49 -g -c
```

4. Replace the 49 `<tspan>` rows inside
   `<text x="15" y="30" font-size="8" class="ascii">` in `light_mode.svg` /
   `dark_mode.svg`, at `y = 30 + 10·i` (last row y=510). 76 cols × 8 px = 365 px
   keeps the art at `x=15…380`, clear of the panel at x=390.

### Consequences

- `-c` (complex charset) beat the custom map, the default charset and `-b`
  braille in the rendered-card comparison: braille halves the cell width and
  its glyphs depend on the viewer's fonts (tested: washed out in Chromium).
- Every panel line must stay ≤ 60 characters wide (Menlo 0.6 em at 16 px) or
  it clips the 985 px canvas.

### Alternatives considered

- **Keeping the background in the art:** the user asked for the figure only.
  Rejected.
- **A committed generator script:** the pipeline is three commands; a script
  would rot when the photo changes. Rejected.
