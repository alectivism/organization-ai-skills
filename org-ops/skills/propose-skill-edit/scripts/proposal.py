#!/usr/bin/env python3
"""propose-skill-edit helper — the deterministic half of the feedback loop.

Staff cannot open pull requests against a private repo they have no seat on, and
prose feedback ("the X skill should mention Y") pushes all the work onto the
maintainer. So a proposal here carries a real unified diff against the
installed plugin file. The maintainer applies it with one command or rejects it.

This script does the filesystem and git work. The submission itself goes through
whatever channel the staffer actually has (Slack, a project tracker, email),
which the agent drives through its MCP tools.

Commands:
  locate [NAME]              Find the installed plugin root, and the file for a
                             skill, agent, or CLAUDE.md if NAME is given.
  draft NAME                 Copy the target file to a scratch working copy and
                             print both paths. Edit the copy, never the install.
  diff ORIGINAL EDITED       Unified diff, paths rewritten repo-relative.
  bundle --title T ...       Write a proposal bundle to the outbox.
  channels                   Report which submission channels look available.
  list                       List proposals in the outbox.
  apply FILE                 Maintainer side: check and apply a bundle's diff.

Outbox: ~/Documents/skill-proposals (override with SKILL_PROPOSAL_DIR).

Plugin root: by default this script finds its own install location (it lives at
<plugin root>/skills/propose-skill-edit/scripts/proposal.py, so it walks up from
its own path). Override with the CLAUDE_PLUGIN_ROOT environment variable, or by
writing a single path to ~/.config/propose-skill-edit/root — useful if you run
this script standalone, outside a plugin install.

Sibling plugins (other plugins in the same repo checkout, e.g. content or
research skills living next to this one) are discovered automatically: any
directory next to the plugin root that itself has a skills/ or agents/
subfolder counts. Nothing here hardcodes your org's plugin names.
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import subprocess
import sys
import time

OUTBOX = os.path.expanduser(
    os.environ.get("SKILL_PROPOSAL_DIR", "~/Documents/skill-proposals"))

CONFIG_FILE = os.path.expanduser("~/.config/propose-skill-edit/root")

# This script's own install location: .../<plugin root>/skills/propose-skill-edit/scripts
SELF_DIR = os.path.dirname(os.path.abspath(__file__))
SELF_PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SELF_DIR)))


def _read_config_root() -> str:
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as fh:
            line = fh.readline().strip()
            if line:
                return os.path.expanduser(line)
    return ""


def find_root() -> str:
    """Return the installed plugin directory (the one holding this skill)."""
    candidates = [
        os.environ.get("CLAUDE_PLUGIN_ROOT", ""),
        _read_config_root(),
        SELF_PLUGIN_ROOT,
    ]
    for cand in candidates:
        if not cand:
            continue
        p = os.path.expanduser(cand)
        if os.path.isdir(os.path.join(p, "skills")):
            return p
    # Broad fallback: search common Claude plugin install locations for any
    # directory that contains this skill, so a relocated or differently-named
    # install is still found without hardcoding an org's plugin name.
    for base in ("~/.claude/plugins", "~"):
        base = os.path.expanduser(base)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, _ in os.walk(base):
            if dirpath.count(os.sep) - base.count(os.sep) > 6:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if not d.startswith(".git")]
            if os.path.isdir(os.path.join(dirpath, "skills", "propose-skill-edit")):
                return dirpath
    sys.exit("Could not find an installed plugin root. Set CLAUDE_PLUGIN_ROOT, "
             "or write its path to ~/.config/propose-skill-edit/root, and retry.")


def repo_root(root: str) -> str:
    """The multi-plugin checkout above this plugin, when there is one."""
    return os.path.dirname(root)


def discover_siblings(root: str) -> list[str]:
    """Other plugins in the same repo checkout: any dir with a skills/ or
    agents/ subfolder, next to this plugin's own root. No hardcoded names."""
    base = repo_root(root)
    sibs = []
    if not os.path.isdir(base):
        return sibs
    for entry in sorted(os.listdir(base)):
        p = os.path.join(base, entry)
        if p == root or entry.startswith("."):
            continue
        if os.path.isdir(p) and (os.path.isdir(os.path.join(p, "skills"))
                                  or os.path.isdir(os.path.join(p, "agents"))):
            sibs.append(p)
    return sibs


