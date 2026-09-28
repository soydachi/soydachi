# Adversarial review · readme-profesional#2

## Checkpoint goal
Add a 'Now' section between the intro and Contact with 3-6 responsive widgets (lifetime commit chart on shieldcn.dev plus the komarev profile-views counter, the rest high-signal shieldcn badges), each a Markdown image with a human-readable alt, every URL measured 200 before commit. Closes §06 defect 4 and satisfies PRD R6.

## Acceptance criteria
- A 'Now' section exists with 3-6 badge images, including the shieldcn lifetime commit chart and the komarev view counter.
- Every badge has a human-readable, self-sufficient alt.
- Every badge URL returns HTTP 200 when measured from the repo root.
- github-readme-stats and any fixed-theme single-provider stats card remain absent.
- check-readme.py (extended with widget checks) exits 0.

## changed_files
- README.md (commit 99d0636)
- .ai-engineering/scripts/check-readme.py (CP2 assertion section, commit 9b6bd95 — test side)

## verify commands
- python3 .ai-engineering/scripts/check-readme.py
- python3 .ai-engineering/scripts/check-readme.py --checkpoint 2
- the curl loop: every markdown image URL in README → HTTP 200
- test -z "$(git status --porcelain -- README.md .ai-engineering/scripts/check-readme.py)"

## Documented deviations (judge these, don't assume they are wrong)
- Implementer used `<div align="center">` instead of `<p align="center">`: claims CommonMark renders `![...](...)` literally inside `<p>` without blank lines, and auto-closes the paragraph (breaking centering) with blank lines. Verify the claim.
- Implementer probed shieldcn `.json` endpoints to reject error-badge candidates that return HTTP 200 with an error body (e.g. `/github/repos/`, `last-commit` showing wrong "Now" data).

## Rules of this thread
Critique only the checkpoint slice and changed_files. Contracts: .ai-engineering/workflow/checkpoints/readme-profesional.json CP2, .ai-engineering/PRD.html R6/R10, research §06 defect 4 + §10 (star-history retired). LEARNINGS L1/L2 lessons apply to the checker: assertion scope must match acceptance scope; mutation-test. Findings cite file+line or rule. Blocks: `**F<n>:** …` then `STATUS: open|upheld|withdrawn|resolved`.

---

## Round 1 · critic (2026-09-28)

Mutations run against a /tmp copy of README.md beside the committed script (repo untouched: `git status --porcelain -- README.md .ai-engineering/scripts/check-readme.py` empty).

**F1:** The CP2 checker's section-scoped assertions are never executed by the contract's or test plan's own verify lines: `DEFAULT = [1]` (check-readme.py:298) makes the bare command run checkpoint 1 only, and both CP2 verify lists use that bare command; the script's own comment (check-readme.py:296-297) says to promote 2 into DEFAULT once the slice lands — it landed (commit 99d0636).
  EVIDENCE: mutation B (all four images moved from `## Now` into `## What I do`, Now left with its lead line) passes every command of contract CP2 verify and test-plan CP2 verify: bare script exit 0, case 2-1 exit 0, case 2-2 exit 0, case 2-3 exit 0, curl loop all 200 — while acceptance 1 is violated; only `--checkpoint 2`, which appears solely in this thread, fails (3 FAILs).
  WHY IT MATTERS: a README that breaks acceptance 1 passes every documented gate because the strong gate is off by default in the flow that relies on it.
  CHECK: `python3 .ai-engineering/scripts/check-readme.py` on the B mutant exits 0; `--checkpoint 2` exits 1.

**F2:** Acceptance 1's "including the shieldcn lifetime commit chart" is not encoded — the assertion only requires any shieldcn.dev URL (check-readme.py:265-266).
  EVIDENCE: mutation A replaces `https://shieldcn.dev/chart/github/commits/soydachi.svg` with `https://shieldcn.dev/github/forks/soydachi/MeetupApi.svg`; `--checkpoint 2` exits 0, all 22 checks pass.
  WHY IT MATTERS: LEARNINGS L1 — the acceptance text is the spec; the one widget the contract names by URL can be deleted and the gate stays green.
  CHECK: run mutation A, observe `--checkpoint 2` exit 0 with the chart absent.

**F3:** Test-plan CP2 cases 2-2 and 2-3 match content file-globally while the acceptance scope is the `## Now` section — the LEARNINGS L2 failure mode re-introduced on the test side.
  EVIDENCE: test-plans/readme-profesional.json:33 (`re.findall` over the whole file) and :34 (`grep -q` over the whole file). Both exit 0 on mutation B (images moved out of Now) and on mutation C (komarev counter moved from Now into the `## Contact` body, 3 shieldcn images left in Now), while the checker's body-scoped assertions correctly fail those same mutants (`FAIL: now: komarev.com/ghpvc counter widget image`, `FAIL: now: 3 to 6 Markdown images inside ## Now: found 0`).
  WHY IT MATTERS: the plan's own cases certify acceptance with a duplicate or moved target outside the named section — the exact counterexample L2 proved against CP1.
  CHECK: run cases 2-2/2-3 against the B and C mutants — exit 0 on both.

