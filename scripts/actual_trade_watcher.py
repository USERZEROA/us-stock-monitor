#!/usr/bin/env python3
"""Write a read-only approval/order audit for same-day Webull activity.

This script never contacts the broker and never places, modifies, or cancels
orders. Run the Webull read-only sync scripts first, then this script consumes
the local snapshots and records whether today's actual/cancelled orders have a
local approval trail and whether BUY attempts breach sizing guardrails.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
ORDER_SNAPSHOT_PATH = ROOT / "webull_order_status_snapshot.json"
PORTFOLIO_SNAPSHOT_PATH = ROOT / "webull_portfolio_snapshot.json"
LAST_SUBMISSION_PATH = ROOT / "webull_last_order_submission.json"
OUT_DIR = ROOT / "reports" / "approval-audit"
ET = ZoneInfo("America/New_York")
OVERSIZED_BUY_PCT = Decimal("20")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def dec(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None


def money(value: Decimal | None) -> str:
    if value is None:
        return "unknown"
    return f"${value.quantize(Decimal('0.01'))}"


def epoch_ms_to_et(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).astimezone(ET)
    except (OSError, TypeError, ValueError):
        return None


def order_ref(order: dict[str, Any]) -> str:
    raw = str(order.get("order_id") or order.get("client_order_id") or "")
    return raw[-10:] if raw else "unknown"


def order_notional(order: dict[str, Any]) -> Decimal | None:
    qty = dec(order.get("total_quantity") or order.get("filled_quantity"))
    price = dec(order.get("limit_price") or order.get("filled_price"))
    if qty is None or price is None:
        return None
    return qty * price


def account_equity() -> Decimal | None:
    snapshot = load_json(PORTFOLIO_SNAPSHOT_PATH)
    if not isinstance(snapshot, dict) or snapshot.get("status") != "success":
        return None
    return dec((snapshot.get("balance_raw") or {}).get("total_net_liquidation_value"))


def submission_refs() -> set[str]:
    data = load_json(LAST_SUBMISSION_PATH)
    refs: set[str] = set()
    if not isinstance(data, dict):
        return refs
    for order in data.get("orders") or []:
        if not isinstance(order, dict):
            continue
        for key in ("order_id", "client_order_id"):
            value = order.get(key)
            if value:
                refs.add(str(value))
    return refs


def same_day_orders(target_date: str, snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    orders = [*(snapshot.get("history_orders") or []), *(snapshot.get("open_orders") or [])]
    selected: list[dict[str, Any]] = []
    for order in orders:
        if not isinstance(order, dict):
            continue
        when = epoch_ms_to_et(order.get("filled_time") or order.get("place_time"))
        if when and when.date().isoformat() == target_date:
            selected.append(order)
    selected.sort(key=lambda item: int(item.get("place_time") or item.get("filled_time") or 0))
    return selected


def audit_order(order: dict[str, Any], equity: Decimal | None, known_submission_refs: set[str]) -> dict[str, Any]:
    side = str(order.get("side") or "")
    status = str(order.get("status") or "")
    symbol = str(order.get("symbol") or "")
    ref = order_ref(order)
    notional = order_notional(order)
    notional_pct = (notional / equity * Decimal("100")) if notional is not None and equity else None
    raw_refs = {
        str(order.get("order_id") or ""),
        str(order.get("client_order_id") or ""),
    }
    has_local_submission = bool(raw_refs & known_submission_refs)
    flags: list[str] = []
    chain_status = "complete" if has_local_submission else "manual_or_unlinked_requires_review"
    if side == "BUY" and notional_pct is not None and notional_pct > OVERSIZED_BUY_PCT:
        flags.append("oversized_buy_gt_20pct_equity")
    if status in {"CANCELLED", "REJECTED"}:
        flags.append(f"order_{status.lower()}")
    if status == "FILLED" and not has_local_submission:
        flags.append("user_manual_or_unlinked_filled_order_requires_review")
    return {
        "order_ref": ref,
        "ticker": symbol,
        "side": side,
        "status": status,
        "quantity": str(order.get("total_quantity") or ""),
        "filled_quantity": str(order.get("filled_quantity") or ""),
        "limit_price": str(order.get("limit_price") or ""),
        "filled_price": str(order.get("filled_price") or ""),
        "placed_at_et": (epoch_ms_to_et(order.get("place_time")) or "").isoformat()
        if epoch_ms_to_et(order.get("place_time"))
        else "",
        "filled_at_et": (epoch_ms_to_et(order.get("filled_time")) or "").isoformat()
        if epoch_ms_to_et(order.get("filled_time"))
        else "",
        "notional": str(notional.quantize(Decimal("0.01"))) if notional is not None else "",
        "notional_pct_equity": str(notional_pct.quantize(Decimal("0.01"))) if notional_pct is not None else "",
        "approval_chain_status": chain_status,
        "local_submission_ref_found": has_local_submission,
        "flags": flags,
    }


def run(target_date: str) -> dict[str, Any]:
    snapshot = load_json(ORDER_SNAPSHOT_PATH)
    if not isinstance(snapshot, dict):
        return {
            "schema_version": "1.0",
            "trading_date": target_date,
            "status": "yellow",
            "error": f"missing or invalid order snapshot: {ORDER_SNAPSHOT_PATH}",
            "orders": [],
        }
    equity = account_equity()
    orders = same_day_orders(target_date, snapshot)
    audits = [audit_order(order, equity, submission_refs()) for order in orders]
    filled = [item for item in audits if item["status"] == "FILLED"]
    flagged = [item for item in audits if item["flags"]]
    severe = [item for item in audits if "oversized_buy_gt_20pct_equity" in item["flags"]]
    return {
        "schema_version": "1.0",
        "trading_date": target_date,
        "run_time_et": datetime.now(tz=ET).strftime("%Y-%m-%d %H:%M:%S ET"),
        "status": "red" if severe else ("yellow" if flagged else "green"),
        "status_reason": (
            "red for oversized BUY attempts; "
            "yellow for user-manual/unlinked fills or cancelled/rejected orders that need review"
            if flagged
            else "no same-day order review flags"
        ),
        "order_snapshot_status": snapshot.get("status"),
        "order_snapshot_time_utc": snapshot.get("synced_at_utc"),
        "portfolio_equity": str(equity) if equity is not None else "",
        "orders_seen": len(audits),
        "filled_orders_seen": len(filled),
        "flagged_orders_seen": len(flagged),
        "orders": audits,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.now(tz=ET).date().isoformat())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = run(args.date)
    if args.write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUT_DIR / f"{args.date}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        record["path"] = str(path)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if record.get("status") != "red" else 1


if __name__ == "__main__":
    raise SystemExit(main())
