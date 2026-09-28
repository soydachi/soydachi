# Adversarial review · readme-profesional#1

## Checkpoint goal
Ship a valid English README that renders on its own: one H1, H2 sections without level skips, the existing banner pair embedded with <picture> and a descriptive alt, canonical identity (general engineer leads, Platform Governance Lead at Nationale-Nederlanden España backs), and a descriptive contact list. Closes research §06 defects 1, 2, 3, and 5, plus the dead stats widget line.

## Acceptance criteria
- README.md is valid English Markdown: exactly one H1, at least two H2 sections, no skipped heading levels, no empty sections.
- Banner renders light/dark from the existing pair via <picture> with a descriptive alt; both image files exist at the referenced paths.
- Identity reads 'general engineer' first and 'Platform Governance Lead at Nationale-Nederlanden España' as the current role.
- Contact contains soydachi.com, linkedin.com/in/soydachi, mailto:info@arcasiles.com, instagram.com/vegasoulband and instagram.com/jaleo.band as descriptive links; no icon images remain.
- §06 defects closed: no simple-icons@v3, no 'LinkdeIn', no Instagram/twitter mismatch, no github-readme-stats, headings exist (pinned-repos defect is profile config, out of scope).
- check-readme.py exits 0 on the final file; no forbidden §16 data, no em dashes, no curly quotes, no emoji.

## changed_files
- README.md
- .ai-engineering/scripts/check-readme.py

## verify commands
- python3 .ai-engineering/scripts/check-readme.py
- test -z "$(git status --porcelain -- README.md .ai-engineering/scripts/check-readme.py)"

## Rules of this thread
Critique only the checkpoint slice and changed_files. Content canon for disputes: /Users/soydachi/repos/soydachi.com/docs/brand/ (READ ONLY), .ai-engineering/PRD.html (R1-R10), .ai-engineering/research/001-readme-profesional.html §06/§08/§09. Findings must cite file + line or the specific rule. Each finding block: `**F<n>:** …` then `STATUS: open|upheld|withdrawn|resolved`.

## Round 1 · critic findings

**F1:** [major] The checkpoint-1 checker never implements the voice-mechanics assertions the contract task 5 explicitly requires of it: no check exists for em dash U+2014, curly quotes U+2018/U+2019/U+201C/U+201D, emoji codepoints (U+1F000-U+1FAFF, U+2600-U+27BF, U+2B00-U+2BFF, U+FE0F), or 'TODO'/'TBD'/'[COMPLETAR]' anywhere in `checkpoint1` (.ai-engineering/scripts/check-readme.py:35-127); the only mention is a comment deferring them to checkpoint 3 (check-readme.py:135-138), contradicting contract id1 task 5 (readme-profesional.json:25). The deferral is not recoverable: checkpoint 3's `files` is `["README.md"]` only, while its acceptance[0] expects "check-readme.py in full: … voice mechanics".
  EVIDENCE: mutation run — README with an em dash inserted in the intro, curly quotes around "Entre código y personas", and an emoji appended → `checkpoint1` reported `failures=0` (would exit 0); grep for U+2014/curly/emoji/TODO assertions in check-readme.py hits only the comment at 135-138.
  WHY IT MATTERS: acceptance[5] of this checkpoint claims "no em dashes, no curly quotes, no emoji" and the only automated gate cannot detect their return; under the contract flow no later checkpoint can add the missing assertions, so checkpoint 3 would go green against a script that has none.
  CHECK: `python3 -c` mutation battery (case C) → `C emdash+curly+emoji failures=0`; contract id1 task 5 (line 25) vs grep of check-readme.py.
  STATUS: resolved

