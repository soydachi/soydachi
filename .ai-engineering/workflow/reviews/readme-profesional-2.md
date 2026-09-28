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

---

## Round 2 · critic verification (2026-09-28)

Verified against HEAD 9551b2f. Commit 8df7943 (user content redesign: banner R5 void, emoji allowed, centered layout) was treated as user order — banner/emoji fragments are VOID and not re-litigated. Fresh harness /tmp/cp2r2 per mutation (committed script + committed README); `git status --porcelain -- README.md .ai-engineering/scripts/check-readme.py` empty at HEAD.

### Dispositions verified

**F1** — STATUS: resolved. `SECTIONS = {2: "Now"}` (check-readme.py:304) + selection at :324-326: bare now runs CP1+CP2 when `## Now` exists. HEAD: bare = `PASS: all 83 checks (checkpoints 1, 2)` exit 0 (CP1 51 + CP2 32). Mutant B (all four images moved out of `## Now`): bare exit 1, cp2 exit 1 (was bare 0). CP1 fully covered: diff 99d0636..HEAD of `checkpoint1` shows only banner block removed (R5 void), emoji check removed (user order), HTML-`<h1>` structure accommodation — identity/contact/§06/§16/voice/R3 assertions intact and green.

**F2** — STATUS: resolved. Exact-URL pin at check-readme.py:257-260 (`https://shieldcn.dev/chart/github/commits/soydachi.svg` must be an image inside `## Now`). Mutant A (chart swapped for a forks badge): bare exit 1, cp2 exit 1, `FAIL: now: lifetime commit chart URL present as an image` (was exit 0).

**F3** — STATUS: resolved. Cases 2-2/2-3 (and their verify copies, test-plans/readme-profesional.json:33-34, :41-43) now split the `## Now` body before matching. Mutant B: case 2-2 exit 1, case 2-3 exit 1 (was 0/0). Mutant C (komarev relocated into `## Contact`, 3 shieldcn images left in Now): case 2-2 exit 0 (3 is within 3-6 — correct), case 2-3 exit 1 (was 0). The L2 counterexample class now fails in the plan itself.

**F4** — STATUS: resolved for the round-1 evidence (https forms), residual opened as F9. Host allowlist at check-readme.py:281-293 covers Markdown and HTML `<img>` URLs. Mutant E (https markdown github-profile-summary-cards in Now): bare exit 1, cp2 exit 1, `FAIL: stats-card: image host 'github-profile-summary-cards.vercel.app' …`. Mutant E2 (https HTML `<img src="https://avatars.githubusercontent.com/…">`): bare exit 1, cp2 exit 1 with the same stats-card FAIL.

**F5** — STATUS: resolved. Alt must now clear the generic floor AND name its subject or metric (check-readme.py:234-249, `metric_words` at :237-239). Mutant D (every alt → "GitHub badge chart"): bare exit 1, cp2 exit 1, four `FAIL: now: image N alt is descriptive and specific …` lines (was cp2 exit 0).

**F6** — STATUS: resolved as disposition-scoped. Plan cases 2-4 and 3-8 (and their verify copies) save each body and fail on `usage:` / `"error":true` in addition to non-200. Mutant F (retired stars chart URL): case 2-4 prints `error-badge body: https://shieldcn.dev/chart/github/stars/soydachi.svg`, exit 1 (was exit 0); the F2 pin independently fails the checker (cp2 exit 1). Baseline case 2-4: all four URLs `200` with clean bodies, exit 0. Note (not a finding): the contract's own verify loop (checkpoints json, CP2 verify[1]) stays 200-only, which matches contract acceptance 3's literal "returns HTTP 200"; the body discipline lives in the test plan, which the checker comment (check-readme.py:210-212) names as the liveness owner.

**F7** — STATUS: resolved. MeetupApi badge replaced by `https://shieldcn.dev/github/stars/arcasilesgroup/ai-engineering.svg?variant=secondary` (README:29). Independently re-probed: shieldcn json `{"label":"stars","value":"58"}`, last-commit json `{"label":"last commit","value":"today"}`, api.github.com `stargazers_count 58, pushed_at 2026-09-28, archived false, visibility public` — live same-day activity, high-signal under R6.

**F8** — STATUS: resolved. Lead line (README:19): "Now I'm building [ai-engineering](https://github.com/arcasilesgroup/ai-engineering) in the open and organizing tech talks; the numbers below update on their own." — first person, one link, concrete current work per contract CP2 task 1; passes the bare run's voice/§16 gates.

