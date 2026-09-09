#!/usr/bin/env python3
"""factual-accuracy scanner — deterministic fabrication-risk checks.

A hook cannot know what is true. It can know what an unverified specific looks
like. So this script does two separate jobs:

  1. BLOCK on fabrication tells: vague authority standing in for a source
     ("industry research shows"), and placeholder leakage into a finished draft
     ("[TBD]", "XX%", "$XX").
  2. GATE the clipboard: refuse to let a draft carrying two or more specific
     claims reach pbcopy until that exact content has a verification receipt.

The receipt is written by `--verified FILE` after the claims have actually been
checked against sources. Writing it to clear the block, rather than because the
facts were checked, defeats the whole mechanism.

Usage:
  claim-scan.py --report FILE     Claim inventory and fabrication tells.
  claim-scan.py --stdin           Same, from stdin.
  claim-scan.py --verified FILE   Record a verification receipt for FILE.
  claim-scan.py --receipts        List current receipts.
  claim-scan.py --hook            PostToolUse(Write|Edit) hook mode.
  claim-scan.py --hook-pbcopy     PreToolUse(Bash) hook mode.

Escape hatches: "<!-- facts-checked -->" in the first three lines of a file, or
FACT_SCAN=0 in the environment. Fenced code blocks are skipped throughout.
Receipts live in ~/.claude/factual-accuracy-receipts.json, newest 200 kept.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time

# --- Fabrication tells: block these ------------------------------------------

# Vague authority used in place of a named source. Suppressed when the same
# sentence names one, so "Acme research shows" and "Nielsen research shows" pass.
AUTHORITY = re.compile(
    r"\b("
    r"(?:industry|academic|recent|new|extensive|our)?\s*"
    r"(?:research|studies|surveys|data|analytics|evidence)\s+"
    r"(?:show|shows|showed|suggest|suggests|indicate|indicates|prove|proves|"
    r"confirm|confirms|reveal|reveals|find|finds)"
    r"|studies\s+(?:have\s+)?found"
    r"|experts\s+(?:agree|say|estimate)"
    r"|analysts\s+(?:agree|say|estimate|expect)"
    r"|it\s+is\s+(?:widely\s+)?(?:known|accepted|understood)"
    r"|most\s+(?:cmos|marketers|brands|companies|members|advertisers)\s+"
    r"(?:report|say|agree|believe|struggle|cite)"
    r"|(?:\d+%\s+of\s+)?(?:cmos|marketers|brands)\s+report\s+that"
    r"|according\s+to\s+(?:industry|recent|multiple)\s+"
    r"(?:research|studies|sources|reports)"
    r")\b", re.I)

# A named source in the same sentence rescues the authority phrase. Generic,
# well-known research firms and institutions ship as defaults. Add your own
# organization's names, internal acronyms, or research partners with the
# CLAIM_SCAN_SOURCES environment variable: a "|"-separated list of regex
# alternatives, e.g. CLAIM_SCAN_SOURCES="Acme Corp|ACME|Acme Research Lab".
# Edit this list only for genuinely generic additions; org-specific names
# belong in the environment variable, not hardcoded here.
_GENERIC_SOURCES = (
    r"Nielsen|Forrester|Gartner|eMarketer|McKinsey|Deloitte|Kantar|Ipsos|WARC"
    r"|IAB|Analytic Partners|EY|BCG|Bain|Accenture|Pew|Statista|Harvard|MIT"
    r"|Stanford"
)
_extra_sources = os.environ.get("CLAIM_SCAN_SOURCES", "").strip()
_source_alts = _GENERIC_SOURCES + (f"|{_extra_sources}" if _extra_sources else "")
NAMED_SOURCE = re.compile(
    rf"\b({_source_alts})\b"
    r"|\b(?:19|20)\d{2}\b(?=[^.]{0,40}(?:study|report|survey|research|paper|filing))"
    r"|\[\d+\]|\(\s*(?:19|20)\d{2}\s*\)|https?://")

PLACEHOLDERS = [
    (re.compile(r"\[\s*(?:TBD|TK|X{1,4}|N/?A|NUMBER|FIGURE|STAT|DATE|NAME|COMPANY"
                r"|AMOUNT|PRICE|COUNT|SOURCE|CITATION|QUOTE)\s*\]", re.I),
     "placeholder left in a finished draft"),
    (re.compile(r"\[\s*(?:insert|add|fill|confirm|verify|check)\b[^\]]{0,40}\]", re.I),
     "instruction-to-self left in the draft"),
    (re.compile(r"(?<![\w$])\$\s?X+\b|(?<![\w])X{2,3}\s?%|(?<![\w])X{2,3}\s+"
                r"(?:members|attendees|companies|people|brands|staff)\b"),
     "unfilled numeric placeholder"),
    (re.compile(r"\b(?:TODO|FIXME)\b:?\s*(?:number|figure|stat|source|cite|confirm)",
                re.I),
     "unresolved fact TODO"),
]

# --- Specific claims: count these, do not judge them -------------------------

CLAIM_TYPES = [
    ("percentage", re.compile(r"(?<![\w.])[+\-]?\d+(?:\.\d+)?\s?%|\b\d+(?:\.\d+)?\s+percent\b")),
    ("money", re.compile(r"\$\s?\d[\d,.]*\s?(?:[kKmMbB]\b|billion|million|thousand)?"
                         r"|\b\d[\d,.]*\s?(?:USD|EUR|GBP)\b")),
    ("multiple", re.compile(r"(?<![\w.])\d+(?:\.\d+)?\s?x\b", re.I)),
    ("count", re.compile(
        r"(?<![\w.$])(?!(?:19|20)\d{2}\b)\d[\d,]*\+?\s+"
        r"(?:members?|member companies|attendees?|registrations?"
        r"|companies|brands?|people|staff|employees|countries|regions|labs?|studies"
        r"|experiments?|capabilities|questions|weeks?|months?|days?|hours?|sessions?"
        r"|respondents?|CMOs?|marketers?|subscribers?|participants?|seats?)\b", re.I)),
    ("date", re.compile(r"\b(?:19|20)\d{2}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                        r"[a-z]*\s+\d{1,2}\b", re.I)),
    ("quotation", re.compile(r"[\"“][^\"“”]{30,}[\"”]")),
    ("link", re.compile(r"https?://\S+")),
    ("superlative", re.compile(
        r"\bthe\s+(?:first|only|largest|biggest|fastest[- ]growing|leading|most)\s+\w+", re.I)),
]

RECEIPTS = os.path.expanduser("~/.claude/factual-accuracy-receipts.json")
RECEIPT_CAP = 200
GATE_THRESHOLD = 2  # specific claims that trigger the clipboard gate

# Filenames that carry claims: outgoing prose plus internal deliverables.
DELIVERABLE_NAME = re.compile(
    r"(?<![a-z])(reply|replies|email|message|draft|slack|teams|linkedin|post|memo"
    r"|outreach|newsletter|announcement|proposal|pitch|brief|recap|summary|report"
    r"|letter|one[-_]?pager|deck|agenda|abstract|bio|case[-_]?study|press)s?(?![a-z])")


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code so examples do not trip the scan."""
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def exempt(text: str) -> bool:
    if os.environ.get("FACT_SCAN") == "0":
        return True
    return "facts-checked" in "\n".join(text.split("\n")[:3]).lower()


