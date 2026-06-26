---
name: meeting-followup
description: Generate segmented follow-up emails after meetings — different messages for attendees, no-shows, speakers, and internal teams. Use for "meeting follow-up", "post-meeting email", or when a transcript or notes are provided.
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you.

# Meeting Follow-Up Email Generator

## Process

### Step 1: Gather Inputs
Collect or ask for:
- Meeting transcript, notes, or summary
- Attendee list with roles (if available)
- Any poll results or survey data
- Action items assigned during the meeting

### Step 2: Analyze & Segment
Identify distinct recipient groups that need different messages:

**Common segments:**
- **Attendees** — thank + recap + action items
- **No-shows / Regrets** — recap + what they missed + next steps
- **Speakers / Presenters** — thank + feedback + next opportunity
- **Internal team** — debrief + action items + follow-up ownership
- **New contacts** — welcome + context + how to get involved

Adjust segments based on the meeting type. Not all segments apply to every meeting.

### Step 3: Extract Key Content
From the transcript/notes, pull:
- Decisions made
- Action items (with owners and deadlines)
- Key insights or findings shared
- Questions raised (answered and unanswered)
- Next meeting date/agenda items

### Step 4: Draft Segmented Emails
For each segment, draft an email following [YOUR ORGANIZATION]'s style:
- **Subject:** [Meeting Name] — [Key Takeaway or Action]
- **Opening:** 1 sentence purpose (not "Thank you for attending...")
- **Body:** Key points as bullets, action items bolded
- **Close:** Next steps with dates
- **Tone:** Direct, warm, action-oriented

### Step 5: Create Recipient Lists
For each email variant, provide:
- Recipient list (names and emails if available)
- Suggested send timing
- Any personalization needed per recipient

## Attribution Rules
- Only attribute insights or wins to people who actually said them
- Don't include things only internal staff mentioned in "what attendees shared" sections
- When quoting, verify the attribution against the transcript

## Output Format
Present as separate email drafts with recipient lists:

### Email 1: [Segment Name]
**To:** [list]
**Subject:** [subject]
**Body:** [formatted email]

### Email 2: [Segment Name]
...

## Confirmation
**Always present all drafts for review before any sending action.**
