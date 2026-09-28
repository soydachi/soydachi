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
    check("structure: no empty section (heading right after heading)",
          all(b[1] > a[1] + 1 for a, b in zip(heads, heads[1:])))

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
    check("banner: light image file exists on disk",
          os.path.isfile(os.path.join(ROOT, ".ai-engineering/images/profile-banner/image-01.jpg")))
    check("banner: dark image file exists on disk",
          os.path.isfile(os.path.join(ROOT, ".ai-engineering/images/profile-banner-dark/image-01.jpg")))

    # --- canonical identity: case 1-4 (PRD R4) ---
    check("identity: 'general engineer' leads (case-insensitive)",
          bool(re.search(r"general engineer", text, re.I)))
    check("identity: 'Platform Governance Lead' present",
          "Platform Governance Lead" in text)
    check("identity: 'Nationale-Nederlanden' present",
          "Nationale-Nederlanden" in text)

    # --- contact list: case 1-5 ---
    for s in ("soydachi.com", "linkedin.com/in/soydachi",
              "mailto:info@arcasiles.com", "instagram.com/vegasoulband",
              "instagram.com/jaleo.band"):
        check(f"contact: '{s}' present", s in text)

    # --- forbidden canonical data: case 1-6 + checkpoint-1 task (PRD R7 / §16) ---
    banned = [
        (r"Cloud Solution", "obsolete NN title"),
        (r"Platform Engineering Lead", "obsolete NN title"),
        (r"Mobile Lead Engineer", "obsolete NN title"),
        (r"instagram\.com/lasobremesa", "lasobremesa link"),
        (r"NN Digital Hub", "NN Digital Hub"),
        (r"~?\s*3[.,]?000\s*members", "false ~3000 members metric"),
        (r"\+150", "false +150 events metric"),
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
    for pat, why in banned:
        check(f"forbidden: absent '{pat}' ({why})",
              not re.search(pat, text, re.I))
    for i, l in enumerate(lines, 1):
        if re.search(r"MVP", l) and not re.search(
                r"former|ex-Microsoft|2015.?2020", l, re.I):
            check(f"forbidden: no active MVP mention (line {i})", False, l.strip())

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
# register it here. Asserts: voice mechanics (no U+2014, no curly quotes,
# no emoji, English heuristic, no TODO markers), full §16 sweep, and link
# liveness (widgets + soydachi.com return 200).

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
