"""Phase 2: Download all indexed NICE TA documents (parallel).

Downloads PDFs from NICE website, organised by TA number and document type.
5 concurrent requests. Skips already-downloaded files for resume capability.

URL pattern: history JSON gives hrefs like /guidance/ta900/history/downloads/TA900-slug.pdf
Actual working URL: /guidance/ta{N}/documents/{slug}
"""

import httpx
import asyncio
import sqlite3
import json
import re
import time
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "nice.db"
DATA_DIR = Path(__file__).parent.parent / "data"
BASE_URL = "https://www.nice.org.uk"
CONCURRENCY = 5

def href_to_download_url(href: str, ta_number: int) -> str | None:
    if not href or "/html-content" in href or "/consultations/" in href:
        return None
    match = re.search(r'/history/downloads/TA\d+-(.+?)\.pdf$', href)
    if match:
        slug = match.group(1)
        return f"{BASE_URL}/guidance/ta{ta_number}/documents/{slug}"
    if href.startswith("http"):
        return href
    return f"{BASE_URL}{href}"

class Stats:
    def __init__(self):
        self.downloaded = 0
        self.skipped = 0
        self.failed = 0
        self.total_bytes = 0
        self.failed_urls: list[str] = []
        self.lock = asyncio.Lock()

async def download_doc(client: httpx.AsyncClient, doc: dict, stats: Stats, semaphore: asyncio.Semaphore):
    ta_num = doc["ta_number"]
    doc_type = doc["doc_type"]
    raw = json.loads(doc["raw_json"])
    href = raw.get("href", "")
    url = href_to_download_url(href, ta_num)

    if not url:
        async with stats.lock:
            stats.skipped += 1
        return

    ta_dir = DATA_DIR / f"ta{ta_num}"
    ta_dir.mkdir(parents=True, exist_ok=True)

    existing = sorted(ta_dir.glob(f"{doc_type}*.pdf"))
    if existing:
        suffix = f"_{len(existing)}"
        filename = f"{doc_type}{suffix}.pdf"
    else:
        filename = f"{doc_type}.pdf"

    filepath = ta_dir / filename

    if filepath.exists() and filepath.stat().st_size > 0:
        async with stats.lock:
            stats.skipped += 1
        return

    async with semaphore:
        try:
            resp = await client.get(url)
            content_type = resp.headers.get("content-type", "")

            if resp.status_code == 200 and "pdf" in content_type and len(resp.content) > 100:
                filepath.write_bytes(resp.content)
                async with stats.lock:
                    stats.downloaded += 1
                    stats.total_bytes += len(resp.content)
            else:
                async with stats.lock:
                    stats.failed += 1
                    stats.failed_urls.append(f"TA{ta_num} {doc_type}: {url} [{resp.status_code}]")
        except Exception as e:
            async with stats.lock:
                stats.failed += 1
                stats.failed_urls.append(f"TA{ta_num} {doc_type}: {url} [ERROR: {e}]")

async def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    docs = conn.execute("""
        SELECT id, ta_number, doc_type, title, download_url, file_size, raw_json
        FROM documents
        WHERE download_url IS NOT NULL AND download_url != ''
        ORDER BY ta_number DESC, doc_type
    """).fetchall()

    total = len(docs)
    print(f"Phase 2: Downloading {total} documents ({CONCURRENCY} concurrent)")
    print("=" * 50)

    stats = Stats()
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient(
        timeout=60,
        headers={"User-Agent": "NICE-KG-Research/1.0 (academic research)"},
        follow_redirects=True,
        limits=httpx.Limits(max_connections=CONCURRENCY + 2),
    ) as client:
        # Process in batches of 50 for progress reporting
        batch_size = 50
        for batch_start in range(0, total, batch_size):
            batch = docs[batch_start:batch_start + batch_size]
            tasks = [download_doc(client, dict(d), stats, semaphore) for d in batch]
            await asyncio.gather(*tasks)

            mb = stats.total_bytes / (1024 * 1024)
            processed = batch_start + len(batch)
            print(f"  Progress: {processed}/{total} | downloaded: {stats.downloaded} | skipped: {stats.skipped} | failed: {stats.failed} | {mb:.0f} MB")

    conn.close()

    # Summary
    mb = stats.total_bytes / (1024 * 1024)
    print("\n" + "=" * 50)
    print("DOWNLOAD COMPLETE")
    print("=" * 50)
    print(f"\nTotal processed: {total}")
    print(f"Downloaded: {stats.downloaded}")
    print(f"Skipped (exists/non-PDF): {stats.skipped}")
    print(f"Failed: {stats.failed}")
    print(f"Total size: {mb:.1f} MB ({mb/1024:.2f} GB)")
    print(f"\nData directory: {DATA_DIR}")

    if stats.failed_urls:
        print(f"\nFirst 30 failures:")
        for f in stats.failed_urls[:30]:
            print(f"  {f}")

if __name__ == "__main__":
    asyncio.run(main())
