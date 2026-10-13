#!/usr/bin/env python3
"""
Download targeted calibration datasets and produce CALIBRATION_SUMMARY.md.

Fetches: VIX history, SPY/QQQ/SMH/KRE/XLF/XLK daily OHLCV, Fed Funds Rate
via FRED (no API key needed via pandas_datareader or direct FRED CSV).

Run: python3 scripts/fetch_calibration_data.py
Output: research/calibration/CALIBRATION_SUMMARY.md + CSV files
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import yfinance as yf
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CALIB_DIR = ROOT / "research" / "calibration"
CALIB_DIR.mkdir(parents=True, exist_ok=True)

TICKERS = {
    "VIX": "^VIX",
    "SPY": "SPY",
    "QQQ": "QQQ",
    "QQQM": "QQQM",
    "SMH": "SMH",
    "KRE": "KRE",
    "XLF": "XLF",
    "XLK": "XLK",
    "TLT": "TLT",
    # Expanded sector coverage (added 2026-07-23)
    "XLE": "XLE",   # Energy
    "XLV": "XLV",   # Healthcare
    "XLC": "XLC",   # Communications
    "XLY": "XLY",   # Consumer Discretionary
    "XLI": "XLI",   # Industrials
    "RSP": "RSP",   # Equal-weight S&P 500 (breadth proxy)
    "IWM": "IWM",   # Russell 2000 (small-cap)
    "HYG": "HYG",   # High Yield Bond (credit stress)
    "MSFT": "MSFT", # Individual holding
    "PYPL": "PYPL", # Individual holding
}

START_ETF = "2000-01-01"
START_VIX = "1990-01-01"
END = datetime.now().strftime("%Y-%m-%d")


def fetch(symbol: str, start: str) -> pd.DataFrame:
    print(f"  Fetching {symbol}...")
    df = yf.download(symbol, start=start, end=END, auto_adjust=True, progress=False)
    if df.empty:
        print(f"  WARNING: no data for {symbol}")
    return df


def vix_analysis(vix: pd.Series) -> dict:
    total = len(vix)
    lt18 = (vix < 18).sum()
    bt1820 = ((vix >= 18) & (vix < 20)).sum()
    gt20 = (vix >= 20).sum()
    gt30 = (vix >= 30).sum()

    # Forward return analysis: after VIX crosses above 18, SPY 20-day return
    # We'll compute using VIX series alone for distribution stats
    return {
        "total_days": total,
        "pct_below_18": round(lt18 / total * 100, 1),
        "pct_18_to_20": round(bt1820 / total * 100, 1),
        "pct_above_20": round(gt20 / total * 100, 1),
        "pct_above_30": round(gt30 / total * 100, 1),
        "median_vix": round(float(vix.median()), 1),
        "p25_vix": round(float(vix.quantile(0.25)), 1),
        "p75_vix": round(float(vix.quantile(0.75)), 1),
        "max_vix": round(float(vix.max()), 1),
    }


def spy_forward_returns_by_vix(spy_close: pd.Series, vix_close: pd.Series) -> dict:
    """For days with VIX in each bucket, compute median SPY 20-day forward return."""
    combined = pd.DataFrame({"SPY": spy_close, "VIX": vix_close}).dropna()
    combined["fwd20"] = combined["SPY"].shift(-20) / combined["SPY"] - 1

    def median_fwd(mask):
        vals = combined.loc[mask, "fwd20"].dropna()
        if len(vals) < 10:
            return None
        return round(float(vals.median() * 100), 2)

    return {
        "vix_below_18_spy_fwd20_median_pct": median_fwd(combined["VIX"] < 18),
        "vix_18_20_spy_fwd20_median_pct": median_fwd(
            (combined["VIX"] >= 18) & (combined["VIX"] < 20)
        ),
        "vix_above_20_spy_fwd20_median_pct": median_fwd(combined["VIX"] >= 20),
        "vix_above_30_spy_fwd20_median_pct": median_fwd(combined["VIX"] >= 30),
    }


def relative_strength_stats(a: pd.Series, b: pd.Series, label: str) -> dict:
    """Daily return spread A - B distribution."""
    ra = a.pct_change().dropna()
    rb = b.pct_change().dropna()
    spread = (ra - rb).dropna() * 100
    return {
        "pair": label,
        "mean_daily_spread_pct": round(float(spread.mean()), 3),
        "std_daily_spread_pct": round(float(spread.std()), 3),
        "p5": round(float(spread.quantile(0.05)), 2),
        "p95": round(float(spread.quantile(0.95)), 2),
        "pct_days_spread_below_neg1pt5": round(
            float((spread < -1.5).mean() * 100), 1
        ),
    }


def render_summary(vix_stats: dict, fwd_ret: dict, rs_stats: list) -> str:
    lines = [
        "# Calibration Summary",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M ET')}",
        f"Data range: VIX from {START_VIX}, ETFs from {START_ETF}, through {END}",
        "",
        "---",
        "",
        "## VIX Distribution (1990–present)",
        "",
        f"- VIX < 18 (open gate):    **{vix_stats['pct_below_18']}%** of trading days",
        f"- VIX 18–20 (reduced gate): {vix_stats['pct_18_to_20']}% of trading days",
        f"- VIX > 20 (paused gate):   {vix_stats['pct_above_20']}% of trading days",
        f"- VIX > 30 (crisis):        {vix_stats['pct_above_30']}% of trading days",
        f"- Median VIX: {vix_stats['median_vix']} | P25: {vix_stats['p25_vix']} | P75: {vix_stats['p75_vix']} | Max: {vix_stats['max_vix']}",
        "",
        "### SPY 20-Day Forward Return by VIX Regime (SPY data from 2000)",
        "",
    ]

    def fmt(v):
        return f"{v:+.2f}%" if v is not None else "n/a"

    lines += [
        f"| VIX Regime | Median SPY 20-day fwd return |",
        f"|------------|------------------------------|",
        f"| VIX < 18   | {fmt(fwd_ret.get('vix_below_18_spy_fwd20_median_pct'))} |",
        f"| VIX 18–20  | {fmt(fwd_ret.get('vix_18_20_spy_fwd20_median_pct'))} |",
        f"| VIX > 20   | {fmt(fwd_ret.get('vix_above_20_spy_fwd20_median_pct'))} |",
        f"| VIX > 30   | {fmt(fwd_ret.get('vix_above_30_spy_fwd20_median_pct'))} |",
        "",
        "**Threshold verdict:** Verify whether the 18/20 split aligns with",
        "a meaningful change in forward returns. If VIX 18-20 median forward",
        "return is similar to VIX < 18, the reduced-gate threshold may need",
        "adjustment. Update MARKET_KNOWLEDGE.md if evidence supports a change.",
        "",
        "---",
        "",
        "## Sector Relative Strength Distributions (2000–present)",
        "",
        "These calibrate the -1.5% flag for KRE vs XLF and SMH confirmation gates.",
        "",
        "| Pair | Mean daily spread | Std | P5 | P95 | Days spread < -1.5% |",
        "|------|-------------------|-----|----|-----|---------------------|",
    ]

    for rs in rs_stats:
        lines.append(
            f"| {rs['pair']} | {rs['mean_daily_spread_pct']:+.3f}% "
            f"| {rs['std_daily_spread_pct']:.3f}% "
            f"| {rs['p5']:+.2f}% "
            f"| {rs['p95']:+.2f}% "
            f"| {rs['pct_days_spread_below_neg1pt5']}% |"
        )

    lines += [
        "",
        "**KRE vs XLF flag calibration:** The -1.5% daily spread threshold",
        "flags KRE as underperforming vs financials broadly. Check p5 value —",
        "if the -1.5% threshold is below p5, it triggers too rarely (tighten).",
        "If it triggers > 20% of days, it is too loose (widen).",
        "",
        "---",
        "",
        "## How To Use This File",
        "",
        "- **Premarket task:** Reference this file when explaining VIX gate rationale.",
        "  E.g., 'VIX at 19 → reduced gate; historically [X]% of days at this level",
        "  with median +[Y]% SPY 20-day return.'",
        "- **Weekly distillation:** Compare current rule performance against these",
        "  baseline distributions before proposing threshold changes.",
        "- **Re-run quarterly:** `python3 scripts/fetch_calibration_data.py`",
        "",
        f"*Source: yfinance (Yahoo Finance). Not survivorship-bias-free for individual stocks.*",
        f"*ETF data reflects index performance, which includes reconstitution effects.*",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    print("=== US Market Calibration Data Fetch ===")
    print(f"Output dir: {CALIB_DIR}")

    # Fetch VIX
    print("\n[1/3] VIX history...")
    vix_df = fetch("^VIX", START_VIX)
    if not vix_df.empty:
        # Handle MultiIndex columns from yfinance
        if isinstance(vix_df.columns, pd.MultiIndex):
            vix_df.columns = vix_df.columns.droplevel(1)
        vix_close = vix_df["Close"].dropna()
        vix_df.to_csv(CALIB_DIR / "vix_history.csv")
        print(f"  VIX: {len(vix_close)} days saved")
    else:
        vix_close = pd.Series(dtype=float)

    # Fetch ETFs
    print("\n[2/3] ETF history...")
    etf_data: dict[str, pd.Series] = {}
    all_etf_frames = []
    for name, symbol in TICKERS.items():
        if name == "VIX":
            continue
        df = fetch(symbol, START_ETF)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            close = df["Close"].dropna()
            etf_data[name] = close
            df["ticker"] = name
            all_etf_frames.append(df)

    if all_etf_frames:
        # Save each ETF separately
        for name, symbol in TICKERS.items():
            if name == "VIX" or name not in etf_data:
                continue
            etf_data[name].to_csv(CALIB_DIR / f"{name.lower()}_history.csv", header=True)
        print(f"  Saved {len(etf_data)} ETF series")

    # Compute statistics
    print("\n[3/3] Computing calibration statistics...")

    vix_stats = vix_analysis(vix_close) if not vix_close.empty else {}
    fwd_ret = {}
    if not vix_close.empty and "SPY" in etf_data:
        fwd_ret = spy_forward_returns_by_vix(etf_data["SPY"], vix_close)
        print(f"  VIX/SPY forward return analysis: {fwd_ret}")

    rs_stats = []
    pairs = [
        ("KRE", "XLF", "KRE vs XLF"),
        ("SMH", "QQQ", "SMH vs QQQ"),
        ("QQQ", "SPY", "QQQ vs SPY"),
        ("XLK", "SPY", "XLK vs SPY"),
        # Expanded sector pairs (added 2026-07-23)
        ("XLE", "SPY", "XLE vs SPY"),
        ("XLV", "SPY", "XLV vs SPY"),
        ("XLC", "QQQ", "XLC vs QQQ"),
        ("XLY", "SPY", "XLY vs SPY"),
        ("XLI", "SPY", "XLI vs SPY"),
        ("RSP", "SPY", "RSP vs SPY"),   # breadth / equal-weight spread
        ("IWM", "SPY", "IWM vs SPY"),   # small-cap vs large-cap
        ("HYG", "SPY", "HYG vs SPY"),   # credit vs equity stress
    ]
    for a, b, label in pairs:
        if a in etf_data and b in etf_data:
            stats = relative_strength_stats(etf_data[a], etf_data[b], label)
            rs_stats.append(stats)
            print(f"  {label}: std={stats['std_daily_spread_pct']:.3f}%, "
                  f"p5={stats['p5']:+.2f}%, p95={stats['p95']:+.2f}%")

    # Write summary
    summary = render_summary(vix_stats, fwd_ret, rs_stats)
    summary_path = CALIB_DIR / "CALIBRATION_SUMMARY.md"
    summary_path.write_text(summary, encoding="utf-8")
    print(f"\nCalibration summary written: {summary_path}")

    # Write JSON for machine reading
    result = {
        "generated_at": datetime.now().isoformat(),
        "vix_stats": vix_stats,
        "spy_forward_returns_by_vix_regime": fwd_ret,
        "relative_strength_stats": rs_stats,
    }
    (CALIB_DIR / "calibration_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("Done.")


if __name__ == "__main__":
    main()
