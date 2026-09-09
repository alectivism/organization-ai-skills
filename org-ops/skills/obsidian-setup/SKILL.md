---
name: obsidian-setup
status: ready
description: Help someone turn the notes they already have into an Obsidian vault, then organize it. Use when someone says they want to set up Obsidian, asks what a vault is, asks how to get their Apple Notes or Granola or Evernote or Notion notes into one place, wants their notes organized into folders or tagged, asks whether Obsidian and Claude Cowork can use the same folder, or is stuck partway through setting Obsidian up.
allowed-tools:
  - Read
  - Bash
  - Glob
---

# Set up someone's Obsidian vault

**Their notes, their folder, their structure**. This has nothing to do with any company
folder, any shared set of pages, or any specific folder name. If a step here only works
because a particular company folder exists, that is a bug.

## Work like a pairing session, not a manual

Ask one question, wait for the answer, do one step, show what happened. Do not print a
numbered guide and walk away. This was the explicit request from the room on a
recent all-hands call: people wanted to watch someone do it, not read instructions and fumble.

Match the language they write to you in.

## Say this first, before any setup

Three sentences, in this order. The first two took the CEO two separate attempts to
absorb, and he had already tried Obsidian before. Do not skip them because they sound
obvious.

1. **"An Obsidian vault is just a folder on your Mac. That is the whole thing."** Not a
   database, not an account, not a server. A folder with your notes in it.
2. **"Your AI agent's working folder (Claude Cowork or an equivalent tool that reads local
   files) and your Obsidian vault can be the same folder. There is no connector and no
   MCP. They both just read files off your disk."** This is the single most
   misunderstood point. Say it plainly, then show it.
3. **"Nothing gets moved or uploaded. We point Obsidian at notes you already have."**

If they ask what it costs: free. The paid tier is only Obsidian's own device sync, which
nobody needs to start. If they ask about an account: **you do not need one.** Download is
`obsidian.md`, desktop app, not a browser tab.

## Step 0: find out where they already are

**Run this before anything else**. It changes nothing and it prints the one next step:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/obsidian-setup/scripts/vault.py" check
```

It reports one of six states. Go straight to the step it names:

| What check says | Where to go |
|---|---|
| Obsidian not installed | Send them to `obsidian.md`. Free, no account. Then re-run check |
| No vaults set up yet | Step 1, the full walkthrough |
| A folder with notes, not a vault yet | Step 2, `init` that folder |
| A vault with no notes in it | Step 3, import |
| A vault with notes loose in the root | Step 5, organize |
| Notes already in folders | Nothing to do. Say so and stop |

Somebody who got part way through with the old, broken version of this skill does not
start over. Run `check`, and pick up at the step it names.

**If check reports a leftover from the old version**, a `00 Shared Brain` symlink or an
empty stub folder, clear it first:

```
vault.py clean '<vault>' --apply
```

That only ever removes a symlink or a provably empty folder. It never touches a file with
content in it.

## Step 1: ask what they use now

**Never open Obsidian first**. Open with:

> "What do you use for notes today?"

This one question did more work than anything else on the call. It routes everything
after it, and the answers are more varied than you would guess. Real answers from
staff: Granola, Apple Notes, Notion, Otter, Fireflies, a running Excel file, paper
notebooks, and "nothing, I let Claude dump things somewhere and drag them around later."

**"Nothing" and "I have no system" are the most common real answers, not edge cases**.
Do not treat that as a problem to fix before starting. It means step 2 is a brand new
empty folder, and that is a perfectly good vault.

Then route with [[import-by-tool]], which has the specific path for each of those.

## Step 2: pick the folder

Find what they already have. This changes nothing:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/obsidian-setup/scripts/vault.py" find
```

It looks in Documents, Desktop, Downloads, and every cloud mount on the machine, and
reports folders that already contain notes. If their notes live somewhere unusual, ask
and pass it in: `find --roots '/path/they/named'`.

**Ask which folder should be the vault**. Do not pick for them and do not require a
particular name. Two good answers:

- **The folder they already point their AI agent (Claude Cowork or similar) at**. Then
  the agent and Obsidian are the same folder, which is the thing worth demonstrating.
