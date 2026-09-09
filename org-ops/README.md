# org-ops

Operations: tracked work, documents, launches, automations, notes, and the path for
fixing a skill that is wrong. For Claude and ChatGPT/Codex. Part of
[organization-ai-skills](https://github.com/alectivism/organization-ai-skills).

## Skills (7)

| Skill | What it does |
|---|---|
| `asana-task` | Create, update, and organize tracked work from natural language |
| `document-find` | Locates a document: search strategy and where each kind of file lives |
| `document-storage` | Read, edit, upload, and set up local sync, across Microsoft 365 or Google Drive |
| `launch-strategy` | Scoping, stakeholders, phased rollout, and go-to-market for a program, report, or event. Ships a project-brief template |
| `zapier-workflow-builder` | Design and troubleshoot Zaps: naming and folder conventions, shared connections, plain-language readback before building |
| `obsidian-setup` | Turns the notes someone already has into an Obsidian vault, then organizes it |
| `propose-skill-edit` | How someone with no seat on your skills repo gets a wrong skill fixed, as a proposal with a patch attached |

`document-find` and `document-storage` split on purpose: the first answers "where is it",
the second does everything past locating it. Overlapping descriptions load the wrong
skill, so they cross-reference each other instead of merging.

## Fill these in

Six of these carry `[BRACKETED]` slots and are marked `status: template`:
`asana-task`, `document-find`, `document-storage`, `launch-strategy`,
`propose-skill-edit`, and `zapier-workflow-builder`. They want your tenant or workspace
names, your document libraries, your department names, your maintainer, and your feedback
channel. All six work unfilled and fall back to generic behavior; they get much better
once filled. `obsidian-setup` needs nothing: it is about someone's own notes, not the org.

One bracket convention in `zapier-workflow-builder` is not a fill-in slot. In a Zap
*title*, `[MARKETING]`, `[OPS]`, `[DAILY]` and friends are the naming convention itself
and belong literally in the name. The `[YOUR ORG]`, `[Department A]` and `[Sub-area]`
entries in the folder tree are real slots. Replace those.

## Scripts

```bash
python3 skills/obsidian-setup/scripts/vault.py --help
python3 skills/propose-skill-edit/scripts/proposal.py --help
```

`proposal.py` locates its own plugin root from its install path and discovers sibling
plugins dynamically. Override with `CLAUDE_PLUGIN_ROOT`, or write a path into
`~/.config/propose-skill-edit/root`. Proposals land in `~/Documents/skill-proposals`
unless `SKILL_PROPOSAL_DIR` says otherwise.

## Related plugins

- **org-meetings** — turn a commitment or action item into an `asana-task`
- **org-content** — `factual-accuracy` before a launch asset ships
- **org-agents** — `org-bulk-worker` for a repetitive update across many tasks or files

## License

MIT.
