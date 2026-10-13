#!/usr/bin/env python3
"""Audit the daily book-learning loop and latest digest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "research" / "BOOK_LEARNING_LATEST.md"
QUEUE = ROOT / "research" / "BOOK_LEARNING_QUEUE.md"
BOOKS = ROOT / "research" / "books"
LOGS = ROOT / "research" / "logs"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def audit() -> dict:
    issues: list[str] = []
    warnings: list[str] = []

    required = [LATEST, QUEUE, BOOKS, LOGS]
    for path in required:
        if not path.exists():
            issues.append(f"missing required path: {path.relative_to(ROOT)}")

    latest_text = read(LATEST) if LATEST.exists() else ""
    queue_text = read(QUEUE) if QUEUE.exists() else ""
    book_files = sorted(BOOKS.glob("*.md")) if BOOKS.exists() else []

    latest_status = "unknown"
    for line in latest_text.splitlines():
        if line.startswith("- Result status:"):
            latest_status = line.split(":", 1)[1].strip().strip("`")
            break

    if "claude" not in latest_text.lower():
        issues.append("latest digest does not record a Claude runtime")
    if "buy 0" not in latest_text.lower() or "sell 0" not in latest_text.lower():
        issues.append("latest digest does not record buy 0 / sell 0 safety summary")
    if "BOOK_LEARNING_LATEST.md" not in latest_text and "Latest Book Learning Digest" not in latest_text:
        warnings.append("latest digest has no self-identifying title")
    if "partial_read" in queue_text and "partial_read" not in queue_text.split("## Status Values", 1)[-1]:
        warnings.append("queue uses partial_read without documenting it in status values")

    accepted = {"completed", "accepted_complete_pdf"}
    if latest_status not in accepted:
        warnings.append(
            f"latest book learning status is {latest_status}; downstream use is candidate-only"
        )

    for path in book_files[-3:]:
        text = read(path)
        lowered = text.lower()
        if "complete reading" not in lowered and "page coverage ledger" not in lowered:
            warnings.append(f"{path.relative_to(ROOT)} lacks a complete reading assessment")
        if "PDF" not in text and "pdf" not in text:
            warnings.append(f"{path.relative_to(ROOT)} does not mention PDF/source format")

    status = "red" if issues else ("yellow" if warnings else "green")
    return {
        "schema_version": "1.0",
        "status": status,
        "issues": issues,
        "warnings": warnings,
        "latest_status": latest_status,
        "latest_path": str(LATEST),
        "book_count": len(book_files),
        "recent_books": [str(path.relative_to(ROOT)) for path in book_files[-5:]],
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# Book Learning Audit",
        "",
        f"- Status: {report['status']}",
        f"- Latest status: {report['latest_status']}",
        f"- Book count: {report['book_count']}",
        "",
    ]
    for issue in report["issues"]:
        lines.append(f"- issue: {issue}")
    for warning in report["warnings"]:
        lines.append(f"- warning: {warning}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 2 if report["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
