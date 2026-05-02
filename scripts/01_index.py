"""Phase 1: Index all NICE Technology Appraisals.

Scrapes the NICE published guidance listing (Next.js JSON API) to get all TAs,
then fetches history.json per TA to identify documents and their download URLs.
Stores everything in SQLite.
"""

import httpx
import sqlite3
import json
import time
import re
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "nice.db"
BASE_URL = "https://www.nice.org.uk"

def get_build_id(client: httpx.Client) -> str:
    """Extract Next.js buildId from the published guidance page."""
    resp = client.get(f"{BASE_URL}/guidance/published?type=ta")
    resp.raise_for_status()
    match = re.search(r'"buildId":"([^"]+)"', resp.text)
    if not match:
        raise RuntimeError("Could not find buildId in page HTML")
    return match.group(1)

def init_db() -> sqlite3.Connection:
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tas (
            ta_number INTEGER PRIMARY KEY,
            title TEXT,
            drug TEXT,
            indication TEXT,
            decision TEXT,
            publication_date TEXT,
            last_updated TEXT,
            status TEXT,
            committee TEXT,
            url TEXT,
            raw_json JSON
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER REFERENCES tas(ta_number),
            doc_type TEXT,
            title TEXT,
            download_url TEXT,
            file_size INTEGER,
            pdf_path TEXT,
            markdown_path TEXT,
            page_count INTEGER,
            group_title TEXT,
            raw_json JSON
        )
    """)
    conn.commit()
    return conn

def fetch_ta_listing(client: httpx.Client, build_id: str) -> list[dict]:
    """Paginate through the TA listing and return all TA records."""
    all_tas = []
    page = 1
    while True:
        url = f"{BASE_URL}/_next/data/{build_id}/guidance/published.json"
        params = {
            "ngt": "Technology appraisal guidance",
            "ndt": "Guidance",
            "ps": "50",
            "pa": str(page),
        }
        resp = client.get(url, params=params)
        if resp.status_code != 200:
            print(f"  Page {page}: HTTP {resp.status_code}, stopping pagination")
            break

        data = resp.json()
        documents = data.get("pageProps", {}).get("results", {}).get("documents", [])
        if not documents:
            break

        all_tas.extend(documents)
        print(f"  Page {page}: {len(documents)} TAs (total: {len(all_tas)})")

        # Check for next page
        pager = data.get("pageProps", {}).get("results", {}).get("pagerLinks", {})
        if not pager.get("next"):
            break

        page += 1
        time.sleep(0.5)

    return all_tas

def parse_ta_number(guidance_ref: str) -> int | None:
    """Extract TA number from guidance reference like 'TA1149'."""
    match = re.match(r"TA(\d+)", guidance_ref)
    return int(match.group(1)) if match else None

def classify_document(title: str, url: str) -> str | None:
    """Classify a document by type based on its title/URL. Returns None to skip."""
    t = title.lower()
    u = url.lower() if url else ""

    if "final appraisal" in t or "fad" in u:
        return "FAD"
    if "appraisal consultation document" in t or ("acd" in u and "comment" not in t):
        return "ACD"
    if "scope" in t and "comment" in t and "response" in t:
        return "scope_comments"
    if "scope" in t and "comment" not in t and "stakeholder" not in t:
        return "scope"
    if "committee papers" in t or "committee paper" in t:
        return "committee_papers"
    if "evaluation report" in t:
        return "evaluation_report"

    return None

def fetch_ta_history(client: httpx.Client, build_id: str, ta_number: int) -> list[dict]:
    """Fetch history.json for a TA and return classified documents."""
    url = f"{BASE_URL}/_next/data/{build_id}/guidance/ta{ta_number}/history.json"
    resp = client.get(url)

    if resp.status_code != 200:
        return []

    data = resp.json()
    project = data.get("pageProps", {}).get("project", {})
    groups = project.get("groups", [])

    documents = []
    for group in groups:
        group_title = group.get("title", "")
        for sub_group in group.get("subGroups", []):
            for link in sub_group.get("resourceLinks", []):
                item_title = link.get("title", "")
                item_url = link.get("href", "")
                file_size = link.get("fileSize")

                doc_type = classify_document(item_title, item_url)
                if doc_type and item_url:
                    full_url = item_url if item_url.startswith("http") else f"{BASE_URL}{item_url}"
                    documents.append({
                        "title": item_title,
                        "doc_type": doc_type,
                        "download_url": full_url,
                        "file_size": file_size,
                        "group_title": group_title,
                        "raw": link,
                    })

    return documents

def main():
    conn = init_db()

    print("Phase 1: Indexing NICE Technology Appraisals")
    print("=" * 50)

    with httpx.Client(
        timeout=30,
        headers={"User-Agent": "NICE-KG-Research/1.0 (academic research)"},
        follow_redirects=True,
    ) as client:
        # Step 1: Get buildId
        print("\n[1/3] Extracting buildId...")
        build_id = get_build_id(client)
        print(f"  buildId: {build_id}")

        # Step 2: Fetch TA listing
        print("\n[2/3] Fetching TA listing...")
        ta_list = fetch_ta_listing(client, build_id)
        print(f"  Total TAs found: {len(ta_list)}")

        # Store TAs in DB
        for ta in ta_list:
            ta_num = parse_ta_number(ta.get("guidanceRef", ""))
            if ta_num is None:
                continue
            def to_str(val):
                if val is None:
                    return ""
                if isinstance(val, list):
                    return val[0] if val else ""
                return str(val)

            conn.execute("""
                INSERT OR REPLACE INTO tas (ta_number, title, publication_date, last_updated, status, url, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ta_num,
                to_str(ta.get("title")),
                to_str(ta.get("publicationDate")),
                to_str(ta.get("lastUpdated")),
                to_str(ta.get("guidanceStatus")),
                to_str(ta.get("pathAndQuery")),
                json.dumps(ta),
            ))
        conn.commit()

        stored_count = conn.execute("SELECT COUNT(*) FROM tas").fetchone()[0]
        print(f"  Stored {stored_count} TAs in database")

        # Step 3: Fetch history for each TA
        print("\n[3/3] Fetching document history per TA...")
        ta_numbers = [r[0] for r in conn.execute("SELECT ta_number FROM tas ORDER BY ta_number").fetchall()]

        total_docs = 0
        errors = 0
        for i, ta_num in enumerate(ta_numbers):
            docs = fetch_ta_history(client, build_id, ta_num)

            for doc in docs:
                conn.execute("""
                    INSERT INTO documents (ta_number, doc_type, title, download_url, file_size, group_title, raw_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    ta_num,
                    doc["doc_type"],
                    doc["title"],
                    doc["download_url"],
                    doc.get("file_size"),
                    doc["group_title"],
                    json.dumps(doc["raw"]),
                ))
                total_docs += 1

            if not docs:
                errors += 1

            if (i + 1) % 50 == 0:
                conn.commit()
                print(f"  Progress: {i+1}/{len(ta_numbers)} TAs processed, {total_docs} docs found")

            time.sleep(0.5)

        conn.commit()

    # Summary
    print("\n" + "=" * 50)
    print("INDEXING COMPLETE")
    print("=" * 50)

    print(f"\nTAs indexed: {stored_count}")
    print(f"Documents found: {total_docs}")
    print(f"TAs with no documents: {errors}")

    print("\nDocuments by type:")
    for row in conn.execute("SELECT doc_type, COUNT(*) FROM documents GROUP BY doc_type ORDER BY COUNT(*) DESC"):
        print(f"  {row[0]}: {row[1]}")

    print(f"\nDatabase: {DB_PATH}")
    conn.close()

if __name__ == "__main__":
    main()
