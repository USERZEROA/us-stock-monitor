#!/usr/bin/env python3
"""Backtest / calibrate knowledge-card activation triggers.

Answers improvement point (4): are the thresholds sane? A trigger that fires
almost every day creates alert fatigue; one that never fires over a long calm+
stress window may have a dead threshold.

Two data modes:
  --reconstruct N   : rebuild the last N calendar days of metrics from the same
                      sources the collector uses (Yahoo daily closes + FRED OAS
                      series) and evaluate every admitted card trigger per day.
                      Metric math mirrors daily_market_metrics.py exactly.
  (default)         : read research/daily_metrics_history.jsonl accumulated by
                      the collector.

Read-only. Never edits cards, prompts, cron, or config. Output is a per-card
activation rate plus a calibration verdict.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

from knowledge_activation_check import load_cards, card_fires  # same-dir import

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "research" / "daily_metrics_history.jsonl"
UA = {"User-Agent": "Mozilla/5.0 (us-market backtest; read-only)"}
TIMEOUT = 20


def _yahoo_series(symbol: str, rng: str = "6mo"):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
           f"?range={rng}&interval=1d")
    req = urllib.request.Request(url, headers=UA)
    d = json.load(urllib.request.urlopen(req, timeout=TIMEOUT))
    res = d["chart"]["result"][0]
    ts = res["timestamp"]
    close = res["indicators"]["quote"][0]["close"]
    return [(t, c) for t, c in zip(ts, close) if c is not None]


def _fred_series(series: str) -> dict:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    data = urllib.request.urlopen(url, timeout=TIMEOUT).read().decode()
    out = {}
    for line in data.strip().splitlines()[1:]:
        date, val = line.split(",")
        if val not in ("", "."):
            out[date] = float(val)
    return out


def reconstruct(days: int) -> list[dict]:
    """Return a list of per-day flat metric dicts for the last `days` sessions."""
    import datetime as dt
    vix = _yahoo_series("%5EVIX"); kre = _yahoo_series("KRE")
    spy = _yahoo_series("SPY"); jpy = _yahoo_series("JPY%3DX")
    move = _yahoo_series("%5EMOVE")
    hy = _fred_series("BAMLH0A0HYM2"); ig = _fred_series("BAMLC0A0CM")

    def closes(series):
        return [c for _, c in series]

    def at(series, i):
        c = closes(series)
        return c[: i + 1]

    # align on VIX trading days (index-based), use last `days`
    n = len(vix)
    rows = []
    start = max(20, n - days)  # need 20d trailing for drawdowns
    for i in range(start, n):
        date = dt.datetime.fromtimestamp(vix[i][0], dt.timezone.utc).strftime("%Y-%m-%d")
        m = {}
        vc = closes(vix)[: i + 1]; m["vix"] = round(vc[-1], 2)
        for name, series in (("kre_drawdown_20d_pct", kre), ("spy_drawdown_20d_pct", spy)):
            c = closes(series)[: i + 1]
            if len(c) >= 20:
                m[name] = round((c[-1] / max(c[-20:]) - 1) * 100, 2)
        mc = closes(move)[: i + 1]
        if mc:
            m["move_index"] = round(mc[-1], 2)
        jc = closes(jpy)[: i + 1]
        if len(jc) > 5:
            m["usdjpy_1w_change_pct"] = round((jc[-1] / jc[-6] - 1) * 100, 2)
        # FRED OAS: use most recent value on/before this date
        for name, fred in (("hy_oas_bps", hy), ("ig_oas_bps", ig)):
            avail = [d for d in fred if d <= date]
            if avail:
                m[name] = round(fred[max(avail)] * 100, 1)
        rows.append({"date": date, **m})
    return rows


def load_history() -> list[dict]:
    if not HISTORY.exists():
        return []
    rows = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reconstruct", type=int, default=0,
                    help="rebuild last N sessions from live sources instead of history file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = reconstruct(args.reconstruct) if args.reconstruct else load_history()
    triggered_cards = [c for c in load_cards()
                       if c.get("status") == "admitted" and c.get("activation_trigger")]

    n = len(rows)
    report = []
    for card in triggered_cards:
        trig = card["activation_trigger"]
        fires = sum(1 for r in rows if card_fires(trig, r)[0])
        rate = (fires / n * 100) if n else 0.0
        if n == 0:
            verdict = "no_data"
        elif rate == 0:
            verdict = "never_fired (check threshold not dead / regime was calm)"
        elif rate > 40:
            verdict = "TOO_FREQUENT (alert-fatigue risk — tighten)"
        else:
            verdict = "ok"
        report.append({"rule_id": card.get("rule_id"), "fires": fires,
                       "days": n, "rate_pct": round(rate, 1), "verdict": verdict})

    out = {"days_evaluated": n,
           "window": f"{rows[0]['date']}..{rows[-1]['date']}" if rows else None,
           "cards": report}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"days_evaluated={n} window={out['window']}")
        for c in sorted(report, key=lambda x: -x["rate_pct"]):
            print(f"  {c['rule_id']:26} fires={c['fires']:>3}/{c['days']:<3} "
                  f"rate={c['rate_pct']:>5}%  {c['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
