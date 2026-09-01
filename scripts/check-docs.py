#!/usr/bin/env python3
"""Fail when the walkthrough's two surfaces drift apart.

GETTING-STARTED.md and docs/src/index.html tell the same story to different
readers — one in a terminal, one in a browser — and neither can be generated
from the other without degrading it. So they cannot share a source.

What they CAN do is diverge loudly instead of silently. This compares their
section headings and exits non-zero when they disagree. Same principle as the
contracts themselves: when you cannot prevent a failure, make it visible.

    python3 scripts/check-docs.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Structural differences that are deliberate. Each one is a decision, written
# down with its reason — an undeclared difference is what this script is for.
EXPECTED_DIFFERENCES = {
    "in plain language":
        "the page opens with the Tokyo example as an unheadinged hook; the "
        "Markdown gives the same content a titled section, because a reader "
        "scanning headings in a terminal needs one",
}


def normalise(t):
    t = re.sub(r"^\s*[\d—-]+\s*·?\s*", "", t.strip())
    return re.sub(r"\s+", " ", t).lower()


def hardcoded_versions():
    """A version number typed into a fragment is a claim that goes stale
    silently. Use {{PACK_VERSION}}; build-docs.py fills it from the pack."""
    bad = []
    for name in ("index.html", "concepts.html"):
        path = os.path.join(ROOT, "docs", "src", name)
        for i, line in enumerate(open(path, encoding="utf-8"), 1):
            if re.search(r"\bv\d+\.\d+\b", line):
                bad.append("%s:%d  %s" % (name, i, line.strip()[:70]))
    return bad


def main():
    stale = hardcoded_versions()
    if stale:
        print("HARDCODED VERSION in a page fragment\n")
        for b in stale:
            print("  %s" % b)
        print("\nUse {{PACK_VERSION}}; build-docs.py fills it from "
              "references/full-pack.txt.")
        return 1

    md = open(os.path.join(ROOT, "GETTING-STARTED.md"), encoding="utf-8").read()
    html = open(os.path.join(ROOT, "docs", "src", "index.html"),
                encoding="utf-8").read()

    md_heads = [normalise(h) for h in re.findall(r"^## (.+)$", md, re.M)]
    html_heads = [normalise(h) for h in
                  re.findall(r"<h2>(.+?)</h2>", html)]

    only_md = [h for h in md_heads
               if h not in html_heads and h not in EXPECTED_DIFFERENCES]
    only_html = [h for h in html_heads
                 if h not in md_heads and h not in EXPECTED_DIFFERENCES]

    if not only_md and not only_html:
        print("walkthrough surfaces agree — %d sections, %d declared difference(s)"
              % (len(md_heads), len(EXPECTED_DIFFERENCES)))
        for h, why in EXPECTED_DIFFERENCES.items():
            print("   declared: %s — %s" % (h, why))
        return 0

    print("DRIFT between GETTING-STARTED.md and docs/src/index.html\n")
    for h in only_md:
        print("  only in the Markdown : %s" % h)
    for h in only_html:
        print("  only in the page     : %s" % h)
    print("\nThe README calls GETTING-STARTED.md canonical for this walkthrough."
          "\nEither bring the page into line or stop calling it canonical.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
