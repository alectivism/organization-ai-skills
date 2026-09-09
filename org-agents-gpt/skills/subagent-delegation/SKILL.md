---
name: subagent-delegation
description: "MANDATORY before starting any multi-part task, spawning any subagent, doing 3+ searches or tool calls, reading or summarizing long material, bulk-processing items, or independently checking important claims. Inspect the active subagent types first, route bounded work to the cheapest advertised suitable worker, prevent duplicate work, and keep synthesis in the main conversation."
status: ready
---

# Subagent Delegation

Treat the main session as the orchestrator. Keep planning, user judgment,
synthesis, and final drafting in the main conversation. Delegate bounded
gathering, reading, checking, and repetitive work when doing so saves time,
cost, or main-context space.

Do not assume that a named agent, model, or reasoning level exists. ChatGPT
Work uses hosted agents. Local Codex can also load custom TOML agents. The
available catalog can differ by product, account, client, and release.

## Start with the active runtime

Before spawning anything, inspect the collaboration or subagent tool schema
shown in the session. Treat a role, model, and effort combination as available
only when that schema advertises it.

Apply this order:

1. Use `org-researcher`, `org-summarizer`, `org-bulk-worker`, `org-fact-checker`,
   or `org-verifier` when the runtime advertises those installed agents. Use
   `terra-ingest` for long-context ingestion and `sol-reviewer` for an
   adversarial read-only review when those installed agents are available.
2. Choose the specialist by task, not by model preference:
   - `org-researcher` is the default for multi-source and source-constrained
     research.
   - `org-summarizer` is the default for faithful compression of long notes,
     documents, threads, or transcripts.
   - `org-bulk-worker` is the default Luna route for high-volume, bounded,
     low-judgment work.
   - `org-fact-checker` is for a claim-by-claim check of a draft against
     sources it opens itself; read-only, returns a verdict, not a rewrite.
   - `terra-ingest` is for large source sets or broad file/repository sweeps
     that need sustained context.
   - `org-verifier` and `sol-reviewer` are for independent, read-only checks.
3. Otherwise choose the smallest advertised built-in role that fits the work.
   Common examples include:
   - `luna-leaf`: one small, sharply bounded lookup or mechanical leaf task.
     In runtimes where it is fixed to Luna/xhigh, do not describe it as
     configurable Luna/high, medium, or low.
   - `terra-ingest`: long-context reading, many files, or a source sweep that
     must remain coherent.
   - `sol-reviewer`: independent, read-only verification when the stakes
     justify a stronger second pass.
   - `ops-executor`: three or more integration operations when that role is
     advertised and the user has authorized those operations.
4. Use an explicit `model` or reasoning override only when the active tool
   schema lists that exact value. Never invent a model slug or claim an effort
   level the runtime did not provide.
5. If no suitable lower-cost worker is advertised, work inline. Do not spawn an
   inherited or unknown-cost agent merely to say the task was delegated.
6. If no subagent capability is available, work inline and never imply that a
   worker ran.

## When delegation pays

Delegate when at least one condition applies:

- Two or more independent, bounded work units can run in parallel.
- The task needs at least three searches, document reads, or integration calls.
- Intermediate source material, logs, or tool output would pollute the main
  context and can be compressed into a short return contract.
- An independent read-only check materially reduces the risk of an important
  send, published number, or difficult-to-reverse decision.

Handle the task inline when it is one quick lookup, requires the user's judgment
at several points, or edits text already in the conversation. Keep emails,
messages, public-facing prose, and other voice work in the main context.
Spawning has fixed overhead and every worker consumes tokens.

## Assign work without duplication

Give each worker one bounded task and exclusive ownership of its sources,
paths, records, or questions. Include all context the worker needs because a
worker may start blank:

- objective and definition of done;
- exact sources, paths, records, or questions it owns;
- sources, paths, and actions it must not touch;
- whether the task is read-only or permits edits or external actions;
- relevant names, dates, org rules, and user constraints;
- exact return contract.

Do not repeat a worker's searches in the main session while waiting. Spot-check
the returned evidence or rerun only the narrow query needed for verification.
Assigning the same item twice is allowed only when the second assignment is an
explicit read-only verification pass.

Keep delegation to two layers. Allow a worker to fan out only when that middle
layer genuinely compresses several sources into one result and the runtime
permits the additional depth.

## Return contracts

Use the contract that matches the job.

**Researcher**

- `SUMMARY`: 3-5 usable bullets.
- `FINDINGS`: each claim with source name, link or path, and date; show
  conflicting evidence both ways.
- `UNVERIFIED`: anything not confirmed.

**Summarizer**

- `HEADLINE`: one sentence.
- `KEY POINTS`: 3-7 concrete bullets.
- `DECISIONS / ACTIONS`: who, what, and by when, only when present.
- `OMITTED`: what was excluded and where it remains available.

**Bulk worker**

- `DONE`: count processed.
- `SKIPPED`: each skipped item and reason.
- `SAMPLE`: three processed results to spot-check.
- Stop instead of improvising when more than 10 percent of items do not fit.

**Fact checker**

- `VERDICT`: clear to send, fix first, or blocked.
- `WRONG`: claim as written, what the source says, source and date.
- `UNVERIFIED`: claim, where you looked, what would settle it.
- `RIGHT BUT MISLABELED`: value correct, framing wrong.
- `CHECKED AND CORRECT`: a count.
- Read-only: reports the gap, never rewrites the draft.

**Verifier**

- `VERDICT`: pass, fail, or pass-with-issues.
- `ISSUES`: exact location, problem, and evidence.
- `UNVERIFIED`: claims that could not be checked.
- Remain read-only. Do not edit, send, post, or fix.

## Local Codex custom agents

Local Codex recognizes standalone TOML agents in `~/.codex/agents/` for one
user or `.codex/agents/` for a trusted project. Hosted ChatGPT Work does not
have a documented mechanism for importing or persisting these local TOML
files.

This skill includes nine Codex templates under `assets/codex-agents/` and a
safe, non-overwriting installer at `scripts/install-codex-agents.sh`. Run the
installer only when the user explicitly asks to install the local agents. The
templates put bounded research, summarization, and bulk work on Luna; reserve
Terra for sustained-context ingestion, and Sol for verification, fact-checking,
or difficult independent reasoning. They remain separate from the runtime-aware Work-mode
fallback above.

## Verification

Re-open changed files, rerun the relevant test or query, and spot-check worker
claims before reporting completion. Use a read-only verifier when stakes
justify the extra cost. If no suitable verifier is available, perform a narrow
inline second pass and label remaining uncertainty.
