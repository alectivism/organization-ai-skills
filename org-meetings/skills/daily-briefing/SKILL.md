---
name: daily-briefing
description: Produce a prioritized daily briefing covering new email received, sent mail still awaiting a reply, upcoming calendar events, and commitments the person still owes, sorted into Urgent / Needs Reply / FYI. Use whenever someone asks for a "daily briefing", "morning brief", "daily brief", "start my day", "what's on my plate", "catch me up on my inbox", "what needs my attention today", or any request to triage their inbox and calendar together. Works with whichever mail and calendar tools are connected (Outlook/Microsoft 365, Gmail/Google Workspace). Lookback defaults to 3 days of mail and is configurable; default output renders in chat.
status: ready
---

# Daily Briefing

One scannable briefing answering four questions: what landed in my inbox, who am
I waiting on, what do I still owe people, and what does today look like. Replace
"I'll scroll through my inbox for 20 minutes" with a 60-second read.

This adapts to whichever mail and calendar tools are connected. The steps below
use Outlook/Microsoft 365 as the worked example, because its quirks were found
the hard way in live use and are worth keeping as documented gotchas. On Gmail
or Google Workspace, substitute the equivalent calls (`search_gmail_messages` /
Gmail search operators, and your connected calendar search tool) and keep the
same lookback, sort, and render logic.

## Inputs

- Mail lookback: 3 days by default, or `lookback_days` from their config if one
  exists. Calendar: today plus the next business day, extended through Monday on
  a Friday.
- The current user's own mailbox. Do not pass a delegate/shared-mailbox
  parameter unless they name a delegate.
- Honor any window they state instead ("past week", "since Monday", "today").
- Read `about-me.md` from the connected workspace folder if one exists. Use it
  for VIP names, accounts, and role. If there is no such file, skip it and say
  nothing; most people will not have one.

## Step 1: Pull the sources in parallel

Make these calls in one turn.

1. **Received** — Outlook: `outlook_email_search`, `folderName: "Inbox"`,
   `afterDateTime: "<lookback> days ago"`, `limit: 25`. Gmail: search the inbox
   with the equivalent date-bounded query.
2. **Sent awaiting reply** — Outlook: `outlook_email_search`,
   `sender: <their address>`, `afterDateTime: "<lookback> days ago"`,
   `limit: 25`. Gmail: search `from:<their address>` over the same window.
3. **Calendar** — Outlook: `outlook_calendar_search`, `query: "*"`,
   `afterDateTime: "today"`, `beforeDateTime: "in 2 days"`, `limit: 50`. Gmail /
   Google Workspace: the connected calendar tool's event list over the same
   window.
4. **Commitments** — if a `meeting-commitments` store exists, run its
   `list --status open`. This is a real ledger of what they promised, and it
   beats inferring obligations from sent mail. If there is no store, skip it;
   do not offer to set one up mid-briefing. See `meeting-commitments`.

**Two hard-won Outlook rules:** do not use `folderName: "Sent Items"`, because
that lookup returns NOT_FOUND in live use even when the folder plainly exists;
the `sender:` filter is reliable. And do not raise `limit` above 25 to catch a
busy inbox, which has overflowed the token budget. Make a second targeted pull
instead, filtered to unread or to VIP senders. (These two are Outlook-specific;
Gmail's search does not have the same failure modes, but keep the same 25-item
cap for token budget reasons.)

## Step 2: Find sent mail with no reply

For each sent item, search the inbox for messages from that recipient after the
sent timestamp, matching subject with `Re:` and `Fwd:` stripped. Nothing found
means awaiting reply.

Skip items where they were the only recipient, and anything whose reply would be
automated: `noreply@`, `calendar-server@`, unsubscribe confirmations. When in
doubt, include it. One extra thread beats one missed one.

## Step 3: Sort into three buckets

**Urgent, needs action today**

- An explicit deadline today or past due.
- Escalations, or anything from leadership carrying urgency.
- Prep for a meeting in the next 24 hours with no prep visible.
- A thread they started, sitting 2+ business days, that is blocking them.
- Customer- or client-facing trouble: bounces, complaints, churn signals.
- A commitment from the ledger that is overdue or promised to someone external.

**Needs Reply, owed but not on fire**

- Direct questions to them, unanswered.
- Routine sent follow-ups awaiting a reply.
- Scheduling, intros, review requests.
- CCs that implicitly ask for input.
- Open commitments with a stated deadline still ahead.

**FYI**

- Newsletters, digests, automated mail.
- CCs where someone else owns the action.
- Announcements and confirmations.
- Events they are only attending, with no prep.

Demote noise willingly. A newsletter with a clickbait subject is still a
newsletter.

## Step 4: Render

```
# Daily Briefing — [Day, Date]

[One sentence: "3 urgent, 7 awaiting your reply, light calendar today."]

## Urgent — Action Today
- **[Subject or topic]** — [Who] — [Why it's urgent, what's needed]

## Needs Reply
### Waiting on you
- **[Subject]** — [Sender] — [What they're asking]
### Sent, no reply yet
- **[Subject]** — to [Recipient], sent [N days ago] — [What you asked]
### You promised
- **[Commitment]** — to [Who], from [Meeting], [N days ago]

## FYI
- [One line each. Group newsletters together.]

## Calendar
### Today
- [Time] — [Event] — [Prep note if any]
### Tomorrow (or Monday)
- [Time] — [Event] — [Prep note if any]

## First moves
1. [Highest-impact thing to do in the next hour]
2. [Next]
3. [Third, if there is a clear one]
```

One line of "why this matters" per item, never a summary of the email. They will
click through if they need more.

Running as a scheduled task: write to the path in their config, defaulting to
`<workspace>/briefings/YYYY-MM-DD.md`, and render in chat as well.

## Optional: region or account scoping

Only if `about-me.md` states a region or account coverage. When it does,
**demote out-of-scope items to FYI, never drop them:** a briefing that silently
deletes mail teaches people not to trust it, and account naming is ambiguous
enough (a subsidiary versus its parent company) that the filter will be wrong
sometimes. Treat the account root as always in scope.

Without a stated coverage in `about-me.md`, do not filter by region at all.

## Guardrails

- **Never invent a deadline:** a message that says "soon" does not mean Thursday.
- **No email bodies verbatim:** quote one only when they ask for it.
- **Surface, do not act:** no auto-reply, no auto-schedule, no auto-archive. If they
  then ask for a draft or a task, confirm before sending or creating.
- **Say when a section is empty:** report the gap rather than padding it.
- **This is for them only:** do not export senders or thread contents to files,
  chat channels, or an artifact unless asked. Health, compensation, and
  performance items never leave the chat.

## Do not use this skill for

- Prep for one specific upcoming meeting, with attendee research and talking
  points → `briefing-prep`
- Drafting a reply to a specific email → the `email-draft` skill (org-content)
- Tracking what they promised in meetings → `meeting-commitments`
- A leadership team agenda for the week → `weekly-agenda`
- Summarizing a Slack channel → `slack-summary`
