#!/usr/bin/env python3
"""Assertions for the readme-profesional rewrite. Run from anywhere.

Usage: python3 .ai-engineering/scripts/check-readme.py [--checkpoint N]
                                       [--list-images]
No --checkpoint runs every checkpoint whose README section exists (baseline
checkpoint 1, plus checkpoint 2 once ## Now is present); --checkpoint N
runs one checkpoint's assertions regardless; --list-images prints every
rendered image URL (all serializations) one per line for the curl cases.
Exit 0 + PASS line when all
selected assertions hold; exit 1 printing each failing assertion.
"""
import os
import re
import sys
from urllib.parse import urlparse

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
    check("voice: no em dash (U+2014)", "—" not in text)
    curly = sorted({f"U+{ord(c):04X}" for c in text
                    if ord(c) in (0x2018, 0x2019, 0x201C, 0x201D)})
    check("voice: no curly quotes (U+2018/U+2019/U+201C/U+201D)",
          not curly, ", ".join(curly))
    # Emoji ban removed 2026-09-28: the user's target layout uses emoji
    # (greeting wave, fact bullets), his example overrides the tone guide.
    upper = text.upper()
    for marker in ("TODO", "TBD", "[COMPLETAR]"):
        check(f"voice: no placeholder '{marker}'", marker not in upper)


def checkpoint1(text):
    lines = text.splitlines()

    # --- structure: cases 1-1, 1-2 (PRD R8, defect 5) ---
    # The user's target layout uses a centered HTML <h1 align="center">, so
    # an HTML h1 line counts as the page's single H1 alongside markdown ones.
    heads = [(len(m.group(1)), i) for i, l in enumerate(lines)
             if (m := re.match(r"^(#{1,6}) ", l))]
    html_h1 = [i for i, l in enumerate(lines) if re.search(r"<h1[\s>]", l)]
    check("structure: at least one heading exists", bool(heads))
    h1s = [h for h in heads if h[0] == 1] + html_h1
    check("structure: exactly one H1", len(h1s) == 1, f"found {len(h1s)}")
    first_heading = min([i for _, i in heads] + html_h1) if (heads or html_h1) else None
    check("structure: first heading is the H1",
          first_heading is not None and first_heading in html_h1)
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

    # --- banner (former case 1-3, PRD R5): assertions removed 2026-09-28 ---
    # The user rejected the banner image ("esa imagen no tiene sentido ahí en
    # medio"); R5 is void by user order, so no <picture> assertion remains.

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
    # link syntax inside the ## Contact section itself — a duplicate target
    # elsewhere (e.g. the LinkedIn link in ## What I do) must not satisfy it.
    contact_idx = next((i for i, (lvl, li) in enumerate(heads)
                        if lvl == 2 and lines[li][2:].strip() == "Contact"),
                       None)
    contact = ("\n".join(section_body(contact_idx))
               if contact_idx is not None else "")
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
        check(f"contact: '{label}' is a descriptive Markdown link in ## Contact",
              bool(re.search(pat, contact)))

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


# F12/F13/F14: one extractor for every image serialization GitHub renders —
# inline markdown, reference-style (resolved against definition lines), and
# HTML <img> in any quoting. Callers pick the input: raw text for the
# file-global allowlist and --list-images; strip_nonrendering() for anything
# that counts rendered widgets, because fences/code/comments render as code
# or not at all. srcset URLs render but carry no alt, so they feed the
# allowlist and liveness only, never the count or alt gate.
# F11: reference-style image usages (![alt][ref], collapsed ![alt][] ,
# shortcut ![alt]) carry no inline URL — resolve against definition lines.
# Only refs actually used in image syntax resolve: a plain link definition is
# not an image and never reaches the allowlist.
def ref_label(label):
    """F15: CommonMark reference labels compare case-insensitively with
    surrounding whitespace stripped and internal whitespace collapsed —
    applied to BOTH the definition and the usage lookup."""
    return re.sub(r"\s+", " ", label.strip()).casefold()


def ref_definitions(text):
    """Reference DEFINITIONS are file-global (CommonMark): collect them from
    the whole file; only the image USAGE has a scope (F14 residual — a
    definition at file end must still resolve an in-section usage)."""
    return {ref_label(k): v
            for k, v in re.findall(r"^\[([^\]]+)\]:\s*(\S+)", text, re.M)}