**F4:** Acceptance 4's broader clause "any fixed-theme single-provider stats card remain absent" is covered only by three literal strings (`github-readme-stats`, `vue-dark` at check-readme.py:197-198; `star-history.com` at :283-284).
  EVIDENCE: mutation E adds `![GitHub profile stats](https://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk)` inside `## Now`; `--checkpoint 2` exits 0 and the bare (CP1) run exits 0 with the image files present in the harness.
  WHY IT MATTERS: a fixed-theme single-provider stats card — the defect-4 genre acceptance 4 bans explicitly — can be re-added with both checkpoints green.
  CHECK: run mutation E; both invocations exit 0.

**F5:** The alt assertion (check-readme.py:256-259) passes non-self-sufficient alts.
  EVIDENCE: mutation D rewrites every `![...]` alt in the file to `GitHub badge chart`; `--checkpoint 2` exits 0 (19 chars, `github` lies outside the generic set at :251-252).
  WHY IT MATTERS: acceptance 2 requires self-sufficient alts; the heuristic floor cannot fail an alt that names no metric. The committed alts (README.md:25-29) were read and are self-sufficient, so this is a checker-only gap, not a content defect.
  CHECK: run mutation D, observe exit 0.

**F6:** The 200-only liveness gate accepts error-badge bodies; the deviation-2 `.json`-probe discipline exists nowhere in the checker or test plan.
  EVIDENCE: `curl -sL https://shieldcn.dev/chart/github/stars/soydachi.svg` → HTTP 200, body is an error card (`usage: /chart/github/stars/{owner}/{repo}.svg`); mutation F (that URL swapped in for the commits chart) passes `--checkpoint 2` and the case 2-4 curl loop.
  WHY IT MATTERS: a future edit can reintroduce a retired/error widget (§10 star-history retirement is cited in the CP2 header itself, check-readme.py:208-209) that satisfies acceptance 3 and renders nothing for readers.
  CHECK: the curl above returns 200 carrying the usage-error text.

**F7:** Widget quality: the MeetupApi star badge (README.md:29) is a weak "Now" widget under R6's "3-6 badges de alta señal".
  EVIDENCE: `api.github.com/repos/soydachi/MeetupApi` → stargazers_count 15, pushed_at 2025-11-20 (≈10 months stale); shieldcn `last-commit` json for the repo returns "10mo ago".
  WHY IT MATTERS: a stale repo's star count proves no current activity in a section whose lead line promises numbers that update on their own; contract task 2 leaves extra badge choice to the implementer, so this is a quality note against R6, not a contract breach.
  CHECK: the two probes above.

**F8:** nit — the lead line (README.md:21) is first-person, concrete, and linked, but states no "what is happening now" (contract CP2 task 1: "one concrete first-person line about what is happening now with a link").
  EVIDENCE: README.md:21 — "I work in the open at github.com/soydachi; the numbers below update on their own."
  WHY IT MATTERS: the section's only prose restates the widget row instead of naming current work.
  CHECK: read README.md:21 against contract task 1.

STATUS: open (F1-F8)

### Deviations judged (both upheld as sound)

- **Deviation 1** (`<div align="center">` instead of `<p align="center">`) — claim verified true against GitHub's own renderer (POST https://api.github.com/markdown, mode=gfm, HTTP 200): `<p align="center">` + Markdown image with no blank lines outputs the literal text `![a](https://x/y.svg)` unprocessed; with blank lines it outputs `<p align="center">\n</p><p><img…></p>`, i.e. the image lands in a separate paragraph and the centering is broken by the implicit `<p>` close — exactly the implementer's claim. Rendering the actual README yields 4 camo images nested inside `<div align="center">` (offsets 1481 < 1573 < 4228) and zero literal `![`. The shieldcn-badges skill's "use `<p align="center">`" guidance wraps raw HTML `<img>` tags, not Markdown images, so there is no conflict to flag.
- **Deviation 2** (`.json` probing of error-badge candidates) — claim verified true: `https://shieldcn.dev/github/repos/soydachi/MeetupApi.json` returns HTTP 200 with `{"value":"invalid repository","error":true}`, and `.../last-commit/soydachi/MeetupApi.json` returns "10mo ago" (stale for a Now widget). The four shipped URLs were re-probed: followers json `61`, stars json `15`, commits chart 9908 bytes with no `usage:`/error text, komarev returns `image/svg+xml`. The probes were sound as a selection step; the gap that it stays unencoded is F6.

### Attacks that did not land

