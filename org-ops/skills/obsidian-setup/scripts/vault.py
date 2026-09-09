#!/usr/bin/env python3
"""Turn a folder of existing notes into an Obsidian vault, then help tidy it.

Commands:
  check                     Where is this person up to, and what is the next step
  clean <vault>             Remove leftovers from the old version of this skill
  find                      Look for note collections already on this Mac
  init <folder>             Make that folder an Obsidian vault (creates .obsidian)
  plan <vault>             Propose subfolders for loose notes. Changes nothing.
  organize <vault>         Apply the plan. Needs --apply. Never overwrites.
  tag <vault>              Add front-matter tags derived from the folder a note sits in
  open <vault>             Open it in Obsidian

Design rules, learned the hard way:
  - Nothing here assumes a company folder, a OneDrive mount, or a shared set of
    pages. A vault is any folder. That is the whole point of the format.
  - `organize` and `tag` are dry-run by default and print the exact moves. They
    refuse to overwrite, refuse to touch `.obsidian`, and skip anything already
    where it should be.
  - No symlinks. They were the single biggest source of breakage in the old
    version of this script and they are not needed to read a folder of notes.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

HOME = Path.home()
OBSIDIAN_APP = Path("/Applications/Obsidian.app")
OBSIDIAN_CFG = HOME / "Library" / "Application Support" / "obsidian" / "obsidian.json"

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"

NOTE_EXT = {".md", ".markdown", ".txt"}
CARRY_EXT = {".pdf", ".docx", ".doc", ".rtf", ".png", ".jpg", ".jpeg", ".webp"}

# Folders that are somebody's whole life, not a note collection. Never scanned.
SKIP_DIRS = {
    ".git", ".obsidian", "node_modules", "Library", "Applications", ".Trash",
    ".venv", "venv", "__pycache__", ".cache", "site-packages",
}


def ok(m):
    print(f"  {GREEN}OK{RESET}    {m}")


def bad(m):
    print(f"  {RED}FAIL{RESET}  {m}")


def warn(m):
    print(f"  {YELLOW}NOTE{RESET}  {m}")


def dim(m):
    print(f"  {DIM}{m}{RESET}")


# --------------------------------------------------------------- helpers

def known_vaults():
    """Vaults Obsidian already knows about. Empty dict is normal on a fresh Mac."""
    if not OBSIDIAN_CFG.is_file():
        return {}
    try:
        d = json.loads(OBSIDIAN_CFG.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return {k: v.get("path") for k, v in (d.get("vaults") or {}).items() if v.get("path")}


def is_vault(p: Path):
    return (p / ".obsidian").is_dir()


def notes_in(p: Path, limit=None):
    """Every note file under p, skipping the noise directories."""
    out = []
    for root, dirs, files in os.walk(p):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if Path(f).suffix.lower() in NOTE_EXT and not f.startswith("."):
                out.append(Path(root) / f)
                if limit and len(out) >= limit:
                    return out
    return out


def front_matter(text):
    """(dict-ish mapping, body) for a note. Deliberately not a YAML parser: this
    only needs to find and rewrite a `tags:` line without disturbing anything."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4:].lstrip("\n")


# Words that describe what a note IS, not what it is ABOUT. Never folder names.
GENERIC = {
    "notes", "note", "meeting", "meetings", "call", "calls", "draft", "drafts",
    "final", "copy", "new", "old", "update", "updates", "misc", "stuff", "temp",
    "doc", "docs", "document", "untitled", "agenda", "minutes", "summary",
    "follow", "recap", "prep", "review", "the", "and", "for", "with", "from",
}


def slug_words(name):
    """Words in a filename, lowercased, punctuation gone, in original order.

    Two exclusions, both learned from real filenames:
      - all-digit tokens: "POSSIBLE 2026" should group under Possible, not 2026
      - GENERIC words: "Board meeting Jan" should group under Board, not Meeting
    """
    return [w for w in re.split(r"[^A-Za-z0-9]+", Path(name).stem.lower())
            if len(w) > 2 and not w.isdigit() and w not in GENERIC]


