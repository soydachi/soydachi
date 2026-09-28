# Changelog

All notable changes, written for someone reading what changed, not how. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `cache/requirements.txt` — dependencies the README build workflow installs to run `today.py`.
- Seeded GitHub stats and the owner-only commit cache (`cache/<sha>.txt`) so the profile never renders placeholder zeros.

### Changed

- `README.md`, `light_mode.svg`, `dark_mode.svg` — profile card rebuilt for soydachi: ASCII portrait generated from the profile photo, panel facts sourced from `soydachi.com/docs/brand`, public links only, no PII.
- `.github/workflows/build.yaml` — bot identity and `USER_NAME` now belong to this profile.
- `today.py` — dropped the upstream age calculation and deleted-repository archive; kept the attribution.

### Fixed

### Removed
