#!/usr/bin/env python3
"""Append-only commitment ledger for the meeting-commitments skill.

The model does the extraction. This script does the bookkeeping, so that
re-running the skill never re-suggests something already handled.

Storage is one JSONL file, append-only. Status changes append a new record
with the same id; the reader folds by id and the last record wins. Nothing is
ever rewritten in place, which is what stops the "it made a new file instead"
failure and survives a crash mid-write.

Stdlib only. Python 3.9+.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys

# ---------------------------------------------------------------- normalizing

FILLER = {
    "i", "ill", "im", "id", "ive", "we", "well", "weve", "let", "lets", "me",
    "my", "our", "the", "a", "an", "to", "for", "of", "on", "in", "at", "and",
    "that", "this", "it", "is", "am", "are", "be", "will", "would", "should",
    "gonna", "going", "want", "need", "just", "kind", "sort", "like", "so",
    "then", "there", "here", "get", "got", "make", "sure", "guess", "think",
    "maybe", "actually", "basically", "really", "okay", "ok", "yeah", "up",
    "out", "back", "over", "with", "about", "some", "thing", "stuff", "do",
    "does", "did", "have", "has", "had", "can", "could", "you", "your",
}

STEM_SUFFIXES = ("ings", "ing", "edly", "ed", "es", "s")

TOKEN_RE = re.compile(r"[a-z0-9]+")


def stem(word):
    for suffix in STEM_SUFFIXES:
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def tokens(text):
    """Content tokens, stemmed, filler removed, order preserved."""
    raw = TOKEN_RE.findall((text or "").lower())
    return [stem(w) for w in raw if w not in FILLER and len(w) > 1]


def key_phrase(text, width=8):
    return " ".join(tokens(text)[:width])


def make_id(owner, text):
    """Deterministic. Same commitment extracted twice yields the same id."""
    basis = f"{(owner or '').strip().lower()}|{key_phrase(text)}"
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]


def overlap(a, b):
    """Overlap coefficient, not Jaccard.

    The same commitment pulled from Granola and from Fireflies differs mostly
    in verbosity: one says "send them the deck", the other says "owner to
    send the deck over by Friday". Jaccard punishes the longer
    extraction for words the shorter one never had, and scores real duplicates
    around 0.5. Dividing by the shorter set instead asks the question that
    matters: is the smaller statement contained in the larger one.
    """
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    shared = sa & sb
    if len(shared) < 2:
        return 0.0  # one word in common is a coincidence, not a match
    return len(shared) / min(len(sa), len(sb))


def is_same_commitment(cand_toks, other_toks, same_meeting, threshold):
    """Two recordings of one call can be merged on weaker evidence than two
    commitments made weeks apart, which need to stay separate."""
    if len(cand_toks) < 3 or len(other_toks) < 3:
        return False  # too short to judge; only an exact id match counts
    bar = threshold - 0.13 if same_meeting else threshold
    return overlap(cand_toks, other_toks) >= bar


def today():
    return dt.date.today().isoformat()


def now():
    return dt.datetime.now().replace(microsecond=0).isoformat()


def days_since(iso):
    if not iso:
        return 0
    try:
        d = dt.date.fromisoformat(str(iso)[:10])
    except ValueError:
        return 0
    return (dt.date.today() - d).days


# ------------------------------------------------------------------- storage


def ledger_path(root):
    return os.path.join(root, "ledger.jsonl")


def load(root):
    """Fold the append-only log into current state, keyed by id."""
    path = ledger_path(root)
    state = {}
    if not os.path.exists(path):
        return state
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue  # tolerate a torn final line
            rid = rec.get("id")
            if not rid:
                continue
            if rid in state:
                merged = dict(state[rid])
                merged.update(rec)
                state[rid] = merged
            else:
                state[rid] = rec
    return state


def append(root, records):
    os.makedirs(root, exist_ok=True)
    with open(ledger_path(root), "a", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ scoring


def new_record(rid, owner, text, cand, mdate, **extra):
    """One place that defines the record shape, so the fresh path and the
    recurrence path can never drift apart."""
    rec = {
        "id": rid,
        "owner": owner,
        "text": text,
        "source": cand.get("source"),
        "meeting": cand.get("meeting"),
        "meeting_date": mdate,
        "captured": now(),
        "status": "open",
        "due": cand.get("due"),
        # A deadline nobody actually said, inferred from context. Kept apart
        # from `due` so an inferred date can never masquerade as a promise.
        "due_implied": cand.get("due_implied"),
        "promised_to": cand.get("promised_to"),
        "requested_by": cand.get("requested_by"),
        "external": bool(cand.get("external")),
        "category": cand.get("category"),
        "quote": cand.get("quote"),
        # Link back to the moment in the recording, so any item can be checked
        # against what was said in one click.
        "deep_link": cand.get("deep_link"),
        # high | medium | low. How sure the extractor is that this is a real
        # commitment rather than a topic. Low-confidence items are shown in a
        # separate block rather than dropped.
        "confidence": cand.get("confidence") or "medium",
        "reaffirmed": [],
    }
    rec.update(extra)
    return rec


def score(rec):
    """Higher surfaces first. Recency, a real deadline, and an external
    promisee are what make an open loop urgent."""
    pts = 0.0
    age = days_since(rec.get("meeting_date") or rec.get("captured"))
    pts += max(0.0, 20.0 - age)
    if rec.get("due"):
        overdue = -days_since(rec["due"])
        pts += 25.0 if overdue <= 0 else max(0.0, 15.0 - overdue)
    elif rec.get("due_implied"):
        # An inferred deadline counts, but never as much as a stated one.
        overdue = -days_since(rec["due_implied"])
        pts += 10.0 if overdue <= 0 else max(0.0, 6.0 - overdue)
    if rec.get("promised_to"):
        pts += 8.0
    if rec.get("external"):
        pts += 12.0
    pts += 3.0 * len(rec.get("reaffirmed") or [])
    pts += {"high": 5.0, "medium": 0.0, "low": -8.0}.get(
        rec.get("confidence") or "medium", 0.0)
    return round(pts, 2)


# ------------------------------------------------------------------ commands


def cmd_init(args):
    root = args.root
    os.makedirs(root, exist_ok=True)
    path = ledger_path(root)
    if not os.path.exists(path):
        open(path, "a", encoding="utf-8").close()
    cfg_path = os.path.join(root, "config.json")
    created_cfg = False
    if not os.path.exists(cfg_path):
        cfg = {
            "owner": args.owner or "me",
            "aliases": [],
            "lookback_days": 7,
            "display_cap": 10,
            "stale_after_days": 30,
            "categories": ["board", "member", "team", "personal", "admin"],
            "output_markdown": os.path.join(root, "open-loops.md"),
            "output_html": os.path.join(root, "open-loops.html"),
        }
        with open(cfg_path, "w", encoding="utf-8") as fh:
            json.dump(cfg, fh, indent=2)
        created_cfg = True
    print(json.dumps({
        "root": root,
        "ledger": path,
        "config": cfg_path,
        "config_created": created_cfg,
    }, indent=2))


def cmd_add(args):
    """Ingest extracted candidates. Reports what was genuinely new."""
    if args.file == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.file, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    if isinstance(payload, dict):
        payload = payload.get("items", [])

    state = load(args.root)
    open_items = {k: v for k, v in state.items() if v.get("status") == "open"}

    writes = []
    report = {"new": [], "reaffirmed": [], "reopened": [], "near_duplicate": []}
    suppressed = 0

    for cand in payload:
        text = (cand.get("text") or "").strip()
        if not text:
            continue
        owner = cand.get("owner") or args.owner or "me"
        cid = make_id(owner, text)
        ctoks = tokens(text)
        mdate = cand.get("meeting_date") or today()

        prior = state.get(cid)

        # Reworded across two recordings of the same call, or across sources.
        if prior is None:
            best, best_score = None, 0.0
            for oid, other in open_items.items():
                if other.get("owner") != owner:
                    continue
                otoks = tokens(other.get("text", ""))
                same_meeting = bool(mdate) and mdate == other.get("meeting_date")
                if not is_same_commitment(ctoks, otoks, same_meeting, args.threshold):
                    continue
                sim = overlap(ctoks, otoks)
                if sim > best_score:
                    best, best_score = oid, sim
            if best:
                prior = open_items[best]
                cid = best
                report["near_duplicate"].append(
                    {"id": best, "text": text, "matched": prior.get("text"),
                     "similarity": round(best_score, 2)})

        if prior is None:
            rec = new_record(cid, owner, text, cand, mdate)
            writes.append(rec)
            state[cid] = rec
            open_items[cid] = rec
            report["new"].append({"id": cid, "text": text})
            continue

        status = prior.get("status")

        if status == "open" or status == "stale":
            # Same loop, said again. Bump it, do not duplicate it.
            seen = list(prior.get("reaffirmed") or [])
            if mdate not in seen and mdate != prior.get("meeting_date"):
                seen.append(mdate)
            rec = dict(prior)
            rec.update({
                "id": cid,
                "status": "open",
                "reaffirmed": seen,
                "due": cand.get("due") or prior.get("due"),
            })
            writes.append(rec)
            state[cid] = rec
            open_items[cid] = rec
            report["reaffirmed"].append({"id": cid, "text": prior.get("text")})
            continue

        # Previously closed. Only a commitment made AFTER the close is real.
        closed_on = str(prior.get("closed") or "")[:10]
        if closed_on and mdate > closed_on:
            n = 2
            while f"{cid}-r{n}" in state:
                n += 1
            rid = f"{cid}-r{n}"
            rec = new_record(rid, owner, text, cand, mdate, recurrence_of=cid)
            writes.append(rec)
            state[rid] = rec
            open_items[rid] = rec
            report["reopened"].append({"id": rid, "text": text})
        else:
            # Already done before this meeting. Drop it silently. This is the
            # line that stops completed work from coming back.
            suppressed += 1

    if writes and not args.dry_run:
        append(args.root, writes)

    report["counts"] = {k: len(v) for k, v in report.items() if isinstance(v, list)}
    report["counts"]["suppressed_already_done"] = suppressed
    report["counts"]["candidates_in"] = len([c for c in payload if c.get("text")])
    print(json.dumps(report, indent=2))


def cmd_list(args):
    state = load(args.root)
    items = [r for r in state.values() if r.get("status") == args.status]
    for r in items:
        r["score"] = score(r)
        r["age_days"] = days_since(r.get("meeting_date"))
    items.sort(key=lambda r: r["score"], reverse=True)
    if args.limit:
        items = items[: args.limit]
    print(json.dumps(items, indent=2))


def cmd_close(args):
    state = load(args.root)
    writes, missing = [], []
    for cid in args.id:
        prior = state.get(cid)
        if not prior:
            missing.append(cid)
            continue
        rec = dict(prior)
        rec.update({
            "id": cid,
            "status": args.status,
            "closed": now(),
            "evidence": args.evidence,
        })
        writes.append(rec)
    if writes:
        append(args.root, writes)
    print(json.dumps({
        "closed": [w["id"] for w in writes],
        "status": args.status,
        "not_found": missing,
    }, indent=2))


def cmd_sweep(args):
    """Age out open items nobody has mentioned in weeks. They stay in the
    ledger, they just stop crowding the list."""
    state = load(args.root)
    cutoff = args.days
    writes = []
    for rec in state.values():
        if rec.get("status") != "open":
            continue
        last = max(
            [rec.get("meeting_date") or ""] + list(rec.get("reaffirmed") or [])
        )
        if days_since(last) > cutoff:
            new = dict(rec)
            new.update({"status": "stale", "closed": now(),
                        "evidence": f"no mention in {cutoff} days"})
            writes.append(new)
    if writes and not args.dry_run:
        append(args.root, writes)
    print(json.dumps({"staled": [w["id"] for w in writes]}, indent=2))


# ----------------------------------------------------------------- rendering


def _group(items):
    out = {}
    for r in items:
        out.setdefault(r.get("category") or "uncategorized", []).append(r)
    return out


def render_markdown(state, cap, owner):
    items = [r for r in state.values() if r.get("status") == "open"]
    for r in items:
        r["score"] = score(r)
    items.sort(key=lambda r: r["score"], reverse=True)
    shown, rest = items[:cap], items[cap:]
    stale = [r for r in state.values() if r.get("status") == "stale"]
    done_recent = [
        r for r in state.values()
        if r.get("status") == "done" and days_since(str(r.get("closed"))[:10]) <= 7
    ]

    lines = [f"# Commitments — {owner}", "",
             f"_Regenerated {now()}. Derived from ledger.jsonl; edits here are lost._",
             ""]
    if not items:
        lines += ["Nothing open.", ""]
    for cat, group in _group(shown).items():
        lines.append(f"## {cat}")
        lines.append("")
        for r in group:
            bits = []
            if r.get("promised_to"):
                bits.append(f"promised to {r['promised_to']}")
            if r.get("due"):
                bits.append(f"due {r['due']}")
            bits.append(f"{r.get('meeting') or 'unknown meeting'}, {r.get('meeting_date')}")
            if r.get("reaffirmed"):
                bits.append(f"raised again {len(r['reaffirmed'])}x")
            lines.append(f"- **{r['text']}**  \n  `{r['id']}` · " + " · ".join(bits))
        lines.append("")
    if rest:
        lines += [f"## Also open ({len(rest)})", ""]
        lines += [f"- {r['text']} · `{r['id']}`" for r in rest] + [""]
    if done_recent:
        lines += [f"## Closed this week ({len(done_recent)})", ""]
        lines += [f"- ~~{r['text']}~~ · {r.get('evidence') or 'marked done'}"
                  for r in done_recent] + [""]
    if stale:
        lines += [f"## Gone quiet ({len(stale)})", "",
                  "Untouched for weeks. Revive or ignore.", ""]
        lines += [f"- {r['text']} · `{r['id']}`" for r in stale] + [""]
    return "\n".join(lines)


def render_html(state, cap, owner):
    items = [r for r in state.values() if r.get("status") == "open"]
    for r in items:
        r["score"] = score(r)
    items.sort(key=lambda r: r["score"], reverse=True)
    shown, rest = items[:cap], items[cap:]

    def esc(s):
        return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;"))

    cards = []
    for r in shown:
        meta = []
        if r.get("promised_to"):
            meta.append(f"promised to {esc(r['promised_to'])}")
        if r.get("due"):
            meta.append(f"due {esc(r['due'])}")
        meta.append(f"{esc(r.get('meeting') or 'unknown meeting')} · {esc(r.get('meeting_date'))}")
        cards.append(
            '<li class="item"><div class="txt">{}</div>'
            '<div class="meta"><span class="cat">{}</span>{}</div></li>'.format(
                esc(r["text"]), esc(r.get("category") or "—"),
                "".join(f"<span>{m}</span>" for m in meta),
            )
        )

    return """<title>Commitments</title>