def extract_images(text, ref_defs=None):
    """(alt, url) for every rendered image: inline, reference, HTML <img>."""
    imgs = [(a, u) for a, u in re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)]
    if ref_defs is None:
        ref_defs = ref_definitions(text)
    for m in re.finditer(r"!\[([^\]]*)\]\[([^\]]*)\]", text):
        url = ref_defs.get(ref_label(m.group(2) or m.group(1)))
        if url:
            imgs.append((m.group(1), url))
    for m in re.finditer(r"!\[([^\]]*)\](?![\[(])", text):
        url = ref_defs.get(ref_label(m.group(1)))
        if url:
            imgs.append((m.group(1), url))
    # F13: HTML <img> in any quoting — these render as badges but carry no
    # inline markdown URL, so they were invisible to the liveness greps.
    for tag in re.findall(r"<img\b[^>]*>", text, re.I):
        src = re.search(r"\ssrc\s*=\s*['\"]?([^'\"\s>]+)", tag, re.I)
        if src:
            alt = re.search(r"\salt\s*=\s*['\"]([^'\"]*)['\"]", tag, re.I)
            imgs.append((alt.group(1) if alt else "", src.group(1)))
    return imgs


def srcset_urls(text):
    """F12: srcset (e.g. <picture><source srcset=...>) is a comma-separated
    URL list with optional width descriptors, quoted or not; every candidate
    is an image URL for the allowlist and liveness."""
    out = []
    for m in re.finditer(r"\ssrcset\s*=\s*(?:['\"]([^'\"]*)['\"]|([^\s'>]+))",
                         text, re.I):
        value = m.group(1) if m.group(1) is not None else m.group(2)
        for part in value.split(","):
            part = part.split()
            if part:
                out.append(part[0])
    return out


