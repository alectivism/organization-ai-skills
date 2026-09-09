---
name: propose-skill-edit
description: "Turn a staff member's feedback about a skill into a reviewable proposal with a real patch attached, and submit it to the maintainer. Use whenever someone says a skill is wrong, out of date, missing something, or gave a bad answer; when they say 'this should say X instead', 'that's not right anymore', 'can you fix the skill', 'who maintains this', or 'how do I suggest a change'; and when a mistake in a skill, agent, or reference file is found while doing other work. Also use on the maintainer side to list pending proposals and apply them. Covers the skills and agents in your org's fork of this pack."
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you.

# Propose an edit to a skill

Your org's skills repo is private and most staff have no seat on it, so "open a
pull request" is not a path they have. Prose feedback is a path, but it pushes
all the work back onto the maintainer, so it queues and dies.

## The fast path: a Slack channel

If your org has set one up and the person is in **[YOUR FEEDBACK CHANNEL]**,
that is the answer. Tell them to post there and tag `@Claude`, naming the repo
in the first message of the thread:

> `@Claude` in the [YOUR SKILLS REPO] repo, the launch-strategy skill lists a
> phase that no longer applies. It was dropped last quarter and I sent someone
> the old process. [Name] confirmed on the [date] team call.

That channel runs Claude Tag against `[YOUR SKILLS REPO]` with admin-granted
access, so it opens the pull request directly. The reporter needs no GitHub seat
and nothing installed. Guardrails live in the repo's own root `CLAUDE.md`, which
loads into the session after the clone.

Use the rest of this skill when they are not in that channel, when Claude Tag is
not set up, or when they want the proposal written up before it goes anywhere.
Setup and prerequisites for the channel: `docs/claude-tag-setup.md` in the repo,
if your org has written one.

## The portable path: a bundled proposal

Capture the feedback, draft the actual edit, attach a unified diff against the
installed file, and send it through whatever channel the person already has. The
maintainer applies it with one command or rejects it.

Helper script for every filesystem and git step: `scripts/proposal.py`.

## Flow

**1. Find the file:** never guess a path, since installs differ.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/propose-skill-edit/scripts/proposal.py" locate document-find
```

With no name it lists every skill and agent installed across the plugins in
your org's fork.

**2. Get the real problem, in their words:** ask what they were doing when the
skill let them down, what it told them, and what it should have said. A proposal
that says "the document-find skill is out of date" cannot be acted on. One that
says "it lists a SharePoint site that was retired and the fallback isn't
mentioned" can.

Push for evidence: where does the correct version come from. A team call, a
meeting note, an internal doc, your own program. Guessing at a correction is the
same failure as the error being reported.

**3. Draft the edit against a working copy:** never edit the install.

```bash
python3 .../proposal.py draft document-find
```

Edit the working copy it prints. Match the file's existing structure, density,
and voice: this is going into a shared skill, so a paragraph that reads
differently from everything around it will get rewritten before it lands.
Change the minimum that fixes the problem.

**4. Bundle it:**

```bash
python3 .../proposal.py bundle document-find \
  --title "Drop the retired SharePoint site from the fallback list" \
  --problem "The fallback list still names a site that was retired last quarter, and I sent someone a dead link." \
  --fix "Remove that entry and note the retirement date." \
  --evidence "[Name] confirmed the retirement on the [date] team call." \
  --author "[Your name]" --type correction \
  --edited ~/Documents/skill-proposals/working-document-find-SKILL.md
```

Types: `correction`, `addition`, `clarification`, `removal`, `bug`. The bundle
lands in the outbox directory (see `scripts/proposal.py`'s docstring for how to
set it) and contains the problem, the fix, the evidence, and an applyable patch.

A proposal with no drafted edit is still worth filing. Omit `--edited` and it
becomes a described request rather than a patch.

**5. Submit it:** check what is available, then send through the highest one
that works:

```bash
python3 .../proposal.py channels
```

| Order | Channel | Use when |
|---|---|---|
| 0 | [YOUR FEEDBACK CHANNEL] with `@Claude` | The person is in that channel. It opens the PR itself; nothing below is needed |
| 1 | GitHub PR | `channels` reports the PR path as available. Branch, commit the patch, `gh pr create` with the bundle as the body |
| 2 | Slack/Teams DM to [YOUR MAINTAINER], or the feedback channel | A chat MCP or connector is in the session. Paste the bundle body, attach the file path |
| 3 | A task assigned to [YOUR MAINTAINER] in your project tracker | A project-management connector is in the session. Bundle body in the description, `skill-proposal` in the title |
| 4 | Email to [YOUR MAINTAINER EMAIL] | A mail MCP or connector is in the session. Subject: `Skill proposal: <title>` |
| 5 | Hand over the file path | Nothing else is wired. Tell them where the bundle is and that [YOUR MAINTAINER] needs it |

**Show the person the full proposal and get explicit approval before sending
anything.** It goes out under their name. State which channel, who receives it,
and what it says.

## What makes a proposal land

- **One change per proposal:** a bundle touching four unrelated things gets
  deferred as a unit.
- **The failure, not the preference:** "this gave someone the wrong renewal
  date" gets applied. "I'd word this differently" gets queued.
- **A NAMED source, not a preference:** corrections to numbers, prices, status
  fields, and dates need evidence with a source and a date, because those are
  exactly the facts that drift. "I think this changed" is not a correction; "X
  confirmed this on the [date] call" is.
- **No new unverified facts:** a correction that swaps one unsourced claim for
  another is not a fix. Run your org's own fact-checking skill, if you have one,
  over any proposal that changes a number, name, date, or price.
- **No PII, contract terms, or embargoed material** in the bundle: it travels
  through Slack and email.

## Maintainer side

```bash
python3 .../proposal.py list                 # pending bundles
python3 .../proposal.py apply FILE --check   # does the patch still apply
python3 .../proposal.py apply FILE           # apply to the working tree
```

Proposals that arrive from the Slack channel show up as pull requests instead, already carrying the PR template's problem, source, and verification sections.

`apply` refuses on a conflict rather than forcing it, which is the right outcome:
the file moved since the proposal was written, so the intent needs re-applying
by hand. Applying stages nothing and commits nothing. Review with `git diff`,
then commit, then bump the plugin version in both `plugin.json` and
`.claude-plugin/marketplace.json` so staff installs pick it up.

Rejecting is a real outcome. Tell the person why in one line, since a proposal
that disappears silently teaches them not to file the next one.
