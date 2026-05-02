"""Phase 3b: Extract large PDFs using split-then-process approach.

Splits large PDFs into 50-page chunks, runs pymupdf4llm on each chunk,
then concatenates. Avoids OOM on 500+ page documents.
"""

import pymupdf
import pymupdf4llm
import time
import tempfile
import shutil
import re
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

DATA_DIR = Path(__file__).parent.parent / "data"
CHUNK_SIZE = 50
WORKERS = 4

STRIP_PATTERNS = [
    re.compile(r"^Page \d+ of \d+\s*$"),
    re.compile(r"^© NICE\b"),
    re.compile(r"^© National Institute"),
    re.compile(r"Subject to Notice of rights"),
    re.compile(r"All rights reserved\. See Notice of Rights"),
    re.compile(r"^Issue date: \w+ \d{4}\s*$"),
]


def strip_boilerplate(text):
    lines = text.split("\n")
    return "\n".join(l for l in lines if not any(p.search(l.strip()) for p in STRIP_PATTERNS))


def extract_large_pdf(pdf_path_str):
    pdf_path = Path(pdf_path_str)
    try:
        doc = pymupdf.open(str(pdf_path))
        total_pages = len(doc)

        chunks_dir = Path(tempfile.mkdtemp())
        chunk_paths = []

        for start in range(0, total_pages, CHUNK_SIZE):
            end = min(start + CHUNK_SIZE, total_pages)
            chunk_doc = pymupdf.open()
            chunk_doc.insert_pdf(doc, from_page=start, to_page=end - 1)
            chunk_path = chunks_dir / f"chunk_{start:04d}.pdf"
            chunk_doc.save(str(chunk_path))
            chunk_doc.close()
            chunk_paths.append((chunk_path, start))

        doc.close()

        all_md_parts = []
        for chunk_path, page_offset in chunk_paths:
            chunks = pymupdf4llm.to_markdown(
                str(chunk_path), page_chunks=True, show_progress=False, use_ocr=False
            )
            for i, chunk in enumerate(chunks):
                page_num = page_offset + i + 1
                all_md_parts.append(f"<!-- page {page_num} -->")
                text = chunk["text"] if isinstance(chunk, dict) else str(chunk)
                all_md_parts.append(strip_boilerplate(text))

        shutil.rmtree(chunks_dir)

        markdown = "\n\n".join(all_md_parts)
        return pdf_path_str, markdown, total_pages

    except Exception as e:
        return pdf_path_str, None, 0


def main():
    all_pdfs = [p for p in DATA_DIR.rglob("*.pdf") if not p.with_suffix(".md").exists()]
    all_pdfs.sort(key=lambda p: p.stat().st_size)

    print(f"Phase 3b: Extracting {len(all_pdfs)} large PDFs ({WORKERS} workers, {CHUNK_SIZE}-page chunks)")
    print("=" * 50)

    extracted = 0
    failed = 0
    total_pages = 0
    failed_files = []
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        futures = {executor.submit(extract_large_pdf, str(p)): p for p in all_pdfs}

        for future in as_completed(futures):
            pdf_path = futures[future]
            try:
                path_str, markdown, page_count = future.result()
                if markdown:
                    Path(path_str).with_suffix(".md").write_text(markdown)
                    extracted += 1
                    total_pages += page_count
                else:
                    failed += 1
                    failed_files.append(str(pdf_path))
            except Exception as e:
                failed += 1
                failed_files.append(f"{pdf_path}: {e}")

            done = extracted + failed
            if done % 10 == 0:
                elapsed = time.time() - start_time
                rate = done / elapsed if elapsed > 0 else 0
                eta = (len(all_pdfs) - done) / rate if rate > 0 else 0
                print(f"  Progress: {done}/{len(all_pdfs)} | extracted: {extracted} | failed: {failed} | pages: {total_pages} | ETA: {eta/60:.0f}m")

    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("EXTRACTION COMPLETE")
    print("=" * 50)
    print(f"\nExtracted: {extracted}")
    print(f"Failed: {failed}")
    print(f"Total pages: {total_pages}")
    print(f"Time: {elapsed:.0f}s ({elapsed/60:.1f}m)")

    if failed_files:
        print(f"\nFailures:")
        for f in failed_files[:20]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