# --------------------------------------------------------------- check

# Left behind by an earlier version of this skill, which symlinked a
# company folder into the vault. Detect it so it can be removed rather than
# leaving a broken link the person will trip over.
LEGACY_NAMES = ("00 Shared Brain", "00 Canon")


def legacy_junk(vault: Path):
    """Broken links and empty stubs the old version of this skill created."""
    out = []
    for name in LEGACY_NAMES:
        p = vault / name
        if p.is_symlink():
            out.append((p, "broken symlink" if not p.exists() else "symlink"))
        elif p.is_dir() and not any(p.iterdir()):
            out.append((p, "empty leftover folder"))
    return out


def classify(vault: Path):
    """Where is this person actually up to? Drives what to do next."""
    if not vault.exists():
        return "missing", 0, 0
    if not is_vault(vault):
        return "not-a-vault", len(notes_in(vault)), 0
    notes = notes_in(vault)
    loose = [f for f in vault.glob("*")
             if f.is_file() and f.suffix.lower() in NOTE_EXT and not f.name.startswith(".")]
    if not notes:
        return "empty", 0, 0
    if len(loose) >= 5 and len(loose) >= len(notes) * 0.6:
        return "unorganized", len(notes), len(loose)
    return "organized", len(notes), len(loose)


def cmd_check(args):
    """Report the state and the single next command. Changes nothing."""
    print("\nObsidian")
    if not OBSIDIAN_APP.is_dir():
        bad("not installed")
        print()
        print("  NEXT: download the desktop app from obsidian.md, then run check again.")
        print("        It is free and it does not need an account.\n")
        return 0
    ok(f"installed at {OBSIDIAN_APP}")

    vaults = known_vaults()
    if args.vault:
        vaults = {"(the one you named)": str(Path(args.vault).expanduser().resolve())}

    print("\nVaults")
    if not vaults:
        dim("none set up yet")
        print()
        print("  NEXT: ask what they use for notes today, then find a folder:")
        print("        vault.py find\n")
        return 0

    nexts = []
    for name, path in vaults.items():
        vp = Path(path)
        state, n, loose = classify(vp)
        if state == "missing":
            warn(f"{path}  registered, but the folder is gone")
            nexts.append(f"vault.py init '{path}' --create    # or ignore it, if it moved")
            continue

        junk = legacy_junk(vp) if is_vault(vp) else []
        if state == "not-a-vault":
            warn(f"{path}  a folder with {n} notes, not a vault yet")
            nexts.append(f"vault.py init '{path}'")
        elif state == "empty":
            warn(f"{path}  a vault with no notes in it yet")
            nexts.append("import their notes, see references/import-by-tool.md")
        elif state == "unorganized":
            ok(f"{path}  {n} notes, {loose} of them loose in the root")
            nexts.append(f"vault.py plan '{path}'")
        else:
            ok(f"{path}  {n} notes, already in folders")

        for jp, kind in junk:
            bad(f"    leftover from the old version of this skill: '{jp.name}' ({kind})")
            nexts.append(f"vault.py clean '{path}'")

    print()
    if nexts:
        print("  NEXT:")
        for c in dict.fromkeys(nexts):
            print(f"        {c}")
    else:
        print("  Nothing to do. It is set up.")
    print()
    return 0


# --------------------------------------------------------------- clean

def cmd_clean(args):
    """Remove wreckage from the old version of this skill. Nothing else is touched."""
    vault = Path(args.vault).expanduser().resolve()
    junk = legacy_junk(vault)
    if not junk:
        ok("nothing left over to clean")
        return 0

    if not args.apply:
        print("\n  Dry run. Re-run with --apply to remove these.\n")
    for p, kind in junk:
        # Only ever a symlink or a provably empty directory. Never a file with
        # content, and never anything recursive.
        if args.apply:
            if p.is_symlink():
                p.unlink()
            elif p.is_dir() and not any(p.iterdir()):
                p.rmdir()
        print(f"  {'removed ' if args.apply else 'would remove '}{p.name}  ({kind})")
    print()
    if args.apply:
        ok("done. Nothing with content in it was touched.")
    print()
    return 0


