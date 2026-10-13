#!/usr/bin/env python3
"""Sync Webull account balance and positions into local portfolio snapshot files."""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from webull_verify import endpoint_for, env_int, load_env_file, require_env


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".webull.env"
SNAPSHOT_PATH = ROOT / "webull_portfolio_snapshot.json"
PORTFOLIO_PATH = ROOT / "PORTFOLIO_STATE.md"
MAIN_PORTFOLIO_PATH = Path("/home/openclaw/.openclaw/workspace/PORTFOLIO_STATE.md")


def json_or_text(response: Any) -> Any:
    try:
        return response.json()
    except Exception:
        return getattr(response, "text", "")


def response_payload(response: Any, name: str) -> Any:
    status_code = getattr(response, "status_code", None)
    payload = json_or_text(response)
    if status_code != 200:
        raise RuntimeError(f"{name} returned HTTP {status_code}: {payload}")
    return payload


def first_account_id(account_list: Any) -> str:
    candidates = account_list
    if isinstance(account_list, dict):
        for key in ("data", "accounts", "accountList", "list"):
            if isinstance(account_list.get(key), list):
                candidates = account_list[key]
                break
    if not isinstance(candidates, list) or not candidates:
        raise RuntimeError("account list did not contain any account records")

    account = candidates[0]
    if not isinstance(account, dict):
        raise RuntimeError("first account record is not an object")
    for key in ("account_id", "accountId", "accountID", "id", "account_no", "accountNo"):
        value = account.get(key)
        if value:
            return str(value)
    raise RuntimeError(f"could not find an account id field in keys: {sorted(account.keys())}")


def find_number(record: Any, preferred_keys: tuple[str, ...]) -> str | None:
    if isinstance(record, dict):
        for key in preferred_keys:
            value = record.get(key)
            if value not in (None, ""):
                return str(value)
        for value in record.values():
            found = find_number(value, preferred_keys)
            if found is not None:
                return found
    elif isinstance(record, list):
        for value in record:
            found = find_number(value, preferred_keys)
            if found is not None:
                return found
    return None


def redact_id(value: Any) -> str:
    text = str(value or "")
    if len(text) <= 8:
        return "***" if text else "unknown"
    return f"{text[:4]}...{text[-4:]}"


def iter_positions(payload: Any) -> list[dict[str, str]]:
    rows: list[Any] = []
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        for key in ("data", "positions", "positionList", "list", "items"):
            if isinstance(payload.get(key), list):
                rows = payload[key]
                break

    positions: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        symbol = (
            row.get("symbol")
            or row.get("ticker")
            or row.get("instrumentSymbol")
            or row.get("instrumentCode")
            or row.get("secCode")
        )
        instrument = row.get("instrument")
        if not symbol and isinstance(instrument, dict):
            symbol = instrument.get("symbol") or instrument.get("ticker") or instrument.get("code")
        quantity = (
            row.get("quantity")
            or row.get("qty")
            or row.get("position")
            or row.get("positionQty")
            or row.get("holding")
        )
        market_value = row.get("marketValue") or row.get("market_value") or row.get("value")
        cost = row.get("cost") or row.get("totalCost") or row.get("total_cost")
        cost_price = row.get("cost_price") or row.get("costPrice") or row.get("averageCost") or row.get("avgCost")
        last_price = row.get("last_price") or row.get("lastPrice") or row.get("last")
        unrealized = (
            row.get("unrealized_profit_loss")
            or row.get("unrealizedProfitLoss")
            or row.get("unrealizedPL")
            or row.get("unrealizedPnl")
        )
        unrealized_rate = row.get("unrealized_profit_loss_rate") or row.get("unrealizedProfitLossRate")
        day_pl = row.get("day_profit_loss") or row.get("dayProfitLoss")
        if symbol or quantity:
            positions.append(
                {
                    "symbol": str(symbol or "UNKNOWN"),
                    "quantity": str(quantity or ""),
                    "cost": str(cost or ""),
                    "cost_price": str(cost_price or ""),
                    "last_price": str(last_price or ""),
                    "market_value": str(market_value or ""),
                    "unrealized_pl": str(unrealized or ""),
                    "unrealized_pl_rate": str(unrealized_rate or ""),
                    "day_pl": str(day_pl or ""),
                }
            )
    return positions


