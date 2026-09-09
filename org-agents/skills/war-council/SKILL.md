---
name: war-council
description: "Convene a panel of expert personas that argue with each other before you commit to a decision. Use when asked for a war council, a panel, pushback, a second opinion, multiple perspectives, a stress test, a pre-mortem, a devil's advocate, \"what am I missing\", or \"poke holes in this\", and before consequential calls on spend, hiring, positioning, vendor choice, or program direction. For one critic rather than a panel, spawn the `verifier` role from `subagent-delegation` instead."
status: ready
---

# War Council

A panel of named experts critiques a decision independently, then you (or the main conversation) reconcile the disagreement. The value is in the clash. Generic advisors produce generic advice, so the personas have to be specific, opinionated, and genuinely unlike each other.

Concept adapted from Wade Foster's war-council skill (github.com/zapier/wade-skills, MIT), with real parallel subagents, cross-model panelists, and standing members you customize for your own organization.

## Start with what's installed

Do not assume a named agent, model, or reasoning level exists. Availability differs by platform, account, and release. Before convening anything, check the active subagent or collaboration tool schema for this session and treat a role as available only when it actually shows up there.

- **Claude:** if a `council-member`-style custom agent is installed, spawn one per persona with the persona injected in the prompt. If not, spawn a general-purpose subagent per persona instead, model set explicitly (spread across models per Step 3), with the full persona and brief in the prompt.
- **GPT-5.6 / Codex:** if `council-member` is advertised (installed via the `org-agents-gpt` plugin's `subagent-delegation` skill, `scripts/install-codex-agents.sh`, then restart Codex), spawn one per persona. If not, spawn whatever generic worker the runtime advertises and put the full persona and brief in the prompt instead.
- **No subagent capability at all:** role-play the members in sequence in one response, and say plainly that you did. Sequential members see each other's arguments and converge, so the independence guarantee is gone; note that limitation in the output.

## Step 1: Frame the decision

Restate it back in five lines before convening anything:

- **Decision:** the call, phrased as a choice between options
- **Current thinking:** where the person is leaning, and why
- **Constraints:** budget, deadline, who approves, what is already committed
- **Stakes:** what breaks if this is wrong, and when they would find out

If a line is guesswork, ask one question. Never convene a council on a decision you had to invent.

Then write the fifth line, which does more work than the other four:

- **What must be true:** the three to six conditions this decision rests on. The facts that must hold, the people who must act, the dependencies that must exist, the numbers that must land in a range.

A panel told to "find problems" will always find problems, including invented ones, and it never knows when to stop. A panel told to test named conditions returns a bounded list and terminates. Carry this list into every member brief.

## Step 2: Build the roster

**Standing members, always present.** These are generic archetype slots: swap in the roles that actually sit around your table before you run this, and add your own via the `[BRACKETED]` slot below.

| Member | Lens |
|---|---|
| The Finance Skeptic (CFO / controller archetype) | Fully loaded cost, return, and what this displaces. Assumes the number is optimistic. |
| The Contrarian | Argues against the room. Has watched hype cycles collapse before and remembers who promised what. |
| The Customer/Member Advocate | Speaks for the person who has to adopt or live with this. Assumes they are busy, skeptical, and did not read the deck. |
| The Operator | Has to ship it next quarter with the team that exists. Allergic to plans that need a new hire. |
| `[YOUR ORGANIZATION'S STANDING PANELIST]` | Add a role specific to your org: a domain expert, a compliance or legal lens, a specific exec seat, whatever standing disagreement your real decisions surface. Repeat this row for more than one. |

**Dynamic experts, two to four, generated per decision.** Ask who in the world would have the most useful opinion on this specific problem, then invent them:

1. First name and a one-line backstory.
2. The backstory includes a failure, not only wins. Scarred experts critique better than decorated ones.
3. A lens no standing member has.
4. On specialized problems (legal, measurement methodology, data architecture, procurement), dynamic experts should outnumber standing members.

Show the roster before running it. The person gets one chance to swap someone out.

## Step 3: Run the panel in parallel

Spawn one subagent per member in a single message so they run concurrently and never see each other's answers. Independence is the whole point; a member who reads another's take converges on it.

**Spread the models where your runtime allows per-spawn model selection.** All personas on one model gives you one model performing disagreement with itself. Put most members on the strongest model available to you, and at least one on a different model family if your runtime offers one. If only one model is available, say so in the output rather than implying the diversity is real.

**Brief each member with the persona prepended:**

> You are [name], [backstory]. You are on a panel advising a leader at [YOUR ORGANIZATION] on this decision: [decision, current thinking, constraints, stakes].
>
> This decision rests on these conditions holding: [the what-must-be-true list].
>
> Respond in under 200 words, in character:
> 1. Your position: for, against, or modified, in the first sentence.
> 2. Which condition on that list is weakest from your lens, and what you would check to test it. If you think a condition is missing from the list, name it.
> 3. The one risk everyone else is underweighting.
> 4. One concrete alternative or modification.
> 5. Your $100 bet on how this plays out, with confidence: high, medium, or low.
>
> No preamble, no flattery, no restating the question. Disagree with the obvious answer if you have grounds. If another discipline should own this call, say so and name it.

## Step 4: Synthesize yourself

Do not delegate this. Reconciling the disagreement is where the value is, and a subagent cannot see the room.

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
[one row per condition, plus any the panel added. A condition nobody could challenge is a green light, not a gap in the critique.]

### Where they agree
[consensus across independent panelists is the strongest signal here]

### Where they clash
[the real disagreement, and the fact that would resolve it]

### Recommendation
[weighted by stated confidence. If the panel is split, say split. Never manufacture consensus.]

### The bet
If I had to put $1,000 on the outcome: [the bet]
Confidence: [X]%
The assumption that would flip it: [one specific thing]
```

## Rules

- Members argue with each other, not with the user. No "great question".
- Every position needs a mechanism. "This feels risky" fails the bar.
- 200 words per member. A long council is a slow council and nobody reads it.
- If the whole council agrees immediately, check the roster for a missing opponent and rebuild it once. If a genuinely diverse second roster also agrees and every condition survives scrutiny, that is the answer. Report it and stop. Do not keep reconvening until someone objects.
- The council informs; the person decides. Do not act on its output without being told to.