def strip_nonrendering(text):
    """F14: drop fenced code, inline code, and HTML comments — GFM renders
    those as code or nothing, so images inside them are not badges."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


# CHECKPOINT 2 — 'Live widgets replace dead stats' (PRD R6, §06 defect 4,
# §10 star-history retirement). Static scope only: the ## Now section and two
# file-global regressions. HTTP 200 is deliberately NOT asserted here — the
# test plan keeps it as its own cli-layer case (one curl per image URL), so
# the unit layer stays offline and the curl case owns liveness.
def checkpoint2(text):
    lines = text.splitlines()
    heads = [(len(m.group(1)), i) for i, l in enumerate(lines)
             if (m := re.match(r"^(#{1,6}) ", l))]

    def heading(lvl, title):
        return next((i for lvl_, i in heads
                     if lvl_ == lvl and lines[i][lvl + 1:].strip() == title),
                    None)

    now_idx = heading(2, "Now")
    contact_idx = heading(2, "Contact")

    # --- section existence, order, non-empty: acceptance[0]/[1] ---
    check("now: '## Now' section exists", now_idx is not None)
    check("now: '## Contact' exists to order against",
          contact_idx is not None)
    check("now: section sits before '## Contact'",
          now_idx is not None and contact_idx is not None
          and now_idx < contact_idx)
    # intro content (tagline/paragraph) must precede the Now heading, so an
    # '## Now' dropped right under the H1 (pushing the intro into the
    # section) fails the order check. The H1 may be markdown or the user's
    # centered HTML <h1>.
    h1_idx = heads[0][1] if heads and heads[0][0] == 1 else next(
        (i for i, l in enumerate(lines) if re.search(r"<h1[\s>]", l)), None)
    check("now: intro content precedes the section",
          now_idx is not None and h1_idx is not None and any(
              l.strip() and not re.match(r"^#{1,6} ", l)
              for l in lines[h1_idx + 1:now_idx]))
    if now_idx is not None:
        end = next((i for _, i in heads if i > now_idx), len(lines))
        body = "\n".join(lines[now_idx + 1:end])
        check("now: section is non-empty",
              any(l.strip() for l in lines[now_idx + 1:end]))

        # --- 3-6 images in ## Now, alt quality, https: PRD R6 ---
        # F14: count badges GFM renders, not syntax — fenced/commented copies
        # render as code/nothing and must not pad the count; reference-style
        # widgets resolve against file-global definitions (CommonMark): the
        # USAGE must be inside ## Now (L2 scope), the definition may sit
        # anywhere in the file. srcset (F12) has no alt and stays out of the
        # count/alt gate; it is covered by the file-global allowlist below.
        imgs = extract_images(strip_nonrendering(body), ref_definitions(text))
        check("now: 3 to 6 Markdown images inside ## Now",
              3 <= len(imgs) <= 6, f"found {len(imgs)}")
        generic = {"image", "chart", "badge", "logo", "picture",
                   "graphic", "stats", "widget"}
        # F5: the generic-set floor passes "GitHub badge chart" for every
        # widget — a self-sufficient alt must also name its subject or the
        # metric it shows (acceptance 2).
        metric_words = ("commit", "star", "follower", "view", "counter",
                        "contribution", "trophy", "streak", "fork",
                        "sponsor", "download", "member", "score", "rank")
        for i, (alt, url) in enumerate(imgs, 1):
            a = alt.strip()
            low = a.lower()
            words = set(re.findall(r"[a-z]+", low))
            check(f"now: image {i} alt is descriptive and specific "
                  f"(>=10 chars, names the subject or the metric)",
                  len(a) >= 10 and bool(words) and not words <= generic
                  and ("soydachi" in low
                       or any(m in low for m in metric_words)),
                  repr(a))
            check(f"now: image {i} URL is https",
                  url.strip().startswith("https://"), url.strip())
        urls = [u for _, u in imgs]

        # --- required providers inside ## Now: PRD R6 / brainstorm d11 ---
        # F2: acceptance 1 names the lifetime commit chart by URL — pin it
        # exactly, not just "any shieldcn.dev widget".
        check("now: lifetime commit chart URL present as an image "
              "(https://shieldcn.dev/chart/github/commits/soydachi.svg)",
              "https://shieldcn.dev/chart/github/commits/soydachi.svg"
              in [u.strip() for _, u in imgs])
        check("now: at least one shieldcn.dev widget image",
              any("shieldcn.dev" in u for u in urls))
        check("now: komarev.com/ghpvc counter widget image",
              any("komarev.com/ghpvc" in u for u in urls))

        # --- widget URLs live only inside Markdown image syntax, never as
        # bare links or raw text (scope: ## Now, per L2) ---
        img_spans = [m.span() for m in
                     re.finditer(r"!\[[^\]]*\]\([^)]*\)", body)]
        for m in re.finditer(r"shieldcn\.dev|komarev\.com/ghpvc", body):
            check("now: widget URL inside Markdown image syntax "
                  "(not a bare link)",
                  any(s <= m.start() and m.end() <= e
                      for s, e in img_spans), m.group(0))

    # --- defect 4 regression + §10: file-global by acceptance ("anywhere") ---
    check("§06: absent 'github-readme-stats' (defect 4, fixed-theme card)",
          not re.search(r"github-readme-stats", text, re.I))
    check("§10: absent 'star-history.com' (retired widget)",
          not re.search(r"star-history\.com", text, re.I))
    # --- F4/F9/F10/F11/F12: acceptance 4 also bans "any fixed-theme
    # single-provider stats card", not just the literals above — fail closed:
    # every image URL the renderer can display must come from the sanctioned
    # widget hosts, in any scheme and any serialization GitHub renders:
    # markdown plain or <angle-bracket> destinations, reference-style, HTML
    # src (all quoting), and srcset/source lists. Scheme-less URLs are
    # relative/local images with no remote host and stay unexamined.
    img_urls = [u for _, u in extract_images(text)] + srcset_urls(text)
    for u in img_urls:
        u = u.strip()
        if u.startswith("<") and u.endswith(">"):
            u = u[1:-1].strip()
        p = urlparse(u)
        if not p.netloc:
            continue
        host = (p.hostname or "").lower()
        check(f"stats-card: image host '{host}' is one of the sanctioned "
              f"widget hosts (shieldcn.dev / komarev.com / img.shields.io)",
              host in ("shieldcn.dev", "komarev.com", "img.shields.io"), u)


# CHECKPOINT 3 — later test writer: add a checkpoint3(text) function and
# register it here. Voice mechanics (no U+2014, no curly quotes, no emoji,
# no TODO markers) and the full §16 sweep already run in checkpoint 1 via
# voice_mechanics() and forbidden_16() above; checkpoint 3 adds the English
# heuristic and link liveness (widgets + soydachi.com return 200).

CHECKPOINTS = {1: checkpoint1, 2: checkpoint2}
# Section each checkpoint's assertions need to exist in the README for the
# bare invocation to run it (checkpoint 1 is the always-on baseline).
SECTIONS = {2: "Now"}


def main():
    args = sys.argv[1:]
    text = read_readme()
    # F13: the liveness cases curl every URL this prints — the same complete
    # extraction the allowlist uses (inline, reference, HTML img, srcset), so
    # an HTML <img> or ref-style widget 404 can no longer pass unprobed.
    if "--list-images" in args:
        if text is None:
            return 1
        seen = []
        for u in [u for _, u in extract_images(text)] + srcset_urls(text):
            u = u.strip()
            if u.startswith("<") and u.endswith(">"):
                u = u[1:-1].strip()
            if urlparse(u).netloc and u not in seen:
                seen.append(u)
        for u in seen:
            print(u)
        return 0
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
    else:
        # Bare invocation runs every checkpoint whose README slice has landed
        # (F1: CP2's verify lines use this bare command, so it must actually
        # exercise the ## Now assertions once the section exists).
        selected = sorted(n for n in CHECKPOINTS
                          if n not in SECTIONS
                          or re.search(rf"^## {SECTIONS[n]}\b", text or "", re.M))

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
