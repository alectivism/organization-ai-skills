---
name: weekly-agenda
description: Sweep the past week across meetings, email, and chat, then force-rank the 5 to 10 topics a leadership team actually needs to discuss. Use when asked to prep for a leadership or team meeting, build an agenda, work out what to raise, or "prep me for Monday". Adapts to whichever meeting, mail, and chat tools are connected. For a personal inbox and calendar triage rather than a team agenda, use daily-briefing instead.
status: ready
---

# Weekly Agenda

Most agendas are a list of everything that happened. A useful agenda is a short, ranked list of what the group has to resolve together. Five strong items beat ten mediocre ones, so the cutting is the work.

## Step 0: Establish whose leadership team this is

An organization is rarely one flat hierarchy. A holding company, a federation of regions, or a matrix of functions and programs each has its own reporting lines, and "the leadership team" means something different depending on who is asking.

Work out the scope before gathering anything. Adjust these to your own structure:

- **A regional or business-unit leader:** the agenda is local to that unit. Group-wide items appear only where they land on the unit.
- **A global function lead:** the agenda spans units, and unit leaders are stakeholders to be briefed or consulted, not direct reports.
- **A program or initiative lead:** the agenda is the program's, and the "leadership team" is its steering group.

**Do not hardcode a roster, and do not guess one.** Find the actual attendees: pull the recurring leadership meeting from the calendar and read its invitee list, or use the `org-context` template skill and whatever staff directory or reporting-line reference your organization keeps. If you still cannot tell, ask who is in the room. An agenda aimed at the wrong group is worse than no agenda.

## Step 1: Gather, using whatever is connected

Check your available tools first. Use what exists; name what you could not reach rather than silently skipping it.

| Source | Try, in this order | Why it matters |
|---|---|---|
| Last meeting's notes | Your meeting-notes tool (e.g. Granola, Fireflies) | Carry-forward items and anything tabled |
| This week's meetings | Meeting-notes tool, then calendar | Where decisions actually got made |
| Sent mail, past 7 days | Your mail connector (Outlook, Gmail) | Escalations and external commitments |
| Chat | Slack, then Teams | Cross-functional threads with real disagreement |

If more than one meeting-notes tool is connected, they often hold the same meeting: prefer the one with the richer content for what was said, and the one with a reliable speaker list for who was present. Skip social channels and one-line exchanges; they generate noise, not agenda items.

## Step 2: Extract candidates

Pull 15 to 25 raw candidates. For each: the topic, its source, which functions or regions it touches, and whether it is carried forward from last time. Over-collect here. The ranking step is where you get strict.

## Step 3: Filter, then score, then cut

**Drop outright:** anything touching one function only, anything already resolved, generic status updates, and anything that is properly an HR or legal matter for a different forum.

**Score what survives, 1 to 5 on each:**

- **Reach:** how many functions or regions it touches
- **Urgency:** does a real deadline force a decision this week
- **Impact:** what changes if the group gets it right or wrong
- **Tension:** is there genuine unresolved disagreement

Tension is the one people under-weight. A topic everybody already agrees on does not need a meeting; send a note instead.

Force-rank and cut to 5 to 10. If two items are close, keep the one with a deadline.

## Step 4: Format

```
**Sources scanned:** [what you actually reached, and what you could not]

## 1. [Topic]
**Treatment:** discuss / decide / inform / follow-up
**Involves:** [functions, regions, or named people]
**Source:** [where this came from]
**Flags:** [carry-forward, deadline, cross-cutting]
**Why it matters:** [one or two sentences, ending on something concrete]
**Suggested framing:** [the question to put to the room]

...

## Below the cut
[items that scored well but did not make it, one line each, so nothing is silently dropped]

## Better as a 1:1
[items that concern two people rather than the group]
```

## Rules

- Every item traces to a real source. Never invent a topic because the agenda looks short. A four-item agenda is a valid outcome.
- Force-rank properly. Refusing to order them puts the cutting back on the person who asked.
- "Suggested framing" is a question, not a title. "Do we fund the second initiative this quarter or defer to next" beats "Funding".
- Say what you could not see. An agenda built only from calendar entries because no transcript tool was connected must say so at the top.
- Propose only. Do not send the agenda, create calendar items, or message attendees without being asked.

## Do not use this skill for

- A personal daily inbox-and-calendar triage → `daily-briefing`
- Tracking what one person promised across meetings over time → `meeting-commitments`
- Prep for one specific upcoming meeting → `briefing-prep`
