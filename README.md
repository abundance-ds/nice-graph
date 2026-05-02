# NICE Appraisals

Knowledge graph and full-text corpus of [NICE Technology Appraisals](https://www.nice.org.uk/guidance/published?ngt=Technology+appraisal+guidance).

826 TAs · 3,307 documents · 555 with structured entity extraction.

**[nice.shoulde.rs](https://nice.shoulde.rs)**

## AI / API access

Point your agent at `https://nice.shoulde.rs/llms.txt` for a machine-readable overview and API guide.

| Endpoint | Description |
|----------|-------------|
| `GET /llms.txt` | Project overview and API guide for AI agents |
| `GET /llms-full.txt` | Full corpus index (826 TAs with document counts) |
| `GET /api/search?q={query}&format=plain` | Full-text search across 3,307 documents |
| `GET /api/corpus/ta{N}/` | Document listing for a TA |
| `GET /api/corpus/ta{N}/{doc}.md` | Raw markdown with `<!-- page N -->` markers |
| `POST /api/chat` | Natural language → SQL → answer (SSE stream) |

## What's in the graph

555 TAs have structured extraction from Final Appraisal Documents:

| Entity | Count |
|--------|-------|
| Drugs | 572 |
| Conditions | 1,298 |
| Methodological decisions | 9,509 (23 categories) |
| Evidence gaps | 3,658 |
| Comparators | 2,769 |
| Clinical trials | 2,206 |
| Cross-references | 952 |
| ICER bands | 926 |
| Economic models | 675 |
| Commercial arrangements | 413 |

Each methodological decision captures the company position, ERG position, and committee preference.

## Pipeline

| Script | Step |
|--------|------|
| `scripts/01_index.py` | Scrape NICE website for all TA listings |
| `scripts/02_download.py` | Download PDFs |
| `scripts/03_extract.py` | PDF → markdown with page markers |
| `scripts/04_chunk.py` | Split into 10-page overlapping windows |
| `scripts/05_tag.py` | AI extraction via Claude Haiku tool calling |
| `scripts/06_resolve.py` | Entity resolution and graph construction |
| `scripts/07_fts_index.py` | Build FTS5 search index |
| `scripts/08_build_downloads.py` | Package corpus archives |

## Run locally

**Pipeline** (rebuilds from scratch):

```bash
uv sync
ANTHROPIC_API_KEY=sk-... uv run python scripts/01_index.py
# ... through 08
```

**Web app** (requires `nice.db` and `data/` from the pipeline):

```bash
cd web
npm install
NUXT_ANTHROPIC_API_KEY=sk-... npx nuxi dev
```

## Ontology

Extraction schema developed over 5 rounds across 50 TAs. Two independent AI agents proposed ontologies from 20 TAs, merged and refined iteratively. 9 entity types, 23 methodological decision categories, 8 ICER bands.

See [`ontology/methods.md`](ontology/methods.md).

## License

MIT
