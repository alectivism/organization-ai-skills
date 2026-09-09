# org-meetings

Meeting prep, daily and weekly triage, follow-ups, and commitment tracking, for Claude
and ChatGPT/Codex. Part of
[organization-ai-skills](https://github.com/alectivism/organization-ai-skills).

Adapts to whichever mail, calendar, chat, and meeting-notes tools are connected
(Microsoft 365 or Google Workspace; Slack or Teams; Granola, Fireflies, or any source
that exposes a transcript).

## Skills (7)

| Skill | What it does |
|---|---|
| `daily-briefing` | New mail, sent mail awaiting a reply, today's calendar, and what you still owe, sorted Urgent / Needs Reply / FYI |
| `weekly-agenda` | Sweeps the past week across meetings, mail, and chat, then force-ranks the 5 to 10 topics a leadership team has to resolve together |
| `briefing-prep` | Prep for one specific upcoming meeting: who is in the room, what happened last time, what to ask |
| `meeting-followup` | Writes up one meeting: decisions, owners, dates, and the follow-up message |
| `meeting-commitments` | Tracks what you promised across many meetings over time, suppresses what is handled, returns a ranked list of what you still owe |
| `research-brief` | A short briefing built off one research question, with sources |
| `slack-summary` | Compresses a long channel or thread into decisions, owners, and open questions |

Two pairs are easy to confuse, so the skills cross-reference each other: `daily-briefing`
is personal inbox and calendar triage, `briefing-prep` is one specific meeting;
`meeting-commitments` tracks promises across meetings over time, `meeting-followup`
writes up a single meeting.

`meeting-commitments` keeps state in a local ledger (`scripts/ledger.py`) so a scheduled
run does not repeat itself. Configure it once with `python3 scripts/ledger.py init`.

## Related plugins

- **org-ops** — `asana-task` to turn a commitment or action item into tracked work
- **org-content** — `email-draft` for the follow-up message itself
- **org-agents** — hand a long transcript to a summarizer worker instead of reading it inline

## License

MIT.
