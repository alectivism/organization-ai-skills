# Claim types: the failure modes, with examples

Read the section you need. Each entry is a way a true fact becomes a false claim.

## Numbers

**Precision:** reproduce at the source's precision. Rounding down and saying so
is honest. Rounding up is a new claim.

| Source says | Honest | Not honest |
|---|---|---|
| 412 registrations | "over 400 registered" | "roughly 500 attended" |
| 828 members | "more than 825 members" (published boilerplate) | "nearly 900 members" |
| +130% lift in one test | "+130% in the [named test]" | "up to 130% lift" |
| 90 items in the catalog | "90 items" | "nearly 100 items" |

**What the number counts:** the single most common way a real figure becomes a
false statement. These are all different, and swapping them is a factual error
even when the digits are right:

- Registrations, attendees, unique companies, unique people, sessions attended
- Members, member companies, member contacts, newsletter subscribers
- Staff, headcount, full-time employees, people across N countries
- Programs, programs recruiting now, programs completed, studies within a program
- Impressions, reach, engaged sessions, clicks

Name the unit in the sentence. "412 registrations for the [event name]"
survives a reader checking it. "412 at the event" does not.

**Never combine across definitions:** do not add a prior-year figure to a
current-year figure to produce a total. Do not compute a growth rate from two
sources that measured different populations. Do not sum regional numbers into a
global one unless the source did, because regions overlap in how members or
customers are counted.

**Projection:** no extrapolating, annualizing, or forecasting unless asked. When
asked, label it in the same sentence as the number, not in a footnote.

**As-of dates:** carry the date wherever the age of the data changes the meaning.
A correct prior-year figure presented as current is wrong. Membership counts,
pricing, program recruiting status, and staff titles all drift within a quarter.

**Your organization's formatting conventions:** apply whatever house style you
use for numerals with units, percentages, dollar amounts, and number ranges (see
the `brand-voice` template skill if installed). A generic default: numerals with
units (4 weeks, 30 experiments); percentages as numeral plus % (+130%); dollars
as $35k, $3M+; spell out one through nine in prose, numerals for 10 and up;
ranges take an en dash (April 27–29).

## Quotes and restating what people said

Applies to email, Slack, meeting transcripts, recordings, and calls as much as
to published sources.

**Quotation marks are a promise the words are exact:** no smoothing for grammar
or brand voice inside the marks. If the words are not exact, drop the marks:

- Exact: `"We're not renewing until we see the attribution work."`
- Honest paraphrase: `Their point was roughly that renewal depends on the
  attribution work landing.`
- False: `"Renewal depends on the attribution work landing."` (a sentence nobody
  said, wearing quotation marks)

Bracketed clarification inside a quote is fine when it adds a referent:
`"they [the finance team] never bought the model."`

**Never attribute a position, commitment, or opinion to someone who did not state
it.** Inferring what a customer probably thinks and writing it as what they said
is the most damaging version of this error, because it can commit your
organization to something or commit a customer to something they will deny.

**Keep the hedges:** dropping a qualifier changes the fact:

| They said | Do not write |
|---|---|
| "We could probably look at Q4" | "They agreed to Q4" |
| "I'd want to see the data first" | "They're interested" |
| "That's not a no" | "They confirmed" |
| "I'll take it to my CFO" | "Their CFO approved it" |

**Attribution mechanics:** distinguish who said a thing from who was in the room.
Attribute a meeting win or complaint only to the person who said it. If a
transcript line is unattributed or the speaker is unclear, say so rather than
assigning it to the likeliest person. In most transcription tools, the speakers
list is the only signal that someone was present, and presence is not authorship.

## Charts and graphs

A chart reads as evidence, so an illustrative chart gets mistaken for a real one.

- Plot only real points. Never pad a series to make a trend look complete or a
  line look smooth.
- Show the range the data covers. Three quarters of data is a three-quarter
  chart, not four with one interpolated.
- Do not pick axis bounds that overstate the size of a change. Label axes and
  units so the scale is not doing quiet persuasion.
- Put the source and the as-of date on or beside the chart. Charts get
  screenshotted and separated from the document that explained them.
- A mock chart is labeled illustrative **on the image**, not only in the message.

## Images, photos, headshots, logos

- Do not present an image as depicting an event, person, place, or product
  without knowing that it does. A generic conference photo in an event recap
  implies it is that event.
- Never generate an image and let it stand in for something real: an event photo,
  a screenshot, a person.
- Do not attach a headshot, a name, and a title to each other without one source
  connecting all three. Titles drift; check your `org-context` skill for staff and
  the member/customer record for outside contacts.
- **Logos are claims about someone else, which makes them worse than a wrong
  number.** Never put a company's mark on a member, sponsor, partner, or client
  slide without confirming the relationship exists (your membership/CRM source)
  and that use of the mark is cleared.
- Say where an image came from when handing it over, so it does not get reused in
  a context that makes it false.

## Links

- Do not cite a URL that was not opened and read in this session.
- Never construct a plausible-looking URL from a pattern.
- Check that links resolve before the draft ships:
  `curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" -L <url>`
- A secondary source repeating a number is not verification of that number.

## Templates and empty slots

A structure creates pressure to fill it. When a slot cannot be filled from a
source, leave it visibly empty with the question attached rather than producing
a plausible value. An empty "Key results" section reads as work in progress. A
fabricated one reads as finished, which is the problem.

## Illustrative and sample content

Legitimate to produce. The risk is downstream reuse, not creation. So:

- Mark the invented parts inside the artifact, not only in the chat message.
- Prefer obviously non-real values (Acme Corp, $1,234, 2099) over plausible ones.
- Label mock charts and mock screenshots on the image itself.
- In the handoff, state which parts are real and which are stand-ins.
- Never use a real member's or customer's name or logo in sample content. A
  forwarded mockup with a real logo on it is indistinguishable from a claim.

## Your organization's specifics worth double-checking

Every organization accumulates its own list of easy-to-get-wrong specifics.
Examples of the shape this takes, so you can build your own:

- **Naming:** your organization's full name and short form, and the forbidden
  variants (list them once in `org-context` or your CLAUDE.md, then point here).
- **Acronym expansions:** a table of what each internal acronym actually stands
  for, kept in one place so it does not drift between documents.
- **Discontinued programs:** anything that used to be active and is not
  anymore. Do not list a sunset program as current.
- **Membership/customer counts:** whatever the current, sourced figure is, plus
  which published boilerplate phrasing is pre-approved to use without
  re-deriving it each time.
- **Recruiting or availability status:** for any program, tier, or offering
  that opens and closes, check current status before writing "open now" or
  "recruiting."
- **Approved value numbers:** every number going into customer-facing text
  should trace to one proof-points reference, with its scope attached, rather
  than being retyped from memory each time.
