---
name: org-context
description: Organizational context reference — structure, teams, programs, events, research, membership/customers, document storage, chat, and tools. Use when referencing staff, departments, initiatives, or internal resources. Populate this before using any other skill that references organization-specific information.
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you. Until filled in, other skills that would normally read this file fall back to generic, organization-neutral defaults instead of failing.

# [YOUR ORGANIZATION] — Organizational Context

Last updated: [DATE] (if a roster below is auto-synced from a source system, note that here too — e.g., "staff roster auto-synced; see `references/staff-directory.meta.example.json`")

---

## About [YOUR ORGANIZATION]

**[YOUR ORGANIZATION FULL NAME]** — [one-sentence description of what the organization does and who it serves].

**Mission/Purpose:** [mission statement or core purpose]

- **[CEO/Executive Director/Leader title]:** [Name]
- **Membership/Customers:** [number and description — e.g., "500+ member companies across 20 countries"]
- **Staff:** [headcount and locations]
- **Founded:** [year] | **Headquarters:** [city]
- **Governance:** [board structure, if any — global board, regional boards, advisory committees]
- **Core claim / key proof point:** [e.g., "Organizations using our frameworks have seen X% improvement in Y"]
- **Notable members/customers/clients:** [short representative list, or "see CRM/roster system"]

**[Additional 1-2 sentences on what makes this organization distinct — its operating model, non-commercial/commercial posture, or research standard]**

---

## Staff Directory (who works here)

For any question about a specific person (their title, team, manager, region, location, work email, or start date), read the roster file rather than answering from the summary table below or from memory — a live roster stays current; a prose table goes stale the day someone changes teams.

**Recommended pattern (auto-synced roster):**
- Keep the authoritative roster as a CSV at `references/staff-directory.csv`, one row per current employee/contractor. A starting shape ships here as `references/staff-directory.example.csv` (header row only, no real people) — copy it, rename to drop `.example`, and populate it from your HR/HRIS or directory source.
- Suggested columns: `name, known_as, title, reports_to, region, department, ft_pt, city, country, email, chat_id, started_at, ai_champion, responsibilities`. Add or drop columns to fit your org; keep the header stable once other skills depend on it.
- Track freshness in a sibling metadata file, `references/staff-directory.meta.json` (example: `references/staff-directory.meta.example.json`) — `last_updated`, `row_count`, `source` (where the data comes from), and `refresh_pipeline` (how it gets there).
- Automate the refresh: a scheduled script (cron, a LaunchAgent, a CI job) that pulls from the system of record (an HR export, a directory API, a spreadsheet) and rewrites the CSV, so the file is never hand-maintained. Exclude anything you would not want distributed this widely (personal email, personal phone, birthday) by design, and say so in the meta file.
- If your chat platform exposes a stable per-user ID (Slack member ID, Teams object ID), include it as a column so an agent can DM or @-mention someone directly without a name search.
- Work email pattern (e.g., `first@yourdomain.com`) can go in prose for reference, but always confirm the actual address against the CSV rather than constructing it.

---

## Departments & Teams (orientation)

Structure and what each team owns. **For who is on each team today, use the roster CSV above** — names here are department lead(s) only, so this table doesn't go stale as fast as a full staff list would.

| Department | Lead(s) | Focus |
|------------|---------|-------|
| Leadership | [Name] ([Title]) | [responsibility] |
| [Department 1] | [Name] ([Title]) | [responsibility] |
| [Department 2] | [Name] ([Title]) | [responsibility] |
| [Department 3] | [Name] ([Title]) | [responsibility] |
| [Regional/functional unit, if applicable] | [Name] ([Title]) — ~[N] staff | [responsibility] |
| [Add rows as needed] | | |

---

## Programs & Initiatives

[Most organizations run more than one kind of program, and the ask of a member/customer/partner differs by kind. A useful split:]

