#!/usr/bin/env python3
"""Collect minute-level public data for a same-day special market event.

This script is read-only. It records public quotes and source availability for
later half-hour analysis; it never trades or sends user-visible messages.
"""

from __future__ import annotations

import json
import re
import argparse
from datetime import datetime, time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "special-event-monitoring"
INTRADAY_MD_DIR = ROOT / "reports" / "intraday-predictions"
INTRADAY_JSONL_DIR = ROOT / "reports" / "structured" / "intraday"
ET = ZoneInfo("America/New_York")
DEFAULT_START_ET = time(9, 45)
DEFAULT_END_ET = time(16, 0)

NASDAQ_ASSETS = {
    "GOOGL": "stocks",
    "GOOG": "stocks",
    "TSLA": "stocks",
    "MSFT": "stocks",
    "QQQ": "etf",
    "QQQM": "etf",
    "SMH": "etf",
    "SPY": "etf",
    "VOO": "etf",
    "XLF": "etf",
    "KRE": "etf",
    "NDX": "index",
    "COMP": "index",
}

WATCH_PAGES = {
    "alphabet_ir_event": "https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Date-of-Second-Quarter-2026-Financial-Results-Conference-Call-2026-2h_R0kzZHY/default.aspx",
    "alphabet_ir_releases": "https://abc.xyz/investor/",
    "tesla_ir_event": "https://ir.tesla.com/press-release/tesla-second-quarter-2026-production-deliveries-and-deployments",
    "tesla_ir": "https://ir.tesla.com/",
}


def load_premarket_plan(target_date: str) -> dict[str, Any]:
    record = load_premarket_record(target_date)
    plan = record.get("special_event_monitoring")
    return plan if isinstance(plan, dict) else {}


def load_premarket_record(target_date: str) -> dict[str, Any]:
    path = ROOT / "reports" / "structured" / "premarket" / f"{target_date}.jsonl"
    if not path.exists():
        return {}
    for line in reversed(path.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            return record
    return {}


def fetch_json(url: str) -> tuple[Any | None, str | None]:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json,text/plain,*/*",
            "Origin": "https://www.nasdaq.com",
            "Referer": "https://www.nasdaq.com/",
        },
    )
    try:
        with urlopen(request, timeout=12) as response:
            return json.load(response), None
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}: {exc}"


def fetch_text_sample(url: str) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,*/*",
        },
    )
    try:
        with urlopen(request, timeout=12) as response:
            text = response.read(120_000).decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    needles = ["Q2 2026", "Second Quarter", "earnings", "results", "shareholder"]
    hits = [needle for needle in needles if needle.lower() in text.lower()]
    return {"ok": True, "title": title[:240], "matched_terms": hits, "bytes_sampled": len(text)}


def quote(symbol: str, asset_class: str) -> dict[str, Any]:
    url = f"https://api.nasdaq.com/api/quote/{symbol}/info?assetclass={asset_class}"
    data, error = fetch_json(url)
    if error:
        return {"symbol": symbol, "asset_class": asset_class, "ok": False, "error": error}
    primary = ((data or {}).get("data") or {}).get("primaryData") or {}
    return {
        "symbol": symbol,
        "asset_class": asset_class,
        "ok": True,
        "last_sale_price": primary.get("lastSalePrice"),
        "net_change": primary.get("netChange"),
        "percentage_change": primary.get("percentageChange"),
        "bid": primary.get("bidPrice"),
        "ask": primary.get("askPrice"),
        "volume": primary.get("volume"),
        "last_trade_timestamp": primary.get("lastTradeTimestamp"),
        "is_real_time": primary.get("isRealTime"),
        "market_status": ((data or {}).get("data") or {}).get("marketStatus"),
    }


