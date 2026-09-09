---
name: audience-personas
description: Your organization's audiences — by type (e.g., end-user, partner, vendor), by role/seniority (executive, governance, technical SME), and by lifecycle stage (prospect, new, renewing) — with what each cares about and how to write, pitch, or present to them. Use when drafting, editing, or tailoring any email, deck, post, or document aimed at a specific audience.
status: template
---

> **Template skill.** Fill in the [BRACKETED] placeholders with your organization's real audience segments — or paste your org context and ask Claude to populate them for you. Safe to ship unfilled: with the placeholders left as-is, this skill still teaches the model to reason about audience generically (who is this for, what do they already know, what do they need from this piece) instead of applying no audience lens at all.

# Audience Personas

When a request names or implies an audience (for example, "draft an email to [a governance-level contact]," "a one-pager for [a partner-type audience]," "pitch this to [an executive persona]"), apply the matching persona below automatically; the user doesn't have to ask for it or define the persona. Naming the audience is enough. Stating the frame in full ("You are {role}. Your audience is {persona}. {task}.") sharpens the result further and is worth doing for high-stakes pieces.

Personas layer on top of your organization's brand voice (see the `brand-voice` template skill, if installed): they adjust *what to emphasize and how deep to go*, and leave the tone unchanged.

## The [YOUR ORGANIZATION TYPE] lens

[Describe your organization's relationship to its audience in one or two sentences — e.g., a trade association's members are peers in a recurring relationship, not one-off buyers; a SaaS company's customers are one-time or repeat buyers; a nonprofit's audience is donors and beneficiaries. Name what makes your audience relationship distinct, and any framing to avoid — e.g., "skip sales-funnel framing" if the organization has no commercial bias.]

**Your organization's own positioning language, reuse verbatim** (pull from board decks, mission statements, or brand guidelines):
- Positioning: "[YOUR ORGANIZATION'S STATED POSITIONING STATEMENT]"
- Purpose: "[YOUR ORGANIZATION'S STATED PURPOSE OR MISSION LINE]"

## Core personas: by audience type

Most audience-facing content targets one of your organization's core audience types. Example shape (three is common, but use however many real segments your organization has):

### [PERSONA 1 — e.g., "Practitioner / end-user"]

- **Who:** [who they are, what relationship they have to your organization, any sub-tiers]
- **Cares about:** [their goals, pressures, what "good" looks like for them]
- **Write to them:** [lead with what, tone adjustments, what evidence or framing lands]
- **Avoid:** [framing or tone that reads wrong to this persona]

### [PERSONA 2 — e.g., "Partner / intermediary"]

- **Who:** [who they are — often a party who serves your core audience on your behalf]
- **Cares about:** [differentiation, credibility with their own clients, staying current]
- **Write to them:** [position your content as something they can use downstream]
- **Avoid:** [assuming they are the end-user]

### [PERSONA 3 — e.g., "Vendor / sell-side"]

- **Who:** [who they are, how they relate commercially to your organization]
- **Cares about:** [credibility, access, standing in the community]
- **Write to them:** [emphasize neutrality or independence if that matters to your organization]
- **Avoid:** [anything that reads as a sales vehicle, if that's a real risk]

## Personas by role and seniority

These cut across audience type: an executive, a governance-level contact, or a technical SME can sit within any of the core personas above.

### [Executive / senior decision-maker]

- **Who:** the most senior person in the core persona's organization who engages with your content
- **Cares about:** business outcomes, proving value up their own chain, risk and opportunity at altitude
- **Already knows** the landscape and the hype cycle. Skeptical of buzzwords; wants evidence and a number.
- **Write to them:** lead with the conclusion and the metric. Executive brevity, evidence over adjectives, decision-useful framing.
- **Avoid:** jargon, tactical minutiae, hedging, anything that reads like a pitch.

### [Governance / board-level contact]

- **Who:** [board, advisory council, or equivalent oversight body]
- **Cares about:** organizational strategy and health, mission, risk, the "so what" above day-to-day programs
- **Write to them:** strategy and impact at altitude; implications, trade-offs, risk. Concise.
- **Avoid:** operational detail, tool specifics, how-to.

### [Technical / analyst SME]

- **Who:** [the specialist audience that evaluates your work on rigor rather than narrative]
- **Cares about:** methodology, data quality, caveats, reproducibility
- **Write to them:** show the method and the numbers; state assumptions and limitations; be precise; never overclaim.
- **Avoid:** vague claims, gloss presented without methodology.

## Lifecycle: prospect / new / renewing

Cuts across all audience types. Adjust for where the reader is in their relationship with your organization:

- **Prospect:** doesn't know your value yet. Lead with the specific outcome; one clear CTA. Skip generic "join us" / "work with us."
- **New (onboarding):** knows they've engaged, not yet what to use. Orient to the highest-value next step for their type and role; make the first action easy.
- **Renewing / repeat:** weighing ongoing value. Remind them of value received, surface what's next; be specific, skip generic gratitude.
- For named contacts and segment detail, pull from the `org-context` template skill if installed.

## Worked example

Same underlying content (a new research finding), three audiences:

| Persona | Lead with | Depth | Avoid |
|---|---|---|---|
| [Practitioner / end-user] | "Here's what changes Monday morning" | Practical application, concrete numbers | Abstraction, hedging |
| [Executive / senior decision-maker] | The conclusion and the metric | Business impact, one supporting number | Tactical detail, jargon |
| [Technical / analyst SME] | The method | Sample size, caveats, reproducibility | Marketing gloss without methodology |

The finding doesn't change. What's emphasized, how deep the piece goes, and what's left out does.

## Combine with

Persona sets the audience; get the substance elsewhere. Research findings from your own research skill if you have one, org facts and names from the `org-context` template skill, tone and mechanics from the `brand-voice` template skill.
