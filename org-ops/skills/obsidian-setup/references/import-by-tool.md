<!-- no-lint -->
# Getting existing notes in, by whatever they use now

Ask "what do you use for notes today?" first, then find them below. The tools in this
file are the ones staff actually named on a recent all-hands call, in roughly the order
they came up. Do not lead with Evernote; one person uses it.

Two rules for every path here:

- **Import into a named subfolder**, never loose into the vault root. `Imported from
  Apple Notes/` is obvious later and trivial to delete if the import lands badly.
- **The original is never touched.** Say this out loud before starting. Their account
  keeps everything.

Do one notebook or one folder first. Look at it together. Then do the rest.

---

## "Nothing", or "I just let Claude dump things somewhere"

The most common real answer, and not a problem to solve first.

Make a folder, make it the vault, done. `~/Notes` is fine. Then point Claude Cowork (or
an equivalent AI agent) at
that same folder so anything it writes from now on lands in the vault by default. That
single change is most of the value for this person, and it takes a minute.

Do not make them go and find historic notes. There may not be any.

---

## Granola

Named by more people than anything else, for meeting notes.

Granola holds its notes in its own app, so this is an export, not a live connection.
Export the meetings worth keeping as markdown and drop them in `Meetings/`.

Do not try to export a year of meetings on day one. Ask which meetings they ever go back
to. Usually the answer is a handful: board meetings, member calls, one-on-ones. Take
those.

Going forward, the higher-value habit is asking Claude to write the meeting summary into
the vault folder rather than exporting from Granola afterwards.

---

## Apple Notes

Obsidian's own Importer plugin reads Apple Notes directly on macOS. No export step.

1. Obsidian, **Settings > Community plugins**, browse for **Importer**, install, enable.
2. Command palette, **Importer: Open importer**.
3. Pick **Apple Notes**, choose an output folder, run it.

It asks permission to read Notes. Expect formatting to come through roughly. Text and
structure survive.

---

## Notion

Workspace **Export**, choose *Markdown & CSV*, unzip, then Importer, or just copy the
unzipped folder in.

Warn them first: Notion's export nests folders deeply and mangles some link formats.
Expect to tidy, or expect to leave it messy and rely on search. Both are acceptable.

Databases come out as CSV and do not become notes. If a Notion database is doing real
work for them, leave it in Notion.

---

## Otter, Fireflies, or any transcription tool

Same shape as Granola. These produce a lot of low-value text, so be selective on
purpose. A folder of 300 raw transcripts makes search worse, not better.

Ask what they actually reuse. Usually it is a synthesis they wrote from several calls,
not the calls. Import those, and skip the raw transcripts unless there is a reason.

---

## A running Excel or Google Sheet

Named on the call as the file tracking open opportunities.

**Leave it alone.** A spreadsheet that people update is doing a job markdown does badly.
Do not convert it.

If they want it readable by Claude alongtheir notes, drop a copy of the file in the
vault, or a short note that says what the sheet is and where it lives. Obsidian will not
render it usefully, and that is fine.

---

## Word documents and PDFs

Copy them into the vault. Obsidian lists them, opens PDFs, and search finds them by
filename. It does not index text inside a PDF.

Claude can read both, which is the actual reason to put them there.

---

## OneNote

Importer signs in to Microsoft and pulls sections directly. No manual export.

---

## Evernote

One person on the team uses this, so do not lead with it.

Select notebooks, **Export** to `.enex`, then Importer. Export notebook by notebook for a
large account rather than everything at once.

An official Evernote MCP server is announced but not generally available. As of
[DATE], re-check before relying on this: Evernote's own documentation and
third-party coverage both describe it as in development with a waitlist. Community
servers exist but need a gated API key. So the import path is the only actionable one
today.

---

## Google Keep

Google Takeout, select Keep. Comes out as HTML plus JSON, which Importer handles.

---

## Paper notebooks

Said on the call, and worth taking seriously rather than treating as a joke. Someone who
has tried several apps and gone back to paper has learned something real.

Do not try to convert the notebooks. The useful move is a single note in the vault for
the handful of things they keep re-deriving, typed once. If they would rather keep paper
for thinking and use the vault only for what Claude produces, that is a good outcome, not
a failure.

---

## Roam, Bear, Craft, Logseq

Export to markdown, copy the folder in. These are already markdown underneath, so they
land cleanly.

---

## The hard rule, whatever the source

**Personal notes stay personal.** The vault is on their machine. Nothing here uploads,
copies, or syncs anyone's notes to the org, and no step should ever ask them to put personal
notes in a company folder.

If a request starts to sound like bulk-importing someone's personal vault into a shared
company location, that is the wrong shape. Say so rather than finding a way to do it.
