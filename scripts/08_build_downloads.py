"""Phase 8: Build downloadable zip archives of the plain-text corpus.

Creates two zip files in web/public/downloads/:
  - nice-corpus-full.zip  — all 3,307 markdown files
  - nice-corpus-fad.zip   — only FAD / FAD_* markdown files

Each zip includes a README.md and llms.txt index at the root.

Usage:
    uv run python scripts/08_build_downloads.py

No external dependencies — uses stdlib zipfile only.
"""

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "web" / "public" / "downloads"

TA_RE = re.compile(r"^ta(\d+)$")
FAD_RE = re.compile(r"^FAD(_\d+)?\.md$")
PAGE_RE = re.compile(r"<!-- page \d+ -->")


def collect_ta_dirs() -> list[Path]:
    """Return sorted list of ta{N}/ directories."""
    dirs = [d for d in DATA_DIR.iterdir() if d.is_dir() and TA_RE.match(d.name)]
    dirs.sort(key=lambda d: int(TA_RE.match(d.name).group(1)))
    return dirs


def count_pages(filepath: Path) -> int:
    """Count <!-- page N --> markers in a file."""
    text = filepath.read_text(errors="replace")
    return len(PAGE_RE.findall(text))


def build_readme(num_tas: int, num_docs: int, num_pages: int, subset: str = "full") -> str:
    """Generate README.md content for the zip."""
    if subset == "full":
        desc = "Complete plain-text corpus of NICE Technology Appraisal documents."
        contents = (
            "Each `ta{N}/` folder contains the available documents for that appraisal:\n"
            "FAD, ACD, scope, scope comments, committee papers, evaluation reports."
        )
    else:
        desc = "Final Appraisal Determination (FAD) documents from NICE Technology Appraisals."
        contents = (
            "Each `ta{N}/` folder contains the FAD document(s) for that appraisal.\n"
            "Long FADs are split into numbered parts (FAD.md, FAD_1.md, ...)."
        )

    return f"""\
# NICE Technology Appraisals — Plain Text Corpus

{desc}

## Stats

- **{num_tas}** technology appraisals
- **{num_docs:,}** documents
- **{num_pages:,}** pages

## Folder structure

```
ta100/
  FAD.md
  ACD.md
  scope.md
  ...
ta101/
  ...
```

{contents}

## Website

<https://nice.shoulde.rs>

## License

Extracted from publicly available NICE documents. For research use.
"""


def build_llms_txt(ta_dirs: list[Path]) -> str:
    """Generate a simple llms.txt index listing all TAs and their files."""
    lines = [
        "# NICE Technology Appraisals — Plain Text Corpus",
        "",
        "> Structured plain-text extractions from NICE Technology Appraisal documents.",
        "> Website: https://nice.shoulde.rs",
        "",
    ]
    for ta_dir in ta_dirs:
        ta_num = TA_RE.match(ta_dir.name).group(1)
        md_files = sorted(f.name for f in ta_dir.iterdir() if f.suffix == ".md")
        if md_files:
            file_list = ", ".join(md_files)
            lines.append(f"- TA{ta_num}: {file_list}")
    lines.append("")
    return "\n".join(lines)


def build_zip(
    zip_path: Path,
    ta_dirs: list[Path],
    file_filter=None,
    subset: str = "full",
):
    """Build a zip archive with matching markdown files, README, and llms.txt."""
    total_docs = 0
    total_pages = 0
    tas_included = 0

    # Collect files first to compute stats for README
    entries: list[tuple[str, Path]] = []  # (arcname, filepath)
    ta_dirs_for_llms: list[Path] = []

    for ta_dir in ta_dirs:
        md_files = sorted(ta_dir.glob("*.md"))
        if file_filter:
            md_files = [f for f in md_files if file_filter(f)]
        if not md_files:
            continue
        tas_included += 1
        ta_dirs_for_llms.append(ta_dir)
        for md_file in md_files:
            arcname = f"{ta_dir.name}/{md_file.name}"
            entries.append((arcname, md_file))
            total_docs += 1
            total_pages += count_pages(md_file)

    readme = build_readme(tas_included, total_docs, total_pages, subset=subset)
    llms_txt = build_llms_txt(ta_dirs_for_llms)

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README.md", readme)
        zf.writestr("llms.txt", llms_txt)
        for arcname, filepath in entries:
            zf.write(filepath, arcname)

    return tas_included, total_docs, total_pages


def fmt_size(nbytes: int) -> str:
    """Format byte count as human-readable string."""
    if nbytes < 1024:
        return f"{nbytes} B"
    elif nbytes < 1024 * 1024:
        return f"{nbytes / 1024:.1f} KB"
    else:
        return f"{nbytes / (1024 * 1024):.1f} MB"


def main():
    ta_dirs = collect_ta_dirs()
    print(f"Found {len(ta_dirs)} TA directories\n")

    # Full corpus
    full_path = OUT_DIR / "nice-corpus-full.zip"
    tas, docs, pages = build_zip(full_path, ta_dirs, subset="full")
    size = full_path.stat().st_size
    print(f"nice-corpus-full.zip")
    print(f"  TAs: {tas}, documents: {docs:,}, pages: {pages:,}")
    print(f"  Size: {fmt_size(size)}")
    print()

    # FAD only
    fad_path = OUT_DIR / "nice-corpus-fad.zip"
    tas, docs, pages = build_zip(
        fad_path,
        ta_dirs,
        file_filter=lambda f: FAD_RE.match(f.name),
        subset="fad",
    )
    size = fad_path.stat().st_size
    print(f"nice-corpus-fad.zip")
    print(f"  TAs: {tas}, documents: {docs:,}, pages: {pages:,}")
    print(f"  Size: {fmt_size(size)}")


if __name__ == "__main__":
    main()
