# organization-ai-skills

Agent Skills for organizational knowledge work (marketing, communications, research, operations), for **Claude and ChatGPT**. They use the open [Agent Skills](https://agentskills.io) standard (`SKILL.md`), so the same skill runs on both platforms unchanged.

The pack is 19 generic skills grouped into five installable plugins, plus two `templates/` files you customize for your own org. Built by [@alectivism](https://github.com/alectivism); derived from the [maven-template](https://github.com/alectivism/maven-template) skill pack. MIT.

## Plugins

| Plugin | Skills | Default stance |
|---|---|---|
| **org-research** | research, search-and-scrape, linkedin-scrape, reddit-scrape | preinstall |
| **org-agents** | subagent-delegation | preinstall |
| **org-content** | content-draft, content-strategy, press-release, case-study, email-draft, event-promo | available |
| **org-meetings** | briefing-prep, meeting-followup, research-brief, slack-summary | available |
| **org-ops** | asana-task, document-find, launch-strategy, zapier-workflow-builder | available |

`.agents/plugins/marketplace.json` ships **org-research** and **org-agents** as `INSTALLED_BY_DEFAULT` and the rest as `AVAILABLE`. Admins override these per org and per group (see [Deploy to your organization](#deploy-to-your-organization-admins)).

## Templates (you customize these)

`templates/org-context` and `templates/brand-voice` are not in any plugin. They are fill-in files: `org-context` (your structure, teams, programs, tools, key people) and `brand-voice` (naming, colors, fonts, tone). Download one, open it in Claude or ChatGPT, paste your org's real details, and ask the model to fill the `[BRACKETED]` placeholders. Then install your filled-in copy like any other skill. The content skills use them when present and fall back to generic defaults when not.

## Install (individuals)

**Claude Code**
- Marketplace: `/plugin marketplace add alectivism/organization-ai-skills`, then install the plugins you want.
- Single skills: `npx skills add alectivism/organization-ai-skills`.

**ChatGPT / Codex**
- `codex plugin marketplace add alectivism/organization-ai-skills`, or in the ChatGPT desktop app: **Settings → Plugins → Add marketplace / Import from GitHub** with `https://github.com/alectivism/organization-ai-skills`.
- Single skills: **chatgpt.com/skills → Create → Upload** a skill folder.

**Manual**
```bash
cp -r org-research/skills/research ~/.claude/skills/research
cp -r templates/brand-voice ~/.claude/skills/brand-voice   # customize first
```

## Deploy to your organization (admins)

Both platforms let an admin push these plugins to everyone, preinstall some and offer others per team, and update by pushing to a repo. The mechanics differ.

### First: fork to a private repo

Claude org marketplaces **require a private or internal repo**; public repos are rejected. ChatGPT can import from public or private. So fork this pack into a **private** repo in your org (for example `your-org/ai-skills`) and connect that fork. Keep the plugin folders inside the repo with relative `source` paths (already set here); Claude's org sync will not fetch plugins from an external repo.

### Claude (Team / Enterprise)

1. Enable **Cowork** and **Skills** for the org; both are required for plugin marketplaces.
2. Go to **Organization settings → Plugins** (`claude.ai/admin-settings/plugins`), create a marketplace, and **connect your private GitHub fork**. Cowork syncs the plugins from it.
3. For each plugin, set an **installation preference**: `Installed by default`, `Available for install`, `Required`, or `Not available`. A good start: org-research and org-agents `Installed by default`; org-content, org-meetings, org-ops `Available`.
4. **Enterprise group overrides:** override the org-wide preference per group. Auto-install org-content for Marketing, leave it Available for everyone else, hide org-ops from teams that do not need it. Resolution order is group, then org-wide, then the marketplace default, and overrides persist across re-syncs.
5. **Updates:** bump a plugin's `version` and merge a pull request to the default branch. With auto-sync on, the marketplace updates automatically; direct pushes do not trigger it, and you can always click **Update** to sync manually. Members cannot edit org-managed plugins, so your version stays the source of truth.

Caveat: org-provisioned plugins install cleanly in Claude Cowork, desktop, and web, but the **Claude Code CLI** currently may not auto-install them ([issue #45323](https://github.com/anthropics/claude-code/issues/45323)); CLI users may need `/plugin marketplace add` plus `/plugin install` once.

### ChatGPT (Enterprise / Edu)

1. Plugins are **off by default** on Enterprise. Enable them in **Workspace settings → Permissions & Roles**, for the whole workspace or specific roles (RBAC).
2. In **Workspace settings → Plugins**, import from your GitHub fork and set each plugin's policy: **available to install** or **installed by default**, for the workspace or per role. This mirrors the `policy.installation` values in `.agents/plugins/marketplace.json`.
3. **Plugin sharing** (members sharing and installing workspace plugins) is off by default on Enterprise; contact your OpenAI account team to enable it. It is on by default for Edu.
4. **Updates:** re-import or re-sync from the fork after you push a new version. The managed workspace-skills library is upload-based, so the plugin-marketplace route is what gives you repo-driven updates.

### Recommended split

Preinstall **org-research** (everyone researches) and **org-agents** (delegation saves cost for everyone). Offer **org-content**, **org-meetings**, and **org-ops** per team. Distribute your filled-in `org-context` and `brand-voice` the way you distribute other skills, or bake them into a private `org-essentials` plugin inside your fork so everyone gets your org's context and brand by default.

## Skills

- **org-research:** research (cited web research), search-and-scrape (routes to parallel-search, Exa, Perplexity, Jina, or Firecrawl), linkedin-scrape, reddit-scrape.
- **org-content:** content-draft, content-strategy, press-release, case-study, email-draft, event-promo.
- **org-meetings:** briefing-prep, meeting-followup, research-brief, slack-summary.
- **org-ops:** asana-task, document-find, launch-strategy, zapier-workflow-builder.
- **org-agents:** subagent-delegation (routes gathering, reading, and bulk work to cheaper worker models and escalates to a stronger model only when it helps; carries a Claude column and a GPT-5.6 column).

## Excluded

`lab-summary`, `member-comms`, `mma-pptx-builder`, and `mma-writing-style` are org-specific and left out of this generic pack. Adapt them from the source template if you need them.

## License

MIT, see [LICENSE](LICENSE).
