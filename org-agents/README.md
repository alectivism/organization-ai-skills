# org-agents

Subagent delegation for Claude.

The `subagent-delegation` skill routes gathering, reading, checking, and bulk
work to cheaper worker subagents, and escalates hard reasoning or a final
check to a stronger model only when that actually helps. The `war-council`
skill convenes a panel of expert personas to stress-test a consequential
decision before you commit to it.

## Agents

Five agent definitions live under `agents/`: `org-researcher`,
`org-summarizer`, `org-bulk-worker`, `org-fact-checker`, and `org-verifier`.
Each pins its own model and effort tier so picking the right one by name is
the cost policy; see `skills/subagent-delegation/SKILL.md` for the full
routing table and return contracts.

## GPT-5.6 / Codex

This is the Claude edition. The ChatGPT Work and local Codex edition is the
separate `org-agents-gpt` plugin. Claude plugin agent definitions
(`agents/*.md` at the plugin root) are a Claude-only mechanism that Codex's
import tooling cannot handle, so the two platforms ship as two plugin
directories rather than one. Install whichever matches your platform, not
both: `org-agents` for Claude, `org-agents-gpt` for ChatGPT Work or Codex.