- Section-scope attacks against the checker itself (images out of Now; komarev relocated to Contact): `--checkpoint 2` fails both mutants — the L2 fix did land in check-readme.py (body-scoped at :248-268).
- Vacuity attack: script at 9b6bd95 vs README at 9b6bd95 (pre-implementation) → `--checkpoint 2` exit 1 with 3 FAILs, bare exit 0 — CP2 assertions are not vacuous and the CP1 baseline was green before and after (bare: 61 checks pass on the committed file).
- HTTP-200 claim (e): re-ran the case 2-4 loop from the repo root — all four URLs print `200`, exit 0.
- Voice attack on the Now section: no U+2014, no curly quotes, no emoji (CP1 `voice_mechanics` runs file-wide and passes; section read directly) — nothing CP3-worthy provable.
- Required-widget presence (a): 4 images, within the 3-6 bound; lifetime commit chart (README.md:25) and komarev counter (README.md:27) both present; alts at README.md:25-29 judged self-sufficient by reading.

VERDICT: FAIL — F1, F2, F3, F4 (notes: F5, F6, F7, F8)

---

## Round 1 · fixer (2026-09-28)

Re-verified every finding against HEAD 8df7943 (user content redesign): that commit touched README.md and check-readme.py but removed only the banner/R5 and emoji assertions — none of F1-F8 were addressed by it. Classification: all eight STILL-OPEN at HEAD (no finding was voided; the banner/emoji parts of the round are VOID by user order and were not re-added).

**F1 response:** STILL-OPEN at 8df7943. Bare invocation now runs every checkpoint whose README section exists (CP1 always, CP2 once `## Now` is present) instead of `DEFAULT = [1]`; usage docstring updated. CP2's checkpoint verify array needed no change — its bare line now exercises the CP2 assertions. Mutation B (images moved out of `## Now`): bare exit 1 (was 0).
STATUS: resolved

**F2 response:** STILL-OPEN (redesign left only "any shieldcn.dev widget"). Checkpoint 2 now pins `https://shieldcn.dev/chart/github/commits/soydachi.svg` as an image inside `## Now`. Mutation A (chart swapped for a forks badge): bare and `--checkpoint 2` exit 1 (was 0).
STATUS: resolved

**F3 response:** STILL-OPEN (test plan untouched by the redesign). Cases 2-2/2-3 — and their verbatim copies in the CP2 verify array — now extract the `## Now` body before matching (L2 scope). Mutations B and C: case 2-2 exit 1 on B; case 2-3 exit 1 on both (previously 0 on both).
STATUS: resolved

**F4 response:** STILL-OPEN (only the `github-readme-stats`/`vue-dark`/`star-history.com` literals survived the redesign). Checkpoint 2 now fails closed on image hosts: every Markdown and HTML image URL in the README must come from shieldcn.dev, komarev.com, or img.shields.io — any other stats-card provider (github-profile-summary-cards etc.) fails by construction. Mutation E: bare and `--checkpoint 2` exit 1 (was 0).
STATUS: resolved

**F5 response:** STILL-OPEN (alt heuristic unchanged by the redesign). An alt must now also name its subject (`soydachi`) or a widget-specific metric word, on top of the generic-set floor. Mutation D (all Now alts → "GitHub badge chart"): `--checkpoint 2` exit 1 (was 0).
STATUS: resolved

**F6 response:** STILL-OPEN. The liveness loop (test-plan cases 2-4 and 3-8 plus their verify copies) now saves each body and fails on error markers (`usage:`, `"error":true`) in addition to non-200 — the deviation-2 probe, encoded. Mutation F (usage-error chart URL): case 2-4 prints `error-badge body: …`, exit 1; F2's exact-URL pin independently fails `--checkpoint 2`. Current four URLs re-probed: 200, no markers.
STATUS: resolved

**F7 response:** STILL-OPEN (MeetupApi badge survived the redesign). Replaced with a second live metric: `https://shieldcn.dev/github/stars/arcasilesgroup/ai-engineering.svg?variant=secondary` — measured before use: .svg 200, json `{"label":"stars","value":"58"}`, last-commit json `today`, api.github.com `pushed_at` 2026-09-28 (same day). Case 2-4: 200 with a clean body.
STATUS: resolved

**F8 response:** STILL-OPEN (lead line unchanged by the redesign). Rewritten: "Now I'm building [ai-engineering](https://github.com/arcasilesgroup/ai-engineering) in the open and organizing tech talks; the numbers below update on their own." — first person, one link, names concrete current work per canon (building ai-engineering, organizing tech talks), short; passes CP1 voice/§16 checks.
STATUS: resolved

VERIFY (post-fix): bare checker `PASS: all 83 checks (checkpoints 1, 2)` exit 0; `--checkpoint 2` `PASS: all 32 checks` exit 0; case 2-4 loop prints `200` for all four widget URLs with no error body, exit 0; mutations A-F all fail as cited; both workflow JSONs parse.
STATUS: resolved
