# Learnings

Accumulated failures and lessons from building features, mostly written by `/ai-orchestrator`. Every planner, implementer, test writer and reviewer reads **Rules** before starting.

- **Log** is append-only: never edit or delete an entry.
- **Rules** is the distilled version. A lesson is promoted here once it has recurred (2 or more log entries) or caused a human-review rejection or a circuit-breaker stop. Each rule cites the entries it came from.

## Rules

<!-- - R1: <imperative rule>. (from L3, L7) -->

## Log

### L1 · 2026-09-28 · readme-profesional #1 · review
- **Failure:** Adversarial round 1, 8 findings: `check-readme.py` implemented only the easy substring subset of contract task 5 — voice mechanics (em dash, curly quotes, emoji) and five §16 bans existed only in a deferring comment; qualitative acceptance terms ("leads", "descriptive links", "no empty section") were unenforced; and the implementer invented CP2's `## Now` section inside CP1.
- **Root cause:** The checker was written to go green, not to encode the acceptance text; nobody mutation-tested the assertions against the contract they claimed to cover.
- **Fix:** Checker strengthened to contract task 5 verbatim (61 checks, 7 mutation cases fire, baseline green); `## Now` removed; canon founding date (November 2024) added to the Arcasiles sentence. Commits 694507e.
- **Lesson:** A gate whose name outclaims its assertion is worse than no gate: the acceptance text is the spec, and every assertion must be mutation-tested before the checkpoint that relies on it.
- **Tags:** tests, review, scope

### L2 · 2026-09-28 · readme-profesional #1 · review
- **Failure:** Adversarial round 2, F5 upheld: contact-link checks were file-global, so a LinkedIn link inside `## What I do` satisfied an acceptance criterion scoped to the `## Contact` section — proven counterexample exited 0 while de-linking Contact.
- **Root cause:** The assertion's scope (whole file) did not match the acceptance criterion's scope (one section), and the mutation test never placed a duplicate of the target outside the section.
- **Fix:** The five patterns now run against the parsed `## Contact` body only; counterexample fails (exit 1), free links elsewhere stay green; commit 845f529.
- **Lesson:** An assertion's scope must match the acceptance criterion's scope — matching content anywhere in the file is not matching it in the section the contract names; mutation-test with a duplicate of the target outside the section.
- **Tags:** tests, review, scope

### L3 · 2026-09-28 · readme-profesional #2 · review
- **Failure:** Review gate hit the 4-round cap with F11 open: reference-style markdown images (`![alt][ref]` + definition line) bypassed every extraction layer, so a banned stats card rendered in GFM while bare, cp1, cp2 and the curl case all stayed green. Two earlier findings in the same loop (F9 http scheme, F10 quoting/bracket serializations) were the same class.
- **Root cause:** The extractor was written around the serializations the README happened to use instead of every serialization the renderer accepts; each round the critic found one more form.
- **Fix:** Extraction now covers inline, HTML (all quoting), angle-bracket, reference/collapsed/shortcut forms, scheme-agnostic, host-allowlisted; mutation-tested per syntax form (commit 895123d, M1/M2/baseline green).
- **Lesson:** An extraction gate must cover every serialization the renderer accepts — mutation-test each syntax form (inline, HTML, reference-style) or the gate's name outclaims its assertion.
- **Tags:** tests, review, extraction