<style>
  :root{--bg:#faf9f7;--card:#fff;--ink:#1a1a1a;--dim:#6b6b6b;--line:#e5e2dd;--accent:#c2410c}
  :root:not([data-theme="light"]){}
  @media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
    --bg:#141414;--card:#1e1e1e;--ink:#f0efed;--dim:#9a9a9a;--line:#2e2e2e;--accent:#fb923c}}
  :root[data-theme="dark"]{--bg:#141414;--card:#1e1e1e;--ink:#f0efed;--dim:#9a9a9a;--line:#2e2e2e;--accent:#fb923c}
  body{background:var(--bg);color:var(--ink);font:16px/1.5 ui-sans-serif,-apple-system,Segoe UI,sans-serif;
       margin:0;padding:2.5rem 1.25rem;}
  .wrap{max-width:720px;margin:0 auto}
  h1{font-size:1.5rem;margin:0 0 .25rem}
  .sub{color:var(--dim);font-size:.85rem;margin-bottom:2rem}
  ul{list-style:none;padding:0;margin:0}
  .item{background:var(--card);border:1px solid var(--line);border-radius:10px;
        padding:.9rem 1rem;margin-bottom:.6rem}
  .txt{font-weight:600;margin-bottom:.35rem}
  .meta{color:var(--dim);font-size:.78rem;display:flex;flex-wrap:wrap;gap:.5rem}
  .meta span::after{content:"·";margin-left:.5rem;opacity:.5}
  .meta span:last-child::after{content:""}
  .cat{color:var(--accent);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
  .more{color:var(--dim);font-size:.85rem;margin-top:1.5rem;border-top:1px solid var(--line);padding-top:1rem}
</style>
<div class="wrap">
  <h1>Commitments — __OWNER__</h1>
  <div class="sub">__COUNT__ open · regenerated __WHEN__</div>
  <ul>__CARDS__</ul>
  __MORE__
</div>""".replace("__OWNER__", esc(owner)).replace("__COUNT__", str(len(items))) \
        .replace("__WHEN__", now()).replace("__CARDS__", "".join(cards)) \
        .replace("__MORE__", f'<div class="more">{len(rest)} more open, not shown.</div>' if rest else "")


def cmd_render(args):
    state = load(args.root)
    cfg_path = os.path.join(args.root, "config.json")
    cfg = {}
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as fh:
            cfg = json.load(fh)
    cap = args.cap or cfg.get("display_cap", 10)
    owner = args.owner or cfg.get("owner", "me")

    # Config has had two shapes: flat output_markdown/output_html, and nested
    # output.{markdown,html}. Accept both so an older config keeps working.
    out = cfg.get("output") or {}
    cfg_md = out.get("markdown") or cfg.get("output_markdown")
    cfg_html = out.get("html") or cfg.get("output_html")

    def resolve(p, default):
        """Config files travel between a host and a sandbox that mount the same
        folder at different absolute paths, and between machines. A bare
        filename is therefore the portable form: anything whose directory does
        not exist here falls back to that filename inside the store."""
        if not p:
            return os.path.join(args.root, default)
        p = os.path.expanduser(p)
        if not os.path.isabs(p):
            return os.path.join(args.root, p)
        if os.path.isdir(os.path.dirname(p)):
            return p
        return os.path.join(args.root, os.path.basename(p))

    cfg_html = resolve(cfg_html, "commitments.html") if (args.html or cfg_html) else None
    md_path = args.markdown or resolve(cfg_md, "commitments.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(state, cap, owner))
    written = {"markdown": md_path}

    if args.html or cfg_html:
        html_path = args.html or cfg_html
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(render_html(state, cap, owner))
        written["html"] = html_path

    counts = {}
    for r in state.values():
        counts[r.get("status", "?")] = counts.get(r.get("status", "?"), 0) + 1
    written["counts"] = counts
    print(json.dumps(written, indent=2))


# ------------------------------------------------------------------ interop


def cmd_merge_state(args):
    """Absorb 'done' ticks made somewhere else.

    A common state-inbox pattern: a dashboard, a phone, or any other surface
    drops a small JSON file saying what the person marked finished, and the
    next run folds it in. This is what lets someone close an item by tapping
    it rather than by talking to an assistant.

    Accepts either shape:
        {"state": {"done": {"<id>": "2026-08-27"}}}
        {"done": ["<id>", "<id>"]}
    """
    inbox = args.inbox or os.path.join(args.root, "state-inbox")
    if not os.path.isdir(inbox):
        print(json.dumps({"merged": [], "note": f"no state-inbox at {inbox}"}))
        return

    state = load(args.root)
    writes, merged, unknown = [], [], []

    # Some mounts, synced folders, and read-only shares let you write a file
    # but not delete one. Deleting is therefore best-effort, and a durable
    # "already processed" marker in the root does the real work.
    seen_path = os.path.join(args.root, "state-inbox-processed.json")
    try:
        with open(seen_path, "r", encoding="utf-8") as fh:
            processed = set(json.load(fh))
    except (OSError, json.JSONDecodeError):
        processed = set()
    stuck = []

    for name in sorted(os.listdir(inbox)):
        if not name.endswith(".json") or name in processed:
            continue
        path = os.path.join(inbox, name)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                blob = json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue

        done = (blob.get("state") or blob).get("done") or {}
        pairs = done.items() if isinstance(done, dict) else [(i, today()) for i in done]

        for cid, when in pairs:
            prior = state.get(cid)
            if not prior:
                unknown.append(cid)
                continue
            if prior.get("status") == "done":
                continue
            rec = dict(prior)
            rec.update({"id": cid, "status": "done", "closed": str(when),
                        "evidence": f"marked done in {name}"})
            writes.append(rec)
            state[cid] = rec
            merged.append(cid)

        processed.add(name)
        if args.consume:
            try:
                os.remove(path)
                processed.discard(name)  # gone for good, no marker needed
            except OSError:
                stuck.append(name)  # can't delete here; the marker covers us

    if writes:
        append(args.root, writes)
    try:
        with open(seen_path, "w", encoding="utf-8") as fh:
            json.dump(sorted(processed), fh, indent=1)
    except OSError:
        stuck.append("(could not write the processed marker)")

    print(json.dumps({
        "merged": merged,
        "unknown_ids": unknown,
        "undeletable": stuck,
        "note": ("marked processed rather than deleted; re-running is safe"
                 if stuck else ""),
    }, indent=2))


def cmd_export(args):
    """Emit open commitments in a plain meeting-actions.json shape, so a
    dashboard can render them without knowing this ledger exists."""
    state = load(args.root)
    items = [r for r in state.values() if r.get("status") == "open"]
    for r in items:
        r["score"] = score(r)
    items.sort(key=lambda r: r["score"], reverse=True)

    meetings, seen = [], set()
    actions = []
    for r in items:
        mid = r.get("meeting") or "unknown"
        if mid not in seen:
            seen.add(mid)
            meetings.append({"id": sid(mid), "title": mid,
                             "date": r.get("meeting_date"),
                             "source": r.get("source")})
        actions.append({
            "id": r["id"],
            "text": r["text"],
            "meetingId": sid(mid),
            "meetingTitle": mid,
            "meetingDate": r.get("meeting_date"),
            "requestedBy": r.get("requested_by"),
            "promisedTo": r.get("promised_to"),
            "context": r.get("quote"),
            "impliedDeadline": r.get("due") or r.get("due_implied"),
            "confidence": r.get("confidence") or "medium",
            "source": r.get("source"),
            "deepLink": r.get("deep_link"),
            "firstSeen": str(r.get("meeting_date") or "")[:10],
        })

    out = {"meetings": meetings, "actionItems": actions, "notes": [],
           "generated": now(), "producer": "meeting-commitments"}
    path = args.out or os.path.join(args.root, "meeting-actions.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps({"exported": path, "meetings": len(meetings),
                      "actionItems": len(actions)}, indent=2))


def sid(*parts):
    """The same 12-char SHA1 scheme a companion dashboard build script can use,
    so an item hashed on either side lands on the same identity."""
    return hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:12]


# --------------------------------------------------------------------- main


def main():
    p = argparse.ArgumentParser(description="Append-only commitment ledger.")
    p.add_argument("--root", default=os.path.expanduser("~/open-loops"),
                   help="directory holding ledger.jsonl and config.json")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("--owner"); s.set_defaults(fn=cmd_init)

    s = sub.add_parser("add")
    s.add_argument("--file", required=True, help="JSON list of candidates, or - for stdin")
    s.add_argument("--owner")
    s.add_argument("--threshold", type=float, default=0.75)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("list")
    s.add_argument("--status", default="open",
                   choices=["open", "done", "stale", "dropped"])
    s.add_argument("--limit", type=int, default=0)
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("close")
    s.add_argument("--id", action="append", required=True)
    s.add_argument("--evidence", default="")
    s.add_argument("--status", default="done", choices=["done", "dropped"])
    s.set_defaults(fn=cmd_close)

    s = sub.add_parser("sweep")
    s.add_argument("--days", type=int, default=30)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_sweep)

    s = sub.add_parser("render")
    s.add_argument("--markdown"); s.add_argument("--html")
    s.add_argument("--cap", type=int); s.add_argument("--owner")
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("merge-state",
                       help="absorb 'done' ticks dropped by another surface")
    s.add_argument("--inbox", help="default <root>/state-inbox")
    s.add_argument("--consume", action="store_true",
                   help="delete each file after merging it")
    s.set_defaults(fn=cmd_merge_state)

    s = sub.add_parser("export",
                       help="write meeting-actions.json for a dashboard")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_export)

    args = p.parse_args()
    args.root = os.path.expanduser(args.root)
    args.fn(args)


if __name__ == "__main__":
    main()