def find_target(root: str, name: str) -> str:
    """Resolve a skill, agent, or reference name to a file in the install."""
    name = name.strip().lower().replace(" ", "-")
    if name in ("claude.md", "claude-md", "always-on", "context"):
        return os.path.join(root, "CLAUDE.md")
    hits = []
    for plugin_dir in [root] + discover_siblings(root):
        for sub in ("skills", "agents"):
            d = os.path.join(plugin_dir, sub)
            if not os.path.isdir(d):
                continue
            for entry in sorted(os.listdir(d)):
                if entry.startswith("."):
                    continue
                stem = entry[:-3] if entry.endswith(".md") else entry
                if name not in stem.lower():
                    continue
                path = os.path.join(d, entry)
                if os.path.isdir(path):
                    path = os.path.join(path, "SKILL.md")
                if os.path.isfile(path):
                    hits.append(path)
        for ref in _walk_refs(plugin_dir, name):
            hits.append(ref)
    if not hits:
        sys.exit(f"No skill, agent, or reference file matching '{name}'. "
                 f"Run `locate` with no argument to list what is installed.")
    if len(hits) > 1:
        exact = [h for h in hits if os.path.basename(os.path.dirname(h)).lower() == name
                 or os.path.basename(h).lower() == f"{name}.md"]
        if len(exact) == 1:
            return exact[0]
        sys.exit("Ambiguous. Name one of:\n  " + "\n  ".join(hits))
    return hits[0]


def _walk_refs(plugin_dir: str, name: str):
    for dirpath, _, files in os.walk(os.path.join(plugin_dir, "skills")):
        if os.path.basename(dirpath) != "references":
            continue
        for f in files:
            if f.endswith(".md") and name in f[:-3].lower():
                yield os.path.join(dirpath, f)


def cmd_locate(args):
    root = find_root()
    print(f"plugin root: {root}")
    print(f"repo root:   {repo_root(root)}")
    if args.name:
        target = find_target(root, args.name)
        print(f"target:      {target}")
        print(f"repo path:   {rel(target, root)}")
        return 0
    for plugin_dir in [root] + discover_siblings(root):
        names = []
        for sub in ("skills", "agents"):
            d = os.path.join(plugin_dir, sub)
            if os.path.isdir(d):
                names += [e[:-3] if e.endswith(".md") else e
                          for e in sorted(os.listdir(d)) if not e.startswith(".")]
        if names:
            print(f"\n{os.path.basename(plugin_dir)}: {', '.join(names)}")
    return 0


def rel(path: str, root: str) -> str:
    """Path relative to the repo checkout, so the diff applies upstream."""
    base = repo_root(root)
    try:
        return os.path.relpath(path, base)
    except ValueError:
        return path


