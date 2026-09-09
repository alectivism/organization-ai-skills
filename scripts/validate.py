#!/usr/bin/env python3
"""Validate the dual-platform plugin marketplace before pushing.

Guards the failure modes that actually break an install:

  1. Unquoted colons (or any malformed YAML) in SKILL.md / agent frontmatter.
     Codex parses frontmatter strictly and silently skips the whole plugin.
  2. A leading HTML comment or blank line before the first `---`. The importer
     then finds no frontmatter at all and skips the skill.
  3. `name:` in a SKILL.md that does not match its folder name. The loader keys
     on the folder, the model reads the frontmatter, and cross-references break.
  4. A Claude-only `agents/` folder inside a plugin listed in the ChatGPT
     manifest. Codex has no named-subagent concept, so that content is dead at
     best and fails the import at worst. Ship a skills-only `-gpt` sibling.
  5. A `.codex-plugin/` directory. It looks right and it BREAKS the ChatGPT
     import: ChatGPT's manifest validation requires `interface.shortDescription`,
     which the published docs call optional. The shape that does import is
     `.claude-plugin/plugin.json` with no `interface` object, dir basename ==
     marketplace entry name == plugin.json name, plus LICENSE and README.md.
  6. A manifest entry pointing at a directory that does not exist.
  7. Org-specific strings left in a file that is supposed to be a generic
     template. This pack is derived from a private org-specific repo, so a
     leak here publishes someone's internal facts.
  8. A skill shipping a MANIFEST.json whose checksums no longer match the files
     on disk, which makes a customization diff compare against a stale baseline
     and silently pass.

Run: python3 scripts/validate.py          (exit 0 = clean, 1 = problems)
     python3 scripts/validate.py --leaks  (only the org-leak scan)
"""
import glob
import hashlib
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LEAKS_ONLY = "--leaks" in sys.argv
problems = []

SKIP_DIRS = ("archive", ".git", "node_modules")


def walk(pattern):
    for f in glob.glob(pattern, recursive=True):
        norm = f.replace("\\", "/")
        if any(norm == d or norm.startswith(d + "/") for d in SKIP_DIRS):
            continue
        yield f, norm


# ---------------------------------------------------------------- frontmatter
if not LEAKS_ONLY:
    for f, norm in walk("**/*.md"):
        text = open(f, encoding="utf-8").read()
        is_skill = os.path.basename(f) == "SKILL.md" or "/agents/" in norm
        if not text.startswith("---"):
            if is_skill:
                problems.append(
                    f"NO LEADING FRONTMATTER: {f} "
                    "(SKILL and agent files must start with '---' on line 1)"
                )
            continue
        try:
            meta = yaml.safe_load(text.split("---", 2)[1]) or {}
        except Exception as e:
            problems.append(f"MALFORMED YAML: {f} -> {str(e).splitlines()[0]}")
            continue
        if not isinstance(meta, dict):
            problems.append(f"FRONTMATTER IS NOT A MAPPING: {f}")
            continue
        if os.path.basename(f) == "SKILL.md":
            folder = os.path.basename(os.path.dirname(f))
            if meta.get("name") != folder:
                problems.append(
                    f"NAME MISMATCH: {f} -> name '{meta.get('name')}' != folder '{folder}'"
                )
            if not str(meta.get("description", "")).strip():
                problems.append(f"NO DESCRIPTION: {f}")
            # `status` marks whether a skill still has [BRACKETED] slots to fill.
            # `template` and the "> **Template skill.**" callout travel together;
            # everything else is `ready`. Files under templates/ are always template.
            status = meta.get("status")
            has_callout = "**Template skill.**" in text
            if status not in ("ready", "template"):
                problems.append(
                    f"STATUS: {f} -> status '{status}', expected 'ready' or 'template'"
                )
            elif norm.startswith("templates/") and status != "template":
                problems.append(f"STATUS: {f} -> under templates/, must be 'template'")
            elif status == "template" and not has_callout:
                problems.append(
                    f"STATUS: {f} -> status 'template' but no "
                    '"> **Template skill.**" callout in the body'
                )
            elif status == "ready" and has_callout:
                problems.append(
                    f"STATUS: {f} -> has the Template skill callout but status 'ready'"
                )
            if status == "template" and not re.search(r"\[[A-Z][A-Z0-9 _/&'-]{2,}\]", text):
                problems.append(
                    f"STATUS: {f} -> status 'template' but no [BRACKETED] placeholder found"
                )


# ------------------------------------------------------------------ manifests
def load(path):
    if not os.path.exists(path):
        problems.append(f"MISSING MANIFEST: {path}")
        return {}
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        problems.append(f"BAD JSON: {path} -> {e}")
        return {}


def src(entry):
    s = entry.get("source")
    return s.get("path") if isinstance(s, dict) else s


