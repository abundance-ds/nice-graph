"""Phase 5: Extract triplets from chunks using LLM.

Three modes:
  test   — Process N chunks via real-time API (validate format, estimate costs)
  batch  — Submit all pending chunks to Anthropic Message Batches API (50% off)
  poll   — Check batch status and download results when ready
  status — Show extraction progress

Usage:
    # Test with 100 chunks (real-time API, validates everything works)
    uv run python scripts/05_tag.py test --n 100

    # Submit all pending to batch API
    uv run python scripts/05_tag.py batch

    # Poll batch status / download results
    uv run python scripts/05_tag.py poll

    # Check progress
    uv run python scripts/05_tag.py status

    # Retry failed chunks
    uv run python scripts/05_tag.py batch --retry
"""

import argparse
import asyncio
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "nice.db"
PROMPT_PATH = Path(__file__).parent.parent / "ontology" / "extraction_prompt.md"
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 4096

import importlib.util
_spec = importlib.util.spec_from_file_location("extraction_tools", Path(__file__).parent / "extraction_tools.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
TOOLS = _mod.TOOLS


def get_system_prompt():
    return PROMPT_PATH.read_text()


def build_user_message(ta_number, doc_type, page_start, page_end, text):
    return (
        f"TA number: TA{ta_number}\n"
        f"Document type: {doc_type}\n"
        f"Pages: {page_start}-{page_end}\n\n"
        f"---\n\n"
        f"{text}"
    )


def parse_tool_response(response):
    """Extract tool call from API response. Returns (parsed_dict, error_string)."""
    for block in response.content:
        if block.type == "tool_use":
            if block.name == "report_no_content":
                return {"no_relevant_content": True}, None
            return block.input, None
    return None, "No tool call in response"


def get_conn():
    return sqlite3.connect(str(DB_PATH))


def print_status():
    conn = get_conn()
    fad_total = conn.execute("SELECT COUNT(*) FROM chunks WHERE doc_type='FAD'").fetchone()[0]
    rows = conn.execute(
        "SELECT status, COUNT(*) FROM chunks WHERE doc_type='FAD' GROUP BY status ORDER BY status"
    ).fetchall()
    total = sum(r[1] for r in rows)

    print(f"\nFAD chunks ({fad_total} total):")
    print(f"{'Status':<15} {'Count':>8} {'%':>7}")
    print("-" * 32)
    for status, cnt in rows:
        print(f"{status:<15} {cnt:>8} {cnt/total*100:>6.1f}%")
    print(f"{'TOTAL':<15} {total:>8}")

    done = sum(r[1] for r in rows if r[0] == "done")
    no_content = conn.execute(
        "SELECT COUNT(*) FROM chunks WHERE doc_type='FAD' AND status='done' AND json_extract(result, '$.no_relevant_content') = 1"
    ).fetchone()[0]
    print(f"\nCompleted: {done} ({no_content} no-content, {done - no_content} with extractions)")

    errors = conn.execute(
        "SELECT error, COUNT(*) FROM chunks WHERE doc_type='FAD' AND status='error' GROUP BY error ORDER BY COUNT(*) DESC LIMIT 5"
    ).fetchall()
    if errors:
        print(f"\nTop errors:")
        for err, cnt in errors:
            print(f"  [{cnt}x] {err[:120]}")

    batch_ids = conn.execute(
        "SELECT DISTINCT batch_id FROM chunks WHERE batch_id IS NOT NULL"
    ).fetchall()
    if batch_ids:
        print(f"\nBatch IDs: {', '.join(r[0] for r in batch_ids)}")

    conn.close()


# --- TEST MODE: real-time API for validation ---

async def cmd_test(args):
    try:
        import anthropic
    except ImportError:
        print("Install: uv add anthropic")
        sys.exit(1)

    conn = get_conn()
    conn.execute("ALTER TABLE chunks ADD COLUMN batch_id TEXT") if "batch_id" not in [
        r[1] for r in conn.execute("PRAGMA table_info(chunks)").fetchall()
    ] else None
    conn.commit()

    pending = conn.execute(
        "SELECT id, ta_number, doc_type, page_start, page_end, text FROM chunks WHERE status='pending' AND doc_type='FAD' ORDER BY id LIMIT ?",
        (args.n,),
    ).fetchall()

    if not pending:
        print("No pending chunks.")
        print_status()
        return

    print(f"Testing {len(pending)} chunks via real-time API ({MODEL})")
    system_prompt = get_system_prompt()
    client = anthropic.AsyncAnthropic()
    semaphore = asyncio.Semaphore(20)

    done = 0
    errors = 0
    empty = 0
    total_input = 0
    total_output = 0
    start = time.time()

    async def process_one(row):
        nonlocal done, errors, empty, total_input, total_output
        chunk_id, ta_number, doc_type, page_start, page_end, text = row

        async with semaphore:
            try:
                resp = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=system_prompt,
                    tools=TOOLS,
                    tool_choice={"type": "any"},
                    messages=[{"role": "user", "content": build_user_message(ta_number, doc_type, page_start, page_end, text)}],
                )
                total_input += resp.usage.input_tokens
                total_output += resp.usage.output_tokens

                parsed, err = parse_tool_response(resp)
                if err:
                    conn.execute("UPDATE chunks SET status='error', error=? WHERE id=?", (err, chunk_id))
                    errors += 1
                else:
                    conn.execute("UPDATE chunks SET status='done', result=? WHERE id=?", (json.dumps(parsed), chunk_id))
                    if parsed.get("no_relevant_content"):
                        empty += 1
                    done += 1
            except Exception as e:
                conn.execute("UPDATE chunks SET status='error', error=? WHERE id=?", (str(e)[:500], chunk_id))
                errors += 1
            conn.commit()

    await asyncio.gather(*[process_one(r) for r in pending])

    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.0f}s: {done} ok, {empty} no-content, {errors} errors")
    print(f"Tokens: {total_input:,} input + {total_output:,} output = {total_input+total_output:,} total")
    if done + errors > 0:
        avg_in = total_input / (done + errors)
        avg_out = total_output / (done + errors)
        remaining = conn.execute("SELECT COUNT(*) FROM chunks WHERE status='pending' AND doc_type='FAD'").fetchone()[0]
        est_in = remaining * avg_in
        est_out = remaining * avg_out
        batch_cost = (est_in / 1e6) * 0.40 + (est_out / 1e6) * 2.00
        print(f"\nProjected for remaining {remaining:,} chunks (Haiku 3.5 batch):")
        print(f"  Input: {est_in/1e6:.0f}M tokens, Output: {est_out/1e6:.0f}M tokens")
        print(f"  Estimated cost: ${batch_cost:.0f}")
    print_status()
    conn.close()


