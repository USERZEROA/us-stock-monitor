#!/usr/bin/env python3
"""Audit whether filled sell-order fees have finalized in local Webull snapshots.

This is a read-only retry/audit layer. It assumes `webull_order_status.py` has
already refreshed the local order snapshot, then records which SELL fills still
use provisional fee estimates after a configurable age.
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
OUT_DIR = ROOT / "reports" / "fee-finalization"
ET = ZoneInfo("America/New_York")
DEFAULT_MIN_AGE_HOURS = 24
# Per user instruction: if broker never posts an actual sell fee, uniformly
# finalize the fee at $0.02/order once the order is past the fallback age,
# instead of leaving it provisional/unresolved forever.
DEFAULT_FEE_FALLBACK = Decimal("0.02")
DEFAULT_FALLBACK_AGE_HOURS = 24


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


def fee_total(order: dict[str, Any]) -> Decimal:
    total = Decimal("0")
    for fee in order.get("fees") or []:
        if not isinstance(fee, dict):
            continue
        value = dec(fee.get("actual_value") or fee.get("receivable_value"))
        if value is not None:
            total += value
    commission = order.get("commission")
    if isinstance(commission, dict):
        value = dec(commission.get("actual_value") or commission.get("receivable_value"))
        if value is not None:
            total += value
    return total


def filled_sell_audits(
    snapshot: dict[str, Any],
    min_age_hours: int,
    fee_fallback: Decimal,
    fallback_age_hours: int,
) -> list[dict[str, Any]]:
    now = datetime.now(tz=ET)
    audits: list[dict[str, Any]] = []
    for order in snapshot.get("history_orders") or []:
        if not isinstance(order, dict):
            continue
        if order.get("side") != "SELL" or order.get("status") != "FILLED":
            continue
        filled_at = epoch_ms_to_et(order.get("filled_time") or order.get("place_time"))
        if filled_at is None:
            continue
        age_hours = (now - filled_at).total_seconds() / 3600
        if age_hours < min_age_hours:
            continue
        fees = fee_total(order)
        if fees > 0:
            fee_status = "final"
            fee_basis = "broker_api"
            fee_total_str = str(fees.quantize(Decimal("0.01")))
        elif age_hours >= fallback_age_hours:
            # Broker never posted an actual fee within the fallback window:
            # finalize uniformly at the $0.02 estimate per user instruction.
            fee_status = "final_estimated_fallback"
            fee_basis = "estimated_fallback"
            fee_total_str = str(fee_fallback.quantize(Decimal("0.01")))
        else:
            fee_status = "provisional_missing_api_fee"
            fee_basis = "pending_broker"
            fee_total_str = ""
        audits.append(
            {
                "order_ref": order_ref(order),
                "ticker": order.get("symbol"),
                "filled_at_et": filled_at.isoformat(),
                "age_hours": round(age_hours, 1),
                "filled_quantity": str(order.get("filled_quantity") or ""),
                "filled_price": str(order.get("filled_price") or ""),
                "fee_status": fee_status,
                "fee_basis": fee_basis,
                "broker_fee_total": fee_total_str,
            }
        )
    audits.sort(key=lambda item: item["filled_at_et"], reverse=True)
    return audits


def run(
    target_date: str,
    min_age_hours: int,
    fee_fallback: Decimal,
    fallback_age_hours: int,
) -> dict[str, Any]:
    snapshot = load_json(ORDER_SNAPSHOT_PATH)
    if not isinstance(snapshot, dict):
        return {
            "schema_version": "1.0",
            "trading_date": target_date,
            "status": "yellow",
            "error": f"missing or invalid order snapshot: {ORDER_SNAPSHOT_PATH}",
            "audits": [],
        }
    audits = filled_sell_audits(snapshot, min_age_hours, fee_fallback, fallback_age_hours)
    # Resolved = broker-final OR finalized via the $0.02 fallback estimate.
    resolved_states = {"final", "final_estimated_fallback"}
    unresolved = [item for item in audits if item["fee_status"] not in resolved_states]
    estimated = [item for item in audits if item["fee_status"] == "final_estimated_fallback"]
    return {
        "schema_version": "1.1",
        "trading_date": target_date,
        "run_time_et": datetime.now(tz=ET).strftime("%Y-%m-%d %H:%M:%S ET"),
        "status": "yellow" if unresolved else "green",
        "order_snapshot_status": snapshot.get("status"),
        "order_snapshot_time_utc": snapshot.get("synced_at_utc"),
        "min_age_hours": min_age_hours,
        "fee_fallback": str(fee_fallback.quantize(Decimal("0.01"))),
        "fallback_age_hours": fallback_age_hours,
        "filled_sell_count": len(audits),
        "unresolved_fee_count": len(unresolved),
        "unresolved_tickers": [str(item.get("ticker")) for item in unresolved],
        "estimated_fallback_count": len(estimated),
        "estimated_fallback_tickers": [str(item.get("ticker")) for item in estimated],
        "audits": audits,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.now(tz=ET).date().isoformat())
    parser.add_argument("--min-age-hours", type=int, default=DEFAULT_MIN_AGE_HOURS)
    parser.add_argument("--fee-fallback", type=Decimal, default=DEFAULT_FEE_FALLBACK)
    parser.add_argument("--fallback-age-hours", type=int, default=DEFAULT_FALLBACK_AGE_HOURS)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = run(args.date, args.min_age_hours, args.fee_fallback, args.fallback_age_hours)
    if args.write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUT_DIR / f"{args.date}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        record["path"] = str(path)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
