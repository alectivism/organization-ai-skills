---
name: lead-research
description: "Research and qualify prospective customers, partners, or members and the people to contact there, using your CRM and an enrichment tool first and LinkedIn or Apify scrapers as backup. Use for 'find prospects like', 'qualify this company', 'who should we talk to at', 'build a target list', or 'research this lead before I call'."
status: ready
---

# Lead research

Turn a target profile or a company name into a ranked, evidence-backed list of prospects with the right person to contact and a reason to reach out. Read-only against the CRM: this skill never creates or edits CRM records. Hand the finished list to the person, who decides what enters the CRM.

## Inputs to confirm first

1. **What we are selling:** membership, a subscription tier, an event sponsorship, a service package, or a partnership. Check your org's own catalog or offerings skill, if you have one, for what's currently open and its qualifying criteria. The offering decides who the buyer is.
2. **The profile or the name:** either an ideal-customer description (industry, region, size, maturity, a problem your organization solves) or one company to qualify. If no profile is given, pull the target profile from the `org-context` template skill.
3. **How many:** default 10 companies, one to two contacts each.

Ask one question if the offering is missing. Everything else can start from defaults.

## Sources, in order

| Step | Tool | What it gives |
|---|---|---|
| 1. Already known to us? | Your CRM (HubSpot, Salesforce, Attio, whichever is connected): search companies and contacts | Whether the company is already a customer, a lapsed one, or an open deal. An active-customer status means this is an account to service, not a lead. Lead status, deal stage, and last activity show who has already touched it. |
| 2. Find and enrich companies | An enrichment tool (Apollo, Clearbit, or similar, if connected) | Firmographics, headcount, industry, HQ, tech stack, funding and hiring signals. |
| 3. Find the people | The same enrichment tool's people search | Titles, seniority, location, verified email where the plan allows. Pull the buyer titles that fit your offering from `org-context`, or ask if it isn't populated yet. |
| 4. Backup and color | LinkedIn MCP (`search_companies`, `get_company_posts`, `get_person_profile`) or Apify LinkedIn scrapers — see the `linkedin-scrape` skill for which to use | Recent posts, job changes, and hiring that the enrichment tool does not surface. Use only when steps 2 and 3 leave a gap, and never to build a person profile beyond title, role, and public posts. For anything not covered by LinkedIn or the CRM, follow `search-and-scrape` for which search or fetch tool to use. |
| 5. Context your organization already holds | Your org's own research or resource catalog, if you have one, plus `org-context` | A study the prospect's industry appears in, an event they attended, a peer company that is already a customer. These are the best conversation starters. |

Enrichment calls that consume credits often report an estimated cost; surface it before running a batch and stop if it is more than the person expects.

## Scoring

Score each company 1 to 10 and show the factors, not just the number:

- **Fit (up to 4):** industry and size match the profile; the relevant function is a real role there (a decision-maker with the right title exists).
- **Need (up to 3):** a signal your organization can act on, such as a new leader in that function in the last six months, a relevant initiative in their posts, a peer competitor who is already a customer, an RFP or hiring in the relevant area.
- **Reachability (up to 2):** a named buyer with a verified contact path, or a warm path through an existing customer or staff contact.
- **Timing (up to 1):** budget cycle, event proximity, a public deadline.

A company with a 4 for fit and nothing else is a 4. Do not round up because the logo would look good on a slide.

## Output

One table, ranked by score, then one short block per company:

| Rank | Company | Score | Industry | Size | In CRM? | Buyer | Signal |

Per company: why they fit (two lines, each ending in a checkable fact), the person to contact with title and source, the offering that matches, and one opener that references the signal. Draft the opener in the sender's own voice using the `brand-voice` template skill if present; otherwise write plainly and flag that voice guidance is missing.

Close with the gaps: companies you could not enrich, contacts with no verified path, and any score that rests on one source.

## Rules

- Every firmographic, title, and signal traces to a tool result in this session. A lead list with an invented headcount is worse than a shorter list. If your organization has a stricter fact-checking discipline, apply that in full.
- Do not write to the CRM or any enrichment tool's outreach sequences from this skill. Offer a CSV in a common CRM import shape (Company name, Domain, Industry, Employees, Contact first and last name, Title, Email, Source, Score, Notes) if the person wants to import.
- Contact data is personal data. Keep it to name, title, company, and business contact path. Do not pull personal email, phone, or home location, and do not paste the list into shared channels or documents without checking your org's data-handling policy.
- A current customer found in step 1 goes to the account team, not into the prospect list.
