#!/usr/bin/env python3
"""Audit filled BUY orders against later structured position reviews.

This is read-only. It consumes the latest Webull order-status snapshot and
existing structured JSONL reports; it never contacts the broker or submits
orders.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
ORDER_SNAPSHOT_PATH = ROOT / "webull_order_status_snapshot.json"
PORTFOLIO_SNAPSHOT_PATH = ROOT / "webull_portfolio_snapshot.json"
STRUCTURED_ROOT = ROOT / "reports" / "structured"
ET = ZoneInfo("America/New_York")
POST_BUY_RULE_ID = "standing-post-buy-review"
DOCUMENTED_FAILURE_PATHS = [
    ROOT / "research" / "queue" / "postmarket-failures.md",
    ROOT / "research" / "EVAL_CASES.md",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {"_error": str(exc)}


def parse_epoch_ms(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).astimezone(ET)
    except (TypeError, ValueError, OSError):
        return None


def parse_report_time(value: Any) -> datetime | None:
    text = str(value or "").strip()
    match = re.match(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})(?::(\d{2}))?", text)
    if not match:
        return None
    seconds = match.group(3) or "00"
    try:
        return datetime.fromisoformat(f"{match.group(1)}T{match.group(2)}:{seconds}").replace(tzinfo=ET)
    except ValueError:
        return None


def iter_structured_records(start: date, end: date) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    current = start
    while current <= end:
        filename = f"{current.isoformat()}.jsonl"
        for report_type in ("premarket", "intraday", "postmarket"):
            path = STRUCTURED_ROOT / report_type / filename
            if not path.exists():
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(record, dict):
                    continue
                run_at = parse_report_time(record.get("run_time_et"))
                if run_at is None:
                    continue
                record["_audit_path"] = str(path)
                record["_audit_line"] = number
                record["_audit_run_at"] = run_at
                records.append(record)
        current += timedelta(days=1)
    records.sort(key=lambda item: item["_audit_run_at"])
    return records


def review_tickers(record: dict[str, Any]) -> set[str]:
    tickers: set[str] = set()
    for review in record.get("position_reviews") or []:
        if isinstance(review, dict) and review.get("ticker"):
            tickers.add(str(review["ticker"]).upper())
    return tickers


def rule_ids(record: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for item in record.get("risk_rules_applied") or []:
        if isinstance(item, dict) and item.get("rule_id"):
            ids.add(str(item["rule_id"]))
        elif isinstance(item, str):
            ids.add(item)
    return ids


def short_ref(order: dict[str, Any]) -> str:
    raw = str(order.get("client_order_id") or order.get("order_id") or "")
    return raw[-8:] if raw else "unknown"


def current_position_symbols() -> set[str]:
    snapshot = load_json(PORTFOLIO_SNAPSHOT_PATH)
    if not isinstance(snapshot, dict) or snapshot.get("status") != "success":
        return set()
    symbols: set[str] = set()
    for position in snapshot.get("positions") or []:
        if isinstance(position, dict) and position.get("symbol"):
            symbols.add(str(position["symbol"]).upper())
    return symbols


def filled_sell_times_by_symbol(orders: list[dict[str, Any]]) -> dict[str, list[datetime]]:
    sells: dict[str, list[datetime]] = {}
    for order in orders:
        if order.get("side") != "SELL" or order.get("status") != "FILLED":
            continue
        symbol = str(order.get("symbol") or "").upper()
        filled_at = parse_epoch_ms(order.get("filled_time") or order.get("place_time"))
        if symbol and filled_at:
            sells.setdefault(symbol, []).append(filled_at)
    for times in sells.values():
        times.sort()
    return sells


def documented_missing_review(symbol: str, filled_at: datetime) -> bool:
    """Return true only for historical gaps already admitted to failure/eval logs."""
    needle_date = filled_at.date().isoformat()
    for path in DOCUMENTED_FAILURE_PATHS:
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            continue
        if (
            needle_date in text
            and symbol in text
            and (
                "post-buy audit" in text
                or "Post-buy review" in text
                or "买后判断" in text
            )
            and ("structured-log gap" in text or "漏项" in text or "first later structured" in text)
        ):
            return True
    return False


def audit(trading_date: str, lookback_days: int) -> dict[str, Any]:
    target = date.fromisoformat(trading_date)
    start = target - timedelta(days=max(0, lookback_days))
    end_dt = datetime.combine(target, time(23, 59, 59), tzinfo=ET)
    snapshot = load_json(ORDER_SNAPSHOT_PATH)
    issues: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    if snapshot is None:
        return {
            "schema_version": "1.0",
            "trading_date": trading_date,
            "status": "yellow",
            "issues": [],
            "warnings": [f"missing order snapshot: {ORDER_SNAPSHOT_PATH}"],
            "checks": [],
        }
    if isinstance(snapshot, dict) and snapshot.get("_error"):
        return {
            "schema_version": "1.0",
            "trading_date": trading_date,
            "status": "yellow",
            "issues": [],
            "warnings": [f"invalid order snapshot json: {snapshot['_error']}"],
            "checks": [],
        }
    if snapshot.get("status") != "success":
        warnings.append(f"order snapshot status is {snapshot.get('status')!r}")

    records = iter_structured_records(start, target)
    if not records:
        warnings.append(f"no structured records found from {start.isoformat()} through {target.isoformat()}")

    history_orders = snapshot.get("history_orders") or []
    current_symbols = current_position_symbols()
    sell_times = filled_sell_times_by_symbol(history_orders)

    for order in history_orders:
        if order.get("side") != "BUY" or order.get("status") != "FILLED":
            continue
        symbol = str(order.get("symbol") or "").upper()
        if not symbol:
            continue
        filled_at = parse_epoch_ms(order.get("filled_time") or order.get("place_time"))
        if filled_at is None:
            warnings.append(f"BUY {symbol} order {short_ref(order)} has no parseable filled_time")
            continue
        if filled_at.date() < start or filled_at > end_dt:
            continue
        later = [record for record in records if record["_audit_run_at"] > filled_at]
        check = {
            "ticker": symbol,
            "order_ref": short_ref(order),
            "filled_at_et": filled_at.isoformat(),
            "review_status": "pending",
            "review_report": None,
        }
        if not later:
            warnings.append(f"BUY {symbol} at {filled_at.isoformat()} has no later structured report yet")
            checks.append(check)
            continue
        first = later[0]
        closed_before_first_report = (
            symbol not in current_symbols
            and any(filled_at < sold_at < first["_audit_run_at"] for sold_at in sell_times.get(symbol, []))
        )
        if closed_before_first_report:
            check["review_status"] = "skipped_closed_before_first_available_report"
            check["review_report"] = {
                "path": first["_audit_path"],
                "line": first["_audit_line"],
                "run_time_et": first.get("run_time_et"),
                "job_label": first.get("job_label"),
            }
            checks.append(check)
            continue
        tickers = review_tickers(first)
        check["review_report"] = {
            "path": first["_audit_path"],
            "line": first["_audit_line"],
            "run_time_et": first.get("run_time_et"),
            "job_label": first.get("job_label"),
        }
        if symbol not in tickers:
            if documented_missing_review(symbol, filled_at):
                check["review_status"] = "documented_missing"
                warnings.append(
                    f"BUY {symbol} at {filled_at.isoformat()} missed first-later-report review, "
                    "but the historical gap is already documented in failure/eval logs"
                )
            else:
                check["review_status"] = "missing"
                issues.append(
                    f"BUY {symbol} at {filled_at.isoformat()} is not reviewed in the first later "
                    f"structured report {first['_audit_path']}:{first['_audit_line']}"
                )
        else:
            check["review_status"] = "ok"
            if POST_BUY_RULE_ID not in rule_ids(first):
                warnings.append(
                    f"BUY {symbol} reviewed in {first['_audit_path']}:{first['_audit_line']} "
                    f"but {POST_BUY_RULE_ID} is not listed in risk_rules_applied"
                )
        checks.append(check)

    status = "red" if issues else "yellow" if warnings else "green"
    return {
        "schema_version": "1.0",
        "trading_date": trading_date,
        "lookback_start": start.isoformat(),
        "status": status,
        "issues": issues,
        "warnings": warnings,
        "checks": checks,
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        f"# Post-Buy Review Audit - {result['trading_date']}",
        "",
        f"- Status: {result['status']}",
        f"- Lookback start: {result.get('lookback_start', 'n/a')}",
        f"- BUY checks: {len(result['checks'])}",
    ]
    if result["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in result["warnings"])
    if result["issues"]:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {item}" for item in result["issues"])
    if result["checks"]:
        lines.extend(["", "## Checks", ""])
        for check in result["checks"]:
            report = check.get("review_report") or {}
            lines.append(
                f"- {check['ticker']} {check['filled_at_et']} -> {check['review_status']} "
                f"({report.get('path', 'pending')}:{report.get('line', '')})"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.now(ET).strftime("%Y-%m-%d"))
    parser.add_argument("--lookback-days", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = audit(args.date, args.lookback_days)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 2 if result["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
