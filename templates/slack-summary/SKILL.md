---
name: slack-summary
description: Summarize Slack channel activity — decisions, action items, key discussions. Use for "summarize Slack", "Slack recap", "catch me up on [channel]", or "what did I miss in Slack".
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you.

# Slack Channel Summary

## Key Channels to Monitor

Populate this table with your organization's Slack channels and what matters in each:

| Channel | What to Watch For |
|---------|------------------|
| #general | Company-wide announcements, policy changes |
| #[leadership-channel] | Executive directives, strategic decisions |
| #[team-1-channel] | [e.g., Project updates, roadmap changes] |
| #[team-2-channel] | [e.g., Client issues, deal progress] |
| #[team-3-channel] | [e.g., Event planning, logistics] |
| #[ops/pmo-channel] | Project status, resource allocation |
| [Add your key channels] | |

## Summary Structure

### Channel: #[channel-name]
**Period:** [date range]

#### Decisions Made
- [Decision] — by [who], [date]

#### Action Items
- [ ] [Task] — assigned to [who], due [date]

#### Key Discussions
- [Topic]: [1-2 sentence summary of the discussion and outcome]

#### Flagged Items
- [Anything that needs attention, is escalating, or is blocked]

## Process
1. Ask which channel(s) and time period to summarize
2. Read recent messages from the channel(s)
3. Extract decisions, action items, and key discussions
4. Flag anything that needs the user's attention
5. Present structured summary

## Guidelines
- Focus on decisions and actions, not chatter
- Attribute decisions to the person who made them
- Note any unresolved debates or open questions
- Flag direct mentions of the user by name
- Keep summaries under 500 words per channel
