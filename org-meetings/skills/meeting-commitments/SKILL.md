---
name: meeting-commitments
description: Track what the person promised in their meetings, suppress what is already handled, and hand back a short ranked list of what they still owe. Use when someone asks what they committed to, what they owe people, what they forgot, what is outstanding from their calls, "collect everything I was supposed to do", "what did I promise", "what am I behind on", "what's still open from my meetings", or asks for a recurring follow-up list. Also use to set that list up as a scheduled task, to mark commitments done, and on first run to configure where the tracker stores its data. Works against any meeting-notes source that exposes transcripts or summaries (Granola and Fireflies are used below as the worked examples). This tracks commitments across meetings over time; it does not write up an individual meeting.
status: ready
---

# Meeting Commitments

Sweep recorded meetings for promises the person made, suppress the ones already
handled, and return the ten that matter. Runs on a schedule without repeating
itself.

The split that makes this work: **you do the extraction, the ledger does the
bookkeeping.** Judging whether "yeah I'll get that to you" is a real commitment
needs a model. Remembering that it was already closed on Tuesday does not, and
a model asked to remember it across runs will get it wrong. Never reconstruct
what is outstanding by reading the previous output file.

## Any meeting-notes source works

The examples below name Granola and Fireflies because they cover the common
case of an AI notetaker. The mechanism only needs a source that can give you,
per meeting: a date, the attendee or speaker list, and either a transcript or a
summary with per-person action items. If your organization uses a different
notetaker, a call-recording platform, or hand-typed meeting minutes in a
document store, substitute its equivalent calls wherever Granola or Fireflies
are named and keep the rest of the pipeline as written.

## Step 0: First run, or every run?

Look for `config.json` in the person's store. If it is missing, this is a first
run: go to **Setup** at the bottom of this file and do the interview. Do not
guess a configuration and start sweeping. If it exists, read it and continue.

The config names the store, the lookback window, the display cap, their
categories, their excluded meetings, and where output goes. If they dislike the
shape of the output, change the config. Never hardcode a different structure
into a run.

## Step 1: Reach the store

Every backend holds the same file, `ledger.jsonl`, and the script only ever
works on a local path. For a remote store, pull the file down, run the script,
push it back. That keeps the engine dependency-free and means the backend is a
config choice, not a code path.

| `store.type` | Get the ledger | Put it back |
|---|---|---|
| `folder` | Already local at `store.path` | Nothing to do |
| `sharepoint` | Fetch the file from your SharePoint/OneDrive connector into a temp dir | Write it back through the same connector |
| `asana` | Search the configured project; the tasks *are* the state | Update tasks to close, create tasks for new |

Resolve the script, never hardcode it:

```bash
LEDGER=$(ls "${CLAUDE_PLUGIN_ROOT}/skills/meeting-commitments/scripts/ledger.py" \
            ~/.claude/skills/meeting-commitments/scripts/ledger.py \
            "$STORE/ledger.py" 2>/dev/null | head -1)
```

Paths inside `config.json` should be bare filenames, not absolute paths. The
same folder is mounted at different absolute paths on a host and in a sandbox,
so an absolute path written on one side breaks on the other. The script falls
back to the store directory when a configured directory does not exist here.

**Prefer a connector API over a synced folder:** a synced OneDrive or Dropbox
path looks like an ordinary directory but a background process rewrites it,
which produces conflicted-copy files and dropped writes. If someone reports the
ledger losing entries or spawning duplicates with "(conflicted copy)" in the
name, that is the cause: move them from `folder` pointed at a synced path to
`sharepoint` through the connector, or to an unsynced local folder.

## Step 2: Pull the window

| Need | Tool | Notes |
|---|---|---|
| Meetings in range | Your notetaker's list/search call (e.g. Granola `list_meetings`, Fireflies `fireflies_get_transcripts`) | Start here to see what exists |
| Ready-made action items | Fireflies `fireflies_get_summary` | Its `action_items` field is already attributed by person. Use it as the primary candidate source where available: far cheaper than reading transcripts, and it commonly catches 1:1 commitments a group-notes tool files as group actions |
| What the primary source missed | Granola `query_granola_meetings` with `document_ids`, or your source's equivalent | Ask for one person's own commitments, with quotes. Better for calls where the verbatim matters |
| Attendees | Your notetaker's speaker list | The only reliable signal of who actually talked |

