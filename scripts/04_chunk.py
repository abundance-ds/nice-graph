"""Phase 4: Chunk markdown files into 10-page windows for extraction.

Reads all .md files in data/, splits on <!-- page N --> markers,
creates overlapping chunks, stores in SQLite chunks table.
Resume-safe: skips documents already chunked.
"""

import re
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = Path(__file__).parent.parent / "nice.db"

CHUNK_PAGES = 10
OVERLAP_PAGES = 2


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ta_number INTEGER,
            doc_type TEXT,
            page_start INTEGER,
            page_end INTEGER,
            text TEXT,
            status TEXT DEFAULT 'pending',
            result JSON,
            error TEXT
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_chunks_status ON chunks(status)
    """)
    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_chunks_unique
        ON chunks(ta_number, doc_type, page_start)
    """)
    conn.commit()


def split_by_page_markers(text):
    """Split markdown text into pages using <!-- page N --> markers."""
    pattern = re.compile(r"<!-- page (\d+) -->")
    pages = []
    current_page_num = None
    current_lines = []

    for line in text.split("\n"):
        m = pattern.match(line.strip())
        if m:
            if current_page_num is not None:
                pages.append((current_page_num, "\n".join(current_lines)))
            current_page_num = int(m.group(1))
            current_lines = []
        else:
            current_lines.append(line)

    if current_page_num is not None:
        pages.append((current_page_num, "\n".join(current_lines)))

    return pages


def chunk_pages(pages, chunk_size, overlap):
    """Create overlapping chunks from a list of (page_num, text) tuples."""
    step = chunk_size - overlap
    chunks = []
    for i in range(0, len(pages), step):
        window = pages[i:i + chunk_size]
        if not window:
            break
        page_start = window[0][0]
        page_end = window[-1][0]
        text = "\n\n".join(f"<!-- page {pn} -->\n{pt}" for pn, pt in window)
        chunks.append((page_start, page_end, text))
    return chunks


def parse_ta_and_doctype(md_path):
    """Extract ta_number and doc_type from path like data/ta310/FAD.md."""
    ta_match = re.search(r"ta(\d+)", str(md_path))
    if not ta_match:
        return None, None
    ta_number = int(ta_match.group(1))
    doc_type = md_path.stem
    return ta_number, doc_type


def main():
    conn = sqlite3.connect(str(DB_PATH))
    init_db(conn)

    existing = set(
        conn.execute("SELECT ta_number, doc_type FROM chunks GROUP BY ta_number, doc_type").fetchall()
    )

    all_mds = sorted(DATA_DIR.rglob("*.md"))
    skipped = 0
    chunked = 0
    total_chunks = 0
    empty = 0

    print(f"Phase 4: Chunking {len(all_mds)} markdown files ({CHUNK_PAGES}-page windows, {OVERLAP_PAGES}-page overlap)")
    print("=" * 60)

    for md_path in all_mds:
        ta_number, doc_type = parse_ta_and_doctype(md_path)
        if ta_number is None:
            continue

        if (ta_number, doc_type) in existing:
            skipped += 1
            continue

        text = md_path.read_text()
        pages = split_by_page_markers(text)

        if len(pages) < 2:
            empty += 1
            continue

        chunks = chunk_pages(pages, CHUNK_PAGES, OVERLAP_PAGES)

        for page_start, page_end, chunk_text in chunks:
            conn.execute(
                "INSERT OR IGNORE INTO chunks (ta_number, doc_type, page_start, page_end, text) VALUES (?, ?, ?, ?, ?)",
                (ta_number, doc_type, page_start, page_end, chunk_text),
            )

        conn.commit()
        chunked += 1
        total_chunks += len(chunks)

        if chunked % 100 == 0:
            print(f"  Chunked: {chunked} docs | {total_chunks} chunks | skipped: {skipped}")

    print(f"\nDone: {chunked} docs → {total_chunks} chunks | skipped: {skipped} | empty: {empty}")

    row = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()
    print(f"Total chunks in DB: {row[0]}")
    conn.close()


if __name__ == "__main__":
    main()
