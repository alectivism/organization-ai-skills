<!-- no-lint -->
# Organizing with folders, in a later session

**Not in the first session.** Import everything, leave it in a heap, let them use search
for a week. Structure imposed before there is anything to structure is the most repeated
reason people abandon this, and it is what broke the first version of this skill.

Come back to this file when they have notes in and have used it a bit.

---

## The one question to ask

People were asked on a recent all-hands call to come back with an answer to exactly this,
so ask it
directly:

> "Do you want one `Projects` folder with everything inside it, or each project as its
> own folder at the top level?"

Both work. Neither is better. Having decided is what matters, because the failure mode is
re-deciding every week.

Rough guide if they want one: a handful of big ongoing things suits top-level folders. A
long tail of small things suits one `Projects` folder. If they cannot decide, use one
`Projects` folder, because it is easier to promote a folder out later than to collapse
twenty back in.

---

## Let the filenames tell you the structure

Do not design a taxonomy. Their existing filenames already encode how they think, and
the script reads that:

```
vault.py plan '<vault>'
```

This proposes subfolders based on words that recur across filenames, and changes nothing.
It groups by the earliest meaningful word, so "Ulta pricing questions" lands under `Ulta`
rather than `Pricing`, and it ignores generic words like *meeting*, *notes*, *call*,
*draft*, and *agenda*, which describe what a note is rather than what it is about.

Show them the plan. Then:

```
vault.py organize '<vault>' --apply
```

Without `--apply` it prints the moves and does nothing. It never overwrites: if a file of
the same name is already in the target folder, it skips and says so, leaving both in
place. Obsidian updates any `[[links]]` to moved notes automatically.

**Notes with nothing in common stay in the root.** A folder holding one note helps
nobody. Leave them; search finds them.

---

## Folders are the organizing system

One note lives in one folder. That is the whole model, and it is enough for almost
everyone. It survives being handed to someone else, it is obvious in Finder, it works
with no plugins, and it is what people already think in.

Depth of two is plenty. If a third level is tempting, the answer was search.

## Tags, if they ask

**Most people never need these, and nothing in this skill leads with them.** Nobody in a
room full of people mentioned tags once. Do not introduce them; answer if asked.

The only thing a tag does that a folder cannot: mark something that cuts across folders.
A note in `Ulta/` and a note in `Board/` can both be tagged `pricing`. If a proposed tag
would just duplicate the folder name, it earns nothing.

Syntax, if it comes up. At the top of a note:

```
---
tags:
  - pricing
---
```

Or inline anywhere: `#pricing`.

There is a helper that tags every note with the folder it sits in, which is a starting
point rather than a goal:

```
vault.py tag '<vault>' --apply
```

It merges into existing front matter, skips notes that already carry the tag, and is safe
to re-run. Without `--apply` it prints what it would do. Reach for it only if someone has
asked for tags and wants a base to edit.

## What not to do

- **No named method.** PARA, Zettelkasten, ACCESS. Over-engineering before content
  exists is the most repeated failure story in the research.
- **No deep nesting.** Two levels is plenty. Three means search was the answer.
- **Do not build the structure out of tags.** Folders do that work. A vault whose
  structure lives in tags is hard to navigate and hard to hand to anyone else.
- **Do not rename everything.** Their filenames are how they find things. Renaming for
  consistency costs an afternoon and buys nothing.
- **Do not delete on their behalf.** If they want old notes gone, let them say which. An
  archive folder is better than a deletion, and "delete anything older than two years"
  should be their instruction, not yours.

---

## When to stop

When they can find a note in under five seconds. That is the whole goal, and it is
reachable with search alone, no folders, and no tags. Everything in this file is
optimization on top of that, and it is worth doing only for someone who has hit an actual
limit rather than someone who wants their vault to look tidy.