# --------------------------------------------------------------- find

def cmd_find(args):
    """Where are this person's notes already? Nothing is assumed about location."""
    roots = [Path(r).expanduser() for r in args.roots] if args.roots else [
        HOME / "Documents", HOME / "Desktop", HOME / "Downloads", HOME / "Notes",
    ]
    # Any cloud mount, whatever the tenant is called. Never hardcode a suffix.
    cs = HOME / "Library" / "CloudStorage"
    if cs.is_dir():
        roots += sorted(p for p in cs.iterdir() if p.is_dir())

    print("\nLooking for note collections. Nothing is moved or changed.\n")
    found = []
    for root in roots:
        if not root.is_dir():
            continue
        # Count notes per immediate subfolder, so we report "a folder with notes
        # in it" rather than 4000 individual files.
        buckets = Counter()
        for f in notes_in(root):
            try:
                rel = f.relative_to(root)
            except ValueError:
                continue
            buckets[rel.parts[0] if len(rel.parts) > 1 else "."] += 1
        total = sum(buckets.values())
        if not total:
            continue
        flag = " (already a vault)" if is_vault(root) else ""
        print(f"  {root}{flag}")
        found.append((root, total))
        for sub, n in buckets.most_common(8):
            label = "loose in this folder" if sub == "." else sub
            print(f"      {n:5d}  {label}")
        if len(buckets) > 8:
            dim(f"      ... and {len(buckets) - 8} more subfolders")
        print()

    if not found:
        print("  Nothing found in the usual places.")
        print("  Ask where they keep notes, then re-run:")
        print("    vault.py find --roots '/path/one' '/path/two'\n")
        return 0

    print("  Next: pick the folder that should become the vault, then")
    print("    vault.py init '<that folder>'\n")
    return 0


# --------------------------------------------------------------- init

def cmd_init(args):
    target = Path(args.folder).expanduser().resolve()

    if not target.exists():
        if not args.create:
            bad(f"{target} does not exist. Pass --create to make it.")
            return 1
        target.mkdir(parents=True)
        ok(f"created {target}")

    if not target.is_dir():
        bad(f"{target} is a file, not a folder.")
        return 1

    if is_vault(target):
        ok(f"{target} is already a vault. Nothing to do.")
        return 0

    # A vault is a folder with a .obsidian directory. That is the entire
    # mechanism, which is why any folder of notes can become one in place.
    cfg = target / ".obsidian"
    cfg.mkdir()
    (cfg / "app.json").write_text(json.dumps({
        "attachmentFolderPath": "Attachments",
        "alwaysUpdateLinks": True,
        "newLinkFormat": "shortest",
        "useMarkdownLinks": False,
    }, indent=2) + "\n")
    (cfg / "core-plugins.json").write_text(json.dumps({
        "file-explorer": True, "global-search": True, "switcher": True,
        "backlink": True, "outgoing-link": True, "tag-pane": True,
        "properties": True, "outline": True, "word-count": True,
        "file-recovery": True, "graph": True,
    }, indent=2) + "\n")

    n = len(notes_in(target))

    # An empty vault is one of the documented reasons people abandon this, so a
    # brand new one gets a single orientation note. A folder that already has
    # notes in it does not need one and does not get one.
    if n == 0:
        seed = Path(__file__).resolve().parent.parent / "assets" / "Start here.md"
        if seed.is_file():
            shutil.copy2(seed, target / seed.name)
            ok(f"added '{seed.name}' so the vault is not empty")

    ok(f"{target} is now a vault")
    dim(f"{n} notes already inside it. Nothing was moved."
        if n else "It was empty, so it has one note to read first.")
    print()
    print("  Next:")
    print(f"    vault.py open '{target}'          open it")
    print(f"    vault.py plan '{target}'          see a proposed folder layout")
    print()
    return 0