if not LEAKS_ONLY:
    claude = load(".claude-plugin/marketplace.json")
    chatgpt = load(".agents/plugins/marketplace.json")

    for label, mkt in (("claude", claude), ("chatgpt", chatgpt)):
        for p in mkt.get("plugins", []):
            path = src(p)
            name = p.get("name")
            if not path or not os.path.isdir(path):
                problems.append(f"{label}: plugin '{name}' -> dir '{path}' not found")
                continue
            base = os.path.basename(path.rstrip("/"))
            if base != name:
                problems.append(
                    f"{label}: entry name '{name}' != dir basename '{base}' ({path})"
                )
            if os.path.isdir(os.path.join(path, ".codex-plugin")):
                problems.append(
                    f"{label}: '{name}' has a .codex-plugin/ directory ({path}). "
                    "It breaks the ChatGPT import (strict validation demands "
                    "interface.shortDescription). Delete it; .claude-plugin/plugin.json "
                    "is the shape that imports."
                )
            pj = os.path.join(path, ".claude-plugin", "plugin.json")
            if os.path.exists(pj):
                try:
                    doc = json.load(open(pj, encoding="utf-8"))
                    if doc.get("name") and doc["name"] != base:
                        problems.append(
                            f"{label}: plugin.json name '{doc['name']}' != dir '{base}' ({path})"
                        )
                    if "interface" in doc:
                        problems.append(
                            f"{label}: '{name}' plugin.json has an 'interface' object ({pj}); "
                            "remove it, it fails the ChatGPT import"
                        )
                except Exception as e:
                    problems.append(f"{label}: bad plugin.json at {pj} -> {e}")
            else:
                problems.append(
                    f"{label}: '{name}' has no .claude-plugin/plugin.json ({path})"
                )
            for companion in ("LICENSE", "README.md"):
                if not os.path.exists(os.path.join(path, companion)):
                    problems.append(f"{label}: '{name}' is missing {companion} ({path})")
            if not os.path.isdir(os.path.join(path, "skills")):
                problems.append(f"{label}: '{name}' has no skills/ directory ({path})")
            if label == "chatgpt" and os.path.isdir(os.path.join(path, "agents")):
                problems.append(
                    f"chatgpt: '{name}' ({path}) has an agents/ folder; "
                    "Codex has no named-subagent concept. Ship a skills-only sibling."
                )

    # Every plugin directory on disk should appear in at least one manifest.
    listed = {os.path.basename(str(src(p)).rstrip("/"))
              for m in (claude, chatgpt) for p in m.get("plugins", [])}
    for d in sorted(os.listdir(".")):
        if os.path.isdir(os.path.join(d, ".claude-plugin")) and d not in listed:
            problems.append(f"ORPHAN PLUGIN: '{d}/' is on disk but in no marketplace manifest")

    # Junk that should never be committed.
    for pattern in ("**/.DS_Store", "**/__pycache__"):
        for f, _ in walk(pattern):
            problems.append(f"JUNK FILE: {f} (add to .gitignore and delete)")


# ------------------------------------------------------------------ org leaks
# This pack is generic by contract. Anything matching here is either a real leak
# from the private source repo or a placeholder that needs bracketing.
LEAK_PATTERNS = [
    (r"\bMMA\b", "source-org acronym"),
    (r"Marketing \+ Media Alliance", "source-org name"),
    (r"mmaglobal", "source-org domain"),
    (r"mma[-_][a-z]+", "source-org skill or plugin name"),
    (r"\bHassan\b", "real person"),
    (r"sharepoint\.com/sites/\S+", "real SharePoint site path"),
    (r"#mma[-a-z]*", "real Slack channel"),
    # No real contact address on a public repo. Attribution goes in plugin.json
    # as name + url. Placeholder domains are the only ones allowed through.
    (r"[A-Za-z0-9._%+-]+@(?!yourdomain\.|example\.|yourorg\.|your-org\.)"
     r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
     "a real email address (use a placeholder domain, or name + url)"),
]
ALLOWED_LEAK_FILES = {
    # The author's own email is a legitimate attribution, not a leak.
    "LICENSE",
    # This file necessarily contains the patterns it searches for.
    "scripts/validate.py",
}
leak_hits = []
for f, norm in walk("**/*"):
    if not os.path.isfile(f):
        continue
    if norm in ALLOWED_LEAK_FILES or norm.endswith(".json") and "plugin" in norm:
        continue
    if os.path.splitext(f)[1].lower() not in (".md", ".py", ".sh", ".json", ".yaml", ".yml", ".csv", ".toml", ".txt", ""):
        continue
    try:
        text = open(f, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        continue
    for pat, why in LEAK_PATTERNS:
        for m in re.finditer(pat, text):
            line = text.count("\n", 0, m.start()) + 1
            leak_hits.append(f"{f}:{line}: {why} -> {m.group(0)!r}")

if leak_hits:
    problems.append(f"ORG-SPECIFIC LEAKS ({len(leak_hits)}):")
    problems.extend("    " + h for h in leak_hits[:60])
    if len(leak_hits) > 60:
        problems.append(f"    ... and {len(leak_hits) - 60} more")


# --------------------------------------------------------- manifest checksums
if not LEAKS_ONLY:
    for man, _ in walk("**/MANIFEST.json"):
        base = os.path.dirname(man)
        try:
            entries = json.load(open(man, encoding="utf-8")).get("files", {})
        except Exception as e:
            problems.append(f"BAD MANIFEST JSON: {man} -> {e}")
            continue
        for rel, meta in entries.items():
            f = os.path.join(base, rel)
            if not os.path.exists(f):
                problems.append(f"MANIFEST references a missing file: {man} -> {rel}")
                continue
            blob = open(f, "rb").read()
            if len(blob) != meta.get("bytes") or hashlib.sha256(blob).hexdigest() != meta.get("sha256"):
                problems.append(
                    f"STALE MANIFEST entry: {man} -> {rel} "
                    f"(disk {len(blob)}B, manifest {meta.get('bytes')}B). "
                    "Regenerate with scripts/rebuild_manifests.py."
                )

if problems:
    print("VALIDATION FAILED:")
    for p in problems:
        print("  -" if not p.startswith("    ") else "", p)
    sys.exit(1)

print("VALIDATION PASSED")
if not LEAKS_ONLY:
    for label, path in (("claude ", ".claude-plugin/marketplace.json"),
                        ("chatgpt", ".agents/plugins/marketplace.json")):
        mkt = json.load(open(path, encoding="utf-8"))
        names = [f"{p['name']} -> {src(p)}" for p in mkt.get("plugins", [])]
        print(f"  {label} manifest: {names}")