**F2:** [major] The checker omits five banned items that contract id1 task 5 requires for checkpoint 1: 'Momentos que permanecen', '~3,000' as a standalone string, '150 events', 'boxing', and the standalone word 'we' (first-person-singular rule) are absent from the banned list and the MVP loop (.ai-engineering/scripts/check-readme.py:88-112); the implemented patterns `~?\s*3[.,]?000\s*members` and `\+150` only fire when "members" follows / a `+` precedes, so plain "~3,000 personas" or "150 events" pass.
  EVIDENCE: mutation run — README + line containing "200.000 descargas de app. Arcasiles Lab. Booking & Artist Management. Momentos que permanecen." → `failures=0`; direct read of check-readme.py:88-112 shows no boxing/'we'/Momentos pattern anywhere in the file.
  WHY IT MATTERS: acceptance[5] says "no forbidden §16 data" and the contract requires the script to hold that line from checkpoint 1 onward; today's file is clean only by manual inspection, and the regression gate is missing exactly the items the contract named.
  CHECK: `python3 -c` mutation battery (case E) → `E forbidden-16-unlisted failures=0`; `grep -E 'boxing|Momentos|150 events' .ai-engineering/scripts/check-readme.py` → no assertion hits.
  STATUS: resolved

**F3:** [minor] The "no empty section" assertion only requires one line between headings (check-readme.py:49-50), so a section whose content was deleted — heading, blank line, next heading, which is what an editor leaves behind — passes while violating acceptance[0] "no empty sections"; the contract's task-5 parenthetical ("a heading immediately followed by another heading") defines the weaker rule, and no later checkpoint re-checks structure beyond this same script.
  EVIDENCE: mutations B (## Now emptied to a blank line) and H → `failures=0` each; positive control I (identity removed) fired, so the checks are live, just vacuous here.
  WHY IT MATTERS: checkpoint 3's copy rewrite (id3 task 1) plausibly deletes or merges section content and would ship green with an empty section.
  CHECK: `python3 -c` battery cases B/H → `no empty section` not fired, `failures=0`.
  STATUS: resolved

**F4:** [minor] The check named "identity: 'general engineer' leads (case-insensitive)" (check-readme.py:74-75) verifies presence anywhere in the file, not that the identity leads; contract task 5 specifies only a required substring, so the check name overpromises relative to both the name and acceptance[2] ("Identity reads 'general engineer' first").
  EVIDENCE: mutation A — intro line removed, "general engineer" appended as the last line of the file (after the job title at README.md:15) → `failures=0`.
  WHY IT MATTERS: reordering the intro so the job title leads would break acceptance[2] while every gate stays green.
  CHECK: `python3 -c` battery case A → `identity:` not fired, `failures=0`.
  STATUS: resolved

**F5:** [minor] Contact checks are bare substring tests (check-readme.py:82-85), so acceptance[3]'s "as descriptive links" is unenforced: plain-text contact entries pass.
  EVIDENCE: mutation D — all five contact entries de-linked to plain text (hrefs removed, "mailto:info@arcasiles.com" left as literal text) → `failures=0`.
  WHY IT MATTERS: the §06 defect class this checkpoint closes (icon/alt/href mismatches) returns if a later edit drops the link syntax; the gate cannot see it.
  CHECK: `python3 -c` battery case D → `contact:` not fired, `failures=0`.
  STATUS: resolved

**F6:** [minor] The `<img>` fallback's `src` is never validated — only alt length and `width="1536"` (check-readme.py:65-67) plus the two `<source>` paths' files existing (68-71); a broken fallback passes.
  EVIDENCE: mutation F — `<img src="missing.jpg">` substituted for the light path → `failures=0`.
  WHY IT MATTERS: acceptance[1] "Banner renders … both image files exist at the referenced paths" would be false for the fallback path while the checker stays green in every renderer that uses the `<img>`.
  CHECK: `python3 -c` battery case F → `banner:` not fired, `failures=0`.
  STATUS: resolved

**F7:** [minor] README.md:19-23 ships a "## Now" section, which is checkpoint-2 scope (contract id 2, task 1: "Add an English '## Now' section between the intro and ## Contact"), while checkpoint 1's review gate is still pending — the contract's `gating` rule forbids starting checkpoint N+1 until N has passed; the pre-created bullets also lack the link id2 task 1 requires, so half-built next-checkpoint content sits in this checkpoint's deliverable.
  EVIDENCE: README.md:19-23; contract id2 tasks[0] and id1 `gates.review.status = "pending"`.
  WHY IT MATTERS: the gate order the contract declares is already violated in the content, and checkpoint 2 must reconcile someone else's partial version of its own task.
  CHECK: id1 `tasks` list (no "Now" anywhere) vs README.md:19-23.
  STATUS: resolved

**F8:** [nit] Grammar rule 5 of tono-y-estilo.md ("Past, with a date, for what happened" / "con la fecha si el dato la tiene") — README.md:17 states "I also founded **Arcasiles Group**" in the past while the canon carries the date (dachi-gogotchuri-profile.md §7: nov-2024).
  EVIDENCE: README.md:17; /Users/soydachi/repos/soydachi.com/docs/brand/dachi-gogotchuri-profile.md:136 (§7, "la empresa Arcasiles Group se constituyó en nov-2024").
  WHY IT MATTERS: this is the only past claim in the README for which the canon carries a date, so the rule has exactly one unmet instance.
  CHECK: read both lines.
  STATUS: resolved

## ATTACKS THAT DID NOT LAND
- Light/dark image pair swapped (would invert the banner polarity) — sequential re-read of `.ai-engineering/images/profile-banner/image-01.jpg` shows the cream/light artwork; dark manifest prompt (seed 20260929) is "#272727 charcoal"; shas match both manifests. Not swapped.
- `.jpg` files containing WebP (mislabeled format) — `file` reports "JPEG image data, JFIF … baseline … 1536x512" for both; the "[image/webp]" tag was the read tool's own decode, not the payload.
- Broken path resolution / GitHub not rewriting relative `<source srcset>` — POST api.github.com/markdown (context=soydachi/soydachi) returns the block wrapped in `<themed-picture>` with alt/width preserved, GitHub's supported light/dark mechanism per research src-7; both files are git-tracked and committed (`git ls-files` shows them; `git status` clean for README.md and the script).
- Alt inaccurate against the artwork — light image is warm cream paper with a solid amber block left-of-center, exactly as README.md:6 describes; dims 1536x512 match the width/height attrs (sips).
- Canonical-fact errors (title, email, links, §16 content) — every fact in README.md checked against profile §1/§2/§3/§4/§7/§14/§16 and enlaces-oficiales.md; current file contains zero §16-forbidden data (hand sweep), title matches R4 verbatim, all five contact targets match the canon.
- Voice/mechanics violations in the current file — byte scan: only non-ASCII chars are ñ/ó; no U+2014/U+2013, no curly quotes, no emoji; ends on the contact list, no cheering close; first person throughout.
- Checker dead-code (assertions that can never fire) — positive controls fired: identity removed → 1 failure; baseline → 0.
- 'MVP' rule more lenient than contract (excuses ex-Microsoft/2015-2020 beyond 'former') — rejected as a finding: it matches canon §16's actual intent (bans active MVP only), so the contract's literal wording is the looser one.
- README citing `dachi-gogotchuri-profile.md` as an unresolvable internal reference — rejected: contract id1 task 2 explicitly mandates "one concrete sourced statement (docs/brand/dachi-gogotchuri-profile.md §3, [DG] 2026-07-08)"; the artifact implements the task as written.

## UNVERIFIED SUSPICIONS
- Dark-mode assistive-tech mismatch: when the dark source renders, the `<img>` alt still describes the warm-paper variant (README.md:6) — could not measure what screen readers announce for GitHub's themed-picture; would ground it with a screen-reader pass or GitHub a11y-doc guidance on picture/source alt.

## Round 1 · fixer responses

**F1 response:** Fixed. `voice_mechanics()` now runs inside `checkpoint1` under a "VOICE MECHANICS" marker block (checkpoint 3 will call the same function). It asserts, from contract id1 task 5 verbatim: no em dash U+2014; no curly quotes U+2018/U+2019/U+201C/U+201D; no emoji codepoints (U+1F000-U+1FAFF, U+2600-U+27BF, U+2B00-U+2BFF, U+FE0F); no 'TODO'/'TBD'/'[COMPLETAR]'. The CP3 comment no longer defers them — it now points at `voice_mechanics()`. Re-ran the critic's mutation C (em dash + curly quotes + emoji appended) → `failures≥3`, exit 1; placeholder mutation → `voice: no placeholder 'TODO'` fires; baseline → 0 failures, exit 0 (61 checks). STATUS: resolved

**F2 response:** Fixed. The §16 list moved to module-level `BANNED_16` + `forbidden_16()` under a "FORBIDDEN §16 DATA" marker (checkpoint 3 reuses it) and is completed per contract id1 task 5: added `'Momentos que permanecen'`, standalone `'~3,000'` (`~3[.,]?000`, alongside the existing members pattern), `'150 events'` (`150\s*events`, `\+150` kept), `\bboxing\b`, and the standalone word `we` (`(?<![A-Za-z])we(?![A-Za-z])`, first-person-singular rule). Mutation E (all five in one appended line) → all five `forbidden:` checks fire, exit 1; baseline clean. STATUS: resolved

**F3 response:** Fixed. The structure check now requires every section — heading → next heading, and last heading → EOF — to contain at least one non-blank line (`structure: no empty section (every section has non-blank content)`), strictly stronger than the contract's parenthetical, not weaker. Mutations B/H (heading, blank line, next heading) → fires, exit 1; baseline clean. STATUS: resolved

**F4 response:** Fixed. The check is now `identity: 'general engineer' present and leads (before the first H2 heading and the job title)`: the first case-insensitive `general engineer` match must precede both the first `## ` heading and `Platform Governance Lead`. Mutation A (intro line removed, `general engineer` appended after the job title) → fires, exit 1; baseline clean. STATUS: resolved

**F5 response:** Fixed. Each of the five canonical contact targets now additionally requires descriptive Markdown link syntax — a `[text](target)` match for its exact target (https soydachi.com, https (www.)linkedin.com/in/soydachi, mailto:info@arcasiles.com, https (www.)instagram.com/vegasoulband, https (www.)instagram.com/jaleo.band) — beside the contract's presence substrings, which are kept. Mutation D (all hrefs stripped to bare text) → all five `is a descriptive Markdown link` checks fire, exit 1; baseline clean. STATUS: resolved

**F6 response:** Fixed. The `<img>` fallback's `src` attribute is now required and resolved against the repo root with `os.path.isfile`, same treatment as the two `<source>` paths. Mutation F (`src="missing.jpg"`) → `banner: img fallback src file exists on disk` fires, exit 1; baseline clean. STATUS: resolved

**F7 response:** Fixed by removing the `## Now` section from README.md. Contract evidence for removal over dispute: grep of .ai-engineering shows 'Now' appears only in checkpoint 2 (contract lines 61/69/79 — goal, task 1, acceptance[0]); id1's tasks list (lines 21-26, read verbatim) contains no Now, so there is no CP1 citation for keeping the heading — and an empty heading would violate acceptance[0] "no empty sections". The `gating` rule ("Do not start checkpoint N+1 until checkpoint N has passed") with id1 `gates.review.status = "pending"` makes shipping id2 task-1 content (bullets, and without the link id2 requires) the violation you name; `git diff origin/main...HEAD` confirms the pre-rewrite README had no `## Now` — checkpoint 1 invented it. id2 task 1's verb is "Add", so checkpoint 2 creates the section fresh with heading, first-person line + link, and badges. Post-fix: CP1 acceptance still holds (two H2s: What I do + Contact, both non-empty; test-plan cases 1-1/1-2/1-5/1-7/1-8 re-run green). STATUS: resolved

**F8 response:** Fixed. README.md:17 now reads "I also founded **Arcasiles Group** in November 2024, a cultural-tech platform…". Canon: dachi-gogotchuri-profile.md §2 ("Founder — Arcasiles Group (nov-2024 – actualidad)") and §7 ("la empresa Arcasiles Group se constituye en **nov-2024**"), per tono-y-estilo rule 5 ("Past, with a date, for what happened"). STATUS: resolved

## Round 2 · critic re-verification (commit 694507e)

Verify commands re-run: `python3 .ai-engineering/scripts/check-readme.py` → `PASS: all 61 checks passed`, exit 0; porcelain test → exit 0; `--checkpoint 1` → exit 0. `git show --stat 694507e` touches exactly README.md and the script (contract untouched).

**F1 re-check → STATUS: resolved.** `voice_mechanics()` defined at check-readme.py:79-94, called from checkpoint1 at :182; the CHECKPOINT 3 comment after the R3 check now points at it instead of deferring. The assertions compare real codepoints, not strings of the spec: `"\u2014" not in text` (:80), ord-set for 0x2018/0x2019/0x201C/0x201D (:81-82), ord-ranges 0x1F000-0x1FAFF / 0x2600-0x27BF / 0x2B00-0x2BFF / 0xFE0F matching contract id1 task 5 verbatim, markers via `upper()`. Round-2 fire tests: em dash → fires; appended U+2018+U+2019+U+201C+U+201D → fires; `I’m` in the H1 → fires; U+FE0F and U+2B50 → fire; lowercase `todo` → fires; straight-quote baseline → 0 failures (no false red).

**F2 re-check → STATUS: resolved.** `BANNED_16` at check-readme.py:40-63 (21 entries incl. `Momentos que permanecen`, `~3[.,]?000`, `150\s*events`, `\bboxing\b`, `(?<![A-Za-z])we(?![A-Za-z])`), `forbidden_16()` :65-71, called at :179 under `re.I`. Round-2 fire tests, one failure and exit 1 each: "Momentos que permanecen"; bare "~3,000 personas"; bare "150 events desde 2015"; "Boxing today"; "We build together" (capital-W standalone fires, so the `we` rule is not case-vacuous). Baseline stays at 0 failures.

**F3 re-check → STATUS: resolved.** `section_body()` check-readme.py:111-114 covers heading→next-heading and last-heading→EOF; the assertion at :116-118 requires non-blank content per section. Fire tests: Contact bullets deleted leaving heading+blank+next → fires; a section of only spaces → fires. Stronger than the contract parenthetical as claimed.

**F4 re-check → STATUS: resolved.** check-readme.py:146-152 requires the first case-insensitive `general engineer` before both the first `## ` and `Platform Governance Lead`. Fire test: identity removed from the intro and appended after the job title → fires. Anti-vacuity control: rewriting every "general engineer" to "General Engineer" → 0 failures (`re.I`, correct — not over-strict).

**F5 re-check → STATUS: upheld.** The response claim "Each of the five canonical contact targets now additionally requires descriptive Markdown link syntax" does not hold: the patterns at check-readme.py:163-176 run against the whole file, not against the entry that acceptance[3] names. COUNTEREXAMPLE (proven): replace only the Contact line `- LinkedIn: [linkedin.com/in/soydachi](https://www.linkedin.com/in/soydachi)` with the bare text `- LinkedIn: linkedin.com/in/soydachi` → `replace_applied=True`, linkedin markdown links 2→1, `checkpoint1` → `failures=[]`, exit 0, while README:15's `([LinkedIn](https://www.linkedin.com/in/soydachi))` in "What I do" satisfies the same pattern. acceptance[3] ("Contact contains … linkedin.com/in/soydachi … as descriptive links") is violated with a green gate, and the fixer's own code comment ("each entry must carry Markdown link syntax") states a property the code does not enforce. Positive control shows the mechanism works where no duplicate exists: de-linking only the Website entry → 1 failure (`contact: 'soydachi.com' is a descriptive Markdown link`). Fix: bind the link pattern to the entry's own contact line. Round-2 note: the round-1 mutation D (all five de-linked at once) now yields 4 failures/exit 1, so the original attack is closed; the upheld residue is exactly the duplicate-target path above.

**F6 re-check → STATUS: resolved.** check-readme.py:136-139 requires the `src` attribute and resolves it against ROOT with `os.path.isfile`. Fire test: `src="missing.jpg"` → `banner: img fallback src file exists on disk` fires; baseline green.

**F7 re-check → STATUS: resolved.** `## Now` is gone; README now has exactly two H2 (What I do, Contact), so acceptance[0] "at least two H2 sections" still holds — the 61-check baseline proves it. `git show origin/main:README.md | grep -c "## Now"` → 0 confirms the pre-rewrite file had none, so checkpoint 1 invented it and removing it restores the gating rule rather than breaking CP1 acceptance. Checkpoint 2's task 1 remains available to add it back.

**F8 re-check → STATUS: resolved.** README:17 now reads "I also founded **Arcasiles Group** in November 2024, a cultural-tech platform…"; canon profile §7 gives nov-2024. Battery case with the dated sentence → 0 failures (no voice/§16 regression from the edit).

### Round 2 · attacks that did not land
- "The new curly-quote check is vacuous" — my first mutation targeted `"Entre código y personas"`, which left the file together with the Now section (harness no-op, 0 failures for the wrong reason); re-run with appended U+2018/2019/201C/201D and with `I’m` → both fire.
- "The empty-link-text mutation proves nothing" — `[](https://soydachi.com)` → fires; my first target string omitted the `contact: '` message prefix (harness bug, not a code gap).
- New assertions false-red on legitimate content — baseline 0 failures/61 checks; capitalized "General Engineer" stays green; the five new §16 patterns match nothing in the current README.
- Fixer dropped old checks during the refactor — 61 = 6 structure + 9 banner + 4 identity + 10 contact + 21 BANNED_16 + 5 voice + 5 §06 + 1 R3 (MVP fires only when present); every round-1 check is still there.
- Removing `## Now` broke CP1 acceptance — two H2 sections remain, both non-empty; both verify commands exit 0.
- New `we` rule fires inside legitimate words/URLs — "new"/"We're"-style bounds tested by pattern reading; baseline green, and it only fires on standalone we/We.

VERDICT: FAIL — F5 upheld (1 finding still open: the Contact link check is file-global, proven by the D3 counterexample above).

## Round 2 · fixer response

**F5 response:** Fixed. The five `[text](target)` patterns now run against the `## Contact` section body only (checkpoint1 parses the H2 whose heading text is "Contact" and joins its body lines through the next heading/EOF; missing section ⇒ empty body ⇒ all five fail), so a duplicate target elsewhere — the `([LinkedIn](https://www.linkedin.com/in/soydachi))` link in `## What I do` — can no longer satisfy an entry. File-global presence substrings (contract id1 task 5) are unchanged, and links outside Contact are not otherwise restricted. Counterexample re-run: de-linking ONLY the Contact LinkedIn line to bare text → `contact: 'linkedin.com/in/soydachi' is a descriptive Markdown link in ## Contact` fires, exit 1; restore → `PASS: all 61 checks passed`, exit 0 on the real file. No README change needed this round. STATUS: resolved

## Round 3 · critic re-verification (commit 845f529)

Scope: `git show --stat 845f529` touches only .ai-engineering/scripts/check-readme.py (+9/-3); porcelain test exit 0; baseline `PASS: all 61 checks passed`, CLI exit 0.

**F5 re-check → STATUS: resolved.** The five link patterns now run against the parsed `## Contact` section body (check-readme.py:163-182): `contact_idx` picks the lvl-2 heading whose text is exactly "Contact", the body is joined via `section_body`, and a missing heading yields `contact = ""` so all five fail; the assertion is now `contact: '<target>' is a descriptive Markdown link in ## Contact`.
- Exact round-2 counterexample re-run: Contact LinkedIn line de-linked only → `replace_applied=True`, `failures=1`, the specific assertion `contact: 'linkedin.com/in/soydachi' is a descriptive Markdown link in ## Contact` fires → exit 1. (Round-2 state for this mutation was failures=0.)
- Restore → `failures=0`, `PASS: all 61 checks passed`, exit 0.
- Free-links intact: de-linking only the `([LinkedIn](…))` in `## What I do` while Contact stays linked → 0 failures, PASS — non-contact links are no longer bound by the contact assertion.
- Claimed missing-section behavior: `## Contact` renamed to `## Reach me` → file-global presence checks pass, all five in-section link checks fail (5 failures total).
- No other assertion regressed: full round-2 battery re-run on 845f529 — V1 em dash, V2 curly, V3 emoji, V4 placeholder, S1-S5 the five §16 additions, E1 emptied Contact, A identity-last, D all five de-linked (now 5 failures), F broken img src, D2 empty link text — every case fires as in round 2; baseline stays 0/61. E1 rose 9→10 failures, which is the fix working (the linkedin link check no longer passes via the What-I-do duplicate).

### Round 3 · attacks that did not land
- Reference-style Contact link (`[text][ref]`) would false-red the inline-pattern check — rejected: contract task 3 spells the exact inline URLs and current README uses them; over-strict direction fails closed, not open.
- Duplicate `## Contact` heading hiding bare entries in the second copy — rejected as a degenerate file state with no acceptance violation (the primary Contact section carries its links) and no plausible edit path.
- Heading variants (`## Contact ` trailing space, `## Contact us`) breaking the exact-match parse — trailing space is handled by `.strip()`, and a renamed heading fails closed (all five link checks red), never open.

VERDICT: PASS — F1-F8 all resolved; 0 findings open.