def is_deliverable(path: str) -> bool:
    p = path.lower()
    if not p.endswith((".md", ".txt", ".html")):
        return False
    extra = [d.lower() for d in os.environ.get("FACT_SCAN_PATHS", "").split(":") if d]
    if any(d in p for d in extra):
        return True
    return bool(DELIVERABLE_NAME.search(os.path.basename(p)))


def scan(text: str):
    """Return (tells, claims). tells block; claims gate."""
    body = strip_code(text)
    tells, claims = [], []
    for i, line in enumerate(body.split("\n"), 1):
        if not line.strip():
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            m = AUTHORITY.search(sentence)
            if m and not NAMED_SOURCE.search(sentence):
                tells.append((i, f"vague authority with no named source: \"{m.group(0).strip()}\"",
                              sentence.strip()[:90]))
        for rx, msg in PLACEHOLDERS:
            m = rx.search(line)
            if m:
                tells.append((i, f"{msg}: \"{m.group(0).strip()}\"", line.strip()[:90]))
        for kind, rx in CLAIM_TYPES:
            for m in rx.finditer(line):
                claims.append((i, kind, m.group(0).strip()[:60]))
    return tells, claims


def digest(text: str) -> str:
    """Hash normalized content, so whitespace edits do not invalidate a receipt."""
    return hashlib.sha256(re.sub(r"\s+", " ", text).strip().encode()).hexdigest()[:16]


