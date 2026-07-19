# organization-ai-skills

A pack of Agent Skills for organizational knowledge work (marketing, communications, research, operations), for Claude and ChatGPT. Add the **org-skills** plugin to get all 19 generic skills at once, or install them individually. Two config files, `templates/org-context` and `templates/brand-voice`, are separate: you customize those for your own org (see below).

Built by [@alectivism](https://github.com/alectivism). Derived from the [maven-template](https://github.com/alectivism/maven-template) skill pack.

---

## Install

### Add as a marketplace (Claude + ChatGPT)
This repo is a plugin marketplace. Install the **org-skills** plugin to get every generic skill at once.

- **Claude Code:** `/plugin marketplace add alectivism/organization-ai-skills`, then install **org-skills**.
- **ChatGPT / Codex:** `codex plugin marketplace add alectivism/organization-ai-skills`, or in the ChatGPT desktop app use **Settings → Plugins → Add marketplace / Import from GitHub** with `https://github.com/alectivism/organization-ai-skills`.

### Individual skills (Claude Code CLI)
```bash
npx skills add alectivism/organization-ai-skills
```

### Manual
Copy any skill folder into your skills directory:
```bash
cp -r org-skills/skills/research ~/.claude/skills/research
cp -r templates/brand-voice ~/.claude/skills/brand-voice   # customize first
```

### Web upload
Zip a skill folder (e.g., `org-skills/skills/research/`) and upload it: claude.ai under **Settings → Skills**, ChatGPT at **chatgpt.com/skills → Create → Upload**.

---

## The plugin vs the templates

**The `org-skills` plugin** is 19 generic skills that work out of the box: marketing, comms, research, and ops workflows with no org-specific setup. Install the plugin (above) and use them immediately in Claude or ChatGPT. Where a skill can use your org's context or brand voice, it reads the two files below if you've added them, and falls back to sensible defaults if you haven't.

**The `templates/` folder** holds two files you customize for your own org, and they are not part of the plugin: `org-context` (your structure, teams, programs, tools, key people) and `brand-voice` (naming rules, colors, fonts, tone). Download one, open it in Claude or ChatGPT, and ask the model to fill in the `[BRACKETED]` placeholders from a paste of your org's real details. Then install your filled-in copy the same way you'd install any skill.

---

## Skills Reference

| Skill | Type | What it does |
|-------|------|-------------|
| **research** | ready | Web research with structured findings and cited sources. Triggered by "research", "look into", "find out about". |
| **search-and-scrape** | ready | Routes search and scrape requests to the right tool — parallel-search, Exa, Perplexity, Jina, or Firecrawl — based on the task. Triggered before any web lookup. |
| **linkedin-scrape** | ready | Scrapes LinkedIn profiles, posts, people, companies, and employees. Uses free local MCP for most tasks; Apify for bulk or shared-account use. |
| **reddit-scrape** | ready | Scrapes Reddit posts and comments via Apify. Single post, subreddit browse, or keyword search. |
| **zapier-workflow-builder** | ready | Designs Zapier workflows from natural language descriptions — architecture, Copilot prompts, task cost analysis, testing guidance. |
| **content-draft** | template | Drafts marketing content in your brand voice — blog posts, newsletter articles, thought leadership, one-pagers, web copy. |
| **content-strategy** | template | Builds content strategies — content pillars, audience matrices, editorial calendars, distribution plans, and KPIs. |
| **social-post** | template | Writes social media posts optimized for LinkedIn and other platforms in your organization's voice. |
| **press-release** | template | Writes wire-ready press releases with structured QA checklists, editor's notes, and source verification. |
| **case-study** | template | Produces case studies from program results, client/member outcomes, or experiment data. |
| **launch-strategy** | template | Plans program, product, research, or event launches — scoping, stakeholders, phased rollout, and go-to-market. |
| **email-draft** | template | Drafts emails in your organization's voice, segmented by audience type (internal, clients, executives, prospects). |
| **meeting-followup** | template | Generates segmented post-meeting follow-up emails from transcripts or notes. |
| **briefing-prep** | template | Prepares structured meeting briefs — attendee research, relationship context, agenda, and talking points. |
| **research-brief** | template | Formats research findings into audience-appropriate briefs — board updates, member summaries, internal updates, public-facing summaries. |
| **event-promo** | template | Writes event promotional content — email invitations, social posts, one-pagers, and sponsor/speaker outreach. |
| **slack-summary** | template | Summarizes Slack channel activity — decisions, action items, and key discussions. |
| **asana-task** | template | Creates and manages Asana tasks with your organization's project structure and naming conventions. |
| **document-find** | template | Locates documents in SharePoint, Google Drive, Notion, or other knowledge bases using your org's folder structure. |
| **org-context** | template | Central reference for your organization's structure, teams, programs, events, tools, and key people. Fill this first — other skills reference it. |
| **brand-voice** | template | Brand reference — naming rules, colors, fonts, tone, logo usage, and document formatting. Fill alongside org-context. |

---

## Excluded from v1

The following skills from the source template were intentionally excluded because they are too organization-specific to generalize cleanly, or require proprietary data sources to function:

- **lab-summary** — requires specific lab/experiment data that varies too much by org
- **member-comms** — member communication patterns are membership-model-specific
- **mma-pptx-builder** — PowerPoint generation tied to a specific slide template and brand
- **mma-writing-style** — writing style guide embedded in a broader content reviewer workflow

If your organization needs these, adapt from the source template directly.

---

## License

MIT — see [LICENSE](LICENSE).
