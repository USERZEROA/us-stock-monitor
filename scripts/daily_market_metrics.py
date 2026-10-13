#!/usr/bin/env python3
"""Daily market-metrics collector for the knowledge-activation pipeline.

Fetches the machine-checkable macro metrics that knowledge-card
`activation_trigger`s reference, writes a flat snapshot to
`research/daily_market_metrics.json`, and appends one row to
`research/daily_metrics_history.jsonl` (used for threshold backtesting).

Sources (all free, no API key):
  - FRED CSV  : HY OAS (BAMLH0A0HYM2), IG OAS (BAMLC0A0CM)  [percent -> bps]
  - Yahoo v8  : ^VIX, KRE, JPY=X, ^MOVE, SPY  (daily closes)

Design principles:
  - Read-only over markets; never touches cards, prompts, cron, or config.
  - Every metric is fetched independently; one source failing never crashes the
    run and never poisons other metrics. Unavailable metrics are omitted from
    the snapshot (the checker treats an absent metric as "trigger did not fire")
    and listed under `unavailable` for transparency.
  - Whole thing is time-bounded so it is safe to call from a cron wrapper.
"""

from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "research" / "daily_market_metrics.json"
HISTORY = ROOT / "research" / "daily_metrics_history.jsonl"
UA = {"User-Agent": "Mozilla/5.0 (us-market metrics collector; read-only)"}
TIMEOUT = 15


def _fred_latest(series: str) -> float:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    data = urllib.request.urlopen(url, timeout=TIMEOUT).read().decode()
    for line in reversed(data.strip().splitlines()):
        parts = line.split(",")
        if len(parts) == 2 and parts[1] not in ("", "."):
            try:
                return float(parts[1])
            except ValueError:
                continue
    raise ValueError(f"no numeric value in FRED {series}")


def _yahoo_closes(symbol: str, rng: str = "3mo") -> list[float]:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
           f"?range={rng}&interval=1d")
    req = urllib.request.Request(url, headers=UA)
    d = json.load(urllib.request.urlopen(req, timeout=TIMEOUT))
    res = d["chart"]["result"][0]
    closes = res["indicators"]["quote"][0]["close"]
    return [c for c in closes if c is not None]


def _dd20(closes: list[float]) -> float:
    window = closes[-20:]
    return (closes[-1] / max(window) - 1.0) * 100.0


def _pct_change(closes: list[float], lookback: int) -> float:
    if len(closes) <= lookback:
        raise ValueError("not enough history")
    return (closes[-1] / closes[-1 - lookback] - 1.0) * 100.0


def collect() -> dict:
    metrics: dict = {}
    unavailable: list[str] = []
    sources: dict = {}

    fred_map = {"hy_oas_bps": "BAMLH0A0HYM2", "ig_oas_bps": "BAMLC0A0CM"}
    for name, series in fred_map.items():
        try:
            metrics[name] = round(_fred_latest(series) * 100.0, 1)  # percent -> bps
            sources[name] = f"FRED:{series}"
        except Exception as exc:  # noqa: BLE001
            unavailable.append(f"{name} (FRED:{series}: {type(exc).__name__})")

    def add(name, symbol, fn, src):
        try:
            metrics[name] = round(fn(_yahoo_closes(symbol)), 2)
            sources[name] = src
        except Exception as exc:  # noqa: BLE001
            unavailable.append(f"{name} ({src}: {type(exc).__name__})")

    add("vix", "%5EVIX", lambda c: c[-1], "Yahoo:^VIX")
    add("move_index", "%5EMOVE", lambda c: c[-1], "Yahoo:^MOVE")
    add("kre_drawdown_20d_pct", "KRE", _dd20, "Yahoo:KRE")
    add("spy_drawdown_20d_pct", "SPY", _dd20, "Yahoo:SPY")
    add("usdjpy_1w_change_pct", "JPY%3DX", lambda c: _pct_change(c, 5), "Yahoo:JPY=X")

    now = datetime.now().astimezone()
    return {
        "as_of_et": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "date": now.strftime("%Y-%m-%d"),
        "metrics": metrics,
        "sources": sources,
        "unavailable": unavailable,
        "metric_count": len(metrics),
    }


def main() -> int:
    snap = collect()
    SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    with HISTORY.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"date": snap["date"], "as_of_et": snap["as_of_et"],
                             **snap["metrics"]}, ensure_ascii=False) + "\n")
    print(json.dumps(snap, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
