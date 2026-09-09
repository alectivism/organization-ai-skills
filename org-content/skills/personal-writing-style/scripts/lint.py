#!/usr/bin/env python3
"""personal-writing-style linter — deterministic catches only.

Standalone by design: this file is the shared rule engine for the plugin and
carries no organization-specific rules, so it keeps working when the skill is
copied into another harness (Codex, a bare repo, another assistant) without the
rest of the plugin. An organization's own house-style linter can import this
module and layer its own naming or banned-term checks on top.

Flags the mechanical, high-confidence AI tells (em dashes, always-replace
vocabulary, empty intensifiers, candor markers, one banned antithesis form,
copy-paste fingerprints, list-label periods). Judgment-heavy structural tells
(false agency, false ranges, rhythm) stay in SKILL.md for the model.

Usage:
  lint.py <file>            Lint a file; findings to stderr; exit 1 if any.
  lint.py --stdin           Lint text from stdin (pipe a draft before pbcopy).
  lint.py --strict FILE     Disallow every em dash, including list separators.
  lint.py --allow-em-dashes Permit em dashes, for a sender whose established
                            style demonstrably uses them.

Em dashes: one per line as a separator in a list item or heading is allowed
("**Label** — description"); in flowing prose, or 2+ per line, flagged.
En dashes: allowed in tight ranges (2024–2026), flagged elsewhere.
Vocabulary matching is inflection-aware: "leverage" also catches "leveraging",
"foster" also catches "fostered".
"<!-- no-lint -->" in the first 3 lines skips the file (internal notes).
Fenced code blocks are skipped.

Token note: run this instead of eyeballing — it returns only the offending
lines, not the whole rule set.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ALWAYS = [  # 5-20x more frequent in AI prose; always replace
    "delve", "leverage", "landscape", "tapestry", "realm", "robust",
    "comprehensive", "seamless", "cutting-edge", "pivotal",
    "crucial", "underscore", "unveil", "harness", "foster", "streamline",
    "empower", "utilize", "synergy", "synergies", "game-changer",
    "game-changing", "unlock", "unleash", "boast", "testament", "elevate",
    "spearhead",
]
NAME_EXEMPT = {"foster"}  # collides with a common surname; flag the lowercase
# verb only, never the capitalized name.
INTENS = ["very", "really", "extremely", "incredibly", "significantly",
          "truly", "world-class"]
CANDOR = [  # self-praising candor markers; state the point, don't label it
    "honestly", "frankly", "candidly",
    "to be honest", "in all honesty", "the honest truth",
]
FINGERPRINTS = [  # near-proof of machine generation
    "i hope this helps", "certainly!", "great question", "as an ai",
    "citeturn", "oai_citation", "contentreference", "utm_source=chatgpt",
    "utm_source=claude", "utm_source=perplexity", "[your name]", "[insert",
    "as of my last update",
]

LIST_OR_HEADING = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|#|\|)")
ANTITHESIS = re.compile(r"\bno\s+[\w'-]+(?:\s+[\w'-]+){0,5}?,\s*just\b", re.I)
SUFFIXES = r"(?:e|es|ed|d|ing|s|ly|ely|ment)?"


def _inflected(word: str) -> str:
    """Base word plus common inflections. A trailing 'e' is dropped before the
    suffix group so leverage -> leveraging/leveraged and delve -> delving."""
    stem = word[:-1] if word.endswith("e") and len(word) > 3 else word
    return r"\b" + re.escape(stem) + SUFFIXES + r"\b"


def _compile(words):
    return [(w, re.compile(_inflected(w), re.I), re.compile(_inflected(w)))
            for w in words]


ALWAYS_RX = _compile(ALWAYS)
INTENS_RX = _compile(INTENS)
CANDOR_RX = _compile(CANDOR)


def em_dash_ok(line: str) -> bool:
    """One em dash as a separator in a list item or heading; everything else is
    the AI clause-splice."""
    return line.count("—") == 1 and bool(LIST_OR_HEADING.match(line))


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")

def staccato_fragments(line):
    """The clipped-fragment tell: 2+ consecutive sentences of <=4 words each.

    "Eight pages. Two ways in." -> flagged. "Not a feature. A hook." -> flagged.
    A line with any sentence of 5+ words is left alone, which keeps ordinary short
    prose out of the results. Returns the offending text or None.
    """
    text = line.strip()
    if not text or len(text) > 120:
        return None
    # Skip table rows, list markers, headings' leading hashes, and bare code.
    if text.startswith(("|", ">", "```", "#!")):
        return None
    text = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|#{1,6}\s+)", "", text)
    text = re.sub(r"`[^`]*`", "X", text)          # code spans are not prose
    text = re.sub(r"\*\*|\*|__|_", "", text)      # emphasis markers
    if not text or text[-1] not in ".!?":
        # An unterminated final clause means we are mid-sentence across lines.
        return None
    parts = [p for p in _SENT_SPLIT.split(text) if p.strip()]
    if len(parts) < 2:
        return None
    counts = [len(_WORD.findall(p)) for p in parts]
    if any(c == 0 for c in counts):
        return None
    # Every sentence short, and at least two of them. Abbreviations like "e.g." would
    # split oddly, so require each part to end in a terminator to count as a sentence.
    if all(c <= 4 for c in counts) and all(p.strip()[-1] in ".!?" for p in parts[:-1]):
        return text
    return None

def lint(text, strict_dashes=False, allow_em_dashes=False):
    """Return [(line_no, finding, snippet)] for one document."""
    lines = text.splitlines()
    if any("<!-- no-lint -->" in l for l in lines[:3]):
        return []
    hits, in_fence = [], False
    for i, line in enumerate(lines, 1):
        _stac = staccato_fragments(line)
        if _stac:
            hits.append((i, "clipped fragments (join them into one sentence)",
                         _stac[:90]))
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        snip = line.strip()[:90]
        if (not allow_em_dashes and "—" in line
                and (strict_dashes or not em_dash_ok(line))):
            hits.append((i, "em dash in prose", snip))
        if re.search(r"[^\w\s]–|–[^\w\s]|\s–|–\s", line):  # en dash outside a range
            hits.append((i, "en dash", snip))
        if re.search(r"\S\s--\s\S", line) and not (
                allow_em_dashes
                or (line.count(" -- ") == 1 and LIST_OR_HEADING.match(line))):
            hits.append((i, "double-hyphen dash (--)", snip))
        for word, rx, rx_cased in ALWAYS_RX:
            if not rx.search(line):
                continue
            # A capitalized-only occurrence of a name-colliding word (the
            # surname "Foster") is not the banned verb.
            if word in NAME_EXEMPT and not rx_cased.search(line):
                continue
            hits.append((i, f"always-replace word: {word}", snip))
        for word, rx, _ in INTENS_RX:
            if rx.search(line):
                hits.append((i, f"empty intensifier: {word}", snip))
        for word, rx, _ in CANDOR_RX:
            if rx.search(line):
                hits.append((i, f"candor marker (state the point, drop the label): {word}", snip))
        if ANTITHESIS.search(line):
            hits.append((i, "banned antithesis 'no X, just Y' (state Y directly)", snip))
        low = line.lower()
        for f in FINGERPRINTS:
            if f in low:
                hits.append((i, f"copy-paste fingerprint: {f}", snip))
        if re.match(r"\s*[-*+]?\s*\*\*[^*]+\.\*\*", line):
            hits.append((i, "list label uses a period (use a colon)", snip))
    return hits


def report(hits, name=""):
    if not hits:
        return
    print(f"writing-style lint{' — ' + name if name else ''}: {len(hits)} issue(s)",
          file=sys.stderr)
    for ln, what, snip in hits:
        print(f"  L{ln}: {what}  |  {snip}", file=sys.stderr)
    print("Fix these (em dashes -> comma/period/colon/parens; replace AI words) "
          "before returning the text.", file=sys.stderr)


# Filename shapes that mean "this file is outgoing prose". Extra directory
# fragments can be added with WRITING_LINT_PATHS (colon-separated), e.g.
# WRITING_LINT_PATHS=/drafts/:/outbox/
PROSE_NAME = re.compile(
    r"(?<![a-z])(reply|replies|email|message|draft|slack|teams|linkedin|post|memo"
    r"|outreach|newsletter|announcement)s?(?![a-z])")


def is_outgoing_prose(path: str) -> bool:
    p = path.lower()
    if not p.endswith((".md", ".txt")):
        return False
    extra = [d.lower() for d in os.environ.get("WRITING_LINT_PATHS", "").split(":") if d]
    if any(d in p for d in extra):
        return True
    # letter-boundaries prevent substring hits ("memory.md" != memo) while still
    # matching across _ - . (email_greg.md, linkedin_post.md)
    return bool(PROSE_NAME.search(os.path.basename(p)))


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Lint a draft for mechanical AI tells.")
    ap.add_argument("file", nargs="?", help="Draft file. Omit when using stdin.")
    ap.add_argument("--stdin", action="store_true", help="Read the draft from stdin.")
    ap.add_argument("--strict", action="store_true",
                    help="Disallow every em dash, including list separators.")
    ap.add_argument("--allow-em-dashes", action="store_true",
                    help="Permit em dashes when the sender's established style uses them.")
    args = ap.parse_args(argv)
    if args.stdin and args.file:
        ap.error("choose either a file or --stdin")
    if args.strict and args.allow_em_dashes:
        ap.error("--strict and --allow-em-dashes contradict each other")
    return args


def main(argv=None):
    args = parse_args(argv)
    if args.stdin or not args.file:
        text, name = sys.stdin.read(), "stdin"
    else:
        path = os.path.expanduser(args.file)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        name = os.path.basename(path)
    hits = lint(text, strict_dashes=args.strict, allow_em_dashes=args.allow_em_dashes)
    report(hits, name)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
