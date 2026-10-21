"""
One-off collection script for Milestone 4. Pulls comments from a handful of
r/nba threads via the public comments RSS feed (no auth needed), cleans the
HTML, dedupes, and writes raw candidates to data/raw_comments.csv.

Timeboxed per the project's own guidance ("if you write a scraper, timebox
it"). This is a single run, not a maintained pipeline.
"""
import csv
import html
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
NS = {"a": "http://www.w3.org/2005/Atom"}
CACHE_DIR = "data/raw_rss"

# A spread of recent r/nba threads: post-game threads (analysis-heavy),
# a fight/reaction thread, an AMA (Q&A, different register), and the daily
# discussion thread (mixed bag). Picked for text variety, not virality.
THREAD_IDS = [
    "1xbasxs",  # Post Game Thread: 76ers def. Knicks (cached, already fetched)
    "1xb54yp",  # Post Game Thread: Pistons comeback
    "1xbdksi",  # Post Game Thread: Thunder def. Spurs
    "1xao1jr",  # Daily Discussion Thread
    "1xa7g1g",  # Jeremy Lin AMA
    "1xbb9rt",  # Fight Ensues Between Spurs & Thunder
]


def fetch_with_retry(thread_id, max_retries=3):
    cache_path = os.path.join(CACHE_DIR, f"{thread_id}.rss")
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return f.read()

    url = f"https://www.reddit.com/r/nba/comments/{thread_id}/.rss?limit=200"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(cache_path, "wb") as f:
                f.write(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait = 60 * (attempt + 1)
                print(f"  429 on {thread_id}, waiting {wait}s before retry...")
                time.sleep(wait)
                continue
            print(f"  FAILED {thread_id}: {e}")
            return None
        except Exception as e:
            print(f"  FAILED {thread_id}: {e}")
            return None
    return None


def parse_comments(data):
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print(f"  PARSE FAILED: {e}")
        return []

    entries = root.findall("a:entry", NS)
    out = []
    for e in entries:
        content = e.find("a:content", NS)
        raw = content.text if content is not None else ""
        text = re.sub("<[^<]+?>", " ", raw or "")
        text = html.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        out.append(text)
    return out


def is_usable(text):
    if not text:
        return False
    low = text.lower()
    if low in ("[removed]", "[deleted]"):
        return False
    if "submitted by" in low and len(text) < 80:
        return False
    if len(text.split()) < 6:
        return False
    return True


def main():
    seen = set()
    rows = []
    for i, tid in enumerate(THREAD_IDS):
        cached = os.path.exists(os.path.join(CACHE_DIR, f"{tid}.rss"))
        print(f"Fetching thread {tid} ({i+1}/{len(THREAD_IDS)}){' [cached]' if cached else ''}...")
        data = fetch_with_retry(tid)
        if data is None:
            continue
        comments = parse_comments(data)
        kept = 0
        for c in comments:
            if not is_usable(c):
                continue
            if c in seen:
                continue
            seen.add(c)
            rows.append({"text": c, "source_thread": tid})
            kept += 1
        print(f"  kept {kept} new comments (total so far: {len(rows)})")
        if not cached and i < len(THREAD_IDS) - 1:
            print("  sleeping 60s to stay under rate limit...")
            time.sleep(60)

    with open("data/raw_comments.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["text", "source_thread"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {len(rows)} raw candidate comments to data/raw_comments.csv")


if __name__ == "__main__":
    main()