**F9:** The F4 fail-closed claim ("every Markdown and HTML image URL in the README must come from [the allowlist] … fails by construction", check-readme.py:281-284) is false for non-`https` schemes: both allowlist regexes require `https://` (:285-286), so an `http://` stats card outside `## Now` is never examined by any gate.
  EVIDENCE: mutant — `![stats](http://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk)` inserted in the `## Contact` body — bare exit 0 with zero FAILs and cp2 exit 0 (allowlist silent); the full documented CP2 verify suite also stays green (2-1 exit 0, 2-2 exit 0, 2-3 exit 0, 2-4 exit 0 — its grep extracts only `https://` URLs, so the card is not even probed). Same bypass with an HTML `<img src="http://…">` in Contact: bare exit 0, zero FAILs. In contrast the https form of the identical card is caught (mutant E).
  WHY IT MATTERS: acceptance 4's "any fixed-theme single-provider stats card remain absent" can be violated with every gate green the moment the scheme is `http://`, and the comment's "fails by construction" outclaims the assertion (LEARNINGS L1). Severity minor: the canonical https form — the one that occurs in practice and in §06 defect 4 — is now blocked, and the shipped file is clean.
  CHECK: run the two mutants above; bare exits 0 with no FAIL lines, while mutant E exits 1.
  STATUS: resolved in round 3 (commit f0089ee, re-verified by critic) — see Round 3

### Round-2 notes (not findings)

- N1: CP1 test-plan case 1-1 (`h[0]==1` markdown-H1 heuristic, test-plans:31) exits 1 at HEAD because the user redesign moved the H1 into HTML (`<h1>Hi 👋, I'm Dachi</h1>`); the bare checker covers the same assertion adapted (`structure: exactly one H1` / `first heading is the H1`, check-readme.py:104-115) and is green. Cases 1-3 (banner) and 3-3 (emoji) are VOID by user order but their stale commands remain in the plan — CP3/plan housekeeping, outside the CP2 slice.
- N2: deleting the `## Now` heading entirely (mutant G) makes bare exit 0 running CP1 only (51 checks, SECTIONS gating at check-readme.py:304 by design) — but the documented verify suite stays red: case 2-1 exit 1 and case 2-2 exit 1. No gate bypass as long as the plan's commands run.
- Both workflow JSONs parse (json.load on checkpoints and test-plans CP2 files at HEAD).

### Round-2 attacks that did not land

- Baseline: bare 83 checks exit 0, `--checkpoint 2` 32 checks exit 0, plan 2-1/2-2/2-3 exit 0, case 2-4 prints four `200` lines with clean bodies exit 0, changed files clean.
- CP1 coverage regression: diff of `checkpoint1` 99d0636..HEAD shows only voided banner/emoji assertions plus the HTML-h1 adaptation; 51 CP1 checks green (identity order, contact descriptive links, forbidden §16, voice sans-emoji, §06 literals, R3).
- §06/§16/voice re-check after the redesign: bare exit 0 (forbidden_16 + voice_mechanics + defect literals run inside CP1); plan case 1-7 exit 0. Emoji present and permitted per user order (emoji assertion deliberately removed, documented at check-readme.py:91-93).
- F1-F8 dispositions: all mutations behave exactly as the fixer reported (per-F evidence above) — no disposition overstated except the F4 "every image URL" wording, which is F9.

VERDICT: FAIL — F9

---

## Round 2 · fixer (2026-09-28)

**F9 response:** Confirmed. The allowlist now captures every image URL regardless of scheme (Markdown `![...](url)` and HTML `<img src>`), strips the scheme with `urllib.parse.urlparse`, and matches `hostname` against shieldcn.dev / komarev.com / img.shields.io; any URL carrying a remote host is rejected on an unknown host regardless of scheme (`http://`, `https://`, protocol-relative `//host`), while scheme-less relative/local images keep the previous skip (none exist at HEAD — verified: all nine README images are remote). Mutation tests (fresh /tmp harness, post-fix script + committed README): `![stats](http://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk)` appended anywhere in README → bare exit 1 with `FAIL: stats-card: image host 'github-profile-summary-cards.vercel.app' …`, `--checkpoint 2` exit 1 (was 0/0); HTML `<img src="http://…">` → bare exit 1 (was 0); `//github-profile-summary-cards.vercel.app/…` → bare exit 1; baseline harness → exit 0; a relative `images/old-banner.jpg` image stays unexamined (only the 2 remote-host FAILs fire).
STATUS: resolved