# --- BATCH MODE: Anthropic Message Batches API ---

def cmd_batch(args):
    try:
        import anthropic
    except ImportError:
        print("Install: uv add anthropic")
        sys.exit(1)

    conn = get_conn()
    for col, typ in [("batch_id", "TEXT")]:
        if col not in [r[1] for r in conn.execute("PRAGMA table_info(chunks)").fetchall()]:
            conn.execute(f"ALTER TABLE chunks ADD COLUMN {col} {typ}")
            conn.commit()

    if args.retry:
        n = conn.execute("UPDATE chunks SET status='pending', batch_id=NULL WHERE status='error'").rowcount
        conn.commit()
        print(f"Reset {n} error chunks to pending.")

    pending = conn.execute(
        "SELECT id, ta_number, doc_type, page_start, page_end, text FROM chunks WHERE status='pending' AND doc_type='FAD' ORDER BY id"
    ).fetchall()

    if not pending:
        print("No pending chunks.")
        print_status()
        return

    print(f"Preparing batch of {len(pending)} chunks...")
    system_prompt = get_system_prompt()
    client = anthropic.Anthropic()

    # Anthropic batch limit: 100K requests or 256MB per batch
    BATCH_SIZE = 50_000
    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch_rows = pending[batch_start:batch_start + BATCH_SIZE]

        requests = []
        for chunk_id, ta_number, doc_type, page_start, page_end, text in batch_rows:
            requests.append({
                "custom_id": f"chunk_{chunk_id}",
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": system_prompt,
                    "tools": TOOLS,
                    "tool_choice": {"type": "any"},
                    "messages": [{
                        "role": "user",
                        "content": build_user_message(ta_number, doc_type, page_start, page_end, text),
                    }],
                },
            })

        print(f"Submitting batch {batch_start // BATCH_SIZE + 1} ({len(requests)} requests)...")
        result = client.messages.batches.create(requests=requests)
        batch_id = result.id

        chunk_ids = [r[0] for r in batch_rows]
        for cid in chunk_ids:
            conn.execute("UPDATE chunks SET status='submitted', batch_id=? WHERE id=?", (batch_id, cid))
        conn.commit()

        print(f"  Batch submitted: {batch_id}")
        print(f"  Status: {result.processing_status}")
        print(f"  Requests: {len(requests)}")

    print(f"\nAll batches submitted. Use 'poll' to check status and download results.")
    conn.close()