def parse_market_number(value: Any) -> Decimal | None:
    if value in (None, ""):
        return None
    text = str(value).replace("$", "").replace(",", "").replace("%", "").strip()
    if not text:
        return None
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def triggered_sell_drafts(premarket_record: dict[str, Any], quotes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return premarket SELL drafts whose price line is breached by fresh quotes.

    The collector is read-only, so this only detects and archives a user-visible
    review prompt. It never places, modifies, or cancels orders.
    """
    quote_by_symbol = {
        str(item.get("symbol", "")).upper(): item
        for item in quotes
        if isinstance(item, dict) and item.get("ok")
    }
    triggered: list[dict[str, Any]] = []
    for draft in premarket_record.get("action_drafts") or []:
        if not isinstance(draft, dict):
            continue
        side = str(draft.get("side") or "").upper()
        symbol = str(draft.get("ticker") or "").upper()
        if side not in {"SELL", "TRIM", "SELL_ALL"} or not symbol:
            continue
        quote_record = quote_by_symbol.get(symbol)
        if not quote_record:
            continue
        current = parse_market_number(quote_record.get("last_sale_price"))
        limit = parse_market_number(draft.get("limit_price"))
        if current is None or limit is None:
            continue
        if current <= limit:
            enriched = dict(draft)
            enriched.update(
                {
                    "triggered_at_price": str(current),
                    "triggered_limit_price": str(limit),
                    "quote_timestamp": quote_record.get("last_trade_timestamp") or "",
                    "trigger_status": "triggered_by_special_event_monitor",
                }
            )
            triggered.append(enriched)
    return triggered


def matching_position_reviews(premarket_record: dict[str, Any], tickers: set[str]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for review in premarket_record.get("position_reviews") or []:
        if not isinstance(review, dict):
            continue
        if str(review.get("ticker") or "").upper() in tickers:
            cloned = dict(review)
            cloned["recommended_action"] = "sell_or_trim_draft_triggered"
            reviews.append(cloned)
    return reviews


def write_intraday_trigger_artifacts(
    target_date: str,
    now: datetime,
    event_window: str,
    record: dict[str, Any],
    premarket_record: dict[str, Any],
    triggered_drafts: list[dict[str, Any]],
) -> None:
    if not triggered_drafts:
        return
    INTRADAY_MD_DIR.mkdir(parents=True, exist_ok=True)
    INTRADAY_JSONL_DIR.mkdir(parents=True, exist_ok=True)
    md_path = INTRADAY_MD_DIR / f"{target_date}.md"
    jsonl_path = INTRADAY_JSONL_DIR / f"{target_date}.jsonl"
    run_time = now.strftime("%Y-%m-%d %H:%M:%S ET")
    tickers = {str(item.get("ticker") or "").upper() for item in triggered_drafts}
    positions = matching_position_reviews(premarket_record, tickers)
    draft_lines = []
    for draft in triggered_drafts:
        ticker = draft.get("ticker")
        shares = draft.get("approx_shares")
        limit = draft.get("limit_price")
        triggered_price = draft.get("triggered_at_price")
        reason = draft.get("reason") or "premarket risk trigger breached"
        draft_lines.append(
            f"- {ticker}: {draft.get('side')} {shares}股草稿；触发价约${triggered_price}，"
            f"盘前线${limit}；原因：{reason}。"
        )
    final_summary = (
        "最终操作总结：本次特殊事件只读监控触发风控线；买入0、自动卖出0、"
        + "；".join(
            f"{draft.get('ticker')} {draft.get('side')} {draft.get('approx_shares')}股为需用户批准的草稿"
            for draft in triggered_drafts
        )
        + "；未获用户明确确认前不得下单、改单、撤单。"
    )
    md_text = (
        "\n---\n"
        f"run_time_et: {run_time}\n"
        "job_label: special_event_manual_monitor\n"
        "archive_source: special_event_minute_collect\n\n"
        f"特殊事件风控触发复核 - {target_date}（{run_time}）\n\n"
        "本记录由只读特殊事件采集脚本生成，用于弥补03/33盘中cron禁用时的用户可见归档。"
        "它不是下单指令，也不会登录券商。\n\n"
        + "\n".join(draft_lines)
        + "\n\n"
        + final_summary
        + "\n"
    )
    with md_path.open("a", encoding="utf-8") as handle:
        handle.write(md_text)

    intraday_record = {
        "schema_version": "1.0",
        "run_time_et": run_time,
        "trading_date": target_date,
        "job_id": "special_event_manual_monitor",
        "job_label": "special_event_manual_monitor",
        "report_type": "intraday",
        "market_status": "open" if DEFAULT_START_ET <= now.time() <= DEFAULT_END_ET else "unknown",
        "archive_status": {
            "markdown_path": str(md_path),
            "jsonl_path": str(jsonl_path),
            "status": "success",
            "error": "",
        },
        "inputs": {
            "webull_portfolio_sync_status": "not_run_by_public_quote_collector",
            "webull_order_sync_status": "not_run_by_public_quote_collector",
            "market_data_sources": ["Nasdaq quote API", "premarket structured action_drafts"],
            "knowledge_files_read": ["reports/structured/premarket/YYYY-MM-DD.jsonl"],
        },
        "predictions": [
            {
                "ticker": draft.get("ticker"),
                "direction": "sell_or_trim",
                "horizon": "intraday",
                "thesis": "premarket risk line breached during special-event monitoring",
                "trigger": f"last price {draft.get('triggered_at_price')} <= limit {draft.get('limit_price')}",
                "invalidation": draft.get("invalidation") or "",
                "confidence": "medium",
                "position_context": "held",
            }
            for draft in triggered_drafts
        ],
        "position_reviews": positions,
        "action_drafts": triggered_drafts,
        "order_lifecycle": {
            "order_drafts": triggered_drafts,
            "user_approvals": [],
            "execution_receipts": [],
            "approval_chain_status": "draft_generated_requires_user_confirmation",
            "notes": "Generated by read-only special-event monitor; no broker action was taken.",
        },
        "execution_cost_layers": {
            "broker_reported_fees": [],
            "estimated_fees": [],
            "fee_status": "not_applicable_no_execution",
            "notes": "No order was executed by this script.",
        },
        "special_event_monitoring": {
            "active": True,
            "plan_source": "premarket_action_drafts",
            "watched_tickers": record.get("watch_tickers") or [],
            "minute_monitor_status": "user_visible_intraday_trigger_artifact_written",
            "thirty_minute_review_required": True,
            "next_review_et": "",
            "failure_reason": "",
            "intraday_cron_disabled": True,
        },
        "final_action_summary": final_summary,
        "risk_rules_applied": [
            {
                "rule_id": "standing-special-event-monitoring",
                "status": "applied",
                "evidence": "special-event quote collector wrote intraday Markdown/JSONL when risk drafts triggered",
            },
            {
                "rule_id": "standing-profit-taking-lines",
                "status": "applied",
                "evidence": "triggered drafts came from premarket position reviews/action_drafts",
            },
        ],
        "failure_flags": [],
        "source_refs": [
            {
                "id": "S-SE-MONITOR",
                "name": "special_event_minute_collect",
                "time": run_time,
                "url": f"local:reports/special-event-monitoring/{target_date}.jsonl",
            },
            {
                "id": "S-PREMARKET",
                "name": "premarket structured action_drafts",
                "time": str(premarket_record.get("run_time_et") or ""),
                "url": f"local:reports/structured/premarket/{target_date}.jsonl",
            },
        ],
    }
    with jsonl_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(intraday_record, ensure_ascii=False, separators=(",", ":")) + "\n")


def parse_time(value: str) -> time:
    try:
        hour_text, minute_text = value.split(":", 1)
        return time(int(hour_text), int(minute_text))
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError("time must be HH:MM in ET")


def in_collection_window(now: datetime, target_date: str, start_et: time, end_et: time) -> bool:
    if now.strftime("%Y-%m-%d") != target_date:
        return False
    current = now.time()
    return start_et <= current <= end_et


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.now(ET).strftime("%Y-%m-%d"))
    parser.add_argument("--start-et", type=parse_time, default=DEFAULT_START_ET)
    parser.add_argument("--end-et", type=parse_time, default=DEFAULT_END_ET)
    parser.add_argument(
        "--event-window",
        default="configured same-day special-event monitoring window",
    )
    parser.add_argument(
        "--tickers",
        default="",
        help="Comma-separated Nasdaq symbols to collect; unknown symbols default to stocks",
    )
    parser.add_argument(
        "--allow-outside-window",
        action="store_true",
        help="write a documented skip artifact instead of exiting without an artifact",
    )
    parser.add_argument(
        "--manual-review-required",
        action="store_true",
        help=(
            "write a manual_review_required artifact when no precise or runnable "
            "one-time monitor is available"
        ),
    )
    args = parser.parse_args()

    now = datetime.now(ET)
    premarket_record = load_premarket_record(args.date)
    plan = premarket_record.get("special_event_monitoring")
    if not isinstance(plan, dict):
        plan = {}
    configured_tickers = args.tickers
    if not configured_tickers and isinstance(plan.get("watched_tickers"), list):
        configured_tickers = ",".join(str(item) for item in plan["watched_tickers"])
    if not configured_tickers:
        configured_tickers = ",".join(sorted(NASDAQ_ASSETS))

    assets = {
        symbol.strip().upper(): NASDAQ_ASSETS.get(symbol.strip().upper(), "stocks")
        for symbol in configured_tickers.split(",")
        if symbol.strip()
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{args.date}.jsonl"
    if args.manual_review_required:
        record = {
            "schema_version": "1.0",
            "collected_at_et": now.strftime("%Y-%m-%d %H:%M:%S ET"),
            "trading_date": args.date,
            "event_window": args.event_window,
            "watch_tickers": sorted(assets),
            "source_plan": "premarket_special_event_monitoring" if plan else "default",
            "status": "manual_review_required",
            "monitoring_replacement": "manual_review_required",
            "reason": (
                "no precise or runnable one-time read-only monitor exists; user-visible "
                "manual review is required and no structured intraday coverage is implied"
            ),
            "trade_permission": "read_only_no_orders",
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        print(f"manual review required artifact -> {path}")
        return 0

    if not in_collection_window(now, args.date, args.start_et, args.end_et):
        if not args.allow_outside_window:
            print(f"skip: outside special-event window at {now.isoformat()}")
            return 0
        record = {
            "schema_version": "1.0",
            "collected_at_et": now.strftime("%Y-%m-%d %H:%M:%S ET"),
            "trading_date": args.date,
            "event_window": args.event_window,
            "watch_tickers": sorted(assets),
            "source_plan": "premarket_special_event_monitoring" if plan else "default",
            "status": "documented_skip_outside_window",
            "monitoring_replacement": "manual_review_required",
            "reason": "collector ran outside configured same-day monitoring window; no intraday coverage is backfilled",
            "trade_permission": "read_only_no_orders",
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
        print(f"documented outside-window skip -> {path}")
        return 0

    record = {
        "schema_version": "1.0",
        "collected_at_et": now.strftime("%Y-%m-%d %H:%M:%S ET"),
        "trading_date": args.date,
        "event_window": args.event_window,
        "watch_tickers": sorted(assets),
        "source_plan": "premarket_special_event_monitoring" if plan else "default",
        "quotes": [quote(symbol, asset) for symbol, asset in assets.items()],
        "source_checks": {name: fetch_text_sample(url) for name, url in WATCH_PAGES.items()},
        "trade_permission": "read_only_no_orders",
    }
    triggered_drafts = triggered_sell_drafts(premarket_record, record["quotes"])
    if triggered_drafts:
        record["triggered_action_drafts"] = triggered_drafts
        record["status"] = "risk_trigger_detected"
        write_intraday_trigger_artifacts(
            target_date=args.date,
            now=now,
            event_window=args.event_window,
            record=record,
            premarket_record=premarket_record,
            triggered_drafts=triggered_drafts,
        )
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"collected {len(record['quotes'])} quotes -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
