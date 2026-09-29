# Changelog

All notable changes, written for someone reading what changed, not how. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `cache/requirements.txt` — dependencies the README build workflow installs to run `today.py`.
- Seeded GitHub stats and the owner-only commit cache (`cache/<sha>.txt`) so the profile never renders placeholder zeros.

### Changed

- `README.md`, `light_mode.svg`, `dark_mode.svg` — profile card rebuilt for soydachi: ASCII portrait generated from the profile photo, panel facts sourced from `soydachi.com/docs/brand`, public links only, no PII.
- `light_mode.svg`, `dark_mode.svg` — portrait regenerated from the current headshot (`me.png`, cut-out already transparent); every panel value right-aligned to column 59; `Language.Programming`, new Focus/Talks/Hobbies.Sport wording.
- `light_mode.svg`, `dark_mode.svg` — portrait upgraded to the `-c` complex charset at 76×49 chars @8px, chosen from a rendered-card comparison against the custom map, the default charset and braille (see `DECISIONS.md` D-002).
- `.github/workflows/build.yaml` — bot identity and `USER_NAME` now belong to this profile.
- `today.py` — dropped the upstream age calculation and deleted-repository archive; kept the attribution; LOC justification width (14) so its row keeps the shared right edge.

### Fixed

### Removed