def load_receipts() -> dict:
    try:
        with open(RECEIPTS, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def write_receipt(text: str, label: str) -> str:
    key = digest(text)
    data = load_receipts()
    data[key] = {"label": label, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if len(data) > RECEIPT_CAP:
        for k in sorted(data, key=lambda k: data[k].get("at", ""))[:len(data) - RECEIPT_CAP]:
            del data[k]
    os.makedirs(os.path.dirname(RECEIPTS), exist_ok=True)
    tmp = RECEIPTS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
    os.replace(tmp, RECEIPTS)
    return key


def has_receipt(text: str) -> bool:
    return digest(text) in load_receipts()


def report_tells(tells, name):
    print(f"\nfactual-accuracy: {len(tells)} fabrication tell(s) in {name}", file=sys.stderr)
    for ln, msg, ctx in tells:
        print(f"  {name}:{ln}  {msg}\n      {ctx}", file=sys.stderr)
    print("\nName the source or cut the claim. See the factual-accuracy skill.\n",
          file=sys.stderr)


def summarize(claims) -> str:
    kinds = {}
    for _, kind, _ in claims:
        kinds[kind] = kinds.get(kind, 0) + 1
    return ", ".join(f"{v} {k}" for k, v in sorted(kinds.items(), key=lambda x: -x[1]))


# --- entry points ------------------------------------------------------------

def cmd_report(text, name):
    if exempt(text):
        print(f"{name}: exempt from the factual-accuracy scan")
        return 0
    tells, claims = scan(text)
    if tells:
        report_tells(tells, name)
    if claims:
        print(f"{name}: {len(claims)} specific claim(s) — {summarize(claims)}")
        for ln, kind, snip in claims:
            print(f"  {ln}: [{kind}] {snip}")
        print("\nEach one needs a source read this session, or it goes in the gap ask.")
    else:
        print(f"{name}: no specific claims found")
    print(f"receipt: {'present' if has_receipt(text) else 'none'} (digest {digest(text)})")
    return 1 if tells else 0


def cmd_hook_write():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not path or not os.path.isfile(path) or not is_deliverable(path):
        return 0
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return 0
    if exempt(text):
        return 0
    tells, claims = scan(text)
    name = os.path.basename(path)
    if tells:
        report_tells(tells, name)
        return 2  # stderr goes back to Claude as feedback
    if len(claims) >= GATE_THRESHOLD and not has_receipt(text):
        heavy = len(claims) >= 5
        note = (
            f"factual-accuracy: {name} carries {len(claims)} specific claims "
            f"({summarize(claims)}). Invoke the factual-accuracy skill. "
            + ("Claim load is 5 or more, so spawn the org-fact-checker subagent "
               "with the draft path and your sources, and wait for its verdict. "
               if heavy else
               "Verify each claim against a source opened this session. ")
            + "Unverifiable claims go into one gap ask, not into the draft. "
            f"When they check out: claim-scan.py --verified '{path}'"
        )
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": note}}))
    return 0


def cmd_hook_pbcopy():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if "pbcopy" not in cmd:
        return 0
    texts = [(cmd, "pbcopy command")]
    m = re.search(r"(?:cat\s+([^\s|;&]+)\s*\|\s*pbcopy|pbcopy\s*<\s*([^\s|;&]+))", cmd)
    src = (m.group(1) or m.group(2)) if m else None
    if src:
        src = os.path.expanduser(src.strip("'\""))
        if os.path.isfile(src):
            try:
                texts.append((open(src, encoding="utf-8", errors="ignore").read(), src))
            except Exception:
                pass
    for text, label in texts:
        if exempt(text):
            return 0
    for text, label in texts:
        tells, claims = scan(text)
        if tells:
            report_tells(tells, label)
            return 2
        if len(claims) >= GATE_THRESHOLD and not has_receipt(text):
            print(
                f"\nfactual-accuracy: blocked. {label} carries {len(claims)} specific "
                f"claims ({summarize(claims)}) with no verification receipt.\n\n"
                "Verify each against a source opened this session, or spawn "
                "org-fact-checker if the load is 5 or more. Then:\n"
                f"  python3 {os.path.abspath(__file__)} --verified <file>\n"
                "  pbcopy < <file>\n\n"
                "Write the receipt because the facts checked out, not to clear this "
                "block. Genuinely illustrative content: add <!-- facts-checked --> to "
                "the top of the file.\n", file=sys.stderr)
            return 2
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    mode = args[0]
    if mode == "--hook":
        return cmd_hook_write()
    if mode == "--hook-pbcopy":
        return cmd_hook_pbcopy()
    if mode == "--receipts":
        data = load_receipts()
        for k, v in sorted(data.items(), key=lambda x: x[1].get("at", ""), reverse=True):
            print(f"{v.get('at','?')}  {k}  {v.get('label','')}")
        print(f"{len(data)} receipt(s) in {RECEIPTS}")
        return 0
    if mode == "--verified":
        if len(args) < 2:
            print("--verified needs a file path", file=sys.stderr)
            return 1
        path = os.path.expanduser(args[1])
        text = open(path, encoding="utf-8", errors="ignore").read()
        tells, claims = scan(text)
        if tells:
            report_tells(tells, os.path.basename(path))
            print("Receipt not written: fix the fabrication tells first.", file=sys.stderr)
            return 1
        key = write_receipt(text, path)
        print(f"receipt written for {os.path.basename(path)} "
              f"({len(claims)} claim(s), digest {key})")
        return 0
    if mode == "--stdin":
        return cmd_report(sys.stdin.read(), "stdin")
    if mode == "--report":
        if len(args) < 2:
            return cmd_report(sys.stdin.read(), "stdin")
        path = os.path.expanduser(args[1])
        return cmd_report(open(path, encoding="utf-8", errors="ignore").read(),
                          os.path.basename(path))
    path = os.path.expanduser(mode)
    if os.path.isfile(path):
        return cmd_report(open(path, encoding="utf-8", errors="ignore").read(),
                          os.path.basename(path))
    print(f"unknown argument: {mode}\n{__doc__}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
