---
name: brand-voice
description: Brand and communications reference — naming rules, colors, fonts, tone, logo usage, brand messaging, and document formatting standards. Use when creating branded content, Word docs, presentations, or any externally-facing materials.
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's details — or paste your org context and ask Claude to populate them for you. Until filled in, other skills that would normally read this file fall back to generic, brand-neutral defaults (plain formatting, no naming enforcement, no linter beyond the platform-neutral AI-tell list below) instead of failing.

# [YOUR ORGANIZATION] Brand Guidelines

Source: [link or path to your brand guidelines document]
Last updated: [DATE]

**This skill is the single source of truth for organization naming, brand voice, the brand archetype, the boilerplate, and standard descriptions:** other skills should point here rather than restating them. If you maintain a separate content-strategy or press-release skill, have it reference this one for those instead of duplicating.

---

## Organization Name Rules

- **Full name:** [YOUR ORGANIZATION FULL NAME]
- **Preferred short form:** [abbreviated name or acronym]
- **First mention in any text:** "[Full Name] ([Acronym])"
- **Subsequent mentions:** "[Acronym]" or "[Short Form]"
- **Legal name:** [if different from marketing name — note when to use/avoid]
- **Tagline:** "[YOUR TAGLINE]"
- **Not acceptable:** [list common naming mistakes — wrong conjunction, wrong word order, defunct legal name, etc.]
- **Regional/divisional format:** [e.g., "[Org] APAC" on first mention, then "[Acronym] APAC"]
- **Events must include the brand name in the title,** unless [exception, e.g., "the acronym is already established with the audience"].

---

## Color Palette

### Primary Colors

