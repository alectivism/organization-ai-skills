# organization-ai-skills

Agent Skills for organizational knowledge work (marketing, communications, research, operations), for **Claude and ChatGPT**. They use the open [Agent Skills](https://agentskills.io) standard (`SKILL.md`), so the same skill runs on both platforms unchanged.

The pack is 30 generic skills grouped into six installable plugins, plus two `templates/` files you customize for your own org. Built by [@alectivism](https://github.com/alectivism); derived from the [maven-template](https://github.com/alectivism/maven-template) skill pack. MIT.

## Plugins

| Plugin | Skills | Default stance |
|---|---|---|
| **org-research** | research, search-and-scrape, linkedin-scrape, reddit-scrape, lead-research | preinstall |
| **org-agents** | subagent-delegation, war-council, plus 5 worker agents | preinstall |
| **org-agents-gpt** | the ChatGPT/Codex edition of org-agents | preinstall |
| **org-content** | content-draft, content-strategy, press-release, case-study, email-draft, event-promo, audience-personas, personal-writing-style, factual-accuracy | available |
| **org-meetings** | briefing-prep, meeting-followup, research-brief, slack-summary, daily-briefing, weekly-agenda, meeting-commitments | available |
| **org-ops** | asana-task, document-find, document-storage, launch-strategy, zapier-workflow-builder, obsidian-setup, propose-skill-edit | available |

`org-agents` and `org-agents-gpt` are the same two skills built for different runtimes.
Install one or the other, never both: Claude users take `org-agents` (it ships five named
worker agents), ChatGPT and Codex users take `org-agents-gpt` (GPT-5.6 model tiers plus
installable Codex agent templates). A plugin directory containing an `agents/` folder
fails the ChatGPT import, which is why they are two directories rather than one.

`.agents/plugins/marketplace.json` ships **org-research** and **org-agents-gpt** as `INSTALLED_BY_DEFAULT` and the rest as `AVAILABLE`. Admins override these per org and per group (see [Deploy to your organization](#deploy-to-your-organization-admins)).

## Templates (you customize these)

`templates/org-context` and `templates/brand-voice` are not in any plugin. They are fill-in files: `org-context` (your structure, teams, programs, tools, key people) and `brand-voice` (naming, colors, fonts, tone). Download one, open it in Claude or ChatGPT, paste your org's real details, and ask the model to fill the `[BRACKETED]` placeholders. Then install your filled-in copy like any other skill. The content skills use them when present and fall back to generic defaults when not.

Each ships something beyond prose. `brand-voice` includes `scripts/lint.py`, a
dependency-free linter for organizational copy whose word lists and naming rules live in
an editable `references/lint-rules.json` rather than in the script. `org-context` includes
a header-only `staff-directory.example.csv` and a documented `.meta.json`, so you can wire
up the same auto-synced roster pattern instead of hand-maintaining a staff list.

Filling these in makes them confidential. Keep your completed copies in your private fork
and run `python3 scripts/validate.py --leaks` before sending anything upstream.

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

- **org-research:** research (cited web research), search-and-scrape (routes to parallel-search, Exa, Perplexity, Jina, or Firecrawl), linkedin-scrape, reddit-scrape, lead-research (ranked prospect lists, read-only against your CRM).
- **org-content:** content-draft, content-strategy, press-release, case-study, email-draft, event-promo, audience-personas (name the audience and the persona applies itself), personal-writing-style (an individual's voice, with a linter), factual-accuracy (the gate before anything ships, with a claim scanner).
- **org-meetings:** briefing-prep, meeting-followup, research-brief, slack-summary, daily-briefing, weekly-agenda, meeting-commitments (a ledger of what you promised, across meetings, over time).
- **org-ops:** asana-task, document-find (where is it), document-storage (read, edit, upload, and local sync across Microsoft 365 or Google Drive), launch-strategy, zapier-workflow-builder, obsidian-setup, propose-skill-edit (how staff with no GitHub seat get a wrong skill fixed).
- **org-agents:** subagent-delegation (routes gathering, reading, and bulk work to cheaper worker models and escalates to a stronger model only when it helps; carries a Claude column and a GPT-5.6 column), war-council (a panel of opinionated personas that argue before you commit), and five ready worker agents: org-researcher, org-summarizer, org-bulk-worker, org-verifier, org-fact-checker.
- **org-agents-gpt:** the same two skills for ChatGPT and Codex, with `agents/openai.yaml` definitions and `assets/codex-agents/*.toml` templates you install with `scripts/install-codex-agents.sh`.

### Two skills worth making mandatory

`factual-accuracy` (org-content) and `subagent-delegation` (org-agents) are the two that
change behavior rather than adding a capability. The first refuses any claim with no
source read in the session, because recall is not a source. The second keeps gathering
and bulk work off your most expensive model. Both are cheap to preinstall and hard to
remember to invoke by hand.

## Validating a fork

`scripts/validate.py` checks the things that actually break an install, each one learned
the hard way: frontmatter that a strict YAML parser rejects (which makes Codex skip a
whole plugin silently), a `name:` that does not match its folder, a `.codex-plugin/`
directory or an `interface` object in a `plugin.json` (both fail the ChatGPT import), a
missing `LICENSE` or `README.md` beside a plugin manifest, a plugin on disk that no
manifest lists, and an `agents/` folder inside a plugin the ChatGPT manifest ships.

It also scans for org-specific strings, which matters most in a fork: once you fill in
`org-context` and `brand-voice` with real staff, numbers, and internal paths, that content
must not travel back to a public repo. Point the `LEAK_PATTERNS` list at your own org's
names before you open a pull request upstream.

```bash
python3 scripts/validate.py          # everything, exit 1 on any finding
python3 scripts/validate.py --leaks  # just the org-specific string scan
```

`scripts/rebuild_manifests.py` regenerates any skill `MANIFEST.json` checksums, for skills
that ship one.

## Excluded

Four kinds of skill are deliberately left out, because genericizing them would leave a
shell with nothing useful in it:

- **A slide-deck builder.** It is inseparable from one real `.pptx` template, its master
  layouts, and its font and logo binaries.
- **Verified-fact catalogs.** An offerings catalog, a research-findings library, a member
  or customer roster, a proof-points list. These are pure org data. `templates/org-context`
  gives you the shape to build your own; the data has to be yours.
- **A personal dashboard.** It carries its own build pipeline, HTML template, and release
  versioning, and it is a product rather than a skill.
- **A scheduled pre-meeting brief.** It depends on a specific cloud scheduled-task runtime
  and a bundled contact roster.

`org-meetings/skills/briefing-prep` covers the manual version of that last one.

## License

MIT, see [LICENSE](LICENSE).
