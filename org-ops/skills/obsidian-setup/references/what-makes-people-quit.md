<!-- no-lint -->
# What makes people quit, and the AI rules

From 16 r/ObsidianMD threads read with comments, plus web research, August 2026.
Practitioner reports rather than vendor material. Where something rests on a single
source it says so.

## The six things that cause abandonment

In the order they show up in the threads.

1. **Building a folder structure before there are notes that need one.** The single
   most repeated failure story. "Folders cannot solve a problem you do not have
   yet." Start flat. Let structure appear when the absence of it hurts.
2. **Installing plugins in week one.** Every plugin should answer a problem the
   person has actually hit. A default install does everything a beginner needs.
3. **Pasting instead of writing.** "A collection of pasted excerpts is a digital
   scrapbook, not a knowledge base." The value comes from having to put it in your
   own words, not from the storage.
4. **Adopting a named method.** PARA, Zettelkasten, and the rest are oversold, and
   over-engineering before content exists is where people stall. Do not teach one.
5. **Judging it in week two.** Linking starts paying off somewhere around 80 to 150
   notes, and most quitting happens before that. **Say this out loud during setup.**
   Someone who expects the payoff at note 15 concludes the tool is useless.
6. **Copying somebody else's finished vault.** Close to consensus that it does not
   take, because the structure has to match how that person thinks.

## The four causes that show up in non-technical write-ups

The six above come from practitioners in the subreddit. Web write-ups aimed at
non-technical users converge on a different and complementary four. Worth knowing
because the org's staff are mostly in this second group.

1. **Terminology overload.** YAML front matter, regex, CSS snippets. All of it reads
   as "built for somebody else."
2. **No guided onboarding.** An empty vault, unexplained icons, and nothing telling
   you what to do first.
3. **Configuring instead of creating.** Tuning the folder structure repeatedly
   instead of writing anything.
4. **Audience mismatch.** It gets recommended to everyone when it was built for
   writers, researchers, and technical users.

Sources: Unmarkdown, "Obsidian is Too Complicated" (2026); ericmjl.github.io PKM
writeup (March 2026).

**This setup already answers three of the four.** The script seeds a `Start here.md`
orientation note, so nobody meets an empty vault. Teaching
four things in a fixed order holds terminology down. And "ask two questions, set up
one pattern, stop" in [[how-people-work]] is aimed squarely at configuring instead
of creating. The fourth, audience mismatch, is real and cannot be designed away:
some people should be told this tool is not for them.

## What not to teach, and what not to install

- **No named method as the starting structure.** PARA, Zettelkasten, ACCESS. Over
  engineering before content exists is the most repeated failure story in the whole
  dataset.
- **No local-LLM plugin.** Ollama-backed Smart Second Brain, Copilot with local
  models. The support threads are hours of CORS and origin errors and multi-minute
  replies on decent hardware. Not viable live, and not viable inside a twenty-minute
  budget.
- **No open write access to the whole vault on day one.** Quarantine AI output to one
  note type, tag, or inbox folder.
- **Tags are not the organizing system.** Repeated view from advanced users: links do
  the real organizing work, and tags and folders are secondary conveniences. Teaching
  tags first sets up a system people abandon.
- **Do not hand someone a finished template vault to copy.** Close to consensus that
  it does not take, because the structure has to match how that person thinks.
- **Do not lead with "second brain."** Spend the opening on mechanics instead.

## Drop the phrase "second brain"

It is the most contested term in every thread read, and the argument about the term
has nothing to do with whether the tool is useful. "Second brain is a buzzword for
notes. Keep notes. That is all."

Say what it does: a place to write things down so you can find them again.

Sell the mechanism rather than the label. Writing something in your own words and
linking it helps you retain and reuse it. That predates the marketing, and it is
defensible in a way the branding is not.

## A shared vault is not everyone's notes merged

Near-unanimous, and worth knowing because it is the objection the org's shared pages
will attract: **"Your brain is not my brain, your knowledge and my knowledge do not
have the same links."**

People are right to reject a merged personal vault, and nothing here asks them to
accept one. Their vault is private, local, and structured however they like. Nothing in
this skill copies their notes anywhere.

The org has no shared company vault today. If a staff member pictures their notes
landing in a company pool, correct it immediately. And if such a thing is ever built,
describe it as a separate thing from a personal vault: blurring the two is what
confused a room full of people on a recent all-hands call.

## Plugins worth naming, and only these

| Plugin | For | Note |
|---|---|---|
| **Omnisearch** | Fast full-text search across the vault | The one people say they would not go without |
| **Obsidian Git** | Version history as a safety net | Load-bearing for anything an AI touches, see below |
| **Smart Connections** | Surfaces related notes by meaning | The AI use case that gets consistently positive reactions |
| **Templater** | Consistent templates and front matter | Only once someone wants repeatable notes |
| **Bases** | Query notes like a light database | Native now. Only for people who ask for it |

**Do not install or demo a local-LLM plugin.** Smart Second Brain, Ollama-backed
Copilot, and similar cost hours in setup errors and produce multi-minute response
times on decent hardware. Wrong fit for a twenty-minute introduction, and it will
be remembered as the thing that did not work.

## Rules for letting AI near a vault

