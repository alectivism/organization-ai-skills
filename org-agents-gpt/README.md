# org-agents-gpt

Subagent delegation for ChatGPT Work and Codex.

The `subagent-delegation` skill routes research, reading, bulk work, and
verification to the cheapest suitable agent actually advertised by the active
runtime. It does not assume that every ChatGPT or Codex surface exposes the
same agent names, models, or reasoning controls.

## Product behavior

- **ChatGPT Work:** the skill uses hosted subagents available in that session.
  Work has no documented persistent custom-agent file registry, so the skill
  selects from the live catalog and falls back inline when needed.
- **Local Codex:** Codex can load persistent custom TOML agents from
  `~/.codex/agents/` or project-scoped `.codex/agents/`. This plugin includes
  nine templates and a safe installer:

  ```bash
  bash skills/subagent-delegation/scripts/install-codex-agents.sh
  ```

  The installer never overwrites an existing agent file. Restart Codex after
  installation. Pass an explicit directory as the first argument to stage or
  test the templates somewhere other than `~/.codex/agents/`.

This is the ChatGPT/Codex edition of `org-agents`, its two skills
(`subagent-delegation` and `war-council`) mirror that plugin's, but this one
speaks in GPT-5.6 model tiers and Codex TOML agents instead of Claude plugin
agent definitions. Install whichever plugin matches your platform, not both:
`org-agents` for Claude, `org-agents-gpt` for ChatGPT Work or Codex.

## Installing the local Codex agents

Use this only in the ChatGPT desktop app's **Codex** mode or another local
Codex client. Hosted ChatGPT Work has no documented way to persist local
custom-agent files.

```text
Use the installed org-agents-gpt subagent-delegation skill. Find its
install-codex-agents.sh script, inspect the nine TOML templates, and install
them into my personal Codex agent directory. Do not overwrite any existing
files. Verify what was installed and tell me whether I need to restart Codex.
```

The installed routing policy is: Luna/high for research, Luna/medium for
summarization, Luna/low for bounded bulk work, Terra/medium for long-context
ingestion, and Sol for verification, fact-checking, or adversarial review.
`luna-leaf` remains for one small, focused task, not broad research or source
sweeps. `council-member` is the ninth template: one persona on a war-council
panel, spawned several at a time in parallel by the `war-council` skill.

For centrally managed devices, deploy the same nine TOML files to each user's
`~/.codex/agents/` directory. For a trusted shared repository, check them into
`.codex/agents/` instead.

## Why this is a separate plugin from `org-agents`

A Claude plugin agent definitions folder (`agents/*.md` at the plugin root) is
a Claude-only mechanism; Codex has no equivalent named-subagent concept and
its import tooling can fail on a plugin directory that includes one. This
plugin ships skills-only, with GPT/Codex-specific assets (`agents/openai.yaml`,
`assets/codex-agents/*.toml`, `scripts/install-codex-agents.sh`) instead.