def cmd_draft(args):
    root = find_root()
    target = find_target(root, args.name)
    os.makedirs(OUTBOX, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-")
    work = os.path.join(OUTBOX, f"working-{slug}-{os.path.basename(target)}")
    shutil.copy2(target, work)
    print(f"original: {target}")
    print(f"working:  {work}")
    print(f"repo path: {rel(target, root)}")
    print("\nEdit the working copy only. The install stays untouched.")
    return 0


def unified(original: str, edited: str, root: str) -> str:
    a = open(original, encoding="utf-8").read().splitlines(keepends=True)
    b = open(edited, encoding="utf-8").read().splitlines(keepends=True)
    r = rel(original, root)
    return "".join(difflib.unified_diff(a, b, fromfile=f"a/{r}", tofile=f"b/{r}", n=3))


def cmd_diff(args):
    root = find_root()
    d = unified(args.original, args.edited, root)
    if not d.strip():
        print("No changes between the two files.", file=sys.stderr)
        return 1
    sys.stdout.write(d)
    return 0


def cmd_bundle(args):
    root = find_root()
    target = find_target(root, args.name)
    diff = unified(target, args.edited, root) if args.edited else ""
    if args.edited and not diff.strip():
        return _fail("The working copy is identical to the installed file.")
    os.makedirs(OUTBOX, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")[:50]
    stamp = time.strftime("%Y-%m-%d")
    out = os.path.join(OUTBOX, f"{stamp}-{slug}.md")
    author = args.author or os.environ.get("USER", "unknown")
    parts = [
        f"# Proposal: {args.title}", "",
        f"- **Target** `{rel(target, root)}`",
        f"- **From** {author}",
        f"- **Date** {stamp}",
        f"- **Type** {args.type}", "",
        "## What is wrong today", "", args.problem.strip(), "",
        "## What it should say instead", "", (args.fix or "See the diff below.").strip(), "",
    ]
    if args.evidence:
        parts += ["## Evidence", "", args.evidence.strip(), ""]
    if diff:
        parts += ["## Patch", "", "```diff", diff.rstrip("\n"), "```", ""]
        parts += ["Maintainer: `proposal.py apply " + out + "`", ""]
    else:
        parts += ["No patch attached: this is a description, not a drafted edit.", ""]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    print(out)
    return 0


def _fail(msg):
    print(msg, file=sys.stderr)
    return 1


def cmd_channels(_args):
    """Report what a submission could travel through. The agent does the sending."""
    root = find_root()
    repo = repo_root(root)
    def ok(cmd):
        try:
            return subprocess.run(cmd, shell=True, capture_output=True,
                                  timeout=15).returncode == 0
        except Exception:
            return False
    git_repo = os.path.isdir(os.path.join(repo, ".git"))
    gh = ok("gh auth status")
    push = git_repo and gh and ok(
        f"git -C {repo!r} ls-remote --exit-code origin >/dev/null 2>&1")
    print(f"github pr      {'yes' if push else 'no'}  "
          f"(git checkout: {git_repo}, gh auth: {gh})")
    print("chat           agent: does the session have a Slack/Teams MCP or connector")
    print("project tracker agent: does the session have an Asana/Jira-style connector")
    print("email          agent: does the session have a mail MCP or connector")
    print(f"\noutbox         {OUTBOX}")
    print("fallback       hand the bundle file to your maintainer directly")
    return 0


def cmd_list(_args):
    if not os.path.isdir(OUTBOX):
        print(f"No outbox yet at {OUTBOX}")
        return 0
    rows = [f for f in sorted(os.listdir(OUTBOX)) if f.endswith(".md")
            and not f.startswith("working-")]
    for f in rows:
        first = ""
        with open(os.path.join(OUTBOX, f), encoding="utf-8") as fh:
            first = fh.readline().strip().removeprefix("# Proposal:").strip()
        print(f"{f}  {first}")
    print(f"\n{len(rows)} proposal(s) in {OUTBOX}")
    return 0


def cmd_apply(args):
    root = find_root()
    repo = repo_root(root)
    text = open(os.path.expanduser(args.file), encoding="utf-8").read()
    m = re.search(r"```diff\n(.*?)\n```", text, re.S)
    if not m:
        return _fail("No ```diff block in that bundle. Apply it by hand.")
    patch = m.group(1) + "\n"
    tmp = os.path.join(OUTBOX, ".apply.patch")
    os.makedirs(OUTBOX, exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(patch)
    check = subprocess.run(["git", "-C", repo, "apply", "--check", "-v", tmp],
                           capture_output=True, text=True)
    if check.returncode != 0:
        print(check.stderr, file=sys.stderr)
        return _fail("Patch does not apply cleanly. The file changed since the "
                     "proposal was written; re-apply the intent by hand.")
    if args.check:
        print("Patch applies cleanly. Re-run without --check to apply it.")
        return 0
    subprocess.run(["git", "-C", repo, "apply", tmp], check=True)
    print(f"Applied to {repo}. Review with `git -C {repo} diff`, then commit.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("locate"); p.add_argument("name", nargs="?"); p.set_defaults(fn=cmd_locate)
    p = sub.add_parser("draft"); p.add_argument("name"); p.set_defaults(fn=cmd_draft)
    p = sub.add_parser("diff"); p.add_argument("original"); p.add_argument("edited")
    p.set_defaults(fn=cmd_diff)
    p = sub.add_parser("bundle")
    p.add_argument("name", help="skill, agent, or file the proposal targets")
    p.add_argument("--title", required=True)
    p.add_argument("--problem", required=True, help="what is wrong today")
    p.add_argument("--fix", help="what it should say instead")
    p.add_argument("--evidence", help="where the correct version came from")
    p.add_argument("--edited", help="the edited working copy, to diff against the install")
    p.add_argument("--author", help="who is proposing this")
    p.add_argument("--type", default="correction",
                   choices=["correction", "addition", "clarification", "removal", "bug"])
    p.set_defaults(fn=cmd_bundle)
    p = sub.add_parser("channels"); p.set_defaults(fn=cmd_channels)
    p = sub.add_parser("list"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("apply"); p.add_argument("file")
    p.add_argument("--check", action="store_true", help="dry run")
    p.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