The threads converge on the same four primitives, and the Weichart AI-native setup
writeup arrived at them independently, which makes this two sources rather than
folklore.

1. **Commit before the AI runs, not after.** Then a review is one diff instead of
   opening ten notes hoping to spot what moved. The best line on this: "the review
   never got faster, the runs got smaller."
2. **Quarantine AI writes** to a declared folder, tag, or note type. Never
   vault-wide write access on day one.
3. **Declare before write.** The agent states which files it intends to touch; a
   write outside that list fails the run rather than getting flagged afterwards.
4. **Tag what the AI wrote** in front matter, so those notes can be filtered and
   spot-checked later.

Worth conceding rather than arguing with: **repeated incremental LLM edits do
corrupt documents.** One commenter cited peer-reviewed work and reported never
seeing an agent make ten sequential edits without damage. Git is the answer, not
vigilance.

## Answering a skeptic honestly

| Objection | The honest answer |
|---|---|
| "It is a buzzword and a course-selling gimmick" | Partly true. The packaged systems are oversold. The underlying mechanism is not |
| "AI organising my notes defeats the purpose" | Correct, if the goal is learning. AI for finding and mechanical chores is fine; AI doing your synthesis is not, because that was the part building your thinking |
| "AI will mangle my notes" | Documented, not paranoia. Which is why git and a declared write-zone come first |
| "This is a privacy risk" | Also correct the moment a cloud model is pointed at it. Obsidian being local is the actual answer, and what may leave the machine has to be a stated rule |
| "Setup will eat my week" | True if you go near a local model. So do not |
| "It will hallucinate about my own notes and I will not catch it, because it is not a fact I can look up" | The strongest objection on this list, and still unsolved in 2026. Use AI to retrieve and draft, never as the source of truth. If it makes a claim about your notes, click through to the note it cites. This is why the setup teaches backlinks and `status` rather than "trust the assistant" |
| "My notes will leak" | A documented risk the moment a cloud model is pointed at them. The answer here is structural: the personal vault is local and never synced to the org, and the shared pages are one-way and read-only. That is a stronger answer than most organizations can give, so say it plainly |
| "AI editing my notes will corrupt them and I will not notice" | Does not apply to this design, and say so: nothing here live-edits a personal vault. AI reaches the shared pages only through a reviewed publish step |

## Demo notes

Backlinks and the quick switcher are the two features that actually land in a live
demo. **Search is the most useful and the least impressive to watch**, so narrate it
("that searched every note instantly") rather than lingering on it.

**Properties do not impress as a note-taking feature**, because they look like a
form. Frame them forward: this is what lets an AI find and filter your notes, and
for shared pages it is how you see who confirmed a fact.

**Graph view is a ten-second moment, not a workflow.** Obsidian's own docs and
long-time users agree: occasional use to spot orphaned notes. Do not oversell it.

## Team sharing, and its ceiling

Obsidian's native sharing works for roughly two to five people with editorial
discipline. Past that it reportedly breaks down: no per-person permissions, no
read-only folders, concurrent-edit conflicts, no audit log, no SSO or offboarding.

**Treat that range as directional.** It comes from a single vendor blog selling an
alternative, so it has an obvious incentive. The pattern technical teams use instead
is a git repository with pull requests, which is what the org's shared pages already do.

## Lines worth using, with attribution

All from r/ObsidianMD unless noted. Attribution matters because these carry weight
as practitioner quotes and lose it as assertions from the org.

- **"Focus on working IN Obsidian, not ON Obsidian."** ("Where can I find someone to
  help build a second brain")
- **"Your brain isn't my brain, your knowledge and my knowledge don't have the same
  links."** ("New to Obsidian, looking for a step-by-step guide"). The single best
  line for defusing the merged-vault fear.
- **"The review never got faster, the runs got smaller."** ("How do you review AI
  changes to your vault?"). The whole case for small AI runs in one sentence.
- **"I don't let it just run wild over my whole vault."** (same thread)
- **"Second brain is a buzzword for notes. Keep notes. That's all."** ("How can I
  treat Obsidian as a second brain")
- **"The rot is inside you. The problem isn't what the computer thinks it is."**
  ("I'm trying to build an AI second brain and I'm losing mine"). Use with care, but
  it is the sharpest version of the point that tooling does not fix thinking.

## Claims in this skill that are not verified

Recorded so nobody treats them as checked:

- **The exact core-plugin ids** (Search, backlinks, properties, graph, templates,
  outline). Not confirmed against Obsidian's own list.
- **The peer-reviewed work on LLMs corrupting documents under repeated incremental
  edits.** Reported by a commenter citing an arXiv paper, not read first-hand.

## The graph-view judgment call

Nothing in this research argues for keeping graph view, and nothing argues against
cutting it. The "overwhelmed by more than a few concepts" and "configuring instead
of creating" findings both point at fewer concepts rather than more, so dropping to
exactly four things is a defensible tightening. The current ten-second version costs
almost nothing either. Treat it as a preference, not a finding.

## Where this came from

Distilled from practitioner research: 16 r/ObsidianMD threads read with comments plus
the Weichart AI-native setup page and other web research, with all 17 source URLs
considered. This file holds the distilled findings; the underlying thread-by-thread
detail and attributed quotes did not all survive the cut.