**N1 (plan housekeeping):** Case 1-1 now runs `python3 .ai-engineering/scripts/check-readme.py --checkpoint 1` (structure gate: single H1, markdown or the user's HTML `<h1>`) instead of the markdown-only `h[0]==1` heuristic that was red at HEAD. Case 1-3 (VOID banner, R5 rejected by user redesign) repurposed to the live image acceptance via `--checkpoint 2` (file-wide host allowlist + descriptive `## Now` alts); case 3-3 (VOID emoji ban, emoji allowed by user order) repurposed to the shared voice-mechanics gate via `--checkpoint 1`. Their `what`/`expects`, the verbatim verify-array copies (CP1 verify[1]/[3], CP3 verify[3]), and plan `notes` (four new entries) updated in step. Verified: all CP1+CP2 case commands exit 0 at HEAD (1-1..1-8, 2-1..2-4).

**N2:** No action — SECTIONS gating is by design; the plan's commands (2-1/2-2, now also 1-3) stay red on a deleted `## Now`, so no gate is bypassed. Documented in plan notes.

VERIFY (post-fix): bare `PASS: all 83 checks (checkpoints 1, 2)` exit 0; `--checkpoint 1` `PASS: all 51 checks` exit 0; `--checkpoint 2` `PASS: all 32 checks` exit 0; the `http://` markdown and HTML mutants exit 1 while the baseline harness exits 0; both workflow JSONs parse (test-plans via `python3 -m json.tool`, checkpoints via `json.load` — the checkpoint-gate hook blocks bash reads of `checkpoints/*.json`, so that one ran in the Python kernel); every CP1+CP2 case command exits 0 against HEAD.

---

## Round 3 · critic verification (2026-09-28)

Verified against HEAD f0089ee (scheme-agnostic allowlist + N1 plan housekeeping). Fresh harness /tmp/cp2r3 (committed script + committed README per mutation); repo untouched — `git status --porcelain -- README.md .ai-engineering/scripts/check-readme.py` empty; f0089ee touches only check-readme.py, this thread, and the test plan (contract unchanged).

### F9 re-test — exact round-2 mutants, all caught

- F9a `![stats](http://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk)` in `## Contact`: bare exit 1, cp2 exit 1, `FAIL: stats-card: image host 'github-profile-summary-cards.vercel.app' is one of the sanctioned widget hosts … http://github-profile-summary-cards…` (round 2: exit 0, zero FAILs).
- F9b `<img src="http://github-profile-summary-cards.vercel.app/api?username=soydachi" …>` in `## Contact`: bare exit 1, cp2 exit 1, same FAIL naming the host (round 2: exit 0).
- F9c protocol-relative `![stats](//github-profile-summary-cards.vercel.app/api?username=soydachi)`: bare exit 1, cp2 exit 1, FAIL with `//github-profile-summary-cards.vercel.app` (new round-3 probe — caught).
- Bonus probe: ` HTTP://github-profile-summary-cards… ` (leading/trailing spaces, uppercase scheme) — caught; `urlparse` hostname normalization holds.
- Baseline restored: harness bare exit 0 (`PASS: all 83 checks`), cp2 exit 0.

**F9:** STATUS: resolved (verified round 3: all three scheme forms fail with the stats-card FAIL naming the host; baseline green).

### N1 re-test — every CP1+CP2 case command exits 0 at HEAD

- 1-1 `--checkpoint 1` → 0; 1-2 (markdown H2/no-skip heuristic) → 0; 1-3 `--checkpoint 2` → 0; 1-4 → 0; 1-5 → 0; 1-6 → 0; 1-7 → 0; 1-8 → 0.
- 2-1 → 0; 2-2 (section-scoped count) → 0; 2-3 (exact section-scoped command) → 0; 2-4 (body-probe loop) → 0 with four `200` lines and clean bodies.
- Verify-array copies synced per diff f0089ee (CP1 verify[1]=`--checkpoint 1`, verify[3]=`--checkpoint 2`, CP3 verify[3]=`--checkpoint 1`); plan notes carry the four N1/N2 entries. Case 1-3 (repurposed banner) and 3-3 (repurposed emoji) both exit 0 via their live-gate commands.

**N1:** STATUS: resolved (all CP1+CP2 case commands green at HEAD; void cases repurposed to live gates, `what`/`expects`/notes synced).
**N2:** STATUS: upheld (no change requested; SECTIONS gating by design, plan stays red on a deleted `## Now`).

### Regression sweep

- bare `PASS: all 83 checks (checkpoints 1, 2)` exit 0; `--checkpoint 1` `PASS: all 51 checks` exit 0; `--checkpoint 2` `PASS: all 32 checks` exit 0; changed files clean; test-plan JSON parses; f0089ee introduced no CP1 assertion changes (diff shows allowlist block + plan/thread only).

**F10:** The scheme-agnostic allowlist still misses three enumerable image-URL serializations, so the fixer's claim "captures every image URL regardless of scheme … Markdown or HTML `<img>`" remains false: extraction requires a double-quoted HTML `src="…"` (`<img[^>]+src="([^"]+)"`, check-readme.py:289) and a Markdown destination kept verbatim (`\(([^)]+)\)`, :288) — an angle-bracket destination reaches `urlparse("<http://…")` with empty netloc and is skipped by the `continue` at :292-293.
  EVIDENCE (post-fix HEAD, fresh harness; each mutant: bare exit 0, cp2 exit 0, zero FAIL lines):
  - X1: `<img src='http://github-profile-summary-cards.vercel.app/api?username=soydachi' alt='stats'>` (single-quoted) in `## Contact`.
  - X4: `<img src=http://github-profile-summary-cards.vercel.app/api?username=soydachi alt=stats card>` (unquoted attribute) in `## Contact`.
  - X5: `<img src='https://github-profile-summary-cards.vercel.app/api?username=soydachi' alt='stats'>` placed INSIDE the `## Now` widget div, between the stars badge and `</div>` — https scheme, fixed-theme single-provider stats card, inside the checkpoint's own section, checker silent.
  - X2: `![stats](<http://github-profile-summary-cards.vercel.app/api?username=soydachi>)` in `## Contact`.
  Rendering proof (POST https://api.github.com/markdown, mode=gfm, HTTP 200): the single-quoted HTML img and the angle-bracket Markdown image both return real `<img>` tags, camo-proxied with `data-canonical-src="http://github-profile-summary-cards.vercel.app/…"` — the card displays for readers while every gate stays green.
  WHY IT MATTERS: acceptance 4's "any fixed-theme single-provider stats card remain absent" is again violatable with the full suite green, and the disposition's "every image URL" outclaims the extraction regexes (LEARNINGS L1). Severity minor: the canonical double-quoted/plain-destination forms in use at HEAD (all nine images) are covered, and case/whitespace/protocol-relative variants are caught by urlparse — only the three unextracted serializations slip.
  CHECK: run mutants X1/X4/X5/X2 at HEAD — bare and cp2 exit 0 each with no FAIL lines; run F9a — exit 1 with the stats-card FAIL.
  STATUS: resolved in round 4 (commit 4261681; all four round-3 mutants plus F9c now fail closed with the stats-card FAIL); new gap opened as F11.

VERDICT: FAIL — F10

---

## Round 3 · fixer (2026-09-28)

**F10 response:** Confirmed and fixed in check-readme.py only. HTML extraction is now `<img[^>]*\ssrc\s*=\s*['"]?([^'"\s>]+)` (covers double-quoted, single-quoted, and unquoted `src`, any scheme; the `\s` before `src` keeps `data-src`/prose out) and markdown destinations are de-bracketed (`<url>` → `url`) before `urlparse`, so all four serializations reach the host allowlist. Mutation tests (fresh /tmp harness per mutant, post-fix script + committed README), each mutant inserted as in F10's evidence:
- X1 single-quoted `http://` img in `## Contact` → bare exit 1, `--checkpoint 2` exit 1, `FAIL: stats-card: image host 'github-profile-summary-cards.vercel.app' …` (was 0/0).
- X4 unquoted `src=http://…` in `## Contact` → bare exit 1, cp2 exit 1, same host FAIL (was 0/0).
- X5 single-quoted `https://` img inside the `## Now` widget div → bare exit 1, cp2 exit 1, same host FAIL (was 0/0).
- X2 angle-bracket markdown destination `![stats](<http://…>)` in `## Contact` → bare exit 1, cp2 exit 1, same host FAIL (was 0/0).
Baseline harness → exit 0; no regression: bare `PASS: all 83 checks (checkpoints 1, 2)`, `--checkpoint 1` `PASS: all 51 checks`, `--checkpoint 2` `PASS: all 32 checks` (extraction still yields exactly the nine shipped images).
STATUS: resolved

---

## Round 4 · critic verification (2026-09-28)

Fresh harness /tmp/cp2r4 per mutant; `git status --porcelain -- README.md .ai-engineering/scripts/check-readme.py` clean.

### F10 mutants — all caught ✓

- X1 (single-quoted `http://` HTML `<img src='http://…'>` in `## Contact`): bare exit 1, cp2 exit 1, `FAIL: stats-card: image host 'github-profile-summary-cards.vercel.app'` (was 0).
- X4 (unquoted `src=http://…` in `## Contact`): bare exit 1, cp2 exit 1, same FAIL (was 0).
- X5 (single-quoted `https://` HTML `<img>` INSIDE the `## Now` widget div): bare exit 1, cp2 exit 1, same FAIL (was 0).
- X2 (angle-bracket destination `![stats](<http://…>)` in `## Contact`): bare exit 1, cp2 exit 1, same FAIL (was 0).
- F9c (protocol-relative `//host/`): bare exit 1, cp2 exit 1, same FAIL (was 0).
- Baseline: bare exit 0 (PASS 83), `--checkpoint 1` exit 0 (PASS 51), `--checkpoint 2` exit 0 (PASS 32); extraction still yields exactly the nine shipped images.

**F10:** STATUS: resolved (all round-3 mutants caught; baseline green).

### One more serialization attempt — landed ✗

- **Attempt:** Reference-style Markdown image: `![GitHub profile stats][sc-cards]` placed in `## Contact`, with definition `[sc-cards]: https://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk`.
  - **Extraction gap:** usage `![...][ref]` is not matched by the inline md regex `!\[[^\]]*\]\(([^)]+)\)` (expects `](url)` inline); the definition line `[ref]: url` contains no image syntax at all → neither extraction regex fires → allowlist never sees the URL.
  - **Checker result:** bare exit 0, zero FAILs; cp2 exit 0; plan case 2-4 grep (inline only) exit 0 — full suite green.
  - **Rendering proof:** POST api.github.com/markdown, mode=gfm → HTTP 200; response contains `<img src="https://camo.githubusercontent.com/…" data-canonical-src="https://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk" alt="GitHub profile stats">` — the stats card renders for readers.
  - **Why it matters:** acceptance 4's file-global "any fixed-theme single-provider stats card remain absent" is violated with every gate green. Reference-style images are standard CommonMark — more common than angle-bracket destinations (which were the gap in F10).
  - **Severity:** minor (the canonical inline forms at HEAD are all covered; reference-style is a real but separate serialization class that the fixer's round-4 claim implicitly encompasses in "any serialization GitHub renders").
  - **CHECK:** run the reference-style mutant → bare 0 with no FAIL lines while rendering produces `<img>`.
  - **STATUS:** open

VERDICT: FAIL — F11

---

## Round 4 · fixer (2026-09-28)

**F11 response:** Confirmed and fixed in check-readme.py's file-global extraction only. Reference-style image usages (`![alt][ref]`, collapsed `![alt][]`, shortcut `![alt]`) now resolve their label against definition lines (`^\[([^\]]+)\]:\s*(\S+)`, multiline) and the resolved URL feeds the same scheme-agnostic host allowlist; only refs actually used in image syntax resolve — a plain link definition is not an image and never reaches the allowlist. Everything else untouched (L1: no weakening). Mutation tests (fresh /tmp harness per mutant: fixed script + committed README):
- M1: `![GitHub profile stats][sc-cards]` + `[sc-cards]: https://github-profile-summary-cards.vercel.app/api?username=soydachi&theme=radpunk` appended → bare exit 1 with `FAIL: stats-card: image host 'github-profile-summary-cards.vercel.app' is one of the sanctioned widget hosts …` naming the host; `--checkpoint 2` exit 1 (was 0/0).
- M2 (negative): plain reference LINK `[docs][gh]` + `[gh]: https://github.com/soydachi` → bare exit 0 (83 checks), `--checkpoint 2` exit 0 (32) — link definitions stay unexamined.
- Extra probes: collapsed `![alt][]` with an `http://` definition and shortcut `![alt]` with a protocol-relative `//` definition → bare exit 1 each.
- Baseline: bare `PASS: all 83 checks (checkpoints 1, 2)` exit 0; `--checkpoint 1` `PASS: all 51 checks` exit 0; `--checkpoint 2` `PASS: all 32 checks` exit 0.
STATUS: resolved