def write_markdown(snapshot: dict[str, Any]) -> None:
    balance = snapshot.get("balance_raw")
    positions = snapshot.get("positions", [])
    total_equity = find_number(
        balance,
        (
            "total_net_liquidation_value",
            "totalNetLiquidationValue",
            "totalEquity",
            "total_equity",
            "netLiquidation",
            "accountValue",
        ),
    )
    cash = find_number(
        balance,
        (
            "total_cash_balance",
            "cashBalance",
            "cash_balance",
            "buyingPower",
            "buying_power",
            "settledCash",
        ),
    )

    lines = [
        "# Latest Confirmed User Portfolio State",
        "",
        f"Last API sync attempt: {snapshot['synced_at_utc']} UTC.",
        "Source priority: Webull OpenAPI live read if `webull_portfolio_snapshot.json` has `status: success`; otherwise use the latest user-confirmed screenshot/trade baseline below.",
        "Cash settlement rule confirmed by user: treat all visible cash / buying power values as settled cash.",
        "",
        "## Account",
        "",
    ]
    if snapshot.get("status") == "success":
        lines.append("- Source: Webull OpenAPI read-only sync.")
        lines.append(f"- Account ID: {redact_id(snapshot.get('account_id', ''))}")
        lines.append(f"- Total equity: {total_equity or 'not found in parsed API payload'}")
        lines.append(f"- Cash / buying power / settled cash: {cash or 'not found in parsed API payload'}")
    else:
        lines.append("- Source: latest user-confirmed fallback because Webull OpenAPI sync is not currently successful.")
        lines.append(f"- API failure: {snapshot.get('error', 'unknown')}")
        lines.append("- Previous working cash estimate after confirmed MSFT/XLF/PYPL buys: about $1,785.")

    lines.extend(
        [
            "",
            "## Holdings",
            "",
            "| Ticker | Quantity | Cost | Avg Cost | Last Price | Market Value | Unrealized P/L | Unrealized P/L % | Day P/L |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    if positions:
        for row in positions:
            rate = row.get("unrealized_pl_rate", "")
            try:
                rate = f"{float(rate) * 100:.2f}%" if rate != "" else ""
            except ValueError:
                pass
            lines.append(
                f"| {row['symbol']} | {row['quantity']} | {row.get('cost', '')} | "
                f"{row.get('cost_price', '')} | {row.get('last_price', '')} | "
                f"{row['market_value']} | {row['unrealized_pl']} | {rate} | {row.get('day_pl', '')} |"
            )
    elif snapshot.get("status") == "success":
        # API succeeded and returned zero positions -> account is genuinely flat.
        # Do NOT fall back to stale screenshot holdings here (caused phantom-holding loop 2026-08-10).
        lines.append("| (none) | 0 |  |  |  |  |  |  |  |")
        lines.append("")
        lines.append("**Account is FLAT — live API returned 0 positions. Not an anomaly.**")
    else:
        # Only use the last user-confirmed screenshot baseline when the live API sync FAILED.
        fallback = [
            ("QQQM", "1.61363", "", "", "", "", "+$72.26 from 09:40 screenshot", "", ""),
            ("VOO", "0.53133", "", "", "", "", "+$15.64 from 09:40 screenshot", "", ""),
            ("PYPL", "6.75", "", "", "", "", "+$0.33 from 09:40 screenshot before later 1.75-share buy", "", ""),
            ("XLF", "1.72", "", "", "", "", "+$0.03 from 09:40 screenshot", "", ""),
            ("XLC", "1", "", "", "", "", "-$0.05 from 09:40 screenshot", "", ""),
            ("MSFT", "1.06", "", "", "", "", "-$1.21 from 09:40 screenshot", "", ""),
        ]
        for row in fallback:
            lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} |")

    lines.extend(
        [
            "",
            "## Handling Rules",
            "",
            "- Prefer a successful Webull OpenAPI snapshot for cash, positions, and account value.",
            "- If API sync fails, state that failure and use the latest user-confirmed screenshot/trade baseline instead of inventing live account data.",
            "- Buy/sell execution remains approval-gated: propose the exact order first and submit only after the user explicitly approves that exact order.",
            "- Do not use financing, options, leveraged ETFs, inverse ETFs, or unattended automated trading.",
            "",
        ]
    )
    content = "\n".join(lines)
    PORTFOLIO_PATH.write_text(content, encoding="utf-8")
    PORTFOLIO_PATH.chmod(0o600)
    if MAIN_PORTFOLIO_PATH.parent.exists():
        MAIN_PORTFOLIO_PATH.write_text(content, encoding="utf-8")
        MAIN_PORTFOLIO_PATH.chmod(0o600)


def make_client():
    logging.disable(logging.CRITICAL)
    load_env_file(ENV_PATH)
    from webull.core.client import ApiClient
    from webull.trade.trade_client import TradeClient

    app_key = require_env("WEBULL_APP_KEY")
    app_secret = require_env("WEBULL_APP_SECRET")
    region = os.environ.get("WEBULL_REGION", "us").strip() or "us"
    env_name = os.environ.get("WEBULL_ENV", "prod").strip() or "prod"
    endpoint = endpoint_for(env_name)
    api_client = ApiClient(
        app_key,
        app_secret,
        region,
        connect_timeout=5,
        timeout=15,
        token_check_duration_seconds=env_int("WEBULL_TOKEN_CHECK_SECONDS", 15),
        token_check_interval_seconds=env_int("WEBULL_TOKEN_CHECK_INTERVAL_SECONDS", 3),
    )
    api_client._stream_logger_set = True
    api_client._file_logger_set = True
    api_client.add_endpoint(region, endpoint)
    return TradeClient(api_client), env_name, endpoint


def main() -> int:
    snapshot: dict[str, Any] = {
        "status": "failure",
        "synced_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    try:
        trade_client, env_name, endpoint = make_client()
        account_list = response_payload(trade_client.account_v2.get_account_list(), "account list")
        account_id = os.environ.get("WEBULL_ACCOUNT_ID", "").strip() or first_account_id(account_list)
        balance = response_payload(trade_client.account_v2.get_account_balance(account_id), "account balance")
        position_payload = response_payload(trade_client.account_v2.get_account_position(account_id), "positions")
        positions = iter_positions(position_payload)
        snapshot.update(
            {
                "status": "success",
                "env": env_name,
                "endpoint": endpoint,
                "account_id": account_id,
                "account_list_raw": account_list,
                "balance_raw": balance,
                "positions_raw": position_payload,
                "positions": positions,
            }
        )
        SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
        SNAPSHOT_PATH.chmod(0o600)
        write_markdown(snapshot)
        print(f"Webull portfolio sync success: {len(positions)} positions")
        return 0
    except Exception as exc:
        snapshot["error"] = f"{exc.__class__.__name__}: {exc}"
        SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
        SNAPSHOT_PATH.chmod(0o600)
        write_markdown(snapshot)
        print(f"Webull portfolio sync failed: {snapshot['error']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
