---
name: subagent-delegation
description: "Use BEFORE starting any multi-part task (research or comparisons across several sources, reading or summarizing long documents and transcripts, bulk updates across many items, audits, or checking a draft or numbers before they go out). Also use when about to spawn any subagent or worker, or when a task needs 3+ searches or tool calls. Routes gathering, reading, and bulk work to cheaper worker models, and escalates hard reasoning or a final check to a stronger model only when that actually helps."
---

# Subagent Delegation

The session model is the expensive orchestrator: it plans, judges, and writes the final output. Gathering, reading, checking, and bulk work belong on cheaper worker subagents. On Anthropic's reported orchestrator-worker benchmark this split kept 96% of the top model's accuracy at 46% of the cost on BrowseComp; OpenAI's GPT-5.6 family is built for the same pattern.

## The roles, and the model to pin

Pick the column for the platform you are running on. Pin model and effort per worker; that choice is the cost policy.

| Role | Claude | GPT-5.6 | Use for |
|---|---|---|---|
| `researcher` | Sonnet / medium | Luna / high | web and file research; 3+ searches or sources |
| `summarizer` | Sonnet / low | Luna / medium | long docs, threads, transcripts into a tight brief |
| `bulk-worker` | Haiku / low | Luna / low | repetitive, fully specified work across many items |
| `verifier` | Opus / high | Sol / high | the high-stakes gate: verify drafts, numbers, and claims before sending or acting |
| `planner` | Opus / high | Sol / high | hard planning, architecture, or reasoning (see the escalation rule below) |

Spawn a worker by setting its model explicitly; never let an ad-hoc subagent inherit the orchestrator's expensive model. If none of the roles fits, use a general-purpose subagent with the model set to the cheap tier (Sonnet, or Luna).

## Delegate down by default; escalate up only when it helps

- **Down (researcher, summarizer, bulk-worker)** is the default. The orchestrator is the pricey model; push gathering, reading, and mechanical work to the cheap tier so it bills at the worker rate and its noise stays out of your context.
- **Up (verifier, planner)** is the exception. Only route to a model stronger than the one you are running on. If you are already the top tier (Fable or Opus on Claude, Sol on GPT-5.6), plan and reason inline. Calling a peer-strength subagent to think for you rarely adds anything and doubles the bill. The up-escalation earns its cost for orchestrators that default to Sonnet, Luna, or Terra: those get real lift from handing a hard architecture decision or a high-stakes plan to a stronger model.
- **The verifier is the one up-escalation worth doing even from a strong orchestrator**, when the stakes are high. An independent pass with fresh context catches the errors an author shares with its own draft. Keep it read-only.

## When to delegate at all

- The task needs 3+ web searches, document reads, or tool and integration calls.
- The work would fill the conversation with intermediate noise (search results, file contents, logs) that gets re-read every turn afterward. A worker burns that in a disposable context and hands back a tight brief.
- Two or more parts are independent: spawn those workers in parallel, in one message.

Handle it inline when the task is one quick lookup, needs the user's judgment at several points, or edits text already in the conversation. Spawning has fixed overhead; for tiny tasks it costs more than it saves.

## Rules

1. Workers start blank: they see none of the conversation. Put everything the worker needs in its prompt, including the task, the boundaries (what NOT to do), paths, names, and any rules that matter.
2. One bounded task per worker. A worker that reports the job is bigger than briefed gets re-planned, not pushed harder.
3. Never delegate voice work (emails, messages, anything in someone's personal style). Draft that in the main conversation.
4. Keep planning, synthesis, and final drafting on the orchestrator, unless you escalated planning up per the rule above.
5. Two layers is the ceiling: workers do not spawn their own workers unless the middle layer genuinely compresses (a researcher fanning out per-source readers).
6. Verify before reporting done: re-open the file, re-run the query, or send high-stakes output through the verifier.

## What each worker returns

Ask each worker for its contract and nothing else:

- **researcher** returns SUMMARY (3-5 usable bullets); FINDINGS (each with the claim, the source as a name plus link or path, and the date; conflicts shown both ways); UNVERIFIED.
- **summarizer** returns HEADLINE (one sentence); KEY POINTS (3-7, each ending on a fact, number, name, or date); DECISIONS and ACTIONS (who, what, by when, if present); OMITTED (one line on what was left out).
- **bulk-worker** returns DONE (count processed); SKIPPED (each item and why); SAMPLE (3 results to spot-check). If more than a tenth of items do not fit, stop and report instead of improvising.
- **verifier** returns VERDICT (pass, fail, or pass-with-issues); ISSUES (location, what is wrong, evidence); UNVERIFIED. Read-only: never edit, send, or fix.
- **planner** returns PLAN (ordered steps or sequence); RISKS (what could go wrong and the checkpoint that would catch it); OPEN QUESTIONS (decisions the orchestrator or user must make).
