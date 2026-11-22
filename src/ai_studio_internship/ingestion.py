"""PDF text extraction and two deterministic chunking strategies."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANUAL_DIR = ROOT / "data" / "day08_manuals"
FIXED_PATH = ROOT / "data" / "day08_chunks_fixed.jsonl"
PARAGRAPH_PATH = ROOT / "data" / "day08_chunks_paragraph.jsonl"


def extract_pdf(path: Path) -> list[str]:
    """Extract layout-preserving text page by page with Poppler's pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError as error:
        raise RuntimeError("Install Poppler so the pdftotext command is available") from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"Could not read {path.name}: {error.stderr.strip()}") from error
    return [page.strip() for page in result.stdout.split("\f") if page.strip()]


def fixed_chunks(text: str, size: int = 300, overlap: int = 60) -> list[str]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("size must be positive and overlap must be smaller than size")
    chunks = []
    start = 0
    while start < len(text):
        piece = text[start : start + size].strip()
        if piece:
            chunks.append(piece)
        start += size - overlap
    return chunks


def paragraph_chunks(text: str, max_chars: int = 420) -> list[str]:
    """Group lines/table rows without splitting a row unless it is oversized."""
    blocks = [line.strip() for line in text.splitlines() if line.strip()]
    chunks: list[str] = []
    current = ""
    for block in blocks:
        pieces = fixed_chunks(block, max_chars, 0) if len(block) > max_chars else [block]
        for piece in pieces:
            candidate = f"{current}\n{piece}".strip() if current else piece
            if current and len(candidate) > max_chars:
                chunks.append(current)
                current = piece
            else:
                current = candidate
    if current:
        chunks.append(current)
    return chunks


def ingest_all(size: int = 300, overlap: int = 60) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fixed: list[dict[str, Any]] = []
    paragraphs: list[dict[str, Any]] = []
    for path in sorted(MANUAL_DIR.glob("*.pdf")):
        manual_id = path.stem.replace("-demo", "")
        for page_number, page in enumerate(extract_pdf(path), start=1):
            for index, text in enumerate(fixed_chunks(page, size=size, overlap=overlap), start=1):
                fixed.append({"id": f"{manual_id}-p{page_number}-f{index}", "manual_id": manual_id, "page": page_number, "text": text})
            for index, text in enumerate(paragraph_chunks(page), start=1):
                paragraphs.append({"id": f"{manual_id}-p{page_number}-p{index}", "manual_id": manual_id, "page": page_number, "text": text})
    return fixed, paragraphs


def _write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(value, ensure_ascii=False) + "\n" for value in values), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract synthetic PDFs and compare fixed/paragraph chunks")
    parser.add_argument("--size", type=int, default=300)
    parser.add_argument("--overlap", type=int, default=60)
    args = parser.parse_args(argv)
    fixed, paragraphs = ingest_all(size=args.size, overlap=args.overlap)
    _write_jsonl(FIXED_PATH, fixed)
    _write_jsonl(PARAGRAPH_PATH, paragraphs)
    print(f"Extracted {len(fixed)} fixed chunks and {len(paragraphs)} paragraph chunks from 3 PDFs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