- **A fresh folder**, if they have no system at all. `~/Notes` is a fine default. Say
  out loud that the name does not matter.

Then:

```
vault.py init '<the folder they chose>'          # add --create if it does not exist yet
```

That writes a `.obsidian` directory and nothing else. No files move.

**Mention both of these now, not later**. Both landed well when they came up:

- They can have more than one vault. A work folder and a personal folder can be separate
  vaults, and switching between them is a menu.
- Claude (or an equivalent AI agent) can watch more than one folder at once. The vault
  folder and a working project folder do not have to be the same folder if they would
  rather keep them apart.

## Step 3: import everything, organize nothing

**Import first, organize second**. Resist tidying in the first pass. Bringing 400 messy
notes in and leaving them in a heap is the correct first outcome, and structure comes
later once they can see what they actually have.

Per-tool steps are in [[import-by-tool]]. Two rules regardless of source:

- **Import into a subfolder, never loose into the vault root**. `Imported from Apple
  Notes/` makes it obvious what came from where and trivial to undo.
- **The original is never deleted**. Say so before starting. Their Apple Notes, Granola
  and Notion accounts are untouched.

Import one notebook or one folder first, look at the result together, then do the rest.
A full-account import that lands badly is miserable to unpick.

## Step 4: open it and show three things

```
vault.py open '<the vault>'
```

Then, and nothing more than this:

1. **Search.** One box, every note. This is what they will actually use daily.
2. **The quick switcher.** Type part of a note name, jump to it.
3. **A link.** Type `[[`, pick a note, then open that note and show the backlink at the
   bottom. This is the moment the idea lands.

**Skip plugins, tags, the graph view, templates, and every published method**. All of it.
Tags especially: folders are the system. The graph view looks impressive and nobody uses
it. Adding any of this in the first
session is what produced the errors and confusion on the call.

Stop here for the first session. Genuinely stop.

## Step 5, a later session: organize

Only once notes are in and they have used it a bit. Full guidance in
[[organizing-with-folders]]. The short version:

```
vault.py plan '<vault>'                  # proposes subfolders, changes nothing
vault.py organize '<vault>' --apply      # moves files, skips any name collision
```

`plan` shows the proposal first, and `organize` is a dry run without `--apply`. Show them
the plan and get a yes before applying anything.

**Folders are the organizing system**. One note lives in one folder, two levels deep at
most. There is a `tag` command and it is deliberately not in this flow: nobody in a
room full of people asked about tags, and a structure built out of tags is hard to navigate and
hard to hand to anyone else. If someone asks for tags,
[[organizing-with-folders]] covers them.

The one structural question worth asking, because people were asked to come back with an
answer to it: **do you want one `Projects` folder, or each project as its own top-level
folder?** Either is fine. Having decided is what matters.

## When they ask why this beats what they already do

They will, and the answer has to be a mechanism rather than a pitch. Two versions of this went
unanswered on the call, so have a real answer ready. It is written out in [[faq]] under
"What does this do that my folder of files does not." Do not answer with "it is what you
make of it."

## When it goes wrong

Every failure seen on that all-hands call, with its fix, is in [[faq]]. The common ones:

- **"It is asking whether I want a new vault or to open a folder as a vault."** Open
  folder as a vault, and pick their folder. It only asks once.
- **"It says something is not in a folder with a certain name."** That was the old
  version of this skill assuming a folder that did not exist. Nothing here needs a
  specific folder name. If you see this, the machine has a stale copy of the skill.
- **"I got more errors than I can imagine."** Run `vault.py check` and read what it
  actually reports rather than guessing.

## What not to do

- Do not assume any company folder, cloud mount, or shared page set exists. None of it
  is required and most of it does not exist yet.
- Do not require a specific folder name or path.
- Do not create symlinks. They were the biggest source of breakage in the previous
  version and they are not needed.
- Do not install a local-LLM plugin. Hours of setup, multi-minute replies.
- Do not teach a named method. See [[what-makes-people-quit]].
- Do not upload or copy anyone's personal notes anywhere. The vault is on their machine.

## Reporting back

Tell them, in plain words: which folder is now a vault, how many notes are in it, what
was imported and from where, and the one thing to try next. Do not list what you ran.