| Kind | What it is | The other side's role |
|---|---|---|
| **[e.g., Lab/Cohort]** | A running initiative that produces new results (a pilot, a consortium study, a working group) | Participates — contributes data, budget, time, or people |
| **[e.g., Tool]** | A diagnostic, assessment, benchmark, template, or framework | Uses it, self-serve or facilitated |
| **[e.g., Report/Publication]** | Published findings or content | Reads/consumes it, no participation required |

### [Program/Division 1 Name]
- **Focus:** [what this program does]
- **Kind:** [lab / tool / report / other]
- **Scale:** [size, reach, participants]
- **Partner(s):** [external partner org, if any]
- **Key outputs:** [reports, tools, events, etc.]
- **Key finding / proof point:** [headline result or stat]
- **Status:** [active / recruiting / paused / discontinued]

### [Program/Division 2 Name]
- **Focus:** [what this program does]
- **Kind:** [lab / tool / report / other]
- **Scale:** [size, reach, participants]
- **Partner(s):** [external partner org, if any]
- **Key outputs:** [reports, tools, events, etc.]
- **Key finding / proof point:** [headline result or stat]
- **Status:** [active / recruiting / paused / discontinued]

### [Add more programs as needed]

For a full program roster (every program, its kind, partner, cost, and status in one table), maintain a dedicated reference file — `references/program-roster.example.md` in this template shows the shape.

---

## Key Research & Publications

- **[Flagship research property]** — [what it is, cadence — e.g., "annual benchmarking study, now in its Nth wave"]
- **[Publication 2]** — [one line: what it covers, scale/reach]
- **[Training/certification program, if any]** — [levels or tracks, registration/completion numbers]
- **[Podcast/recurring content series, if any]** — [hosts, cadence]
- **[Add more as needed]**

---

## Events

| Event | Description | Cadence / Next Date |
|-------|-------------|---------------------|
| [Flagship event] | [what it is, who attends, scale] | [annual / quarterly / date] |
| [Executive/closed-door event] | [what it is, who attends, scale] | [annual / quarterly / date] |
| [Training/certification event] | [what it is, who attends, scale] | [annual / quarterly / date] |
| [Awards program, if any] | [what it is, scope] | [annual / date] |

---

## Strategic Priorities ([CURRENT YEAR])

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
4. [Priority 4]
5. [Add as needed]

---

## Membership / Customer Structure

**Who can join/engage:** [description of eligible organizations or individuals]

| [Member/Customer Type] | [Dues/Tier Basis] |
|---|---|
| [Type 1] | [basis — revenue, headcount, flat fee, etc.] |
| [Type 2] | [basis] |

**Scope:** [regional vs. global tiers, if applicable]

**What [members/customers] get:** [bullet list of key benefits — research access, program participation, event discounts, community access, etc.]

---

## Standard Tools

**Core:** [list primary tools — e.g., Microsoft 365, Google Workspace, Slack, Teams]
**Project/Work Management:** [Asana, Jira, Monday, etc.]
**CRM & Sales:** [Salesforce, HubSpot, Apollo, Outreach, etc.]
**Communications:** [email platform, video conferencing, messaging]
**Content & Design:** [tools used]
**AI & Automation:** [Claude, other assistants, Zapier, meeting-transcription tools, etc.]
**Document Storage:** [SharePoint, Google Drive, Notion, Dropbox, etc. — name the platform, not the specific site/folder]
**Chat / Messaging Platform:** [Slack, Teams, Discord — name the platform; workspace/channel specifics belong in `references/`, not here]

---

## Key Internal Resources

| Resource | Location |
|----------|----------|
| [Brand guidelines] | [URL or path — or "see the `brand-voice` template skill"] |
| [Staff directory] | [URL or path — or "see `references/staff-directory.csv` above"] |
| [Project/document storage] | [URL or path] |
| [Project management] | [tool and workspace URL] |
| [Internal wiki or knowledge base] | [URL or path] |
| [Chat workspace] | [workspace name/URL] |
