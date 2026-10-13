#!/usr/bin/env python3
"""Default-classify newly admitted macro knowledge cards for the activation layer.

Background
----------
The coverage audit (scripts/knowledge_activation_check.py --coverage-audit)
requires every ``status=admitted`` + ``domain=macro`` card to be wired to the
activation layer with EITHER an ``activation_trigger`` (a machine-checkable daily
market condition) OR a governance tag ``no_daily_activation`` (structural /
long-horizon; explicitly not a daily trading trigger). A freshly admitted card
has neither, so it trips the audit red until a human classifies it.

Why the safe default is ``no_daily_activation``
-----------------------------------------------
KNOWLEDGE_GOVERNANCE carries a "latest-knowledge bias" guardrail: knowledge that
was just read must NOT auto-arm a same-day trading trigger (that would be
overfitting to whatever was read that morning). So the correct conservative
default for any not-yet-wired admitted macro card is ``no_daily_activation``
(treat as background context only). Promoting a card to a daily signal stays a
DELIBERATE, manual action: a human attaches an explicit ``activation_trigger``.

This tool therefore ONLY adds ``no_daily_activation`` and NEVER fabricates an
``activation_trigger``. A card that already carries an ``activation_trigger`` is
left completely untouched, so no real daily signal is ever suppressed.

Usage
-----
    python3 scripts/knowledge_default_activation.py           # apply defaults
    python3 scripts/knowledge_default_activation.py --dry-run # report only

Exit code is always 0 on success (idempotent; stamping nothing is fine).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
CARDS_DIR = ROOT / "research" / "knowledge" / "cards"
# Human-review trail: every auto-default is appended here so a person can later
# decide whether any card deserves a real activation_trigger. This preserves the
# governance signal that would otherwise be lost by silently auto-classifying.
REVIEW_LOG = ROOT / "research" / "logs" / "knowledge_auto_default.jsonl"

DEFAULT_REASON = (
    "Auto-default at admission: admitted macro card not yet wired to the "
    "activation layer. Per KNOWLEDGE_GOVERNANCE latest-knowledge-bias guardrail, "
    "newly admitted knowledge does not auto-arm a daily trigger and is treated as "
    "structural/background context only. To promote it to a daily signal, a human "
    "must attach an explicit activation_trigger (and drop this tag)."
)


def et_today() -> str:
    return datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")


def needs_default(card: dict) -> bool:
    """True for an admitted macro card wired to neither activation field."""
    if card.get("status") != "admitted" or card.get("domain") != "macro":
        return False
    return not card.get("activation_trigger") and not card.get("no_daily_activation")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report cards that would be stamped without writing changes",
    )
    args = parser.parse_args()

    if not CARDS_DIR.exists():
        print(json.dumps({"status": "error", "error": f"missing {CARDS_DIR}"}))
        return 0

    today = et_today()
    stamped: list[str] = []
    skipped_has_trigger: list[str] = []

    for path in sorted(CARDS_DIR.glob("*.json")):
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(card, dict):
            continue
        # Never touch a card that is already a daily trigger.
        if (
            card.get("status") == "admitted"
            and card.get("domain") == "macro"
            and card.get("activation_trigger")
            and not card.get("no_daily_activation")
        ):
            skipped_has_trigger.append(card.get("rule_id", path.stem))
            continue
        if not needs_default(card):
            continue
        stamped.append(card.get("rule_id", path.stem))
        if args.dry_run:
            continue
        card["no_daily_activation"] = {
            "reason": DEFAULT_REASON,
            "tagged": today,
            "source": "auto_default_admission",
        }
        path.write_text(
            json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        try:
            REVIEW_LOG.parent.mkdir(parents=True, exist_ok=True)
            with REVIEW_LOG.open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "tagged": today,
                            "rule_id": card.get("rule_id", path.stem),
                            "title": card.get("title", ""),
                            "action": "auto_default_no_daily_activation",
                            "human_review": "pending: promote to activation_trigger only if a daily signal is genuinely warranted",
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        except OSError:
            pass  # logging is best-effort; never fail the stamp on it

    print(
        json.dumps(
            {
                "status": "ok",
                "dry_run": args.dry_run,
                "stamped_count": len(stamped),
                "stamped": stamped,
                "left_as_daily_trigger": skipped_has_trigger,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
