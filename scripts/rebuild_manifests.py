#!/usr/bin/env python3
"""Regenerate every skill MANIFEST.json from the files on disk.

A MANIFEST.json is the baseline a customization diff compares against: it lets a
skill tell an installed copy apart from the shipped one. When it drifts, the diff
compares against a file that has already moved and silently reports no change,
which is worse than having no manifest at all. That drift has happened, so
validate.py now fails on it and this script is the fix.

Run after editing any file a manifest tracks:
    python3 scripts/rebuild_manifests.py            # rewrite all
    python3 scripts/rebuild_manifests.py --check     # report drift, change nothing

The version field is read from the sibling VERSION file when one exists, so this
never invents a version number.
"""
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHECK = "--check" in sys.argv
drift = []
written = []

for man in sorted(glob.glob("**/MANIFEST.json", recursive=True)):
    if man.startswith("archive" + os.sep):
        continue
    base = os.path.dirname(man)
    doc = json.load(open(man, encoding="utf-8"))
    tracked = sorted(doc.get("files", {}))
    if not tracked:
        continue

    version_file = os.path.join(base, "VERSION")
    if os.path.exists(version_file):
        doc["version"] = open(version_file, encoding="utf-8").read().strip()

    files = {}
    for rel in tracked:
        path = os.path.join(base, rel)
        if not os.path.exists(path):
            drift.append(f"{man} -> {rel} is tracked but missing on disk")
            continue
        blob = open(path, "rb").read()
        digest = hashlib.sha256(blob).hexdigest()
        old = doc["files"].get(rel, {})
        if old.get("sha256") != digest or old.get("bytes") != len(blob):
            drift.append(
                f"{man} -> {rel} (disk {len(blob)}B, manifest {old.get('bytes')}B)"
            )
        files[rel] = {"bytes": len(blob), "sha256": digest}

    doc["files"] = files
    if not CHECK:
        with open(man, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1)
            fh.write("\n")
        written.append(man)

if drift:
    print("DRIFT:" if CHECK else "REBUILT (was drifting):")
    for d in drift:
        print("  -", d)
else:
    print("All manifests already matched their files.")

if written:
    print("\nWrote:")
    for w in written:
        print("  -", w)

sys.exit(1 if (CHECK and drift) else 0)
