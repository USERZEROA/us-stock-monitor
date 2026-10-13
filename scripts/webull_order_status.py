#!/usr/bin/env python3
"""Summarize recent Webull order status and realized P/L for reports."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from webull_portfolio_sync import (
    ROOT,
    first_account_id,
    json_or_text,
    make_client,
    response_payload,
)


SNAPSHOT_PATH = ROOT / "webull_order_status_snapshot.json"
STATUS_PATH = ROOT / "WEBULL_ORDER_STATUS.md"
PORTFOLIO_SNAPSHOT_PATH = ROOT / "webull_portfolio_snapshot.json"
LAST_SUBMISSION_PATH = ROOT / "webull_last_order_submission.json"
DEFAULT_SELL_FEE_ESTIMATE = Decimal("0.02")


def dec(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def money(value: Decimal | None) -> str:
    if value is None:
        return "unknown"
    return f"${value.quantize(Decimal('0.01'))}"


def qty(value: Any) -> Decimal:
    return dec(value) or Decimal("0")


def fee_total(order: dict[str, Any]) -> Decimal:
    total = Decimal("0")
    for fee in order.get("fees") or []:
        value = dec(fee.get("actual_value") or fee.get("receivable_value"))
        if value is not None:
            total += value
    commission = order.get("commission")
    if isinstance(commission, dict):
        value = dec(commission.get("actual_value") or commission.get("receivable_value"))
        if value is not None:
            total += value
    return total


def flatten_orders(groups: Any) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []
    if not isinstance(groups, list):
        return flat
    for group in groups:
        if not isinstance(group, dict):
            continue
        for order in group.get("orders") or []:
            if isinstance(order, dict):
                merged = dict(order)
                merged.setdefault("combo_order_id", group.get("combo_order_id"))
                flat.append(merged)
    return flat


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def position_cost_map() -> dict[str, Decimal]:
    data = load_json(PORTFOLIO_SNAPSHOT_PATH) or {}
    costs: dict[str, Decimal] = {}
    for row in data.get("positions_raw") or []:
        if not isinstance(row, dict):
            continue
        symbol = str(row.get("symbol") or "")
        cost_price = dec(row.get("cost_price") or row.get("costPrice") or row.get("averageCost") or row.get("avgCost"))
        if symbol and cost_price is not None:
            costs[symbol] = cost_price
    return costs


def infer_average_buy_cost(symbol: str, orders: list[dict[str, Any]], before_ms: int | None = None) -> Decimal | None:
    total_qty = Decimal("0")
    total_cost = Decimal("0")
    for order in orders:
        if order.get("symbol") != symbol or order.get("side") != "BUY" or order.get("status") != "FILLED":
            continue
        filled_qty = qty(order.get("filled_quantity"))
        price = dec(order.get("filled_price"))
        if filled_qty <= 0 or price is None:
            continue
        filled_time = order.get("filled_time")
        try:
            filled_ms = int(filled_time) if filled_time is not None else None
        except ValueError:
            filled_ms = None
        if before_ms is not None and filled_ms is not None and filled_ms > before_ms:
            continue
        total_qty += filled_qty
        total_cost += filled_qty * price
    if total_qty <= 0:
        return None
    return total_cost / total_qty


def infer_average_cost_before_sell(target: dict[str, Any], orders: list[dict[str, Any]]) -> Decimal | None:
    """Replay filled orders and return weighted-average cost just before a sell."""
    symbol = str(target.get("symbol") or "")
    target_order_id = str(target.get("order_id") or target.get("client_order_id") or "")
    held_qty = Decimal("0")
    held_cost = Decimal("0")
    for order in sorted(orders, key=order_sort_key):
        if order.get("symbol") != symbol or order.get("status") != "FILLED":
            continue
        order_id = str(order.get("order_id") or order.get("client_order_id") or "")
        filled_qty = qty(order.get("filled_quantity"))
        price = dec(order.get("filled_price"))
        if filled_qty <= 0:
            continue
        if order.get("side") == "BUY" and price is not None:
            held_qty += filled_qty
            held_cost += filled_qty * price
            continue
        if order.get("side") != "SELL":
            continue
        average_cost = held_cost / held_qty if held_qty > 0 else None
        if target_order_id and order_id == target_order_id:
            return average_cost
        if average_cost is not None:
            reduce_qty = min(filled_qty, held_qty)
            held_qty -= reduce_qty
            held_cost -= reduce_qty * average_cost
    return None


def order_sort_key(order: dict[str, Any]) -> int:
    for key in ("place_time", "filled_time"):
        try:
            return int(order.get(key) or 0)
        except ValueError:
            pass
    return 0


def pnl_for_sell(order: dict[str, Any], all_orders: list[dict[str, Any]], current_costs: dict[str, Decimal]) -> dict[str, Any]:
    symbol = str(order.get("symbol") or "")
    filled_qty = qty(order.get("filled_quantity"))
    price = dec(order.get("filled_price"))
    api_fees = fee_total(order)
    fees = api_fees if api_fees else DEFAULT_SELL_FEE_ESTIMATE
    cost_price = infer_average_cost_before_sell(order, all_orders)
    try:
        filled_ms = int(order.get("filled_time") or order.get("place_time") or 0)
    except ValueError:
        filled_ms = None
    if cost_price is None:
        cost_price = infer_average_buy_cost(symbol, all_orders, before_ms=filled_ms)
    if cost_price is None:
        cost_price = current_costs.get(symbol)
    if filled_qty <= 0 or price is None or cost_price is None:
        return {
            "cost_price": str(cost_price) if cost_price is not None else "",
            "gross_pnl": "",
            "fees": str(fees),
            "net_pnl": "",
            "note": "insufficient filled price, quantity, or cost basis",
        }
    gross = (price - cost_price) * filled_qty
    net = gross - fees
    return {
        "cost_price": str(cost_price.quantize(Decimal("0.0001"))),
        "gross_pnl": str(gross.quantize(Decimal("0.01"))),
        "fees": str(fees.quantize(Decimal("0.01"))),
        "net_pnl": str(net.quantize(Decimal("0.01"))),
        "note": ""
        if api_fees
        else f"API returned no actual fee; finalized uniformly at ${DEFAULT_SELL_FEE_ESTIMATE} fallback estimate",
    }


def line_for_order(order: dict[str, Any], all_orders: list[dict[str, Any]], current_costs: dict[str, Decimal]) -> str:
    side = order.get("side", "")
    symbol = order.get("symbol", "")
    status = order.get("status", "")
    total_qty = order.get("total_quantity", "")
    filled_qty = order.get("filled_quantity", "")
    limit_price = order.get("limit_price", "")
    filled_price = order.get("filled_price", "")
    if side == "SELL" and status == "FILLED":
        pnl = pnl_for_sell(order, all_orders, current_costs)
        note = f", 净盈亏 {money(dec(pnl['net_pnl']))}"
        if pnl.get("note"):
            note += f"（{pnl['note']}）"
    else:
        note = ""
    return (
        f"- {side} {symbol} {filled_qty}/{total_qty} 股，状态 {status}，"
        f"限价 {limit_price or '-'}，成交价 {filled_price or '-'}{note}"
    )


def line_for_attempt(
    attempt: dict[str, Any],
    known_by_client_id: dict[str, dict[str, Any]],
    all_orders: list[dict[str, Any]],
    current_costs: dict[str, Decimal],
) -> str:
    client_order_id = attempt.get("client_order_id")
    known = known_by_client_id.get(str(client_order_id or ""))
    if known:
        return line_for_order(known, all_orders, current_costs)
    symbol = attempt.get("symbol", "")
    side = attempt.get("side", "")
    qty_value = attempt.get("qty", "")
    limit_price = attempt.get("limit_price", "")
    error = attempt.get("error")
    if error:
        return f"- {side} {symbol} 0/{qty_value} 股，状态 REJECTED，限价 {limit_price or '-'}，原因：{error}"
    status = attempt.get("status_code", "unknown")
    return f"- {side} {symbol} 0/{qty_value} 股，状态 UNKNOWN/{status}，限价 {limit_price or '-'}"


def write_markdown(snapshot: dict[str, Any]) -> None:
    history = snapshot.get("history_orders", [])
    open_orders = snapshot.get("open_orders", [])
    last_submission = snapshot.get("last_submission_raw") or {}
    current_costs = {k: dec(v) for k, v in (snapshot.get("current_costs") or {}).items()}
    current_costs = {k: v for k, v in current_costs.items() if v is not None}
    recent_orders = sorted(history, key=order_sort_key, reverse=True)[:12]
    filled_sells = [o for o in recent_orders if o.get("side") == "SELL" and o.get("status") == "FILLED"]
    submitted = [o for o in open_orders if o.get("status") == "SUBMITTED"]
    known_by_client_id = {
        str(o.get("client_order_id")): o
        for o in [*history, *open_orders]
        if o.get("client_order_id")
    }

    lines = [
        "# Webull Order Status",
        "",
        f"Last order status sync: {snapshot['synced_at_utc']} UTC.",
        "",
        "## Required In Every Market Report",
        "",
        "- State what the last attempted orders were.",
        "- State which orders filled and which remain open/unfilled.",
        "- For filled sell orders, calculate realized gross and net P/L after API-returned fees when available.",
        f"- If the broker does not return an actual fee, uniformly finalize at the ${DEFAULT_SELL_FEE_ESTIMATE} small-order fee estimate (fee_basis=estimated_fallback).",
        "",
        "## Last Attempted Orders",
        "",
    ]
    attempted_orders = last_submission.get("orders") if isinstance(last_submission, dict) else None
    if attempted_orders:
        for attempt in attempted_orders:
            if isinstance(attempt, dict):
                lines.append(line_for_attempt(attempt, known_by_client_id, history, current_costs))
    else:
        lines.append("- None recorded locally.")

    lines.extend(
        [
            "",
        "## Open / Unfilled Orders",
        "",
        ]
    )
    if submitted:
        for order in submitted:
            lines.append(line_for_order(order, history, current_costs))
    else:
        lines.append("- None.")

    lines.extend(["", "## Recent Filled Sell Orders", ""])
    if filled_sells:
        for order in filled_sells:
            lines.append(line_for_order(order, history, current_costs))
    else:
        lines.append("- None in recent order history.")

    lines.extend(["", "## Recent Orders", ""])
    if recent_orders:
        for order in recent_orders:
            lines.append(line_for_order(order, history, current_costs))
    else:
        lines.append("- No recent orders returned by API.")

    content = "\n".join(lines) + "\n"
    STATUS_PATH.write_text(content, encoding="utf-8")
    STATUS_PATH.chmod(0o600)


def main() -> int:
    snapshot: dict[str, Any] = {
        "status": "failure",
        "synced_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    try:
        trade_client, env_name, endpoint = make_client()
        account_id = os.environ.get("WEBULL_ACCOUNT_ID", "").strip() or first_account_id(response_payload(trade_client.account_v2.get_account_list(), "account list"))
        open_payload = response_payload(trade_client.order_v3.get_order_open(account_id, page_size=50), "open orders")
        history_payload = response_payload(trade_client.order_v3.get_order_history(account_id, page_size=50), "order history")
        open_orders = flatten_orders(open_payload)
        history_orders = flatten_orders(history_payload)
        current_costs = {k: str(v) for k, v in position_cost_map().items()}
        snapshot.update(
            {
                "status": "success",
                "env": env_name,
                "endpoint": endpoint,
                "account_id": account_id,
                "open_orders_raw": open_payload,
                "history_raw": history_payload,
                "open_orders": open_orders,
                "history_orders": history_orders,
                "current_costs": current_costs,
                "last_submission_raw": load_json(LAST_SUBMISSION_PATH),
            }
        )
        SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
        SNAPSHOT_PATH.chmod(0o600)
        write_markdown(snapshot)
        print(f"Webull order status sync success: {len(open_orders)} open, {len(history_orders)} recent")
        return 0
    except Exception as exc:
        snapshot["error"] = f"{exc.__class__.__name__}: {exc}"
        SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
        SNAPSHOT_PATH.chmod(0o600)
        STATUS_PATH.write_text(
            f"# Webull Order Status\n\nLast order status sync failed: {snapshot['synced_at_utc']} UTC.\n\n{snapshot['error']}\n",
            encoding="utf-8",
        )
        STATUS_PATH.chmod(0o600)
        print(f"Webull order status sync failed: {snapshot['error']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
