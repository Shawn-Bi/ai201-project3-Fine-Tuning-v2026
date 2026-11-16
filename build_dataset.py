"""Build data/raw_posts.txt from data/links.txt via the Arctic Shift API."""
import re
import sys
from pathlib import Path

import json
import urllib.parse
import urllib.request

ROOT = Path(__file__).parent
LINKS = ROOT / "data" / "links.txt"
OUT = ROOT / "data" / "raw_posts.txt"
API = "https://arctic-shift.photon-reddit.com/api/posts/ids"
BATCH = 40

link_re = re.compile(r"\[(.*)\]\((\S+?)\)\s*$")
id_re = re.compile(r"/comments/([A-Za-z0-9]+)")


def main():
    ids, urls = [], {}
    dup = bad = 0
    for line in LINKS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        m = link_re.search(line.strip())
        i = id_re.search(m.group(2)) if m else None
        if not i:
            bad += 1
            continue
        pid = i.group(1)
        if pid in urls:
            dup += 1
            continue
        urls[pid] = m.group(2)
        ids.append(pid)

    fetched = {}
    for n in range(0, len(ids), BATCH):
        chunk = ids[n:n + BATCH]
        try:
            url = API + "?" + urllib.parse.urlencode({"ids": ",".join(chunk)}, safe=",")
            req = urllib.request.Request(url, headers={"User-Agent": "takemeter-class-project/1.0 (student dataset)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r).get("data", [])
        except Exception as e:
            sys.exit(f"API error on batch starting at index {n}: {e!r}")
        for p in data:
            fetched[p["id"]] = p

    saved = 0
    empty = missing = 0
    blocks = []
    for pid in ids:
        p = fetched.get(pid)
        if p is None:
            missing += 1
            continue
        body = p.get("selftext") or ""
        if body.strip() in ("", "[removed]", "[deleted]"):
            empty += 1
            continue
        blocks.append(f"TITLE: {p.get('title', '')}\nBODY: {body}\nURL: {urls[pid]}\n===\n")
        saved += 1

    OUT.write_text("".join(blocks), encoding="utf-8")
    print(f"Saved: {saved}")
    print(f"Skipped: {dup + bad + empty + missing}")
    print(f"  duplicate IDs: {dup}")
    print(f"  unparseable lines: {bad}")
    print(f"  empty/[removed]/[deleted] selftext: {empty}")
    print(f"  not returned by API: {missing}")


if __name__ == "__main__":
    main()