Default lookback is 7 days. Overlap between runs is expected and free: the
ledger is idempotent, so a wider window costs tokens and nothing else.

If more than one source captures the same call, they will disagree more than
you would expect. Pass both extractions through rather than choosing; the
ledger merges genuine duplicates and keeps the rest.

**Skip private meetings:** therapy, medical, coaching, interviews, and anything
in the config's `exclude_meetings`. Solo-participant meetings are private by
default. When a meeting looks personal but you are unsure, leave it out and say
you skipped it rather than mining it.

## Step 3: Extract commitments, not topics

This is where a 142-item list comes from. Discipline here is the whole job.

**Include** a first-person commitment by the owner or their aliases, or a task
handed to them by name and not refused:

- "I'll send them the deck" → yes, `high`
- "Let me look at that and come back to you" → yes, `medium`, vague but owed
- "Can you call the account?" / "Yep" → yes, `high`
- "I could probably take a look at that sometime" → yes, `low`
- "Somebody should fix the clips" → no, unowned
- "We need to think about attribution" → no, a topic
- "I sent that yesterday" → no, that is completion evidence, see Step 5

Set `confidence` to what the transcript supports. Low-confidence items are held
in a separate block
rather than dropped, so the person can promote or bin them. Guessing high is
how the list becomes noise; guessing low on everything is how it becomes
useless.

**Separate stated deadlines from inferred ones:** `due` is a date someone
actually said. `due_implied` is one you worked out from context, such as a
commitment needed before a meeting on the calendar. An inferred date ranks
lower and is labeled as inferred. Never put a guess in `due`.

```json
[{"text":"send the board deck","owner":"[owner alias]","meeting":"Board Prep",
  "meeting_date":"2026-08-24","source":"fireflies","promised_to":"[Name]",
  "requested_by":"[Name]","external":true,"category":"board",
  "due":"2026-08-28","due_implied":null,"confidence":"high",
  "quote":"I'll get the deck over before Friday",
  "deep_link":"https://app.fireflies.ai/view/01M0DV…?t=441"}]
```

`text` is a short imperative rewrite. `quote` is verbatim so a disputed item can
be checked against what was said. `deep_link` jumps to that moment in the
recording, which is what makes an item verifiable in one click. Fireflies gives
you `https://app.fireflies.ai/view/{id}?t={seconds}` for free; use it. If your
source has an equivalent timestamped link, carry it the same way.

```bash
python3 "$LEDGER" --root "$STORE" add --file candidates.json --owner [owner alias]
```

The report distinguishes `new`, `reaffirmed` (said again, bumped not
duplicated), `near_duplicate` (same commitment caught twice), `reopened`
(promised again after a close), and `suppressed_already_done`. Report those
counts. "23 in, 0 new" is what builds trust that it is not re-listing
everything.

## Step 4: Absorb ticks made elsewhere

If anything else can mark items done, fold that in before you show a list:

```bash
python3 "$LEDGER" --root "$STORE" merge-state --consume
```

This reads `<store>/state-inbox/*.json`, a drop-folder pattern any dashboard or
companion app can write to. On a mount that forbids deletes, files are marked
processed instead; re-running is safe either way.

## Step 5: Check the open items for evidence they are done

```bash
python3 "$LEDGER" --root "$STORE" list --status open
```

| Evidence | Where | Strength |
|---|---|---|
| Person says so | This conversation | Conclusive |
| Matching task completed | Your task tool (e.g. Asana) | Strong |
| Matching message in Sent | Mail connector | Strong, if recipient and timing both match |
| Matching Slack/Teams message | `from:` the person, after the commitment date | Strong |
| Said in past tense later | A transcript after the commitment date | Good |
| Deliverable exists | A file created after the date in your document store | Weak on its own |

