#!/usr/bin/env python3
"""Audit long-run knowledge governance and machine-readable knowledge cards."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = ROOT / "research" / "KNOWLEDGE_GOVERNANCE.md"
LATEST = ROOT / "research" / "BOOK_LEARNING_LATEST.md"
MARKET_KNOWLEDGE = ROOT / "MARKET_KNOWLEDGE.md"
FAILED_IDEAS = ROOT / "research" / "FAILED_IDEAS.md"
KNOWLEDGE_DIR = ROOT / "research" / "knowledge"
CARDS_DIR = KNOWLEDGE_DIR / "cards"
DOMAINS_DIR = KNOWLEDGE_DIR / "domains"
BOOKS_DIR = ROOT / "research" / "books"

ALLOWED_STATUSES = {"candidate", "admitted", "deprecated", "rejected"}
ALLOWED_DOMAINS = {
    "methodology",
    "risk_management",
    "market_microstructure",
    "portfolio_construction",
    "equity_events",
    "macro",
    "derivatives",
    "accounting_valuation",
    "behavioral",
    "system_engineering",
}
REQUIRED_CARD_FIELDS = {
    "schema_version",
    "rule_id",
    "title",
    "status",
    "domain",
    "source_type",
    "source_title",
    "source_authors",
    "source_year",
    "source_path",
    "source_pages",
    "evidence_grade",
    "core_conclusion",
    "mechanism",
    "applicable_environment",
    "non_applicable_environment",
    "prohibited_use",
    "downstream_roles",
    "revalidation_trigger",
    "last_review_date",
}
LIST_FIELDS = {
    "source_authors",
    "applicable_environment",
    "non_applicable_environment",
    "prohibited_use",
    "downstream_roles",
}
PROTECTED_MARKERS = {
    "protected_cron_forbidden": "Forbidden without explicit user approval",
    "latest_bias_guard": "Latest-Knowledge Bias Guard",
    "storage_budget": "Storage And Budget",
    "topic_rotation": "Topic Rotation",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_card(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return json.loads(read_text(path)), None
    except json.JSONDecodeError as exc:
        return None, f"{relative(path)} invalid JSON: {exc}"
    except Exception as exc:
        return None, f"{relative(path)} unreadable: {exc}"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_card(path: Path, market_text: str) -> tuple[list[str], list[str], dict[str, Any] | None]:
    issues: list[str] = []
    warnings: list[str] = []
    card, error = load_card(path)
    if error or card is None:
        return [error or f"{relative(path)} failed to load"], warnings, None

    missing = sorted(REQUIRED_CARD_FIELDS - set(card))
    if missing:
        issues.append(f"{relative(path)} missing required fields: {missing}")

    rule_id = str(card.get("rule_id") or "")
    if not rule_id:
        issues.append(f"{relative(path)} has empty rule_id")
    elif path.stem != rule_id:
        warnings.append(f"{relative(path)} filename does not match rule_id {rule_id}")

    status = str(card.get("status") or "")
    if status not in ALLOWED_STATUSES:
        issues.append(f"{relative(path)} has invalid status {status!r}")

    domain = str(card.get("domain") or "")
    if domain not in ALLOWED_DOMAINS:
        issues.append(f"{relative(path)} has invalid domain {domain!r}")
    else:
        domain_path = DOMAINS_DIR / f"{domain}.md"
        if not domain_path.exists():
            warnings.append(f"{relative(path)} domain index missing: {relative(domain_path)}")
        elif rule_id and rule_id not in read_text(domain_path):
            warnings.append(f"{relative(path)} not referenced by {relative(domain_path)}")

    for field in LIST_FIELDS:
        value = card.get(field)
        if not isinstance(value, list) or not value:
            issues.append(f"{relative(path)} field {field} must be a non-empty list")

    source_path_value = card.get("source_path")
    if isinstance(source_path_value, str) and source_path_value:
        source_path = ROOT / source_path_value
        if not source_path.exists():
            issues.append(f"{relative(path)} source_path missing: {source_path_value}")
    else:
        issues.append(f"{relative(path)} source_path must be a non-empty string")

    if status == "admitted":
        if rule_id and rule_id not in market_text and str(card.get("title") or "") not in market_text:
            warnings.append(
                f"{relative(path)} is admitted but rule_id/title was not found in MARKET_KNOWLEDGE.md"
            )
        if not str(card.get("revalidation_trigger") or "").strip():
            issues.append(f"{relative(path)} admitted card lacks revalidation_trigger")
        if not card.get("prohibited_use"):
            issues.append(f"{relative(path)} admitted card lacks prohibited_use")

    return issues, warnings, card


def audit() -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    required_paths = [
        GOVERNANCE,
        LATEST,
        MARKET_KNOWLEDGE,
        FAILED_IDEAS,
        KNOWLEDGE_DIR,
        CARDS_DIR,
        DOMAINS_DIR,
        BOOKS_DIR,
    ]
    for path in required_paths:
        if not path.exists():
            issues.append(f"missing required path: {relative(path)}")

    governance_text = read_text(GOVERNANCE) if GOVERNANCE.exists() else ""
    for marker_name, marker in PROTECTED_MARKERS.items():
        if marker not in governance_text:
            issues.append(f"KNOWLEDGE_GOVERNANCE.md missing marker {marker_name}: {marker}")

    latest_text = read_text(LATEST) if LATEST.exists() else ""
    if "Result status: `completed`" in latest_text and "candidate-only" in latest_text.lower():
        warnings.append("latest digest says completed but still contains candidate-only language")
    if "Latest Book Learning Digest" not in latest_text:
        warnings.append("BOOK_LEARNING_LATEST.md lacks latest digest title")

    market_text = read_text(MARKET_KNOWLEDGE) if MARKET_KNOWLEDGE.exists() else ""
    card_paths = sorted(CARDS_DIR.glob("*.json")) if CARDS_DIR.exists() else []
    cards: list[dict[str, Any]] = []
    seen_rule_ids: dict[str, str] = {}
    for path in card_paths:
        card_issues, card_warnings, card = audit_card(path, market_text)
        issues.extend(card_issues)
        warnings.extend(card_warnings)
        if card is None:
            continue
        cards.append(card)
        rule_id = str(card.get("rule_id") or "")
        if rule_id in seen_rule_ids:
            issues.append(
                f"duplicate rule_id {rule_id}: {seen_rule_ids[rule_id]} and {relative(path)}"
            )
        elif rule_id:
            seen_rule_ids[rule_id] = relative(path)

    admitted_count = sum(1 for card in cards if card.get("status") == "admitted")
    candidate_count = sum(1 for card in cards if card.get("status") == "candidate")
    if admitted_count == 0:
        warnings.append("no admitted knowledge cards found")

    pdf_paths = sorted(BOOKS_DIR.glob("*.pdf")) if BOOKS_DIR.exists() else []
    pdf_hashes: dict[str, str] = {}
    oversized_pdfs: list[str] = []
    duplicate_pdfs: list[str] = []
    total_pdf_bytes = 0
    for path in pdf_paths:
        size = path.stat().st_size
        total_pdf_bytes += size
        if size > 100 * 1024 * 1024:
            oversized_pdfs.append(f"{relative(path)} ({size} bytes)")
        digest = file_sha256(path)
        if digest in pdf_hashes:
            duplicate_pdfs.append(f"{relative(path)} duplicates {pdf_hashes[digest]}")
        else:
            pdf_hashes[digest] = relative(path)

    if oversized_pdfs:
        warnings.append(f"PDF files above 100MB need review: {oversized_pdfs}")
    if duplicate_pdfs:
        warnings.append(f"duplicate PDF files detected: {duplicate_pdfs}")
    if total_pdf_bytes > 2 * 1024 * 1024 * 1024:
        warnings.append(f"research/books PDF storage exceeds 2GB: {total_pdf_bytes} bytes")

    status = "red" if issues else ("yellow" if warnings else "green")
    return {
        "schema_version": "1.0",
        "status": status,
        "issues": issues,
        "warnings": warnings,
        "card_count": len(cards),
        "admitted_count": admitted_count,
        "candidate_count": candidate_count,
        "pdf_count": len(pdf_paths),
        "total_pdf_bytes": total_pdf_bytes,
        "cards": [
            {
                "rule_id": card.get("rule_id"),
                "status": card.get("status"),
                "domain": card.get("domain"),
                "source_title": card.get("source_title"),
            }
            for card in cards
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Knowledge Governance Audit",
        "",
        f"- Status: {report['status']}",
        f"- Cards: {report['card_count']} total, {report['admitted_count']} admitted, {report['candidate_count']} candidate",
        f"- PDFs: {report['pdf_count']} files, {report['total_pdf_bytes']} bytes",
        "",
    ]
    for issue in report["issues"]:
        lines.append(f"- issue: {issue}")
    for warning in report["warnings"]:
        lines.append(f"- warning: {warning}")
    if not report["issues"] and not report["warnings"]:
        lines.append("- No issues or warnings.")
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