# --------------------------------------------------------------- plan / organize

def propose(vault: Path):
    """Group the notes sitting loose in the vault root into candidate subfolders.

    Grouping is by the most common meaningful word shared across filenames, which
    in practice recovers how people already name things (by project, client,
    podcast, or event) without imposing a method on them.
    """
    loose = [f for f in vault.glob("*") if f.is_file()
             and f.suffix.lower() in NOTE_EXT and not f.name.startswith(".")]
    if not loose:
        return {}, []

    word_files = defaultdict(list)
    word_pos = defaultdict(list)
    for f in sorted(loose):
        seen = set()
        for i, w in enumerate(slug_words(f.name)):
            if w in seen:
                continue
            seen.add(w)
            word_files[w].append(f)
            word_pos[w].append(i)

    def rank(kv):
        word, files = kv
        # Biggest group wins. Then the word appearing earliest in the filenames,
        # because people write "Ulta pricing questions", project first. Then
        # alphabetical, so `plan` and `organize` can never disagree (set
        # iteration order is not stable across processes).
        return (-len(files), sum(word_pos[word]) / len(word_pos[word]), word)

    groups, claimed = {}, set()
    for word, files in sorted(word_files.items(), key=rank):
        picked = [f for f in files if f not in claimed]
        if len(picked) < 3:
            continue
        groups[word.title()] = sorted(picked)
        claimed.update(picked)

    leftover = sorted(f for f in loose if f not in claimed)
    return groups, leftover


def cmd_plan(args):
    vault = Path(args.vault).expanduser().resolve()
    if not is_vault(vault):
        bad(f"{vault} is not a vault yet. Run: vault.py init '{vault}'")
        return 1

    groups, leftover = propose(vault)
    total_loose = sum(len(v) for v in groups.values()) + len(leftover)
    print(f"\n{total_loose} notes are loose in the vault root.\n")
    if not total_loose:
        ok("Nothing loose. The vault is already organized.")
        print()
        return 0

    if groups:
        print("  Proposed subfolders, by what the filenames already have in common:\n")
        for name, files in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            print(f"    {name}/  ({len(files)} notes)")
            for f in files[:3]:
                dim(f"        {f.name}")
            if len(files) > 3:
                dim(f"        ... and {len(files) - 3} more")
            print()
    if leftover:
        print(f"  {len(leftover)} notes with nothing in common. Leave them in the root;")
        print("  search finds them, and a folder with one note in it helps nobody.\n")

    print("  Nothing has moved. To apply:")
    print(f"    vault.py organize '{vault}' --apply\n")
    return 0


def cmd_organize(args):
    vault = Path(args.vault).expanduser().resolve()
    if not is_vault(vault):
        bad(f"{vault} is not a vault yet. Run: vault.py init '{vault}'")
        return 1

    groups, _ = propose(vault)
    if not groups:
        ok("Nothing worth moving.")
        return 0

    if not args.apply:
        print("\n  Dry run. Re-run with --apply to move files.\n")

    moved = skipped = 0
    for name, files in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        dest = vault / name
        for f in files:
            target = dest / f.name
            if target.exists():
                warn(f"skipped, name already taken: {name}/{f.name}")
                skipped += 1
                continue
            if args.apply:
                dest.mkdir(exist_ok=True)
                shutil.move(str(f), str(target))
            print(f"  {'moved ' if args.apply else 'would move '}{f.name} -> {name}/")
            moved += 1

    print()
    if args.apply:
        ok(f"{moved} notes moved, {skipped} skipped")
        dim("Obsidian updates any [[links]] to these notes automatically.")
    else:
        dim(f"{moved} would move, {skipped} would be skipped")
    print()
    return 0


# --------------------------------------------------------------- tag

