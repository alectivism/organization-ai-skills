---
name: factual-accuracy
description: Verify every specific claim against a real source before a deliverable goes out, and spawn a fact-checker subagent when the claim load is heavy. Use whenever producing or editing anything containing a statistic, percentage, dollar figure, price, date, count, attendance number, headcount, name, job title, membership or customer status, quote, restatement of what someone said in email/Slack/a meeting, chart, image, logo, or external link. Also use before any send or publish, when a template has slots that cannot be filled from known sources, when tempted to round or estimate a figure, and when asked "is this accurate", "can we say this", "where did this come from", "check this before I send", or "fact-check this". Applies to proposals, decks, one-pagers, prospect and customer email, letters, Slack replies, spreadsheets, charts, briefs, recaps, and board material. Relax only when explicitly asked for illustrative, sample, or placeholder content.
status: ready
---

# Factual accuracy

Every specific claim in a deliverable traces to a source read in this session: a
file, a tool result, a page actually fetched, a transcript, or the user's own
words in this conversation. Recall is not a source. Being fairly sure is the
exact state in which errors get written confidently.

These documents go to customers, members, partners, or prospects deciding
whether to trust your organization. One invented attendance figure turns the
reader's question from "should I trust this" to "what else in here is wrong."
A gap is fixable. A confident invention is a liability nobody downstream can see.

## Sort every claim before writing it

| State | Test | Action |
|---|---|---|
| **Verified** | Traced to a source opened this session | Write it |
| **Inferred** | Reasoned from verified facts | Write it only with the inference visible in the prose ("their Q3 filing implies"), never as a bare fact |
| **Unknown** | Cannot be traced | Do not write it. Collect it for the gap ask below |

## Check your organization's own sources, never memory

These change, and asserting them from memory is the likeliest way to be wrong in
a way a reader notices.

| Claim | Source |
|---|---|
| Membership/customer status, join and renewal dates | Your own membership or CRM skill, if you have one |
| What a program, tier, or offering includes, what it costs, approved value wording | Your own catalog/offerings skill, if you have one, and any proof-points reference inside it for any number going into customer-facing text |
| Research findings, statistics, positions your organization holds | Your own research skill, if you have one |
| Staff names, titles, teams, events, program structure | The `org-context` template skill, if filled in |
| Acronym expansions | Your organization's own acronym table (in `org-context` or your CLAUDE.md), if one exists |

## When to hand it to a fact-checker

Run the check yourself when the deliverable has four or fewer specific claims and
every source is already open in this session.

Otherwise spawn **`org-fact-checker`** (read-only, returns a verdict, never
edits, ships in the `org-agents` plugin) and wait for its verdict before the
draft goes anywhere. Spawn it when any of these is true:

- Five or more specific claims in the draft
- Any claim whose source has not been opened yet this session
- The deliverable is customer-facing, prospect-facing, or otherwise external
- Numbers were carried across from another document rather than recomputed

When `org-fact-checker` is not installed, spawn a general-purpose subagent with
its model pinned high (not the default) and paste
`references/fact-checker-brief.md` as its instructions: same checks, same
return format.

Escalate to a higher-effort reviewer instead when the send is hard to reverse:
board material, press, pricing, a published research number, or anything going
out under an executive's name.

Give the subagent the draft path, the sources you used, and the list of claims you
could not trace. Its verdict is a report, not an edit: apply the fixes yourself.

A subagent reporting "all verified" is a claim. Spot-check the two claims that
would be most expensive to get wrong before you accept a clean pass.

## Doubt the draft before the gate

Checking your own work confirms what you already believe. For anything
customer-facing, hard to reverse, or resting on a judgment call, put the draft in
front of a reviewer that has none of your reasoning:

1. **Name the decision** in two or three lines: what the draft asserts or
   recommends and why it matters. If that takes longer, it is an intuition, not
   a decision yet.
2. **Hand over only the artifact and the contract:** the draft (or the section)
   and what it must satisfy (audience, facts it must match, what it must not
   claim). Never pass your reasoning or your conclusion; a reviewer who reads
   the justification agrees with it.
3. **Frame the review as an attack:** "Find what is wrong with this. Assume it is
   overconfident. Look for unstated assumptions, a number carried from another
   context, a claim about someone else, a commitment your organization has not
   made." A fact-checker or verifier agent should already be prompted this way.
4. **Reconcile each finding against the text**, in this order: the contract was
   misread (fix the contract first), valid and actionable (fix the draft, run
   again), a trade-off you accept (write it down), noise (note it and tighten
   the contract next time). You remain the editor; do not rubber-stamp.
5. **Stop** when a pass returns only repeated or trivial findings, after three
   passes, or when the person says ship it. Substantive issues after three
   passes go to the person, not a fourth pass.

## Verify, then stop

Verification is a gate, not an invitation to keep working.

- Turn the acceptance conditions into the smallest proof that settles them, and
  run the narrowest check first (the one claim, the one number) before any
  broad sweep.
- Report each check as **pass**, **fail**, **unavailable** (source could not be
  reached), or **blocked** (needs a person). Do not blur unavailable into pass.
- The moment the proof is sufficient, stop. No polish, no cleanup, no "while I
  was in there" edits to a draft that already passed. Anything you touch after
  the pass is unverified again.
- If a check reused an earlier result, say so; a result is reusable only if
  nothing it depended on changed since.
