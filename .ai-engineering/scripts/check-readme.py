#!/usr/bin/env python3
"""Assertions for the readme-profesional rewrite. Run from anywhere.

Usage: python3 .ai-engineering/scripts/check-readme.py [--checkpoint N]
No --checkpoint runs every implemented checkpoint. Exit 0 + PASS line when
all selected assertions hold; exit 1 printing each failing assertion.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README = os.path.join(ROOT, "README.md")

failures = []
checks = 0


def check(name, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        failures.append(f"{name}{': ' + detail if detail else ''}")


def read_readme():
    try:
        with open(README, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        failures.append("README.md: file not found")
        return None


# =============================================================================
# FORBIDDEN §16 DATA — contract id1 task 5. Checkpoint 1 runs this from day
# one; checkpoint 3's full sweep reuses it via forbidden_16() — extend the
# list here, never in a second copy.
# =============================================================================
BANNED_16 = [
    (r"Cloud Solution", "obsolete NN title"),
    (r"Platform Engineering Lead", "obsolete NN title"),
    (r"Mobile Lead Engineer", "obsolete NN title"),
    (r"instagram\.com/lasobremesa", "lasobremesa link"),
    (r"NN Digital Hub", "NN Digital Hub"),
    (r"Momentos que permanecen", "retired tagline"),
    (r"~?\s*3[.,]?000\s*members", "false ~3000 members metric"),
    (r"~3[.,]?000", "false ~3,000 metric"),
    (r"\+150", "false +150 events metric"),
    (r"150\s*events", "false 150 events metric"),
    (r"\bboxing\b", "boxing as current activity"),
    (r"(?<![A-Za-z])we(?![A-Za-z])", "first person plural 'we'"),
    (r"\bai-mem\b", "private repo name"),
    (r"\bpostflow\b", "private repo name"),
    (r"\bpaperclip\b", "private repo name"),
    (r"arcasiles-hq", "private repo name"),
    (r"solution-intents", "private repo name"),
    (r"\blifeos\b", "private repo name"),
    (r"arcasiles-lens", "private repo name"),
    (r"lens\.arcasiles", "private repo name"),
    (r"https://(?:www\.)?arcasiles\.com", "dead arcasiles.com contact link"),
]


def forbidden_16(text):
    for pat, why in BANNED_16:
        check(f"forbidden: absent '{pat}' ({why})",
              not re.search(pat, text, re.I))
    for i, l in enumerate(text.splitlines(), 1):
        if re.search(r"MVP", l) and not re.search(
                r"former|ex-Microsoft|2015.?2020", l, re.I):
            check(f"forbidden: no active MVP mention (line {i})", False, l.strip())


# =============================================================================
# VOICE MECHANICS — contract id1 task 5. Checkpoint 3's voice sweep calls this
# same function; add new mechanics here so every checkpoint shares one gate.
# =============================================================================
def voice_mechanics(text):
    check("voice: no em dash (U+2014)", "\u2014" not in text)
    curly = sorted({f"U+{ord(c):04X}" for c in text
                    if ord(c) in (0x2018, 0x2019, 0x201C, 0x201D)})
    check("voice: no curly quotes (U+2018/U+2019/U+201C/U+201D)",
          not curly, ", ".join(curly))
    emoji = sorted({f"U+{ord(c):04X}" for c in text
                    if 0x1F000 <= ord(c) <= 0x1FAFF
                    or 0x2600 <= ord(c) <= 0x27BF
                    or 0x2B00 <= ord(c) <= 0x2BFF
                    or ord(c) == 0xFE0F})
    check("voice: no emoji codepoints (U+1F000-U+1FAFF, U+2600-U+27BF, "
          "U+2B00-U+2BFF, U+FE0F)", not emoji, ", ".join(emoji))
    upper = text.upper()
    for marker in ("TODO", "TBD", "[COMPLETAR]"):
        check(f"voice: no placeholder '{marker}'", marker not in upper)


def checkpoint1(text):
    lines = text.splitlines()

    # --- structure: cases 1-1, 1-2 (PRD R8, defect 5) ---
    heads = [(len(m.group(1)), i) for i, l in enumerate(lines)
             if (m := re.match(r"^(#{1,6}) ", l))]
    check("structure: at least one heading exists", bool(heads))
    h1s = [h for h in heads if h[0] == 1]
    check("structure: exactly one H1", len(h1s) == 1, f"found {len(h1s)}")
    check("structure: first heading is the H1", bool(heads) and heads[0][0] == 1)
    check("structure: at least two H2 sections",
          sum(1 for h in heads if h[0] == 2) >= 2)
    check("structure: no heading level skipped",
          all(b <= a + 1 for (a, _), (b, _) in zip(heads, heads[1:])))
    def section_body(i):
        start = heads[i][1] + 1
        end = heads[i + 1][1] if i + 1 < len(heads) else len(lines)
        return lines[start:end]

    check("structure: no empty section (every section has non-blank content)",
          bool(heads) and all(any(l.strip() for l in section_body(i))
                              for i in range(len(heads))))

    # --- banner: case 1-3 (PRD R5) ---
    m = re.search(r"<picture>.*?</picture>", text, re.S)
    pic = m.group(0) if m else ""
    check("banner: a <picture> block exists", bool(m))
    dark = re.search(r'<source[^>]*prefers-color-scheme:\s*dark[^>]*>', pic, re.I)
    check("banner: dark source uses prefers-color-scheme dark",
          bool(dark) and "profile-banner-dark/image-01.jpg" in dark.group(0))
    light = re.search(r'<source[^>]*prefers-color-scheme:\s*light[^>]*>', pic, re.I)
    check("banner: light source uses prefers-color-scheme light",
          bool(light) and "profile-banner/image-01.jpg" in light.group(0)
          and "profile-banner-dark" not in light.group(0))
    img = re.search(r"<img[^>]*>", pic, re.I)
    alt = re.search(r'alt="([^"]*)"', img.group(0)) if img else None
    check("banner: img fallback with alt of at least 15 chars",
          bool(alt) and len(alt.group(1).strip()) >= 15)
    check("banner: img width 1536", bool(img) and 'width="1536"' in img.group(0))
    src = re.search(r'src="([^"]*)"', img.group(0)) if img else None
    check("banner: img fallback has a src attribute", bool(src))
    check("banner: img fallback src file exists on disk",
          bool(src) and os.path.isfile(os.path.join(ROOT, src.group(1))))
    check("banner: light image file exists on disk",
          os.path.isfile(os.path.join(ROOT, ".ai-engineering/images/profile-banner/image-01.jpg")))
    check("banner: dark image file exists on disk",
          os.path.isfile(os.path.join(ROOT, ".ai-engineering/images/profile-banner-dark/image-01.jpg")))

    # --- canonical identity: case 1-4 (PRD R4) ---
    ge = re.search(r"general engineer", text, re.I)
    pg = re.search(r"Platform Governance Lead", text)
    first_h2 = re.search(r"^## ", text, re.M)
    check("identity: 'general engineer' present and leads (before the first "
          "H2 heading and the job title)",
          bool(ge and pg and first_h2)
          and ge.start() < pg.start() and ge.start() < first_h2.start())
    check("identity: 'Platform Governance Lead' present",
          "Platform Governance Lead" in text)
    check("identity: 'Nationale-Nederlanden' present",
          "Nationale-Nederlanden" in text)

    # --- contact list: case 1-5 (presence per contract task 5) ---
    for s in ("soydachi.com", "linkedin.com/in/soydachi",
              "mailto:info@arcasiles.com", "instagram.com/vegasoulband",
              "instagram.com/jaleo.band"):
        check(f"contact: '{s}' present", s in text)
    # Acceptance[3] "as descriptive links": each entry must carry Markdown
    # link syntax, not sit in the file as bare text.
    for label, pat in (
            ("soydachi.com", r"\[[^\]]+\]\(https://soydachi\.com\)"),
            ("linkedin.com/in/soydachi",
             r"\[[^\]]+\]\(https://(?:www\.)?linkedin\.com/in/soydachi\)"),
            ("mailto:info@arcasiles.com",
             r"\[[^\]]+\]\(mailto:info@arcasiles\.com\)"),
            ("instagram.com/vegasoulband",
             r"\[[^\]]+\]\(https://(?:www\.)?instagram\.com/vegasoulband\)"),
            ("instagram.com/jaleo.band",
             r"\[[^\]]+\]\(https://(?:www\.)?instagram\.com/jaleo\.band\)")):
        check(f"contact: '{label}' is a descriptive Markdown link",
              bool(re.search(pat, text)))

    # --- forbidden canonical data: case 1-6 + checkpoint-1 task (PRD R7 / §16) ---
    forbidden_16(text)

    # --- voice mechanics: contract id1 task 5 (checkpoint 3 reuses the same) ---
    voice_mechanics(text)

    # --- research §06 defects: case 1-7 ---
    for pat, defect in (
        (r"twitter\.com", "defect 1: twitter.com href"),
        (r"LinkdeIn", "defect 2: LinkdeIn typo"),
        (r"simple-icons", "defect 3: simple-icons@v3 icons"),
        (r"github-readme-stats", "defect 4: dead stats card"),
        (r"vue-dark", "defect 4: fixed vue-dark theme"),
    ):
        check(f"§06: absent '{pat}' ({defect})", not re.search(pat, text, re.I))

    # --- no projects section: case 1-8 (PRD R3) ---
    check("PRD R3: no projects/portfolio section heading",
          not any(re.search(r"projects|portfolio", lines[i], re.I)
                  for _, i in heads))


# CHECKPOINT 2 — later test writer: add a checkpoint2(text) function and
# register it here. Asserts: '## Now' section exists; exactly 3-6 https
# Markdown images with non-empty alt; at least one shieldcn.dev badge and
# the komarev.com counter; widget URLs measured 200.
#
# CHECKPOINT 3 — later test writer: add a checkpoint3(text) function and
# register it here. Voice mechanics (no U+2014, no curly quotes, no emoji,
# no TODO markers) and the full §16 sweep already run in checkpoint 1 via
# voice_mechanics() and forbidden_16() above; checkpoint 3 adds the English
# heuristic and link liveness (widgets + soydachi.com return 200).

CHECKPOINTS = {1: checkpoint1}


def main():
    args = sys.argv[1:]
    selected = sorted(CHECKPOINTS)
    if "--checkpoint" in args:
        try:
            n = int(args[args.index("--checkpoint") + 1])
        except (IndexError, ValueError):
            print("usage: check-readme.py [--checkpoint N]")
            return 2
        if n not in CHECKPOINTS:
            print(f"FAIL: checkpoint {n} checks are not implemented yet")
            return 1
        selected = [n]

    text = read_readme()
    if text is not None:
        for n in selected:
            CHECKPOINTS[n](text)

    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        print(f"{len(failures)} of {checks} checks failed "
              f"(checkpoints {', '.join(map(str, selected))})")
        return 1
    print(f"PASS: all {checks} checks passed "
          f"(checkpoints {', '.join(map(str, selected))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