def cmd_poll(args):
    try:
        import anthropic
    except ImportError:
        print("Install: uv add anthropic")
        sys.exit(1)

    conn = get_conn()
    batch_ids = [r[0] for r in conn.execute(
        "SELECT DISTINCT batch_id FROM chunks WHERE batch_id IS NOT NULL AND status='submitted' AND doc_type='FAD'"
    ).fetchall()]

    if not batch_ids:
        print("No submitted batches to poll.")
        print_status()
        return

    client = anthropic.Anthropic()

    for batch_id in batch_ids:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        print(f"\nBatch {batch_id}: {batch.processing_status}")
        print(f"  processing={counts.processing} succeeded={counts.succeeded} errored={counts.errored} "
              f"canceled={counts.canceled} expired={counts.expired}")

        if batch.processing_status != "ended":
            print(f"  Still processing. Check back later.")
            continue

        print(f"  Downloading results...")
        downloaded = 0
        errors = 0

        for result in client.messages.batches.results(batch_id):
            custom_id = result.custom_id
            chunk_id = int(custom_id.replace("chunk_", ""))

            if result.result.type == "succeeded":
                msg = result.result.message
                parsed, err = parse_tool_response(msg)

                if err:
                    conn.execute(
                        "UPDATE chunks SET status='error', error=? WHERE id=?",
                        (err, chunk_id),
                    )
                    errors += 1
                else:
                    conn.execute(
                        "UPDATE chunks SET status='done', result=? WHERE id=?",
                        (json.dumps(parsed), chunk_id),
                    )
                    downloaded += 1
            elif result.result.type == "errored":
                err_msg = str(result.result.error)[:500] if hasattr(result.result, 'error') else "batch_error"
                conn.execute(
                    "UPDATE chunks SET status='error', error=? WHERE id=?",
                    (err_msg, chunk_id),
                )
                errors += 1
            elif result.result.type in ("expired", "canceled"):
                conn.execute(
                    "UPDATE chunks SET status='pending', batch_id=NULL WHERE id=?",
                    (chunk_id,),
                )

        conn.commit()
        print(f"  Downloaded: {downloaded} ok, {errors} errors")

    print_status()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Phase 5: Extract triplets from chunks")
    sub = parser.add_subparsers(dest="cmd")

    p_test = sub.add_parser("test", help="Test N chunks via real-time API")
    p_test.add_argument("--n", type=int, default=100)

    p_batch = sub.add_parser("batch", help="Submit all pending to batch API")
    p_batch.add_argument("--retry", action="store_true", help="Reset errors to pending first")

    p_poll = sub.add_parser("poll", help="Check batch status and download results")

    sub.add_parser("status", help="Show progress")

    args = parser.parse_args()

    if args.cmd == "test":
        asyncio.run(cmd_test(args))
    elif args.cmd == "batch":
        cmd_batch(args)
    elif args.cmd == "poll":
        cmd_poll(args)
    elif args.cmd == "status":
        print_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
