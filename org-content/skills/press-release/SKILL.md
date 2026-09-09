---
name: press-release
description: Wire-ready press releases in your organization's voice — for research, program results, partnerships, events, and announcements. Use for "write a press release", "draft a PR", "announcement for media".
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you.

# Press Release — [YOUR ORGANIZATION] Standards

## Voice

Wire-ready and journalistic, on top of your organization's standard voice. Use the `brand-voice` template skill when present for voice attributes and brand archetype, and tone-by-content-type; fall back to the defaults below if it isn't installed.

**Defaults (if no `brand-voice` skill is present):** professional, confident, evidence-anchored. Restrained use of bullets. Minimal headers.

What is specific to a release: minimal headers, italicized report names, restrained bullets, evidence-anchored language. One vivid phrase per release is acceptable when tied to a stat or a quote.

## Inputs to Collect

Gather these before drafting. Use [PLACEHOLDER] for anything missing and flag gaps in Editor's Notes.

1. Report/announcement title + 1-2 sentence description
2. Partner organizations and roles (if any)
3. Quotes (or identify who should be quoted)
4. Dateline city and date (default: **[YOUR CITY], [STATE] — [today's date] —**)
5. Key themes and insights — top 1-2 with supporting stats (never invent data)
6. Methodology highlights (n-size, audience, geography, field dates) if available
7. Report URL or CTA link (exact URL or [PLACEHOLDER_URL])

## Structure

### 1. Headlines (3 numbered options)
- Bold, Title Case
- 100 characters max each, no period
- Do NOT mention partner names in headlines unless it's a true co-announcement (new board member, formal partnership)

### 2. Subheads (3 numbered options)
- Sentence case, no period
- 150 characters max each

### 3. Dateline + Lede
- Bold dateline: **City, ST — Month D, YYYY —**
- Lede paragraph: 45 words max
- Answer the 5Ws (Who/What/When/Where/Why) + most newsworthy insight with one number
- If the announcement is embargoed, state the embargo date/time above the dateline (e.g., "EMBARGOED UNTIL [DATE, TIME ZONE]") and confirm the release date before distribution — an embargo header that slips out of sync with the actual dateline is a real failure mode, not a formality

### 4. Body Paragraphs
- Context + implications
- Inverted pyramid: most important to least
- Weave methodology in one concise clause if relevant
- Weave in key themes and insights naturally, not as a separate recap section
- Short paragraphs: 1-3 sentences each

### 5. Quotes (1-2 total, placed naturally — no "Quotes" header)
- **Subject matter lead quote:** Authoritative, specific, practical, data-grounded. Identify lead and title via web search if needed.
- **[YOUR CEO/EXECUTIVE] quote:** Plainspoken, pragmatic, growth-oriented, alliance-minded if relevant. Direct "we" voice. No buzzwords.
- Each quote: 35 words max
- Mark generated quotes with [DRAFT] before the quote

### 6. Optional Bulleted List (0 or 1 per release)
- 3-5 concise bullets, no nesting, ~120 words total max
- Precede with a setup line ending in a colon (e.g., "Key findings:", "Notable takeaways:", "Quantitative highlights:")

### 7. CTA
- Single sentence with exact report/hub/event URL (or placeholder)
- No separate header

### 8. About [YOUR ORGANIZATION] Boilerplate (word-for-word, no quotation marks)

**Copy the canonical boilerplate from the `brand-voice` template skill's Standard Boilerplate section.** It is not reproduced here on purpose: a boilerplate copy-pasted into every skill that needs it drifts from the source over time (punctuation, an updated stat, a changed URL) until nobody notices two versions disagree, which is exactly the failure a wire release cannot afford.

**Never type it from memory or reconstruct it:** if the `brand-voice` skill is not installed or has the boilerplate section unfilled, stop and ask for the boilerplate rather than approximating it. An approximated boilerplate reads correct and is wrong, which is worse than a visible gap.

### 9. Media Contact
Each field on its own line. Default if none provided (or copy from `brand-voice`'s Media Contact section):

```
For media inquiries:
[Name]
[Title], [YOUR ORGANIZATION]
[Email]
[Phone]
```

---

## Length & Formatting

- **Body target:** 400-550 words (excludes boilerplate and contact)
- **Paragraphs:** 1-3 sentences
- **Lists:** Zero or one bulleted/numbered list per release
- **Bold:** Headlines and dateline only — not body text
- **Italics:** Report/study names
- **Dashes:** NEVER use em dashes (—) in body text. Use commas and periods instead. (Dateline em dash is the sole exception.)
- **Exclamation points:** Only in brand/event names

---

## Writing Rules

- Lead with the most newsworthy insight. Factual, precise, journalistic — not promotional.
- Prefer concrete nouns and precise verbs: signals, highlights, accelerates, consolidates, validates, standardizes, advances. The linter is the arbiter if a verb here ever conflicts with it.
- Delete filler: "Looking ahead," "Across the board," "In practice," etc.
- Keep qualifiers tight. Use specific comparisons with timeframe, geography, and sample size (e.g., "higher than [comparison] in this sample").
- Numbers: round sensibly, include n-size/timeframe/geography when feasible, never fabricate. Each stat appears only once in body text (either bullets or prose, not both).
- Partners: credit clearly, no salesy claims. For co-authored reports, mention partner in body text only — not headline/subhead.
- Write for a busy reader skimming for the news. Each paragraph delivers one idea.
- AP style leaning.

## Terms to Avoid

Prefer running this against the `personal-writing-style` skill's linter, which mechanically enforces an avoid list plus empty intensifiers and AI tells this file doesn't repeat:

```
python3 <path-to-personal-writing-style-skill>/scripts/lint.py <draft-file>
```

**Defaults (if no linter is available):** Unlock, Unleash, Synergy, Uncover, Furthermore, Leverage (as verb), Landscape, Delve, Prowess, Realm, Unearth, Tapestry, Crucial, Critical, Pivotal, Revolutionary, Lifeblood, Treasure trove, Dive into, Game-changing, Cutting edge, Empower (as cliché), "Not only [...], but also", Paradigm shift, Best-in-class, Seamless.

A hand-checked list is strictly weaker than a linter. Retain a flagged term only if it is part of a proper noun or title. Otherwise rewrite.

---

## Editor's Notes (include after horizontal rule below the PR)

1. **Missing inputs** — list anything that would strengthen the release
2. **Character/word counts** — headline and subhead character counts, body word count (excluding boilerplate)
3. **Revision checklist** — 3 items
4. **Sources for verification** — map each stat or factual claim to its primary source (report page, figure, table label, or external URL). One bullet per source. Include short quoted claim text for scanning. Exclude style materials, prior releases, boilerplate references.

Format example:
- Page 2, Exhibit 5: "performance marketing now commands 57% of budgets"
- Page 3, Methodology: "Survey of 389 senior marketers; fielded [DATE RANGE]"

---

## QA Checklist (run before delivering)

- [ ] Body within 400-550 words
- [ ] Lede answers 5Ws in 45 words or fewer
- [ ] Headlines 100 chars or fewer, subheads 150 chars or fewer
- [ ] 0 or 1 bulleted list (with setup line ending in colon)
- [ ] 1-2 quotes, marked [DRAFT] if generated
- [ ] No em dashes in body text
- [ ] Linter run and clean (or terms-to-avoid defaults checked by hand)
- [ ] CTA uses exact URL or [PLACEHOLDER_URL]
- [ ] Boilerplate copied verbatim from `brand-voice`, not retyped
- [ ] Media contact present
- [ ] Every stat in body has a matching bullet in Sources for Verification
- [ ] [YOUR ORGANIZATION] naming conventions followed (full name on first mention, short form after)
- [ ] Partner not named in headline/subhead (unless true co-announcement)
- [ ] Embargo date/time (if any) matches the dateline