| Name | Hex | RGB | CMYK | Pantone | Usage |
|------|-----|-----|------|---------|-------|
| **[Color Name]** | `#[HEXVAL]` | [R / G / B] | [C / M / Y / K] | [Pantone #] | [primary use — e.g., headlines, buttons] |
| **[Color Name]** | `#[HEXVAL]` | [R / G / B] | [C / M / Y / K] | [Pantone #] | [primary use — e.g., foundation, authority] |

### Secondary Colors

| Name | Hex | RGB | CMYK | Pantone | Usage |
|------|-----|-----|------|---------|-------|
| **[Color Name]** | `#[HEXVAL]` | [R / G / B] | [C / M / Y / K] | [Pantone #] | [secondary use] |
| **[Color Name]** | `#[HEXVAL]` | [R / G / B] | [C / M / Y / K] | [Pantone #] | [secondary use] |

### Tints/Light Variants (optional)

| Name | Hex | RGB |
|------|-----|-----|
| **[Lt Color Name]** | `#[HEXVAL]` | [R / G / B] |

---

## Typography

### Primary Fonts

| Font | Weight | Usage | Leading | Tracking |
|------|--------|-------|---------|----------|
| **[Your Display Font]** | [weight] | [headlines, headers, emphasis] | [e.g., +10%] | [e.g., 0] |
| **[Your Body Font]** | [weight] | [body text, subheads] | [e.g., +20%] | [e.g., 0] |
| **[Optional serif/distinction font]** | [weight] | [long-form body, pull quotes] | [leading] | [tracking] |

### Substitute Fonts (when primary fonts are unavailable)

| Primary | Substitute |
|---------|-----------|
| [Primary font] | [Substitute — e.g., Arial Bold] |
| [Primary font] | [Substitute — e.g., Arial Regular] |

Use substitutes on platforms that don't support custom font uploads (email, basic web pages, Office documents). Note: python-docx/python-pptx and similar libraries only write font *names* into the file; a machine actually rendering the document still needs the fonts installed to display them correctly.

---

## Brand Messaging

### Messaging House

- **Purpose:** [why the organization exists, one sentence]
- **Positioning:** [who you serve and what you help them do, one sentence]
- **Key Message:** "[YOUR KEY MESSAGE — the one line that should show up in taglines, closers, and CTAs]"
- **Call to Action:** [the standard invitation to act — e.g., "Join us in...", "Get started with..."]

### Proof Points (use when describing [YOUR ORGANIZATION])

- [Proof point 1 — a value or behavior claim, not a stat]
- [Proof point 2]
- [Proof point 3]
- [Proof point 4]

### Internal Pillars (optional — the org's own framing of what it delivers)

1. [Pillar 1]
2. [Pillar 2]
3. [Pillar 3]
4. [Pillar 4]

---

## Brand Voice & Tone

### Brand Archetype: [YOUR ARCHETYPE — e.g., The Expert / The Hero / The Guide]

[1-2 sentences describing how the archetype shows up in communication — what the brand stands for and how it expresses that. If you use a named archetype system, e.g., "The Hero," describe what it IS and what it explicitly is NOT, so the model doesn't drift into the archetype's failure mode (e.g., Hero drifting into "lone savior" instead of "assembles a team").]

**[YOUR ARCHETYPE] IS:**
- [Behavior/trait 1]
- [Behavior/trait 2]
- [Behavior/trait 3]

**[YOUR ARCHETYPE] is NOT:**
- [Failure mode 1]
- [Failure mode 2]

### Voice Attributes

| Our voice IS | Our voice is NOT |
|-------------|-----------------|
| [Attribute 1] | [What it's NOT] |
| [Attribute 2] | [What it's NOT] |
| [Attribute 3] | [What it's NOT] |
| [Attribute 4] | [What it's NOT] |

### Writing Principles
- **[Principle 1]** — [brief explanation, e.g., "Lead with insight, not setup"]
- **[Principle 2]** — [brief explanation, e.g., "Data-first claims — back assertions with research"]
- **[Principle 3]** — [brief explanation, e.g., "Active voice throughout"]
- **[Principle 4]** — [brief explanation, e.g., "Specific over vague — use real numbers"]

### Standard Descriptions — canonical

Reproduce these word for word elsewhere; don't let other skills or drafts reconstruct them from memory.

**[YOUR ORGANIZATION] (short):** [one-sentence description]

**Key message:** "[YOUR KEY MESSAGE]"

**CTA:** [standard call to action]

**About (medium, 2-4 sentences):** [the standard "about us" paragraph used in bios, intros, and social profiles — distinct from the full external boilerplate below, which is longer and carries more detail]

### Tone by Content Type

| Type | Tone | Length |
|------|------|--------|
| Blog post | [e.g., Authoritative, energetic] | [word count range] |
| Newsletter article | [e.g., Concise, action-oriented] | [word count range] |
| Thought leadership | [e.g., Analytical, provocative] | [word count range] |
| One-pager | [e.g., Dense, data-driven] | 1 page |
| Social post | [e.g., Sharp, curiosity-driving] | 1-3 sentences |
| Press release | [e.g., Wire-ready, journalistic] | 400-550 words |
| Email (internal) | [e.g., Direct, casual] | Varies |
| Email (external) | [e.g., Professional, peer-level] | Varies |

---

## Terms to Avoid

Never use in marketing copy: [list banned words or phrases specific to your org's style]. The platform-neutral AI-tell words that should always be avoided regardless of org (leverage, synergy, delve, foster, utilize, etc.) live in `references/lint-rules.example.json` and are enforced by `scripts/lint.py` — add your org-specific terms to that same file rather than keeping a second list here.

---

## Logo Usage Rules

- **Primary mark:** [describe primary logo — mark + wordmark, or wordmark only]
- **Safe zone:** [minimum clear space rule]
- **On light backgrounds:** [version to use]
- **On dark backgrounds:** [version to use]
- **Standalone icon/mark (if the wordmark is dropped at small sizes):** [when this is allowed, and any embargo/rollout restriction]
- **Never:** [list prohibited logo treatments — e.g., stretch, recolor, add effects, place on non-brand colors]

---

## Brand Hierarchy (optional — for orgs with sub-brands)

- **Primary Mark** (top level)
  - **Regional brands** (e.g., "[Org] APAC") — [treatment rule]
  - **Sub-groups / local chapters** — [treatment rule]
  - **Divisions or practice areas** — [treatment rule, e.g., "use brand colors + a shared design element"]
  - **Products** — [treatment rule]

---

## Key Assets Location

- **Logos:** [where logo files live — a folder in this skill, a design-system repo, a shared drive. Do not commit logo binaries to a public repo; reference an internal location instead.]
- **Fonts:** [where font files live, if licensed and not publicly distributable]
- **Templates:** [email signature, letterhead, deck template — file paths or links]
- **Full brand kit (not bundled here):** [SharePoint/Drive/Notion path to the complete guidelines deck, animated logo, ad/social creative guidelines]

---

## Document Formatting

### Word Documents
- **Font:** [e.g., Calibri 11pt] — use when [primary font] is unavailable
- **Heading Hierarchy:** [Title / H1 / H2 / H3 sizes and weights]
- **Body:** [style — e.g., Normal style, 1.15 line spacing]
- **Layout:** [margins, paragraph spacing, page numbers]
- **Accent elements:** [how to use brand color for rules, table headers, highlights]
- **Cover page (when applicable):** [title treatment, subtitle, logo placement, accent element]
- **General rules:** first mention of the org name, bullet points for lists of 3+ items, bold key terms/program names on first mention

### Presentations
- **Headline font:** [font + weight]
- **Body font:** [font + weight]
- **Slide dimensions:** [16:9 standard / other]
- **Template location:** [file path or URL, or "see your org's own presentation-builder skill, if you have one"]

---

## Standard Boilerplate

Use this word-for-word in press releases, one-pagers, and other external materials:

> [YOUR ORGANIZATION BOILERPLATE — the standard "About Us" paragraph used in external publications. Include: full name, what you do, who you serve, key stats, and website URL.]

---

## Media Contact (default)

```
[Name]
[Title]
[Email]
[Phone]
```

---

## Style Linter

`scripts/lint.py` is a deterministic, dependency-free linter for organizational copy: em dashes in flowing prose, banned/always-replace vocabulary, empty intensifiers, copy-paste fingerprints, and any org-specific naming or terms-to-avoid rules you add. Its word lists and patterns live in `references/lint-rules.example.json`, not hardcoded in the script — copy that file (drop `.example`), add your org's banned terms and naming rules, and the linter picks them up automatically.

```
python3 scripts/lint.py <file>       # lint a file; exit 1 if it finds anything
python3 scripts/lint.py --stdin      # lint piped text
```

One rule ships off: `flag_clipped_fragments`. Set it `true` in your config to flag two or
more consecutive sentences of four words or fewer as a staccato tell. It is off by default
because two short declarative sentences in a row are ordinary organizational prose, so
leaving it on produces false positives on clean copy.

**This is the organizational linter** (brand naming, org terms-to-avoid, org tone rules). If your pack also includes a *personal* writing-style skill (for example `org-content/skills/personal-writing-style`), that one lints an individual's own voice for person-to-person writing (emails, Slack messages, personal posts) and is a separate tool with its own config — don't merge the two or point one at the other's rule file.
