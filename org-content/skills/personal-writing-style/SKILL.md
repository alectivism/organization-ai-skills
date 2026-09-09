---
name: personal-writing-style
description: Draft and revise emails, Slack messages, replies, memos, and personal posts in the individual sender's own voice, and strip AI tells from personal prose. The sender's own writing skill, style file, samples, and stated preferences are the authority; this skill fills gaps and supplies defaults only when no personal source exists. Not an organizational style guide. Do not load the organizational brand-voice guide for person-to-person writing.
status: ready
---

# Personal writing style

Write as the sender, not as this skill. Everything below is a fallback that yields to anything more specific about how that person actually writes.

## Whose voice wins

Use the strongest person-specific evidence available, in this order:

1. The user's instructions for this draft
2. A maintained personal writing skill, voice profile, or style file for that sender
3. The sender's real writing samples, saved preferences, and personal templates
4. The current thread, audience, relationship, and channel
5. The defaults in this skill

Within a level, prefer the source that is explicitly named, confirmed by the sender, more recent, and closer to the current channel. Ask only when a conflict would change the draft.

When a personal writing skill or style file exists, it is the voice authority. Use this skill only for what that source leaves open: task framing, channel structure, factual discipline, final checks. Preserve its wording, rhythm, punctuation, warmth, and formatting. Do not build a competing profile and do not quietly move the sender toward the defaults below. If the two disagree, the personal source wins and no explanation is needed.

## Do not load the organizational brand-voice guide

The `brand-voice` template skill (if installed) is the voice of your organization as an institution. It is not evidence of how any person writes.

Do not open it because the plugin is installed, because the draft mentions the organization's name, or because a search for "writing style" returns it. Open it only when the user asks for official organizational voice, or the deliverable speaks for the organization as a whole (report, press release, campaign, org-wide announcement).

Naming is the exception, and it does not require reading that skill: apply your organization's naming convention (typically full name on first mention, then the short form or acronym, per whatever the `org-context` or `brand-voice` skill states). If no such skill is installed, use whatever form the sender themselves already uses. Apply the convention, keep the sender's tone.

## Find the sender's voice

Check, in this order, and stop at the first real source:

- Instructions in the current prompt or thread
- Project or user instruction files (`CLAUDE.md`, `AGENTS.md`, and the like)
- A personal skill in the available skill list, usually named for the person or something like `writing-style`, `my-voice`, `<name>-style`
- Stored memory or preferences about how this person writes
- The sender's own earlier messages in this thread, or samples they paste

Do not adopt a source because its name contains "writing style". Confirm it describes this sender.

From samples, extract things you can check rather than adjectives:

- Typical sentence length, and whether it varies
- Greeting and sign-off, copied verbatim
- Contractions, sentence case or lowercase, emoji, exclamation points
- How they ask for something, disagree, and admit uncertainty
- Words and constructions they repeat, and ones they never use

When there is no personal source, say so in one line, draft with the defaults below, and offer to capture their preferences once. Do not stall the draft to run an interview.

## Workflow

1. Identify artifact, sender, audience, relationship, purpose, and the action requested.
2. Separate confirmed facts from assumptions. Never invent status, deadlines, agreement, availability, budget, or commitments on the sender's behalf. Mark anything you had to guess.
3. Apply the sender's primary voice source.
4. Draft one strong version. Offer alternatives only when a different tone would change the outcome.
5. Strip the AI tells below.
6. Compare against the sender's source and cut anything they would not say.
7. Run the linter, or apply the mechanical list by hand when there is no shell.

## Defaults when no personal source exists

- Start with the point, request, or decision.
- Sound like a specific person talking to another person.
- Vary sentence length. Keep paragraphs short.
- Use "I" for ownership and "you" for the ask.
- Use contractions when the relationship allows.
- Plain verbs, concrete nouns, real numbers and names.
- State uncertainty directly instead of hedging around it.
- Say the true thing rather than the comfortable one. Correct a wrong premise when it matters.
- Cut throat-clearing, restated conclusions, and ceremonial politeness. Keep context that the reader needs.
- No corporate voice, slogans, motivational filler, or generic praise.
- No em dashes. Use a comma, period, colon, or parentheses.

Skip canned openings ("I hope you're well", "I wanted to reach out", "Great question") and canned closings ("I hope this helps", a summary that repeats the message) unless the sender demonstrably uses them.

### By channel

- **Email** — specific, action-oriented subject; first sentence says why they are getting this; bullets only for three or more scannable items; end on the exact request, decision, or next step; match the sender's normal sign-off and never invent one.
- **Slack or Teams** — one compact paragraph, or a short lead plus bullets. No email greeting or sign-off. Name the owner and the ask. Informal without going vague.
- **Memo or internal note** — conclusion first, then facts, interpretation, decisions, and open questions kept apart. Headings only when they aid navigation.
- **Personal post** — open on the observation or argument, grounded in the person's own experience. No engagement bait, no inspirational filler, no company tagline voice.

## AI tells to strip

These apply to every draft, including one written in a strong personal voice. They are about machine texture, not taste.

### Mechanical

The linter catches these. Apply them by hand when no shell is available.

