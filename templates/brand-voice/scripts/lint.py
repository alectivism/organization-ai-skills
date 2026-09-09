#!/usr/bin/env python3
"""brand-voice linter — deterministic, config-driven, dependency-free.

This is the ORGANIZATIONAL linter: brand naming, org-specific terms to avoid,
and the platform-neutral AI-tell patterns (em dashes, always-replace
vocabulary, empty intensifiers, clipped staccato fragments, copy-paste
fingerprints). If your pack also ships a *personal* writing-style skill (for
example `org-content/skills/personal-writing-style`), that one is a separate
tool for an individual's own voice in person-to-person writing — the two do
not share rules or code, so editing one never changes the other.

All word lists and org-naming patterns live in `references/lint-rules.json`
(copy `references/lint-rules.example.json` and edit it; this script falls
back to the .example file if the non-example one doesn't exist yet, so it
works before you customize anything). Nothing here is organization-specific.

Usage:
  lint.py <file>            Lint a file; findings to stderr; exit 1 if any.
  lint.py --stdin           Lint text from stdin (pipe a draft before pbcopy).
  lint.py --strict FILE     Disallow every em dash, including list separators.
  lint.py --allow-em-dashes Permit em dashes, for a voice that demonstrably
                            uses them deliberately.

Em dashes: one per line as a separator in a list item or heading is allowed
("**Label** — description"); in flowing prose, or 2+ per line, flagged.
En dashes: allowed in tight ranges (2024-2026 written with an en dash),
flagged elsewhere.
"<!-- no-lint -->" in the first 3 lines skips the file (internal notes).
Fenced code blocks are skipped.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR.parent / "references" / "lint-rules.json"
CONFIG_EXAMPLE_PATH = SCRIPT_DIR.parent / "references" / "lint-rules.example.json"

LIST_OR_HEADING = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|#|\|)")
SUFFIXES = r"(?:e|es|ed|d|ing|s|ly|ely|ment)?"
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")


def load_config():
    path = CONFIG_PATH if CONFIG_PATH.is_file() else CONFIG_EXAMPLE_PATH
    if not path.is_file():
        raise RuntimeError(
            f"No lint-rules config found. Expected {CONFIG_PATH} or {CONFIG_EXAMPLE_PATH}.")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh), path


def _inflected(word: str) -> str:
    """Base word plus common inflections. A trailing 'e' is dropped before the
    suffix group so leverage -> leveraging/leveraged and delve -> delving."""
    stem = word[:-1] if word.endswith("e") and len(word) > 3 else word
    return r"\b" + re.escape(stem) + SUFFIXES + r"\b"


def _compile_words(words):
    return [(w, re.compile(_inflected(w), re.I), re.compile(_inflected(w)))
            for w in words]


def _compile_naming(rules):
    compiled = []
    for rule in rules or []:
        flags = re.I if "i" in (rule.get("flags") or "") else 0
        compiled.append((re.compile(rule["pattern"], flags), rule["message"]))
    return compiled


def em_dash_ok(line: str) -> bool:
    """One em dash as a separator in a list item or heading; everything else is
    the AI clause-splice."""
    return line.count("—") == 1 and bool(LIST_OR_HEADING.match(line))


def staccato_fragments(line):
    """The clipped-fragment tell: 2+ consecutive sentences of <=4 words each.

    "Eight pages. Two ways in." -> flagged. A line with any sentence of 5+
    words is left alone, which keeps ordinary short prose out of the results.
    Returns the offending text or None.
    """
    text = line.strip()
    if not text or len(text) > 120:
        return None
    if text.startswith(("|", ">", "```", "#!")):
        return None
    text = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|#{1,6}\s+)", "", text)
    text = re.sub(r"`[^`]*`", "X", text)          # code spans are not prose
    text = re.sub(r"\*\*|\*|__|_", "", text)      # emphasis markers
    if not text or text[-1] not in ".!?":
        return None
    parts = [p for p in _SENT_SPLIT.split(text) if p.strip()]
    if len(parts) < 2:
        return None
    counts = [len(_WORD.findall(p)) for p in parts]
    if any(c == 0 for c in counts):
        return None
    if all(c <= 4 for c in counts) and all(p.strip()[-1] in ".!?" for p in parts[:-1]):
        return text
    return None


def lint(text, config, strict_dashes=False, allow_em_dashes=False):
    """Return [(line_no, finding, snippet)] for one document."""
    lines = text.splitlines()
    if any("<!-- no-lint -->" in l for l in lines[:3]):
        return []

    always_rx = _compile_words(config.get("always_replace", []))
    name_exempt = set(config.get("name_exempt", []))
    intens_rx = _compile_words(config.get("empty_intensifiers", []))
    candor_rx = _compile_words(config.get("candor_markers", []))
    fingerprints = config.get("copy_paste_fingerprints", [])
    naming_rules = _compile_naming(config.get("naming_rules", []))

    # Off by default: two short declarative sentences in a row are ordinary
    # organizational prose, not an AI tell. Orgs whose house style bans the
    # staccato rhythm turn it on in the config.
    flag_clipped = bool(config.get("flag_clipped_fragments", False))

    hits, in_fence = [], False
    for i, line in enumerate(lines, 1):
        if flag_clipped:
            stac = staccato_fragments(line)
            if stac:
                hits.append((i, "clipped fragments (join them into one sentence)", stac[:90]))

        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        snip = line.strip()[:90]

        if (not allow_em_dashes and "—" in line
                and (strict_dashes or not em_dash_ok(line))):
            hits.append((i, "em dash in prose", snip))
        if re.search(r"[^\w\s]–|–[^\w\s]|\s–|–\s", line):
            hits.append((i, "en dash outside a tight range", snip))
        if re.search(r"\S\s--\s\S", line) and not (
                allow_em_dashes
                or (line.count(" -- ") == 1 and LIST_OR_HEADING.match(line))):
            hits.append((i, "double-hyphen dash (--)", snip))

        for word, rx, rx_cased in always_rx:
            if not rx.search(line):
                continue
            if word in name_exempt and not rx_cased.search(line):
                continue
            hits.append((i, f"always-replace word: {word}", snip))
        for word, rx, _ in intens_rx:
            if rx.search(line):
                hits.append((i, f"empty intensifier: {word}", snip))
        for word, rx, _ in candor_rx:
            if rx.search(line):
                hits.append((i, f"candor marker (state the point, drop the label): {word}", snip))

        low = line.lower()
        for f in fingerprints:
            if f in low:
                hits.append((i, f"copy-paste fingerprint: {f}", snip))

        if re.match(r"\s*[-*+]?\s*\*\*[^*]+\.\*\*", line):
            hits.append((i, "list label uses a period (use a colon)", snip))

        for rx, msg in naming_rules:
            if rx.search(line):
                hits.append((i, f"org naming: {msg}", snip))

    return sorted(hits, key=lambda h: h[0])


def report(hits, name=""):
    if not hits:
        return
    print(f"brand-voice lint{' — ' + name if name else ''}: {len(hits)} issue(s)",
          file=sys.stderr)
    for ln, what, snip in hits:
        print(f"  L{ln}: {what}  |  {snip}", file=sys.stderr)
    print("Fix these (em dashes -> comma/period/colon/parens; replace flagged words) "
          "before returning the text.", file=sys.stderr)


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Lint organizational copy for brand/style tells.")
    ap.add_argument("file", nargs="?", help="Draft file. Omit when using --stdin.")
    ap.add_argument("--stdin", action="store_true", help="Read the draft from stdin.")
    ap.add_argument("--strict", action="store_true",
                    help="Disallow every em dash, including list separators.")
    ap.add_argument("--allow-em-dashes", action="store_true",
                    help="Permit em dashes when the org's established style uses them.")
    args = ap.parse_args(argv)
    if args.stdin and args.file:
        ap.error("choose either a file or --stdin")
    if args.strict and args.allow_em_dashes:
        ap.error("--strict and --allow-em-dashes contradict each other")
    return args


def main(argv=None):
    args = parse_args(argv)
    config, config_path = load_config()
    if args.stdin or not args.file:
        text, name = sys.stdin.read(), "stdin"
    else:
        path = os.path.expanduser(args.file)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        name = os.path.basename(path)
    hits = lint(text, config, strict_dashes=args.strict, allow_em_dashes=args.allow_em_dashes)
    report(hits, name)
    if config_path == CONFIG_EXAMPLE_PATH:
        print(f"(using example config at {config_path}; copy it to lint-rules.json "
              "and customize for your org)", file=sys.stderr)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
