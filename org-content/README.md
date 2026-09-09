# org-content

Content and communications drafting, for Claude and ChatGPT/Codex. Part of
[organization-ai-skills](https://github.com/alectivism/organization-ai-skills).

Most of these skills read the `brand-voice` template skill for naming, tone, boilerplate,
and terms to avoid. Fill that in once and every skill here inherits it; with it unfilled
they fall back to stated generic defaults.

## Skills (9)

| Skill | What it does |
|---|---|
| `content-draft` | Blog posts, newsletter articles, thought leadership, web copy, one-pagers |
| `content-strategy` | What to publish, for whom, on which channel, and in what order |
| `press-release` | Wire-ready releases: dateline, embargo handling, quote rules, boilerplate, verification sources |
| `case-study` | Customer or member stories built on a problem, an intervention, and a measured result |
| `email-draft` | Announcement, outreach, renewal, and onboarding email |
| `event-promo` | Promotion copy for an event across its run-up |
| `audience-personas` | Name the audience and the matching persona applies automatically, adjusting emphasis and depth without changing tone |
| `personal-writing-style` | Person-to-person writing in the sender's own voice, and stripping AI tells from it. Ships a linter |
| `factual-accuracy` | The gate before anything ships: every specific claim traces to a source read this session. Ships a claim scanner |

## The two linters are different tools

- `personal-writing-style/scripts/lint.py` lints an **individual's** voice for
  person-to-person writing (email, chat, personal posts).
- `brand-voice/scripts/lint.py` (in `templates/`) lints **organizational** copy: brand
  naming, org terms to avoid, house tone.

They have separate configs. Do not point one at the other's rule file.

## The accuracy gate

`factual-accuracy` is the one skill here worth making mandatory. It sorts a draft's
specific claims (numbers, dates, names, titles, quotes, links) and refuses the ones with
no source read in the session, because recall is not a source. Its
`scripts/claim-scan.py` finds them mechanically:

```
python3 scripts/claim-scan.py <file>
python3 scripts/claim-scan.py --stdin
CLAIM_SCAN_SOURCES='Your Research Arm|Your Data Partner' python3 scripts/claim-scan.py <file>
```

When the claim load is heavy it hands off to the `org-fact-checker` agent in
**org-agents**, or to a general-purpose subagent with the model pinned high.

## Related plugins

- **org-agents** — `org-fact-checker` and `org-verifier`, the independent checks before a send
- **org-research** — gather the evidence a draft cites
- **org-meetings** — `meeting-followup` writes the meeting up, `email-draft` sends it

## License

MIT.