- **Em dashes** — zero in flowing prose, in either the long-dash or the double-hyphen form. One per line is allowed as a separator in a list item or heading, as in this bullet. En dashes only in tight ranges (`2024–2026`).
- **Always-replace words** — delve, leverage, landscape, tapestry, realm, robust, comprehensive, seamless, cutting-edge, pivotal, crucial, underscore, unveil, harness, foster, streamline, empower, utilize, synergy, game-changer, unlock, unleash, boast, testament, elevate, spearhead, and their inflected forms. Use the plain word: utilize to use, facilitate to help, foster to encourage, streamline to simplify, underscore to highlight, unveil to reveal.
- **Empty intensifiers** — very, really, extremely, incredibly, significantly, truly, world-class. Cut them or replace with a fact.
- **Candor markers** — honestly, frankly, candidly, "to be honest". State the point without announcing its sincerity.
- **Copy-paste fingerprints** — "I hope this helps", "Certainly!", "Great question", "As an AI", citation artifacts (`citeturn`, `oai_citation`, `contentReference`), AI-tool UTM parameters in links, unfilled placeholders (`[Your Name]`, `[INSERT ...]`), "as of my last update".
- **List labels take a colon, not a period** — `**Owner:** Priya`, never `**Owner.** Priya`.

### Structural

These give AI away more reliably than word choice, and no linter catches them.

- **False agency** — "the data tells us", "the decision emerges", "the market rewards". Name the person who acts, or use "you".
- **The antithesis family** — "It's not X, it's Y", "This isn't about X, it's about Y", "not just X but also Y", "no X, just Y". State Y. One contrast per piece at most.
- **Negative listing** — "Not a tool. Not a feature. A platform." Say what it is.
- **False ranges** — "from the boardroom to the codebase", "from startups to the Fortune 500". Name the real scope.
- **Stacked hedges** — "could potentially", "may eventually", "might ultimately". Pick one hedge or commit.
- **Inflation words** — "real value", "genuine traction", "actual results", with no named contrast.
- **Narrative closers** — "as we move forward", "only time will tell", "is poised to become". End on a next step or a claim that can be checked.
- **Self-labeled significance** — "the interesting part", "here's the key insight". If it is, the content shows it.
- **Throat-clearing and hooks** — "Here's the thing", "The truth is", "Let's be clear", "So why does this matter?". Cut and state the point.
- **Rule of three** — repeated three-item lists and "adj, adj, and adj" triads. Vary the grouping.
- **Symmetric bullet lists** — five verbless items of near-identical length read as machine organizing. Turn them into sentences or into claims someone could check.
- **Over-structuring** — headings every few lines, or formulaic ones (Overview, Key Points, Takeaways). In a message, usually no headings at all.

## Run the linter

- **Claude Code** — `python3 "${CLAUDE_PLUGIN_ROOT}/skills/personal-writing-style/scripts/lint.py" <draft-file>`
- **Codex or any shell without that variable** — resolve `scripts/lint.py` relative to this skill's own directory.
- **No shell (plain chat, mobile, web)** — apply the mechanical list above by hand. That list is complete; the script only automates it.

Flags: `--stdin` for piped text, `--strict` to reject every em dash including list separators, `--allow-em-dashes` when the sender's established style genuinely uses them (a confirmed personal pattern outranks the default).

The script is self-contained and loads no organization voice guide. Fix every hit, or state why a hit is a real feature of that person's writing.

### Extending the banned-word list

`scripts/lint.py` ships with a generic, non-org-specific set of AI-tell words (see `ALWAYS`, `INTENS`, and `CANDOR` in the script). If your organization has its own house-style banned terms (jargon, clichés specific to your industry, words your organization has decided never to use), do not edit the script. Instead maintain them in the `brand-voice` template skill's "Terms to Avoid" section and check a draft against both: the linter for the generic AI tells, the `brand-voice` list by hand or with a small wrapper script for organization-specific terms.

## Before returning

1. Every mechanical hit fixed or justified.
2. Structural tells hunted specifically, not skimmed for.
3. Read it aloud. Three same-length sentences in a row means break one.
4. Cut test: if 30% can go with nothing lost, it is restating itself.
5. Nothing asserted that was not confirmed. No invented commitments.
6. It sounds like this sender, not like a well-written message from nobody.

**Do not over-polish:** applying every rule at full strength produces the same sanded, uniform texture you are trying to avoid, and it erases the sender. Real people repeat themselves a little, start sentences with "and", and have habits. Keep them. A draft that fails one rule but sounds like the person beats a clean one that does not.

## Building a reusable profile

When the user wants their voice captured for reuse, use [references/voice-profile-template.md](references/voice-profile-template.md). Derive every entry from real examples and label inferences as provisional until confirmed.

If a maintained personal skill or profile already exists, add to it. Do not create a second one.

The durable version of this is the user's own skill, not a profile file. Once preferences are confirmed, offer to write them to a personal skill (in Claude Code, `~/.claude/skills/<name>-writing-style/SKILL.md`) or to their user instructions file. Do not save, commit, or modify anything in memory or a shared workspace unless they ask.

## Safety

- Keep private analysis separate from recipient-facing text.
- Never expose credentials, personal data, member data, financials, or contract terms. Use a placeholder when a sensitive detail is not needed.
- Draft only. Do not send, post, publish, or update an external system without explicit approval.

### Clipped fragments (the loudest tell)

Do not write two short sentences where one belongs. This pattern is banned:

- "Eight pages. Two ways in."
- "Not a feature. A hook."
- "One source. Two doors."
- "It works. Mostly."

Two or more consecutive sentences of four words or fewer, used for punch. It reads as
machine-written to anyone who has spent time around AI output, and it is the single
most recognisable tell in Claude's default voice.

Join them, or pick one:

| Instead of | Write |
|---|---|
| "Eight pages. Two ways in." | "Eight pages, and two ways to read them" |
| "Not a feature. A hook." | "It is a hook rather than a feature" |
| "One source. Two doors." | "One source, read through two doors" |

Applies to slide titles and headings as much as to prose, and headings are where it
shows up most. `lint.py` flags it as "clipped fragments" and blocks on it.

A single short sentence is fine. Two in a row is the problem, and three is a
signature.
