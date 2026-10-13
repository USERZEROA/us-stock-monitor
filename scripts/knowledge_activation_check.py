#!/usr/bin/env python3
"""Knowledge-card activation checker (prototype).

Closes the "knowledge -> decision" gap: admitted knowledge cards can carry a
machine-evaluable `activation_trigger`. Given the day's market metrics, this
script decides which cards MUST be consulted-and-cited in a given report type
(premarket / postmarket / intraday), so long-horizon macro cards stop sitting
in a silo with zero decision footprint.

Two modes:
  1. Activation list (default): print cards whose trigger fires for the metrics.
  2. Audit (--audit-report PATH): additionally check whether each activated
     card id actually appears in the given report file; flag any that are
     missing so the closed-loop health check can warn.

This script is read-only over the knowledge base and reports. It never edits
cards, prompts, cron, or config.

Metrics are supplied either as --metric name=value (repeatable) or via
--metrics-json PATH (a flat {"name": number} object). Unknown metrics are
ignored; a trigger clause referencing an absent metric simply does not fire.

activation_trigger schema (all fields optional except any_of):
  {
    "description": "human text",
    "any_of": [ {"metric": "vix", "op": ">=", "value": 25}, ... ],
    "all_of": [ ... ],                 # optional AND group
    "must_cite_in": ["premarket", "postmarket"],   # default: all report types
    "note": "what the report must do when fired"
  }
A card fires when (any_of matches OR all_of matches). If only one group is
present, only that group is evaluated.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS_DIR = ROOT / "research" / "knowledge" / "cards"
DEFAULT_METRICS = ROOT / "research" / "daily_market_metrics.json"

OPS = {
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    "==": lambda a, b: a == b,
}


def _clause_fires(clause: dict, metrics: dict) -> bool:
    name = clause.get("metric")
    op = clause.get("op")
    val = clause.get("value")
    if name not in metrics or op not in OPS:
        return False
    try:
        return OPS[op](float(metrics[name]), float(val))
    except (TypeError, ValueError):
        return False


def _group_fires(group: list, metrics: dict, mode: str) -> bool:
    fired = [_clause_fires(c, metrics) for c in group]
    if not fired:
        return False
    return any(fired) if mode == "any" else all(fired)


def card_fires(trigger: dict, metrics: dict) -> tuple[bool, list]:
    """Return (fired, matched_clause_descriptions)."""
    matched = []
    fired = False
    any_of = trigger.get("any_of") or []
    all_of = trigger.get("all_of") or []
    if any_of and _group_fires(any_of, metrics, "any"):
        fired = True
        matched += [c for c in any_of if _clause_fires(c, metrics)]
    if all_of and _group_fires(all_of, metrics, "all"):
        fired = True
        matched += all_of
    return fired, matched


def load_cards() -> list[dict]:
    cards = []
    for p in sorted(CARDS_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        cards.append(d)
    return cards


def _load_metrics_file(path: Path) -> dict:
    """Accept either a flat {name: value} object or the collector snapshot
    (which nests the values under a "metrics" key)."""
    obj = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(obj.get("metrics"), dict):
        return dict(obj["metrics"])
    return {k: v for k, v in obj.items() if isinstance(v, (int, float))}


def parse_metrics(pairs: list[str], metrics_json: str | None) -> dict:
    metrics: dict = {}
    if metrics_json:
        metrics.update(_load_metrics_file(Path(metrics_json)))
    elif not pairs and DEFAULT_METRICS.exists():
        # No explicit metrics supplied: fall back to the daily collector snapshot
        # so premarket/postmarket/health can call the checker with no arguments.
        metrics.update(_load_metrics_file(DEFAULT_METRICS))
    for pair in pairs or []:
        if "=" not in pair:
            continue
        k, v = pair.split("=", 1)
        try:
            metrics[k.strip()] = float(v)
        except ValueError:
            pass
    return metrics


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report-type", default="premarket",
                    choices=["premarket", "postmarket", "intraday", "any"])
    ap.add_argument("--metric", action="append", default=[],
                    help="name=value (repeatable)")
    ap.add_argument("--metrics-json", default=None)
    ap.add_argument("--audit-report", default=None,
                    help="report file path; flag activated cards not cited in it")
    ap.add_argument("--coverage-audit", action="store_true",
                    help="check every admitted macro card has activation_trigger "
                         "OR no_daily_activation; flag cards wired to neither")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.coverage_audit:
        uncovered = []
        conflicted = []
        for card in load_cards():
            if card.get("status") != "admitted" or card.get("domain") != "macro":
                continue
            has_trigger = bool(card.get("activation_trigger"))
            has_no_daily = bool(card.get("no_daily_activation"))
            if not has_trigger and not has_no_daily:
                uncovered.append(card.get("rule_id"))
            elif has_trigger and has_no_daily:
                # Contradictory wiring: a daily trigger AND a "never daily" tag.
                # The activation stage fail-safes to no_daily_activation, but the
                # card still needs a human to resolve the intent.
                conflicted.append(card.get("rule_id"))
        cov = {
            "coverage_audit": True,
            "uncovered_cards": uncovered,
            "conflicted_cards": conflicted,
            "status": "red" if (uncovered or conflicted) else "green",
        }
        if args.json:
            print(json.dumps(cov, ensure_ascii=False, indent=2))
        else:
            print(
                f"coverage status={cov['status']} uncovered={len(uncovered)} "
                f"conflicted={len(conflicted)}"
            )
            for c in uncovered:
                print(f"  MISSING wire: {c}")
            for c in conflicted:
                print(f"  CONFLICT (trigger + no_daily_activation): {c}")
        return 1 if (uncovered or conflicted) else 0

    metrics = parse_metrics(args.metric, args.metrics_json)
    activated = []
    for card in load_cards():
        if card.get("status") != "admitted":
            continue
        # Fail-safe: a card explicitly tagged no_daily_activation is never a daily
        # signal, even if it also carries a (contradictory) activation_trigger.
        if card.get("no_daily_activation"):
            continue
        trig = card.get("activation_trigger")
        if not trig:
            continue
        must_cite = trig.get("must_cite_in") or ["premarket", "postmarket", "intraday", "any"]
        if args.report_type != "any" and args.report_type not in must_cite:
            continue
        fired, matched = card_fires(trig, metrics)
        if fired:
            activated.append({
                "rule_id": card.get("rule_id"),
                "title": card.get("title"),
                "matched": matched,
                "note": trig.get("note", ""),
            })

    result = {
        "report_type": args.report_type,
        "metrics": metrics,
        "activated_count": len(activated),
        "activated_cards": activated,
        "status": "green",
    }

    if args.audit_report:
        text = ""
        try:
            text = Path(args.audit_report).read_text(encoding="utf-8")
        except Exception as exc:
            result["audit_error"] = f"cannot read report: {exc}"
        missing = [a["rule_id"] for a in activated if a["rule_id"] and a["rule_id"] not in text]
        result["report_path"] = args.audit_report
        result["missing_citations"] = missing
        result["status"] = "red" if missing else "green"

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"report_type={result['report_type']} activated={result['activated_count']} "
              f"status={result['status']}")
        for a in activated:
            print(f"  MUST-CITE {a['rule_id']}: {a['title'][:70]}")
            for m in a["matched"]:
                print(f"      trigger: {m.get('metric')} {m.get('op')} {m.get('value')}")
        if args.audit_report:
            miss = result.get("missing_citations", [])
            if miss:
                print(f"  AUDIT RED — activated but NOT cited in report: {', '.join(miss)}")
            else:
                print("  AUDIT GREEN — all activated cards cited (or none activated)")

    return 1 if result["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
