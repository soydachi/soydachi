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

1. Segment the person from the background first (macOS Vision,
   `VNGeneratePersonSegmentationRequest`, person mask over the photo).
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
