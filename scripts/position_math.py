#!/usr/bin/env python3
"""
Quantitative position sizing engine.

Usage (CLI):
    python3 scripts/position_math.py \
        --ticker QQQM \
        --win-rate 0.57 \
        --reward-ratio 2.0 \
        --stop-pct 2.0 \
        --price 215.40 \
        --confirmation-score 7

Or from Python:
    from scripts.position_math import compute_position_math
    result = compute_position_math("QQQM", win_rate=0.57, reward_ratio=2.0,
                                   stop_pct=2.0, price=215.40, confirmation_score=7)

Output: JSON with Kelly fraction, EV, position size, risk dollars.
Writes to position_math_last.json for reports to read.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Core math formulas
# ---------------------------------------------------------------------------

def kelly_fraction(win_rate: float, reward_ratio: float) -> float:
    """
    Kelly Criterion: f* = W - (1-W)/R
    Derivation: maximise E[ln(wealth)] over f gives f* = (p*b - q) / b
    where p=W, q=1-W, b=R (net odds).
    Clamped to [0, 1].
    """
    loss_rate = 1.0 - win_rate
    f = win_rate - (loss_rate / reward_ratio)
    return max(0.0, min(f, 1.0))


def expected_value(win_rate: float, gain_frac: float, loss_frac: float) -> float:
    """
    EV per dollar invested = W * gain - (1-W) * loss
    Positive EV is a necessary (not sufficient) condition to trade.
    """
    return win_rate * gain_frac - (1.0 - win_rate) * loss_frac


def break_even_win_rate(reward_ratio: float) -> float:
    """
    Minimum W for EV > 0: solve W*R - (1-W) = 0 → W = 1/(1+R)
    """
    return 1.0 / (1.0 + reward_ratio)


def expected_log_growth(win_rate: float, kelly_f: float, reward_ratio: float) -> float:
    """
    Expected log-wealth growth per trade at fraction f:
    g(f) = W*ln(1 + f*R) + (1-W)*ln(1 - f)
    This is what Kelly maximises. Useful for comparing full vs half Kelly.
    Returns NaN if log domain violated (f >= 1 or f*R would be -1).
    """
    if kelly_f <= 0:
        return 0.0
    if kelly_f >= 1.0 or (1.0 - kelly_f) <= 0:
        return float("nan")
    try:
        g = win_rate * math.log(1.0 + kelly_f * reward_ratio) + \
            (1.0 - win_rate) * math.log(1.0 - kelly_f)
        return round(g, 6)
    except ValueError:
        return float("nan")


def sortino_proxy(ev: float, win_rate: float, loss_frac: float) -> float:
    """
    Single-trade Sortino proxy: EV / downside_deviation
    downside_deviation ≈ (1-W) * loss (only negative outcomes considered)
    Higher is better; > 1.0 means expected gain exceeds downside deviation.
    """
    downside_dev = (1.0 - win_rate) * loss_frac
    if downside_dev <= 0:
        return float("inf")
    return round(ev / downside_dev, 4)


# ---------------------------------------------------------------------------
# Account and snapshot helpers
# ---------------------------------------------------------------------------

def load_account_value() -> float:
    """Load net liquidation from Webull snapshot; fall back to PORTFOLIO_STATE.md baseline."""
    snapshot_path = ROOT / "webull_portfolio_snapshot.json"
    if snapshot_path.exists():
        try:
            data = json.loads(snapshot_path.read_text(encoding="utf-8"))
            if data.get("status") == "success":
                value = find_number(
                    data,
                    (
                        "total_net_liquidation_value",
                        "totalNetLiquidationValue",
                        "totalEquity",
                        "total_equity",
                        "netLiquidation",
                        "net_liquidation",
                        "accountValue",
                        "account_value",
                        "totalMarketValue",
                    ),
                )
                if value is not None:
                    return float(value)
        except Exception:
            pass
    # Try to parse from PORTFOLIO_STATE.md (look for a $ dollar amount line)
    portfolio_path = ROOT / "PORTFOLIO_STATE.md"
    if portfolio_path.exists():
        text = portfolio_path.read_text(encoding="utf-8")
        # Look for patterns like "Account Value: $3,620.00" or "Net Liq: $3,620"
        m = re.search(r"(?:total equity|account.*?value|net.*?liq)[:\s]+\$?([\d,]+\.?\d*)",
                      text, re.IGNORECASE)
        if m:
            return float(m.group(1).replace(",", ""))
    return 3600.0  # Conservative default


def find_number(record: Any, preferred_keys: tuple[str, ...]) -> str | None:
    if isinstance(record, dict):
        for key in preferred_keys:
            value = record.get(key)
            if value not in (None, ""):
                return clean_number(value)
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


def clean_number(value: Any) -> str:
    return re.sub(r"[^0-9.\-]", "", str(value))


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_position_math(
    ticker: str,
    win_rate: float,
    reward_ratio: float,
    stop_pct: float,
    price: Optional[float] = None,
    confirmation_score: int = 5,
    account: Optional[float] = None,
    max_position_pct: float = 0.20,
    is_inverse_etf: bool = False,
) -> dict:
    """
    Full quantitative position sizing calculation.

    Parameters
    ----------
    ticker : str
    win_rate : float — estimated probability trade closes profitably (0–1)
    reward_ratio : float — target_gain / stop_loss (e.g. 2.0 means 2:1 R:R)
    stop_pct : float — stop-loss distance as % below entry (e.g. 2.0 = 2%)
    price : float, optional — current market price for share-count calculation
    confirmation_score : int — 0-10: number of independent confirmation signals met
    account : float, optional — account size; auto-loaded from Webull snapshot if None
    max_position_pct : float — hard cap per position (default 20% = 0.20)
    is_inverse_etf : bool — applies 8-10% hard cap for inverse ETFs
    """
    if account is None:
        account = load_account_value()

    # Derived percentages
    stop_frac = stop_pct / 100.0
    gain_frac = stop_frac * reward_ratio

    # ---- Core formulas ----
    f_kelly = kelly_fraction(win_rate, reward_ratio)
    be_wr = break_even_win_rate(reward_ratio)
    ev = expected_value(win_rate, gain_frac, stop_frac)
    ev_pct = ev * 100  # expressed as % of position value

    # Half-Kelly is the standard applied size (full Kelly has too large drawdowns)
    f_half = f_kelly / 2.0

    # Signal-scaled Kelly: reduce size when confirmation is weak
    # Scale linearly from 0 (no signals) to full half-Kelly (all signals)
    signal_factor = confirmation_score / 10.0
    f_adjusted = f_half * signal_factor

    # Hard caps
    if is_inverse_etf:
        max_position_pct = min(max_position_pct, 0.09)  # 9% cap for inverse ETFs

    f_capped = min(f_adjusted, max_position_pct)

    # Dollar amounts
    dollar_full_kelly = account * f_kelly
    dollar_half_kelly = account * f_half
    dollar_adjusted = account * f_adjusted
    dollar_recommended = account * f_capped

    # Fixed 2% risk rule (alternative sizing method for comparison)
    dollar_fixed_2pct_risk = account * 0.02 / max(stop_frac, 0.001)
    # Take the more conservative of Kelly-derived and 2%-risk-based sizes
    dollar_conservative = min(dollar_recommended, dollar_fixed_2pct_risk)

    # EV in dollars
    ev_dollar = ev * dollar_conservative

    # Log-growth at each Kelly variant
    g_full = expected_log_growth(win_rate, f_kelly, reward_ratio)
    g_half = expected_log_growth(win_rate, f_half, reward_ratio)
    g_adj = expected_log_growth(win_rate, f_capped, reward_ratio)

    # Sortino proxy
    sortino = sortino_proxy(ev, win_rate, stop_frac)

    # Shares and risk
    shares = None
    actual_dollars = dollar_conservative
    risk_dollars = actual_dollars * stop_frac
    whole_share_blocked = False

    if price and price > 0:
        shares = int(actual_dollars / price)
        if shares <= 0:
            whole_share_blocked = True
            actual_dollars = 0.0
        else:
            actual_dollars = shares * price
        risk_dollars = actual_dollars * stop_frac

    # Proceed gate: EV > 0, W > W_min, confirmation ≥ 5/10
    ev_positive = ev > 0
    w_above_min = win_rate > be_wr
    signals_ok = confirmation_score >= 5
    proceed = ev_positive and w_above_min and signals_ok and not whole_share_blocked

    result = {
        "ticker": ticker,
        "timestamp": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M ET"),
        "inputs": {
            "account_size_usd": round(account, 2),
            "win_rate_estimate": win_rate,
            "reward_ratio": reward_ratio,
            "stop_loss_pct": stop_pct,
            "gain_target_pct": round(gain_frac * 100, 2),
            "current_price": price,
            "confirmation_score": f"{confirmation_score}/10",
            "is_inverse_etf": is_inverse_etf,
        },
        "math": {
            "break_even_win_rate": round(be_wr, 4),
            "break_even_win_rate_pct": f"{be_wr*100:.1f}%",
            "win_rate_edge": f"+{(win_rate - be_wr)*100:.1f}%" if win_rate > be_wr else f"{(win_rate - be_wr)*100:.1f}%",
            "ev_per_dollar": round(ev, 5),
            "ev_pct": f"{ev_pct:+.3f}%",
            "sortino_proxy": sortino,
        },
        "kelly": {
            "full_kelly_fraction": round(f_kelly, 4),
            "half_kelly_fraction": round(f_half, 4),
            "signal_adjusted_fraction": round(f_adjusted, 4),
            "recommended_fraction": round(f_capped, 4),
            "full_kelly_usd": round(dollar_full_kelly, 2),
            "half_kelly_usd": round(dollar_half_kelly, 2),
            "signal_adjusted_usd": round(dollar_adjusted, 2),
            "recommended_usd": round(dollar_conservative, 2),
            "log_growth_full_kelly": g_full,
            "log_growth_half_kelly": g_half,
            "log_growth_at_recommended": g_adj,
        },
        "position": {
            "shares": shares,
            "actual_dollars": round(actual_dollars, 2),
            "risk_dollars": round(risk_dollars, 2),
            "risk_pct_of_account": f"{risk_dollars/account*100:.2f}%",
            "max_position_cap_applied": f"{max_position_pct*100:.0f}%",
            "whole_share_blocked": whole_share_blocked,
        },
        "ev_dollar": round(ev_dollar, 2),
        "verdict": {
            "proceed": proceed,
            "ev_positive": ev_positive,
            "w_above_break_even": w_above_min,
            "signals_adequate": signals_ok,
            "whole_share_affordable_under_risk_cap": not whole_share_blocked,
            "reason": (
                f"EV{'✓' if ev_positive else '✗'} "
                f"| W≥{be_wr*100:.0f}%min{'✓' if w_above_min else '✗'} "
                f"| Signals{'✓' if signals_ok else '✗'}({confirmation_score}/10) "
                f"| Whole-share cap{'✓' if not whole_share_blocked else '✗'}"
            ),
        },
    }
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Kelly / EV / ATR position sizing for US market trades"
    )
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--win-rate", type=float, required=True,
                        help="Estimated win probability 0.0–1.0 (e.g. 0.57)")
    parser.add_argument("--reward-ratio", type=float, required=True,
                        help="Target gain / stop loss distance (e.g. 2.0)")
    parser.add_argument("--stop-pct", type=float, required=True,
                        help="Stop-loss distance as %% below entry (e.g. 2.0)")
    parser.add_argument("--price", type=float, default=None,
                        help="Current market price for share-count")
    parser.add_argument("--confirmation-score", type=int, default=5,
                        help="0–10: independent signals confirmed (default 5)")
    parser.add_argument("--account", type=float, default=None,
                        help="Account size USD (auto-loaded from Webull snapshot if omitted)")
    parser.add_argument("--inverse-etf", action="store_true",
                        help="Apply 8-10%% hard cap for inverse ETF positions")
    args = parser.parse_args()

    result = compute_position_math(
        ticker=args.ticker,
        win_rate=args.win_rate,
        reward_ratio=args.reward_ratio,
        stop_pct=args.stop_pct,
        price=args.price,
        confirmation_score=args.confirmation_score,
        account=args.account,
        is_inverse_etf=args.inverse_etf,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Write to disk for downstream report reading
    out_path = ROOT / "position_math_last.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[Saved to {out_path}]", flush=True)


if __name__ == "__main__":
    main()