**Searching sent mail (Outlook):** do not use `folderName: "Sent Items"`. That
lookup returns NOT_FOUND in live use even when the folder exists. Use
`outlook_email_search` with `sender:` set to the person's address, or
`recipient:` set to who they promised. Keep `limit` at 25 or below; higher has
overflowed the token budget in practice. On Gmail, search `from:` or `to:` the
relevant address over the same window.

```bash
python3 "$LEDGER" --root "$STORE" close \
  --id b8393c2b8558 --evidence "Sent mail: to [Name] 2026-08-26"
```

Use `--status dropped` for something overtaken rather than completed. Both stop
it resurfacing; only `done` claims it happened.

**Do not close on a weak match, and never close on an empty search:** finding no
sent mail is the normal result, not proof. A wrongly closed item disappears in
silence, which is worse than one extra line on a list. When a match is plausible
but unproven, leave it open and mark it "possibly done" in the reply.

Then age out the rest:

```bash
python3 "$LEDGER" --root "$STORE" sweep --days 30
```

Untouched for a month stops crowding the list but stays in the ledger under
"gone quiet", so nobody declares bankruptcy by hand.

## Step 6: Render and deliver

```bash
python3 "$LEDGER" --root "$STORE" render
```

Markdown always, HTML if the config names one. Both are derived views,
regenerated whole, safe to overwrite. **Never hand-edit them and never append to
them directly.** Every durable fact belongs in the ledger.

If the config sets `dashboard_export: true`, also run `export`, which writes a
`meeting-actions.json` in a plain shape any dashboard can read without knowing
this ledger exists:

```bash
python3 "$LEDGER" --root "$STORE" export --out <dashboard-data-dir>/meeting-actions.json
```

Lead the chat reply with the count line, then the list:

```
Swept 9 meetings, Aug 20–27. 23 commitments seen, 0 new, 3 closed on evidence, 20 open.
```

## Setup: the first-run interview

Ask these in one pass, with a recommendation attached to each. Do not ask
anything you can detect yourself.

1. **Where should this live?** Check what is connected first and lead with it.
   A connected workspace folder is the default and the simplest. Offer
   SharePoint (or your equivalent document store) for someone who works across
   machines or has no folder connected, and Asana (or your task tool) for
   someone who wants commitments to become real tasks. Say plainly that a task
   backend means bad extractions become real tasks too.
2. **What are your categories?** Offer a starting set based on their role and
   let them edit. This is the thing people most want to change.
3. **Which meetings should never be swept?** Seed from recurring titles you can
   see. Confirm that solo meetings are excluded by default.
4. **How many items do you want to see?** Default 10.
5. **When should it run, and where should the result land?** Chat, a file, a
   direct message to themselves, or an artifact/dashboard. Then offer to create
   the scheduled task with the `schedule` skill, using a prompt that names this
   skill, because a scheduled run starts with no conversation context and will
   not find the logic otherwise.

Write the config, run one sweep immediately so they see real output, and only
then offer the schedule. A person who has seen it work once will keep it; a
person handed a cron job will not.

## Rules

- Propose, never execute. No task created, no mail sent, no item closed on your
  own judgment without saying so in the same reply.
- Never invent a commitment, a promisee, or a date. "Said, but no owner and no
  date" is a real finding.
- The ledger is the only state. If a rendered file and the ledger disagree, the
  ledger is right and the file is stale.
- Cap the output. A list nobody reads is the failure mode this exists to fix.
- Private meetings stay out. Health, compensation, and performance items that do
  surface are shown to the owner only, never pushed to a shared channel or a
  published artifact.
- Transcripts carry sensitive and third-party content. The ledger stays in the
  person's own store. Do not paste commitment text into a third-party tool that
  was not already the source.

## Do not use this skill for

- Writing up one meeting that just ended: ask for a debrief and recap directly, there is no separate skill for it
- Triaging today's inbox and calendar → `daily-briefing`
- Building a leadership team agenda → `weekly-agenda`
- Building or fixing a personal dashboard → your own dashboard-building skill, if you have one
