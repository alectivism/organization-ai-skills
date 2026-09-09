<!-- no-lint -->
# FAQ, from the questions actually asked

Every question in this file was asked out loud by staff on a recent all-hands
call, in their words. Where the answer given on the call was weak or missing, that is
noted and a real answer is written out. Use these answers; they are the ones people
needed and did not always get.

---

## "Where is this vault actually stored?"

Asked by one attendee, who added that their "security brain clicks in."

A folder on their own Mac. That is all a vault is. Nobody at the org can see it, there is no
admin view, and nothing is uploaded anywhere by Obsidian.

If they put that folder inside iCloud Drive, OneDrive, or Dropbox, then it syncs the way
any folder in those places syncs, with the same access rules those already have. That is
their choice and it is a good one for backup. If they keep it in `~/Notes` it never
leaves the machine, and it is also not backed up, so say that.

Obsidian sells its own sync service. Nobody needs it to start.

---

## "What does this do that the local storage is not doing?"

Asked by one attendee. The CEO called it the question underlying everything, and
**it never got a real answer on the call.** Do not repeat that. The answer:

Nothing, if all they want is somewhere to put files. A vault *is* a folder of files.
Obsidian adds four specific things on top of that folder:

1. **Search across every note at once**, including the body text, in one box. Finder
   search over a nest of folders is slower and misses content inside files.
2. **Links between notes that work in both directions.** Open a note and see everything
   that points at it. A folder cannot tell you what refers to what.
3. **A jump-to-note box** so they never navigate a folder tree again.
4. **Plain text that an AI can read without an API.** Claude reads markdown off the disk.
   No connector, no export, no upload.

And the honest limit: if they have thirty notes, they will not feel any of this. It pays
off at a few hundred. Say that rather than overselling.

---

## "What does this replace that I'm already using?"

Asked by one attendee. Also never answered on the call.

Usually nothing, and that is the honest answer. It is not a replacement for Granola,
which records meetings, or for Asana, which tracks tasks, or for Excel, which holds the
opportunity pipeline. Those keep doing their jobs.

What it replaces is the pile: the notes currently spread across Apple Notes, downloads,
desktop, and files Claude wrote somewhere. It becomes the one place those land so they
can be found later and read by an AI.

If someone already has a system that works, the correct advice is to leave it alone.

---

## "Is Obsidian a level up from that, that then is conversational with you?"

Asked by one attendee.

No. Obsidian by itself is not conversational at all. It is a window onto a folder of
text files.

The conversation comes from Claude, pointed at that same folder. Which is why the next
question matters so much.

---

## "I can't connect Claude to Obsidian. Has anyone managed that?"

Asked by one attendee, and the confusion that took longest to clear on the whole call.
They needed two passes.

**There is nothing to connect.** No connector, no MCP, no integration, no plugin. Both
programs read files from the same folder on the disk.

Make it concrete rather than explaining it twice:

> "Point Claude Cowork at the folder `/Users/you/Notes`. Now open that same folder as
> your Obsidian vault. Write a note in Obsidian, then ask Claude about it. It can read
> it, because it is the same folder."

Claude Cowork (or an equivalent AI agent) can also watch several folders at once, which was news to people and
landed well. The vault and a working project folder do not have to be the same folder.

---

## "Does everybody even know what an Obsidian vault is?"

Asked by one attendee, polling the room. Several people said no, including someone who
had looked it up mid-call and someone for whom English is a second language.

Assume the answer is no. Start from "it is a folder" every time, in plain words, and
avoid: vault, PKM, second brain, frontmatter, YAML, wikilink, graph. Say folder, note,
search, link.

---

## "Does this make us more efficient on token usage, or jack it up because it's looking through our vault every time?"

Asked by one attendee. Answered vaguely on the call.

A better answer: Claude does not read the whole vault. It searches for the files that
match, then reads those. So cost scales with what it opens, not with vault size. Reading
local markdown is cheaper and faster than calling out to a hosted tool for the same
content.

If they want it tighter than that, the honest answer is that it depends on how the
question is asked, and the way to keep it small is a vault of many small notes rather
than a few enormous ones.

---

## "Do you have to sign up with an email and a password?"

**No.** Download and use it. No account.

This was asked on the call, answered with uncertainty, then corrected by another
attendee. Get it right the first time.

---

## "Which one do I download? Some of these say they aren't for Mac."

Asked by two attendees separately. There are lookalikes in search results.

`obsidian.md`, the desktop app, macOS. Not a browser tab, not an App Store lookalike.
Free.

---

## "Is there an instruction guide? It's asking whether I want a new vault or to open a folder as a vault."

Asked by one attendee, the most useful bug report of the call.

**Open folder as a vault**, then pick their folder. "Create new vault" is for starting
empty, which is only right if they have no notes anywhere. It asks once.

Skip the Obsidian Sync prompt. That is the paid service and it is not needed.

---

## "It says it doesn't have something in a certain folder named a certain way. Is it set up to read very specific locations and file names?"

Asked by the same attendee. It was, and that was the bug this skill was rewritten to remove.

Nothing in the current version needs a particular folder name, path, cloud mount, or
company folder. If a message like this still appears, the machine has an old copy of the
skill. Nothing here should ever ask anyone to put their notes in a company folder.

---

## "I typed the skill and it gave me more errors than I can imagine."

One attendee, running the previous version.

Run `vault.py check` and read what it reports rather than guessing. It changes nothing
and prints exactly what is and is not set up.

---

## "It started configuring and talking to me in Portuguese by itself."

Reported on the call.

Match the language the person is writing in and say so plainly. If someone
prefers Portuguese or Spanish, run the whole session in it, including the folder names
if they want.

---

## "Instead of going off and doing it on our own, could I watch you work with somebody?"

One attendee. Worth honoring rather than answering.

Do not hand over a numbered guide. Ask one question, wait, do one step, show the result.
People who wanted to watch a build will follow a conversation and will abandon a manual.

---

## "Lots of people work on the same document at the same time. How does that work if there's a source of truth?"

One attendee, framed as a logistics question about board documents.

A personal vault is not for live collaborative editing, and Obsidian is bad at it.
Documents several people revise at once belong in Word or Google Docs.

A vault is for notes one person owns, and for finished documents kept for reference
after they stop changing.

---

## "Is this an intranet?"

One attendee's framing, which the CEO then picked up.

Not for this skill. What this sets up is one person's own notes on their own machine. A
shared company knowledge base is a separate thing and does not exist yet. If someone
asks about it, say that plainly rather than blurring the two, because blurring them is
what confused the room.

---

## "Do I have to do this?"

The switching cost is real, and pretending otherwise loses people. Anyone with a system
that works should keep it. Someone who has cycled through several note apps and gone
back to paper has learned something true about themselves, and the right answer may be
that a vault is only for the things Claude writes for them.

The lowest-value version of this is still useful: one folder, everything lands there,
Claude can read it. That alone beats notes scattered across four apps.
