# org-research

Web research and platform scraping, for Claude and ChatGPT/Codex. Part of
[organization-ai-skills](https://github.com/alectivism/organization-ai-skills).

Fill in the `org-context` template skill first if you want `lead-research` to know your
buyer titles and what you actually sell. Everything here works without it.

## Skills (5)

| Skill | What it does |
|---|---|
| `research` | Cited web research: sources named, dated, and attributed, conflicts shown both ways |
| `search-and-scrape` | Picks the search and fetch tool per job instead of defaulting to one (parallel-search, Exa, Perplexity, Jina Reader, Firecrawl) |
| `linkedin-scrape` | Profiles, posts, companies, and people. LinkedIn MCP by default, Apify for high-volume or contact-enrichment work |
| `reddit-scrape` | Posts and comments via the Apify connector: single post, subreddit, user, or keyword search |
| `lead-research` | Turns a target profile or company name into a ranked, evidence-backed prospect list with the right person to contact. Read-only against your CRM |

## Related plugins

- **org-agents** — delegate a multi-source research sweep to a cheaper worker model
- **org-content** — draft from what the research found
- **org-meetings** — `research-brief` for a briefing built off one research question

## License

MIT.
