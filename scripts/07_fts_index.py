"""Phase 7: Full-text search index over raw markdown corpus.

Scans all .md files in data/ta*/ and builds:
  - corpus: regular table with metadata + full text
  - corpus_fts: FTS5 virtual table for full-text search

Usage:
    uv run python scripts/07_fts_index.py

Idempotent — drops and recreates tables on each run.
"""

import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "nice.db"
DATA_PATH = Path(__file__).parent.parent / "data"

PAGE_RE = re.compile(r"<!-- page \d+ -->")
TA_RE = re.compile(r"^ta(\d+)$")
SUFFIX_RE = re.compile(r"_\d+$")


def doc_type_from_filename(filename: str) -> str:
    """FAD.md -> FAD, scope_1.md -> scope, committee_papers_2.md -> committee_papers."""
    stem = Path(filename).stem
    return SUFFIX_RE.sub("", stem)


def count_pages(content: str) -> int:
    return len(PAGE_RE.findall(content))


def create_tables(conn: sqlite3.Connection):
    conn.execute("DROP TABLE IF EXISTS corpus_fts")
    conn.execute("DROP TABLE IF EXISTS corpus")
    conn.executescript("""
        CREATE TABLE corpus (
            id INTEGER PRIMARY KEY,
            ta_number INTEGER NOT NULL,
            doc_type TEXT NOT NULL,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            page_count INTEGER NOT NULL,
            size_bytes INTEGER NOT NULL
        );

        CREATE VIRTUAL TABLE corpus_fts USING fts5(
            ta_number, doc_type, content,
            content=corpus, content_rowid=id
        );
    """)
    conn.commit()


def main():
    md_files = sorted(DATA_PATH.glob("ta*/*.md"))
    print(f"Found {len(md_files)} markdown files")

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    create_tables(conn)

    inserted = 0
    skipped = 0
    total_bytes = 0
    total_pages = 0

    for path in md_files:
        ta_match = TA_RE.match(path.parent.name)
        if not ta_match:
            skipped += 1
            continue

        ta_number = int(ta_match.group(1))
        doc_type = doc_type_from_filename(path.name)
        content = path.read_text(encoding="utf-8", errors="replace")
        size_bytes = path.stat().st_size
        page_count = count_pages(content)

        inserted += 1
        total_bytes += size_bytes
        total_pages += page_count

        conn.execute(
            "INSERT INTO corpus (id, ta_number, doc_type, filename, content, page_count, size_bytes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (inserted, ta_number, doc_type, path.name, content, page_count, size_bytes),
        )

    # Populate FTS index from content table
    conn.execute("INSERT INTO corpus_fts(corpus_fts) VALUES('rebuild')")
    conn.commit()

    # Stats
    ta_count = conn.execute("SELECT COUNT(DISTINCT ta_number) FROM corpus").fetchone()[0]
    doc_types = conn.execute(
        "SELECT doc_type, COUNT(*), SUM(page_count), SUM(size_bytes) "
        "FROM corpus GROUP BY doc_type ORDER BY COUNT(*) DESC"
    ).fetchall()

    print(f"\n{'='*55}")
    print(f" FTS index built")
    print(f"{'='*55}")
    print(f"  Documents indexed:  {inserted:>8}")
    print(f"  Documents skipped:  {skipped:>8}")
    print(f"  TAs covered:        {ta_count:>8}")
    print(f"  Total pages:        {total_pages:>8}")
    print(f"  Total size:         {total_bytes / 1_000_000:>7.1f} MB")
    print(f"\n  {'Doc type':<25s} {'Files':>6} {'Pages':>7} {'MB':>7}")
    print(f"  {'-'*45}")
    for doc_type, count, pages, size in doc_types:
        print(f"  {doc_type:<25s} {count:>6} {pages:>7} {size / 1_000_000:>7.1f}")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