def cmd_tag(args):
    """Give every note a tag matching the folder it sits in.

    Tags are the cross-cutting layer: a note lives in exactly one folder but can
    carry several tags, which is the only reason to have both.
    """
    vault = Path(args.vault).expanduser().resolve()
    if not is_vault(vault):
        bad(f"{vault} is not a vault yet. Run: vault.py init '{vault}'")
        return 1

    if not args.apply:
        print("\n  Dry run. Re-run with --apply to write tags.\n")

    changed = already = 0
    for f in notes_in(vault):
        if f.suffix.lower() != ".md":
            continue
        try:
            rel = f.relative_to(vault)
        except ValueError:
            continue
        if len(rel.parts) < 2:
            continue  # loose in the root, no folder to derive a tag from
        tag = "/".join(re.sub(r"[^A-Za-z0-9]+", "-", p).strip("-").lower()
                       for p in rel.parts[:-1])
        if not tag:
            continue

        text = f.read_text(errors="replace")
        fm, body = front_matter(text)
        if fm is not None and re.search(rf"(^|[\s,\[]){re.escape(tag)}($|[\s,\]])", fm):
            already += 1
            continue

        if fm is None:
            new = f"---\ntags:\n  - {tag}\n---\n\n{text.lstrip()}"
        elif re.search(r"^tags:", fm, re.M):
            new_fm = re.sub(r"^tags:\s*\n", f"tags:\n  - {tag}\n", fm, count=1, flags=re.M)
            if new_fm == fm:  # inline form: tags: [a, b]
                new_fm = re.sub(r"^tags:\s*\[(.*?)\]",
                                lambda m: f"tags: [{m.group(1)}, {tag}]", fm,
                                count=1, flags=re.M)
            new = f"---\n{new_fm}\n---\n\n{body}"
        else:
            new = f"---\n{fm}\ntags:\n  - {tag}\n---\n\n{body}"

        if args.apply:
            f.write_text(new)
        print(f"  {'tagged ' if args.apply else 'would tag '}{rel}  #{tag}")
        changed += 1

    print()
    if args.apply:
        ok(f"{changed} notes tagged, {already} already had it")
    else:
        dim(f"{changed} would be tagged, {already} already have it")
    print()
    return 0


# --------------------------------------------------------------- open

def cmd_open(args):
    vault = Path(args.vault).expanduser().resolve()
    if not is_vault(vault):
        bad(f"{vault} is not a vault. Run: vault.py init '{vault}'")
        return 1
    subprocess.run(["open", "-a", str(OBSIDIAN_APP), str(vault)], check=False)
    ok(f"opened {vault}")
    dim("If Obsidian shows the vault picker, choose 'Open folder as vault' and")
    dim(f"pick {vault}. It only asks once.")
    return 0


# --------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check")
    c.add_argument("--vault", help="Check one specific folder instead of the registry")
    c.set_defaults(fn=cmd_check)

    cl = sub.add_parser("clean")
    cl.add_argument("vault")
    cl.add_argument("--apply", action="store_true", help="Actually remove them")
    cl.set_defaults(fn=cmd_clean)

    f = sub.add_parser("find")
    f.add_argument("--roots", nargs="*", help="Folders to look in, if you know them")
    f.set_defaults(fn=cmd_find)

    i = sub.add_parser("init")
    i.add_argument("folder")
    i.add_argument("--create", action="store_true", help="Make the folder if missing")
    i.set_defaults(fn=cmd_init)

    p = sub.add_parser("plan")
    p.add_argument("vault")
    p.set_defaults(fn=cmd_plan)

    o = sub.add_parser("organize")
    o.add_argument("vault")
    o.add_argument("--apply", action="store_true", help="Actually move files")
    o.set_defaults(fn=cmd_organize)

    t = sub.add_parser("tag")
    t.add_argument("vault")
    t.add_argument("--apply", action="store_true", help="Actually write tags")
    t.set_defaults(fn=cmd_tag)

    op = sub.add_parser("open")
    op.add_argument("vault")
    op.set_defaults(fn=cmd_open)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
