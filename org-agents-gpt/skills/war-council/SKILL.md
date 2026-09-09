---
name: war-council
description: "Convene a panel of expert personas that argue with each other before you commit to a decision. Use when asked for a war council, a panel, pushback, a second opinion, multiple perspectives, a stress test, a pre-mortem, a devil's advocate, \"what am I missing\", or \"poke holes in this\", and before consequential calls on spend, hiring, positioning, vendor choice, or program direction. For one critic rather than a panel, use org-verifier."
status: ready
---

# War Council

A panel of named experts critiques a decision independently, then the main
conversation reconciles the disagreement. The value is in the clash, so the
personas must be specific, opinionated, and genuinely unlike each other.
Generic advisors produce generic advice.

Concept adapted from Wade Foster's war-council skill
(github.com/zapier/wade-skills, MIT).

## Start with the active runtime

Do not assume a named agent, model, or reasoning level exists. ChatGPT Work
uses hosted agents; local Codex can also load custom TOML agents; the catalog
differs by product, account, and release. Inspect the collaboration or
subagent tool schema shown in this session and treat a role, model, and effort
combination as available only when that schema advertises it.

- If `council-member` is advertised, spawn one per persona and inject the
  persona in the prompt.
- If it is not, spawn whatever generic worker the runtime advertises and put
  the full persona and brief in the prompt instead.
- If the runtime advertises no subagents at all, role-play the members in
  sequence in one response. Say that you did, because sequential members see
  each other's arguments and converge.

To install `council-member` and the other Codex agent templates locally, run
`scripts/install-codex-agents.sh` from the subagent-delegation skill, then
restart Codex.

## Step 1: Frame the decision

Restate it in five lines before convening anything:

- **Decision:** the call, phrased as a choice between options
- **Current thinking:** where the person is leaning, and why
- **Constraints:** budget, deadline, who approves, what is committed already
- **Stakes:** what breaks if this is wrong, and when they would find out

If a line is guesswork, ask one question. Never convene a council on a
decision you had to invent.

Then write the fifth line, which does more work than the other four:

- **What must be true:** the three to six conditions this decision rests on.
  The facts that must hold, the people who must act, the dependencies that
  must exist, the numbers that must land in a range.

A panel told to "find problems" will always find problems, including invented
ones, and it never knows when to stop. A panel told to test named conditions
returns a bounded list and terminates. Carry the list into every member brief.

## Step 2: Build the roster

**Standing members, always present.** These are generic archetype slots:
swap in the roles that actually sit around your table before you run this,
and add your own via the bracketed slot below.

| Member | Lens |
|---|---|
| The Finance Skeptic (CFO / controller archetype) | Fully loaded cost, return, and what this displaces. Assumes the number is optimistic. |
| The Contrarian | Argues against the room. Has watched hype cycles collapse before and remembers who promised what. |
| The Customer/Member Advocate | Speaks for the person who has to adopt or live with this. Assumes they are busy, skeptical, and did not read the deck. |
| The Operator | Has to ship it next quarter with the team that exists. Allergic to plans that need a new hire. |
| `[YOUR ORGANIZATION'S STANDING PANELIST]` | Add a role specific to your org: a domain expert, a compliance or legal lens, a specific exec seat, whatever standing disagreement your real decisions surface. Repeat this row for more than one. |

**Dynamic experts, two to four, generated per decision.** Ask who in the world
would have the most useful opinion on this specific problem, then invent them:
a first name, a one-line backstory that includes a failure rather than only
wins, and a lens no standing member has. On specialized problems (legal,
measurement methodology, data architecture, procurement), the dynamic experts
should outnumber the standing members.

Show the roster before running it. The person gets one chance to swap someone.

## Step 3: Run the panel in parallel

Spawn all members in one turn so they run concurrently and never see each
other's answers.

**Spread the models where the runtime allows per-spawn model selection.** All
personas on one model gives you one model performing disagreement with itself.
Put most members on the strongest advertised model and vary at least one. If
only one model is available, say so rather than implying the diversity is real.

Prompt each member with the persona prepended:

> You are [name], [backstory]. You are on a panel advising a leader at
> [YOUR ORGANIZATION] on this decision: [decision, current thinking,
> constraints, stakes].
>
> It rests on these conditions holding: [the what-must-be-true list].
>
> Under 200 words, in character: POSITION (for, against, or modified, in the
> first sentence), WEAKEST CONDITION (which one fails first from your lens and
> what you would check to test it; name any condition missing from the list),
> UNDERWEIGHTED RISK, ALTERNATIVE, BET ($100 with confidence high, medium, or
> low). No preamble, no flattery, no restating the question.

## Step 4: Synthesize in the main conversation

Do not delegate this. Reconciling the disagreement is the value, and a
subagent cannot see the room.

```
## War Council Verdict

### The question
[one sentence]

### Positions
| Member | Position | Confidence | Risk flagged |
|---|---|---|---|

### Condition check
| Must be true | Verdict | Who challenged it | What would settle it |
|---|---|---|---|
[one row per condition, plus any the panel added. A condition nobody could
challenge is a green light, not a gap in the critique.]

### Where they agree
[consensus across independent panelists is the strongest signal here]

### Where they clash
[the real disagreement, and the fact that would resolve it]

### Recommendation
[weighted by stated confidence. If the panel is split, say split. Never
manufacture consensus.]

### The bet
If I had to put $1,000 on the outcome: [the bet]
Confidence: [X]%
The assumption that would flip it: [one specific thing]
```

## Rules

- Members argue with each other, not with the user. No "great question".
- Every position needs a mechanism. "This feels risky" fails the bar.
- 200 words per member. A long council is a slow council and nobody reads it.
- If the whole council agrees immediately, check the roster for a missing
  opponent and rebuild it once. If a genuinely diverse second roster also
  agrees and every condition survives scrutiny, that is the answer. Report it
  and stop. Do not keep reconvening until someone objects.
- The council informs; the person decides. Do not act on its output without
  being told to.