- Report the checks you ran and their outcomes, not a summary that the draft
  "looks good".

## When a claim is Unknown: finish, then ask once

Do not fill the gap with a plausible number, and do not quietly drop the point
either. A silently omitted claim distorts a piece as much as an invented one.

1. Finish everything verified, so the work is as far along as it can be.
2. Collect **all** gaps into a single ask. Six questions at once beats six
   interruptions.
3. Make each one answerable in a line: name the claim, say where you already
   looked, say what would settle it.
4. Hand over the partial draft with the questions attached.

> The proposal is complete except for three things I could not verify. I checked
> the 2025 conference recap deck and the customer roster.
>
> 1. **2025 flagship event attendance:** the recap deck gives registrations
>    (412) but not actual attendance. Do we have the final figure, or should the
>    proposal cite registrations?
> 2. **[Company X] membership/account status:** not in the roster I have, last
>    updated March. Any change?
> 3. **[Executive]'s line on stage:** I have a paraphrase in the recap notes, not
>    their words. Is there a recording?

Ask immediately, before drafting, only when the answer is load-bearing for the
whole piece.

## The rules that catch the most errors

**Numbers:** reproduce at the source's precision. 412 to "over 400" is honest;
412 to "roughly 500" is not. Say what the number counts, since registrations,
attendees, and unique companies are different things. Never combine figures from
different periods or definitions into one total. Do not extrapolate or annualize
unless asked. Carry the as-of date wherever the age of the data changes what it
means.

**Quotes and restatements:** a quotation mark promises the words are exact. If
they are not, drop the marks and paraphrase it plainly. Never attribute a position,
commitment, or opinion to a colleague, customer, or prospect who did not state it:
that version can commit your organization to something. Keep the hedges, because
"we could probably look at Q4" is not "they agreed to Q4." Separate who said a
thing from who was in the room. If a transcript line is unattributed, say so
rather than assigning it to the likeliest speaker.

**Charts:** plot only real points, over the range the data actually covers. Never
pad a series to smooth a trend. Do not pick axis bounds that overstate a change.
Put the source and date next to the chart, because charts get screenshotted away
from the document.

**Images and logos:** do not present an image as depicting an event, person, or
product without knowing that it does: a generic conference photo in a recap
implies it is that event. Never let a generated image stand in for something
real. Do not attach a headshot, name, and title to each other without one source
connecting all three. Never put a company's logo on a customer, sponsor, or
partner slide without confirming the relationship exists and the mark is
cleared, because that is a false claim about someone else.

Longer detail on each, plus the illustrative-content rules:
**`references/claim-types.md`**.

## Where fabrication actually enters

- **A template with an empty slot:** a "Key results" heading manufactures
  pressure to produce key results. An empty section with a question beats a
  filled one that is fiction.
- **The number that would make the argument land:** wanting a stat to exist is
  not evidence that it does.
- **Vague authority standing in for a source:** "industry research shows",
  "studies suggest", "most customers report". If the study cannot be named, the
  claim is not usable. The bundled hook blocks these.
- **Momentum near the end of a long task:** the last fields of a deck get the
  least scrutiny and are where invented specifics cluster.
- **A URL that was never opened:** do not cite a link you did not fetch, and
  never construct a plausible-looking one.
- **Unrequested precise texture:** "founded in 1994", "a 40-person team". Nobody
  asked, and it can be wrong.

In each case, name the gap out loud rather than resolving it privately.

## Provenance without clutter

Track where each claim came from while working. Keep citations out of the
deliverable unless asked, since these documents usually go straight to a
prospect or customer. The point of tracking is to answer "where did this come
from" for any line immediately, without redoing the work. When asked, return a
short list mapping each number, quote, and image to its source and date.

## The gate on outbound content

`scripts/claim-scan.py` can run as a bundled hook on every file write and every
`pbcopy`. It is deterministic and does not know what is true; it knows what
unverified specifics look like.

- **Blocks** on vague-authority phrasing and on placeholder leakage (`[TBD]`,
  `XX%`, `$XX`, and bracketed instructions-to-self).
- **Blocks a `pbcopy`** of a draft carrying two or more specific claims until
  the content has a verification receipt.

After the claims check out, write the receipt, then copy:

```bash
python3 scripts/claim-scan.py --verified draft.md
pbcopy < draft.md
```

Only write the receipt after actually verifying. Writing it to clear the block is
the failure this skill exists to prevent.

Inventory the claims in a file without a hook:

```bash
python3 scripts/claim-scan.py --report draft.md
```

Escape hatches, for genuinely illustrative content: `<!-- facts-checked -->` in
the first three lines of the file, or `FACT_SCAN=0` in the environment.

If your organization has its own named research firms, publications, or
internal source names it wants recognized as a "named source" (which rescues a
sentence from the vague-authority block), add them with the `CLAIM_SCAN_SOURCES`
environment variable (a `|`-separated list of regex alternatives) rather than
editing the script. See the comment above `NAMED_SOURCE` in the script.

## Illustrative content, when it is genuinely wanted

Sample data, placeholder copy, mockups, and hypotheticals are legitimate
requests. Honor them and make the labeling unmistakable: mark the invented parts
inside the artifact itself, not only in the message. Use obviously non-real
values over plausible ones. Label a mock chart as illustrative on the image,
because the image is what travels. State in the handoff which parts are real.
The risk is not creating it, it is someone forwarding it a week later having
forgotten which parts were invented.
