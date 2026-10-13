#!/usr/bin/env python3
"""One entry point that wires the knowledge-activation pipeline together.

Flow (each stage read-only over markets; never edits cards/prompts/cron/config):

  1. daily_market_metrics.py       -> research/daily_market_metrics.json
                                       (+ append daily_metrics_history.jsonl)
  2. knowledge_activation_check    -> which admitted cards MUST be cited today
                                       for the given report type (reads snapshot)
  3. coverage audit                -> every admitted macro card wired to a
                                       trigger OR no_daily_activation (governance)
  4. (optional) --audit-report P   -> did report P actually cite the activated
                                       cards? missing -> red

Intended callers:
  - premarket (09:00) / postmarket (16:20): stages 1-2, embed the must-cite list.
  - closed-loop health (17:05): stages 3-4 against the day's reports.

Usage:
  python3 scripts/knowledge_activation_pipeline.py --report-type premarket
  python3 scripts/knowledge_activation_pipeline.py --report-type postmarket \
      --audit-report reports/postmarket-reviews/2026-08-23.md
  python3 scripts/knowledge_activation_pipeline.py --no-collect   # reuse snapshot
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def _run(argv: list[str], timeout: int) -> dict:
    p = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=timeout, check=False)
    return {"argv": argv, "rc": p.returncode, "out": p.stdout}


def _json_tail(out: str) -> dict | None:
    start = out.find("{")
    if start == -1:
        return None
    try:
        return json.loads(out[start:])
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report-type", default="premarket",
                    choices=["premarket", "postmarket", "intraday", "any"])
    ap.add_argument("--audit-report", default=None)
    ap.add_argument("--no-collect", action="store_true",
                    help="skip the network collector; reuse existing snapshot")
    args = ap.parse_args()

    result: dict = {"report_type": args.report_type, "stages": {}}

    if not args.no_collect:
        c = _run([PY, "scripts/daily_market_metrics.py"], timeout=120)
        snap = _json_tail(c["out"]) or {}
        result["stages"]["collect"] = {
            "rc": c["rc"], "metric_count": snap.get("metric_count"),
            "unavailable": snap.get("unavailable", []), "as_of": snap.get("as_of_et"),
        }

    chk_argv = [PY, "scripts/knowledge_activation_check.py",
                "--report-type", args.report_type, "--json"]
    if args.audit_report:
        chk_argv += ["--audit-report", args.audit_report]
    chk = _run(chk_argv, timeout=60)
    result["stages"]["activation"] = _json_tail(chk["out"]) or {"rc": chk["rc"]}

    cov = _run([PY, "scripts/knowledge_activation_check.py",
                "--coverage-audit", "--json"], timeout=60)
    result["stages"]["coverage"] = _json_tail(cov["out"]) or {"rc": cov["rc"]}

    act = result["stages"]["activation"]
    covr = result["stages"]["coverage"]
    result["overall_status"] = "red" if (
        act.get("status") == "red" or covr.get("status") == "red"
    ) else "green"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["overall_status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
