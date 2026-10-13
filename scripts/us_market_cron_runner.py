#!/usr/bin/env python3
"""Run a us-market cron role through the local embedded agent runtime.

Gateway cron command jobs use this wrapper so market reports can access the
workspace filesystem, Webull read-only sync scripts, and local validators.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = ROOT / "research" / "cron_prompts"
MODEL = "openai/gpt-5.5"
CLAUDE_BOOK_MODEL = "anthropic/claude-sonnet-4-6"
ACCOUNT_ID = "us-market"
CHANNEL = "telegram"
TARGET = os.environ.get("OPENCLAW_TELEGRAM_TARGET", "YOUR_TELEGRAM_CHAT_ID")

# Transient-failure retry for the local agent invocation. The claude-cli
# backend can intermittently be killed by its own 180s idle-output watchdog
# (FailoverError / "produced no output ... was terminated") with no model
# fallback candidate (next=none), which turns an otherwise-runnable window into
# a hard cron failure even though the same chain succeeds on adjacent runs.
# A bounded retry recovers these intermittent hangs without touching protected
# cron schedules, model routing, auth, or delivery targets. Non-transient
# errors (e.g. model-policy violations) are never retried.
MAX_AGENT_ATTEMPTS = 2
RETRY_SLEEP_SECONDS = 20
TRANSIENT_ERROR_MARKERS = (
    "FailoverError",
    "produced no output",
    "was terminated",
    "reason=timeout",
    "candidate_failed",
    "agent returned no text payload",
    "live session close",
)

NONFATAL_BOOK_LIMIT_MARKERS = (
    "weekly limit",
    "rate_limit",
    "resets ",
    "You've hit your weekly limit",
)


def is_transient_error(message: str) -> bool:
    """True when an agent failure looks like an intermittent backend hang."""
    return any(marker in message for marker in TRANSIENT_ERROR_MARKERS)


def is_nonfatal_book_limit(role: str, message: str) -> bool:
    """True when book learning is blocked only by the external Claude quota."""
    return role == "daily_book_learning_claude" and any(
        marker in message for marker in NONFATAL_BOOK_LIMIT_MARKERS
    )

ROLES = {
    "premarket_prediction": {
        "deliver": True,
        "thinking": "high",
        "timeout": 1200,
        "job_id": "9b80bc8f-c054-4503-8d71-924b2861ed04",
        "job_label": "premarket_09",
        "report_type": "premarket",
    },
    "intraday_prediction_33": {
        "deliver": True,
        "thinking": "high",
        "timeout": 1200,
        "job_id": "ed297920-efc6-4001-9674-a5235b10c726",
        "job_label": "cron_33",
        "report_type": "intraday",
    },
    "intraday_prediction_03": {
        "deliver": True,
        "thinking": "high",
        "timeout": 1200,
        "job_id": "f00b7b64-8c16-475c-bda9-b5ae5019d0af",
        "job_label": "cron_03",
        "report_type": "intraday",
    },
    "postmarket_audit": {
        "deliver": True,
        "thinking": "high",
        "timeout": 1500,
        "job_id": "46bb4476-0b37-4dfd-9ba6-10791c3658cf",
        "job_label": "postmarket_1620",
        "report_type": "postmarket",
    },
    "closed_loop_health": {"deliver": True, "thinking": "high", "timeout": 900},
    "research_a": {"deliver": False, "thinking": "high", "timeout": 1800},
    "weekly_distillation_b": {"deliver": True, "thinking": "high", "timeout": 2700},
    "monthly_prompt_eval_c": {"deliver": True, "thinking": "high", "timeout": 3600},
    "daily_book_learning_claude": {
        "deliver": False,
        "thinking": "high",
        "timeout": 7200,
        "model": CLAUDE_BOOK_MODEL,
        "skip_webull_sync": True,
        "require_model_prefix": "claude",
    },
}

# Roles whose agent runs can admit new knowledge cards. After a successful run
# these trigger default-classification of freshly admitted macro cards for the
# activation layer (see scripts/knowledge_default_activation.py).
CARD_ADMITTING_ROLES = {"daily_book_learning_claude", "research_a", "weekly_distillation_b"}

# Roles that CONSUME knowledge activation/coverage and must observe a reconciled
# state. Running the default-classifier as a PRE-step here makes the "every
# admitted macro card is classified" invariant hold no matter HOW a card was
# admitted (manual edit, candidate->admitted promotion, or any future role) --
# a reconciliation loop instead of relying on catching every admission event.
# This does not change protected cron schedules or delivery; it only prepares
# local knowledge-card state before a report role reads the activation pipeline.
PRE_RECONCILE_ROLES = {
    "premarket_prediction",
    "intraday_prediction_33",
    "intraday_prediction_03",
    "postmarket_audit",
    "closed_loop_health",
}


def extract_json(stdout: str) -> dict:
    start = stdout.find('{\n  "payloads"')
    if start == -1:
        start = stdout.find('{"payloads"')
    if start == -1:
        raise ValueError("openclaw agent output did not contain JSON payload")
    # Some long report payloads can contain unescaped control characters in
    # nested text fields even when the CLI is asked for JSON. Accept them here
    # so the runner can still archive and deliver the report instead of turning
    # a completed agent run into a cron failure.
    decoder = json.JSONDecoder(strict=False)
    payload, _ = decoder.raw_decode(stdout[start:])
    return payload


def run_command(argv: list[str], timeout: int = 60) -> dict:
    proc = subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return {
        "argv": argv,
        "returncode": proc.returncode,
        "output_tail": proc.stdout[-3000:],
    }


DEFAULT_EXCERPT_CHARS = 6000


def read_excerpt(path: str, max_chars: int = DEFAULT_EXCERPT_CHARS) -> dict:
    full_path = ROOT / path
    try:
        text = full_path.read_text(encoding="utf-8")
    except Exception as exc:
        return {"path": path, "status": "failed", "error": str(exc)}
    return {
        "path": path,
        "status": "ok",
        "chars": len(text),
        "excerpt_chars": min(len(text), max_chars),
        "excerpt": text[-max_chars:],
    }


def context_files_for_role(role: str, health_date: str) -> list[tuple[str, int]]:
    common = [
        ("PORTFOLIO_STATE.md", 5000),
        ("WEBULL_ORDER_STATUS.md", 5000),
        ("research/OPERATIONAL_CHECKLIST.md", 12000),
        ("research/BOOK_LEARNING_LATEST.md", 5000),
        ("research/KNOWLEDGE_GOVERNANCE.md", 5000),
        ("research/knowledge/domains/methodology.md", 4000),
        ("research/SYSTEM_STATE.md", 5000),
        ("research/DATA_SOURCE_POLICY.md", 5000),
    ]
    if role == "premarket_prediction":
        return [
            *common,
            ("reports/approved-pending-drafts.md", 4000),
            ("research/REPORT_TEMPLATE.md", 5000),
            ("research/MACRO_CALENDAR.md", 7000),
            ("research/FAILED_IDEAS.md", 7000),
            ("MARKET_KNOWLEDGE.md", 10000),
            ("research/calibration/CALIBRATION_SUMMARY.md", 4000),
            (f"reports/closed-loop-health/{health_date}.md", 4000),
        ]
    if role == "postmarket_audit":
        return [
            *common,
            ("reports/approved-pending-drafts.md", 4000),
            ("research/REPORT_TEMPLATE.md", 5000),
            ("research/FAILED_IDEAS.md", 6000),
            ("MARKET_KNOWLEDGE.md", 7500),
            ("research/rules/RULE_PERFORMANCE.md", 7000),
            ("research/queue/postmarket-failures.md", 7000),
            (f"reports/premarket-predictions/{health_date}.md", 8000),
            (f"reports/intraday-predictions/{health_date}.md", 8000),
            (f"reports/closed-loop-health/{health_date}.md", 4000),
        ]
    if role == "closed_loop_health":
        return [
            *common,
            ("research/CLOSED_LOOP_MANIFEST.json", 9000),
            ("research/STRUCTURED_LOG_SCHEMA.md", 9000),
            ("research/rules/RULE_PERFORMANCE.md", 7000),
            ("research/queue/postmarket-failures.md", 7000),
            (f"reports/closed-loop-health/{health_date}.md", 7000),
        ]
    if role == "daily_book_learning_claude":
        return [
            ("research/RESEARCH_PROGRAM.md", 9000),
            ("research/BOOK_LEARNING_PROGRAM.md", 12000),
            ("research/BOOK_LEARNING_QUEUE.md", 9000),
            ("research/BOOK_LEARNING_LATEST.md", 5000),
            ("research/KNOWLEDGE_GOVERNANCE.md", 8000),
            ("research/knowledge/domains/methodology.md", 5000),
            ("research/RESEARCH_INDEX.md", 6000),
            ("research/FAILED_IDEAS.md", 7000),
            ("MARKET_KNOWLEDGE.md", 9000),
            ("research/SYSTEM_STATE.md", 5000),
            ("research/STRUCTURED_LOG_SCHEMA.md", 6000),
        ]
    if role in {"research_a", "weekly_distillation_b", "monthly_prompt_eval_c"}:
        return [
            ("research/RESEARCH_PROGRAM.md", 9000),
            ("research/RESEARCH_QUEUE.md", 6000),
            ("research/BOOK_LEARNING_LATEST.md", 5000),
            ("research/KNOWLEDGE_GOVERNANCE.md", 6000),
            ("research/knowledge/domains/methodology.md", 5000),
            ("research/RESEARCH_INDEX.md", 5000),
            ("research/SYSTEM_STATE.md", 5000),
            ("research/STRUCTURED_LOG_SCHEMA.md", 5000),
            ("research/rules/RULE_PERFORMANCE.md", 5000),
            ("research/queue/postmarket-failures.md", 5000),
            ("research/FAILED_IDEAS.md", 5000),
            ("MARKET_KNOWLEDGE.md", 6000),
        ]
    return [
        *common,
        ("research/FAILED_IDEAS.md", 6000),
        ("MARKET_KNOWLEDGE.md", 8000),
        (f"reports/closed-loop-health/{health_date}.md", 4000),
    ]


def build_context_budget(file_excerpts: list[dict]) -> dict:
    ok_files = [item for item in file_excerpts if item.get("status") == "ok"]
    total_excerpt_chars = sum(int(item.get("excerpt_chars") or 0) for item in ok_files)
    return {
        "files_requested": len(file_excerpts),
        "files_loaded": len(ok_files),
        "total_excerpt_chars": total_excerpt_chars,
        "warning": "context excerpt budget above 65000 chars"
        if total_excerpt_chars > 65000
        else "",
    }


def current_et_date() -> str:
    proc = subprocess.run(
        ["bash", "-lc", "TZ=America/New_York date +%F"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.stdout.strip() or datetime.now().date().isoformat()


def build_context(role: str) -> str:
    now = datetime.now().astimezone().isoformat()
    health_date = current_et_date()
    commands = []
    if not ROLES.get(role, {}).get("skip_webull_sync"):
        commands = [
            run_command(["timeout", "45s", "python3", "scripts/webull_portfolio_sync.py"], 60),
            run_command(["timeout", "45s", "python3", "scripts/webull_order_status.py"], 60),
        ]
    activation_report_type = {
        "premarket_prediction": "premarket",
        "postmarket_audit": "postmarket",
        "intraday_prediction_33": "intraday",
        "intraday_prediction_03": "intraday",
    }.get(role)
    if activation_report_type:
        # Knowledge-activation pipeline: fetch today's macro metrics and compute
        # which admitted knowledge cards MUST be cited in this report. Injected as
        # a preflight result so the agent consumes the must-cite list without
        # needing shell/network tool access itself. Degrades to 0-activated green
        # if a data source is unavailable.
        commands.append(
            run_command(
                ["python3", "scripts/knowledge_activation_pipeline.py",
                 "--report-type", activation_report_type],
                180,
            )
        )
    if role == "closed_loop_health":
        commands.append(
            run_command(
                ["python3", "scripts/knowledge_activation_pipeline.py",
                 "--report-type", "postmarket",
                 "--audit-report", f"reports/postmarket-reviews/{health_date}.md"],
                180,
            )
        )
        commands.extend(
            [
                run_command(
                    [
                        "python3",
                        "scripts/market_closed_loop_validate.py",
                        "--date",
                        health_date,
                        "--require-all-archives",
                        "--write-health",
                    ],
                    60,
                ),
                run_command(["python3", "scripts/cron_prompt_audit.py"], 180),
                run_command(
                    ["python3", "scripts/post_buy_review_audit.py", "--date", health_date, "--lookback-days", "7"],
                    60,
                ),
                run_command(["python3", "scripts/book_learning_audit.py"], 60),
                run_command(["python3", "scripts/knowledge_audit.py"], 60),
                run_command(
                    ["python3", "scripts/actual_trade_watcher.py", "--date", health_date, "--write"],
                    60,
                ),
                run_command(
                    ["python3", "scripts/fee_finalization_audit.py", "--date", health_date, "--write"],
                    60,
                ),
            ]
        )

    files = context_files_for_role(role, health_date)
    file_excerpts = [read_excerpt(path, max_chars=max_chars) for path, max_chars in files]
    context = {
        "generated_at": now,
        "workspace": str(ROOT),
        "role": role,
        "local_preflight_commands": commands,
        "context_budget_report": build_context_budget(file_excerpts),
        "file_excerpts": file_excerpts,
    }
    return (
        "LOCAL_COMMAND_RUNNER_CONTEXT（由本地cron wrapper注入，视为本次任务的一手本地上下文）：\n"
        "本次由本地 command runner 执行。不要调用 message(action=send)，不要调用 sessions_spawn 来完成本地文件/脚本任务；"
        "runner 会在你 final 后负责单次 Telegram 投递和本地归档。你必须在 final 中写完整用户可见正文或静默任务摘要。\n"
        "下面 JSON 包含本地只读同步/验证命令结果和关键文件摘录；若命令失败，必须透明写出失败，不得伪装成功。\n"
        "知识激活（若 local_preflight_commands 含 knowledge_activation_pipeline 结果）：对 stages.activation.activated_cards "
        "中的每一张卡，必须在报告「采用的长期规则」段落逐张写明 adopt 或 exclude 及理由；activated_count=0 时写"
        "「宏观激活卡：0（当日指标未触及压力阈值，已核对）」。引用≠下单：激活只要求评估与说明，不得据此机械买卖（对照 FAILED_IDEAS）。"
        "健康巡检若 stages.activation.missing_citations 非空或 stages.coverage.status=red，必须在闭环健康检查小节标 RED 并列出缺失卡。\n"
        "```json\n"
        + json.dumps(context, ensure_ascii=False, indent=2)
        + "\n```\n\n"
    )


def run_agent(role: str, prompt: str, config: dict) -> tuple[dict, str]:
    cmd = [
        "openclaw",
        "agent",
        "--local",
        "--agent",
        ACCOUNT_ID,
        "--session-key",
        f"agent:{ACCOUNT_ID}:cron-local:{role}",
        "--thinking",
        config["thinking"],
        "--timeout",
        str(config["timeout"]),
    ]
    if config.get("model"):
        cmd.extend(["--model", str(config["model"])])
    cmd.extend(
        [
            "--message",
            build_context(role) + prompt,
            "--json",
        ]
    )
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=config["timeout"] + 120,
        check=False,
    )
    stdout = proc.stdout.decode("utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"openclaw agent failed with exit {proc.returncode}\n{stdout[-4000:]}")
    return extract_json(stdout), stdout


def send_message(text: str) -> dict:
    proc = subprocess.run(
        [
            "openclaw",
            "message",
            "send",
            "--account",
            ACCOUNT_ID,
            "--channel",
            CHANNEL,
            "--target",
            TARGET,
            "--message",
            text,
            "--json",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"message send failed with exit {proc.returncode}\n{proc.stdout[-2000:]}")
    try:
        return json.loads(proc.stdout[proc.stdout.find("{") :])
    except Exception:
        return {"raw": proc.stdout.strip()}


def et_date() -> str:
    return current_et_date()


def final_action_summary(text: str) -> str:
    for line in reversed(text.splitlines()):
        if "最终操作总结" in line:
            return line.strip()
    return "最终操作总结：本时间段买入0、卖出0；未识别到可执行订单草稿，所有交易仍需用户批准。"


def load_json_file(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def as_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None


def as_float(value: object) -> float | None:
    number = as_decimal(value)
    return float(number) if number is not None else None


def holding_type_for_symbol(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol in {"VOO", "SPY"}:
        return "broad_core_etf"
    if symbol in {"QQQM", "QQQ"}:
        return "growth_broad_etf"
    if symbol in {"MSFT", "AAPL", "NVDA", "AMZN", "GOOGL", "GOOG", "META"}:
        return "mega_cap_quality"
    if symbol in {"PYPL", "KRE"}:
        return "event_recovery"
    if symbol in {"XBI"}:
        return "biotech_high_volatility"
    return "other"


def profit_lines_for_holding_type(holding_type: str) -> tuple[int, int]:
    return {
        "broad_core_etf": (6, 12),
        "growth_broad_etf": (8, 15),
        "mega_cap_quality": (8, 18),
        "event_recovery": (5, 12),
        "biotech_high_volatility": (12, 25),
        "low_quality_theme": (8, 15),
    }.get(holding_type, (8, 15))


def build_position_reviews_from_snapshot() -> list[dict]:
    snapshot = load_json_file(ROOT / "webull_portfolio_snapshot.json")
    if snapshot.get("status") != "success":
        return []
    reviews: list[dict] = []
    for position in snapshot.get("positions") or []:
        if not isinstance(position, dict):
            continue
        symbol = str(position.get("symbol") or "").upper().strip()
        quantity = as_decimal(position.get("quantity"))
        if not symbol or quantity is None or quantity <= 0:
            continue
        holding_type = holding_type_for_symbol(symbol)
        profit_line, full_exit_line = profit_lines_for_holding_type(holding_type)
        unrealized_rate = as_decimal(position.get("unrealized_pl_rate"))
        unrealized_pct = float(unrealized_rate * Decimal("100")) if unrealized_rate is not None else None
        profit_triggered = bool(unrealized_pct is not None and unrealized_pct >= profit_line)
        full_exit_triggered = bool(unrealized_pct is not None and unrealized_pct >= full_exit_line)
        current_price = as_float(position.get("last_price"))
        action = "hold"
        if full_exit_triggered:
            action = "sell_70_to_100_pct"
        elif profit_triggered:
            action = "trim"
        elif unrealized_pct is not None and unrealized_pct < 0:
            action = "hold"
        reviews.append(
            {
                "ticker": symbol,
                "position_context": "held",
                "holding_type": holding_type,
                "quantity": as_float(quantity),
                "cost_basis": as_float(position.get("cost_price")),
                "current_price": current_price,
                "unrealized_pl_pct": round(unrealized_pct, 2) if unrealized_pct is not None else None,
                "profit_audit_line_pct": profit_line,
                "full_exit_line_pct": full_exit_line,
                "loss_limit_pct": None,
                "loss_limit_price": None,
                "loss_limit_basis": (
                    "Runner fallback cannot set an individualized loss limit; "
                    "the human report must apply instrument type, six-month "
                    "event window, peer/sector confirmation, and concentration."
                ),
                "profit_audit_triggered": profit_triggered,
                "full_exit_triggered": full_exit_triggered,
                "loss_limit_triggered": None,
                "probability_edge_status": "unknown_wrapper_fallback",
                "recommended_action": action,
                "moving_stop_or_invalidation": (
                    "Runner fallback reconstructed the holding from Webull read-only "
                    "snapshot; inspect the human report for exact invalidation lines."
                ),
                "requires_user_approval": True,
            }
        )
    return reviews


def build_hold_action_drafts(position_reviews: list[dict]) -> list[dict]:
    drafts: list[dict] = []
    for review in position_reviews:
        ticker = review.get("ticker")
        if not ticker:
            continue
        drafts.append(
            {
                "ticker": ticker,
                "side": "HOLD",
                "max_usd": 0,
                "approx_shares": review.get("quantity"),
                "limit_price": None,
                "requires_user_approval": True,
                "reason": "Runner fallback reconstructed a conservative hold/no-new-order state from current holdings.",
                "invalidation": "Use the human report's explicit trigger; fallback does not create new trade authority.",
            }
        )
    return drafts


def webull_status_from_local_snapshot() -> str:
    snapshot = load_json_file(ROOT / "webull_portfolio_snapshot.json")
    status = snapshot.get("status")
    return str(status) if status else "attempted_by_runner"


def order_status_from_local_snapshot() -> str:
    snapshot = load_json_file(ROOT / "webull_order_status_snapshot.json")
    status = snapshot.get("status")
    if status:
        return str(status)
    legacy = load_json_file(ROOT / "webull_order_status.json")
    status = legacy.get("status")
    return str(status) if status else "attempted_by_runner"


def build_postmarket_fallback_fields(position_reviews: list[dict]) -> dict:
    """Postmarket-only required fields for runner-written fallback records.

    The postmarket schema requires audit_results, operation_reviews and
    rule_updates. When the runner writes a fallback/documented-failure record it
    must still populate these keys (from the Webull-derived position reviews) so
    the record passes closed-loop validation. No market judgment is fabricated:
    entries are explicitly labelled as runner fallback.
    """
    operation_reviews = [
        {
            "ticker": review.get("ticker", ""),
            "rating": "runner_fallback_hold",
            "note": (
                "Runner fallback: agent structured record missing; holding carried "
                "from Webull snapshot with type-specific profit/exit lines, no new "
                "same-day judgment fabricated."
            ),
        }
        for review in position_reviews
    ]
    audit_results = [
        {
            "window": "postmarket_1620",
            "rating": "runner_fallback",
            "note": (
                "Agent did not write a structured postmarket record; runner emitted "
                "a schema-complete fallback from the Webull snapshot. See Markdown "
                "body and research/queue/postmarket-failures.md for the audit trail."
            ),
        }
    ]
    rule_updates = [
        "RUNNER-FALLBACK: agent structured record missing this run; no new rule "
        "updates captured by the runner (see postmarket Markdown / failures queue)."
    ]
    return {
        "audit_results": audit_results,
        "operation_reviews": operation_reviews,
        "rule_updates": rule_updates,
    }


def build_wrapper_fallback_record(
    role: str,
    text: str,
    config: dict,
    date: str,
    now: str,
    md_path: Path,
    jsonl_path: Path,
) -> dict:
    position_reviews = build_position_reviews_from_snapshot()
    action_drafts = build_hold_action_drafts(position_reviews)
    risk_rules_applied = [
        {
            "rule_id": "OPENCLAW_CRON_LOCAL_WORKSPACE_DELEGATION",
            "status": "applied",
            "evidence": "fallback wrapper record; agent did not write a structured record",
        }
    ]
    if position_reviews:
        risk_rules_applied.append(
            {
                "rule_id": "standing-profit-taking-lines",
                "status": "applied",
                "evidence": (
                    "Runner fallback reconstructed one position review per Webull "
                    "holding and applied type-specific profit-audit/full-exit lines."
                ),
            }
        )
    record = {
        "schema_version": "1.0",
        "run_time_et": now,
        "trading_date": date,
        "job_id": config["job_id"],
        "job_label": config["job_label"],
        "report_type": config.get("report_type"),
        "market_status": "unknown",
        "archive_status": {
            "markdown_path": str(md_path),
            "jsonl_path": str(jsonl_path),
            "status": "success",
            "error": "",
        },
        "inputs": {
            "webull_portfolio_sync_status": webull_status_from_local_snapshot(),
            "webull_order_sync_status": order_status_from_local_snapshot(),
            "market_data_sources": ["agent_report", "Webull local read-only snapshot"],
            "knowledge_files_read": [
                "MARKET_KNOWLEDGE.md",
                "research/FAILED_IDEAS.md",
                "research/DATA_SOURCE_POLICY.md",
                "research/OPERATIONAL_CHECKLIST.md",
            ],
        },
        "predictions": [],
        "position_reviews": position_reviews,
        "action_drafts": action_drafts,
        "order_lifecycle": empty_order_lifecycle(),
        "execution_cost_layers": empty_execution_cost_layers(),
        "special_event_monitoring": {
            "active": False,
            "plan_source": "",
            "watched_tickers": [],
            "minute_monitor_status": "not_applicable",
            "thirty_minute_review_required": False,
            "next_review_et": "",
            "failure_reason": "",
        },
        "final_action_summary": final_action_summary(text),
        "risk_rules_applied": risk_rules_applied,
        "failure_flags": ["agent_structured_record_missing_wrapper_fallback"],
        "source_refs": [
            {
                "id": "S-FALLBACK-WEBULL",
                "name": "Webull local read-only snapshot",
                "time": now,
                "url": "local:webull_portfolio_snapshot.json",
            }
        ],
    }
    # Postmarket schema requires audit_results / operation_reviews / rule_updates.
    # When the agent did not write its own structured record and this wrapper
    # fallback is used, still emit these three so the postmarket record stays
    # schema-valid instead of failing closed-loop validation.
    if config.get("report_type") == "postmarket":
        record.update(build_postmarket_fallback_fields(position_reviews))
    return record


def has_full_structured_record(path: Path, job_label: str) -> bool:
    if not path.exists():
        return False
    for line in reversed(path.read_text(encoding="utf-8", errors="replace").splitlines()):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict) or record.get("job_label") != job_label:
            continue
        if any(record.get(field) for field in ("predictions", "position_reviews", "action_drafts")):
            return True
        return False
    return False


def empty_order_lifecycle() -> dict:
    return {
        "order_drafts": [],
        "user_approvals": [],
        "execution_receipts": [],
        "approval_chain_status": "not_available_in_wrapper_fallback",
        "notes": "Runner fallback record only; inspect the human report, Telegram approval, and Webull order status for authoritative details.",
    }


def empty_execution_cost_layers() -> dict:
    return {
        "broker_reported_fees": [],
        "estimated_fees": [],
        "fee_status": "not_applicable",
        "notes": "No executed trade was reconstructed by the runner fallback record.",
    }


def normalize_structured_schema_version(path: Path) -> bool:
    """Ensure every JSON record in a structured JSONL carries schema_version.

    The agent writes its own premarket/postmarket structured record and has
    repeatedly omitted the required `schema_version` field, tripping
    market_closed_loop_validate. This backfills it in place (idempotent) as a
    writer-level guard so a missing field never reaches the validator.
    """
    if not path.exists():
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    touched = False
    for line in lines:
        if not line.strip():
            out.append(line)
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            out.append(line)
            continue
        if isinstance(record, dict) and "schema_version" not in record:
            record = {"schema_version": "1.0", **record}
            touched = True
        out.append(json.dumps(record, ensure_ascii=False))
    if touched:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return touched


def archive_result(role: str, text: str, config: dict) -> dict:
    date = et_date()
    result: dict = {"role": role, "date": date, "paths": []}
    report_type = config.get("report_type")
    if report_type:
        md_dirs = {
            "premarket": "reports/premarket-predictions",
            "intraday": "reports/intraday-predictions",
            "postmarket": "reports/postmarket-reviews",
        }
        md_path = ROOT / md_dirs[report_type] / f"{date}.md"
        jsonl_path = ROOT / "reports" / "structured" / report_type / f"{date}.jsonl"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S ET")
        agent_wrote_structured = has_full_structured_record(jsonl_path, config["job_label"])
        with md_path.open("a", encoding="utf-8") as handle:
            handle.write(
                "\n---\n"
                f"run_time_et: {now}\n"
                f"job_label: {config['job_label']}\n"
                f"job_id: {config['job_id']}\n"
                "archive_source: local_command_runner\n\n"
                + text
                + "\n"
            )
        if not agent_wrote_structured:
            record = build_wrapper_fallback_record(
                role=role,
                text=text,
                config=config,
                date=date,
                now=now,
                md_path=md_path,
                jsonl_path=jsonl_path,
            )
            with jsonl_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        # Writer-level guard: agent-authored records have repeatedly omitted the
        # required schema_version; backfill in place so validate never sees it missing.
        normalize_structured_schema_version(jsonl_path)
        result["paths"].extend([str(md_path), str(jsonl_path)])
    else:
        log_path = ROOT / "research" / "logs" / f"{date}-{role}.md"
        if role == "closed_loop_health":
            log_path = ROOT / "reports" / "closed-loop-health" / f"{date}.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("\n---\n")
            handle.write(f"run_time_et: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S ET')}\n")
            handle.write("archive_source: local_command_runner\n\n")
            handle.write(text + "\n")
        result["paths"].append(str(log_path))
    return result


def archive_failure(role: str, error: Exception, config: dict) -> dict:
    date = et_date()
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S ET")
    result: dict = {"role": role, "date": date, "paths": [], "status": "documented_failure"}
    error_text = str(error)[-4000:]
    report_type = config.get("report_type")
    if report_type:
        md_dirs = {
            "premarket": "reports/premarket-predictions",
            "intraday": "reports/intraday-predictions",
            "postmarket": "reports/postmarket-reviews",
        }
        md_path = ROOT / md_dirs[report_type] / f"{date}.md"
        jsonl_path = ROOT / "reports" / "structured" / report_type / f"{date}.jsonl"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        with md_path.open("a", encoding="utf-8") as handle:
            handle.write(
                "\n---\n"
                f"run_time_et: {now}\n"
                f"job_label: {config['job_label']}\n"
                f"job_id: {config['job_id']}\n"
                "archive_source: local_command_runner_failure\n\n"
                "本窗口原始 agent 运行失败，已按 documented_failure 归档；"
                "不得事后编造当时的交易判断。\n\n"
                f"failure_tail:\n```\n{error_text}\n```\n"
            )
        record = {
            "schema_version": "1.0",
            "run_time_et": now,
            "trading_date": date,
            "job_id": config["job_id"],
            "job_label": config["job_label"],
            "report_type": report_type,
            "market_status": "unknown",
            "archive_status": {
                "markdown_path": str(md_path),
                "jsonl_path": str(jsonl_path),
                "status": "documented_failure",
                "error": error_text,
            },
            "inputs": {
                "webull_portfolio_sync_status": "attempted_by_runner",
                "webull_order_sync_status": "attempted_by_runner",
                "market_data_sources": [],
                "knowledge_files_read": [
                    "MARKET_KNOWLEDGE.md",
                    "research/FAILED_IDEAS.md",
                    "research/DATA_SOURCE_POLICY.md",
                ],
            },
            "predictions": [],
            "position_reviews": [],
            "action_drafts": [],
            "order_lifecycle": empty_order_lifecycle(),
            "execution_cost_layers": empty_execution_cost_layers(),
            "special_event_monitoring": {
                "active": False,
                "plan_source": "",
                "watched_tickers": [],
                "minute_monitor_status": "failed_before_report",
                "thirty_minute_review_required": False,
                "next_review_et": "",
                "failure_reason": error_text,
            },
            "final_action_summary": (
                "最终操作总结：本窗口原始运行失败并已归档为 documented_failure；"
                "买入0、卖出0；不得事后补写交易判断。"
            ),
            "risk_rules_applied": [
                {
                    "rule_id": "OPENCLAW_CRON_FAILURE_DOCUMENTATION",
                    "status": "applied",
                    "evidence": "runner archived a failed cron run as documented_failure",
                }
            ],
            "failure_flags": ["runner_documented_failure"],
            "source_refs": [],
        }
        # Keep documented-failure postmarket records schema-complete too.
        if report_type == "postmarket":
            record.update(
                {
                    "audit_results": [
                        {
                            "window": config["job_label"],
                            "rating": "documented_failure",
                            "note": "Original postmarket run failed; archived as documented_failure. "
                            + error_text[-500:],
                        }
                    ],
                    "operation_reviews": [],
                    "rule_updates": [
                        "RUNNER-DOCUMENTED-FAILURE: original run failed before producing "
                        "reviews/rules; no fabricated post-hoc judgment."
                    ],
                }
            )
        with jsonl_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        result["paths"].extend([str(md_path), str(jsonl_path)])
    else:
        log_path = ROOT / "research" / "logs" / f"{date}-{role}.md"
        if role == "closed_loop_health":
            log_path = ROOT / "reports" / "closed-loop-health" / f"{date}.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("\n---\n")
            handle.write(f"run_time_et: {now}\n")
            handle.write("archive_source: local_command_runner_failure\n\n")
            handle.write("本窗口原始 agent 运行失败，已按 documented_failure 归档。\n\n")
            handle.write(f"failure_tail:\n```\n{error_text}\n```\n")
        result["paths"].append(str(log_path))
    return result


def archive_skip(role: str, reason: str) -> dict:
    date = et_date()
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S ET")
    log_path = ROOT / "research" / "logs" / f"{date}-{role}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n---\n")
        handle.write(f"run_time_et: {now}\n")
        handle.write("archive_source: local_command_runner_nonfatal_skip\n\n")
        handle.write("本窗口未执行模型推理，已按非致命跳过归档。\n\n")
        handle.write(f"skip_reason:\n```\n{reason[-3000:]}\n```\n")
    return {
        "role": role,
        "date": date,
        "paths": [str(log_path)],
        "status": "nonfatal_skip",
        "reason": reason[-1000:],
    }


def book_learning_already_succeeded_today() -> bool:
    """True when today's ET book-learning run already archived a success entry.

    A successful runner archive writes the exact line
    ``archive_source: local_command_runner`` into
    research/logs/<date>-daily_book_learning_claude.md, whereas a failure writes
    ``archive_source: local_command_runner_failure``. The daily book-learning
    cron fires at 03:00 and 06:00 ET; the 06:00 slot is a backup only needed when
    03:00 failed. If 03:00 already succeeded, the 06:00 run is redundant and
    (because reading a whole book is heavy) tends to hit the Claude CLI daily
    session limit, flipping the cron to error for no real reason. Detecting the
    prior success lets the backup skip cleanly.
    """
    date = et_date()
    log_path = ROOT / "research" / "logs" / f"{date}-daily_book_learning_claude.md"
    if not log_path.exists():
        return False
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip() == "archive_source: local_command_runner":
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", required=True, choices=sorted(ROLES))
    args = parser.parse_args()

    config = ROLES[args.role]

    if args.role == "daily_book_learning_claude" and book_learning_already_succeeded_today():
        print(
            json.dumps(
                {
                    "status": "ok",
                    "role": args.role,
                    "run_started": datetime.now().astimezone().isoformat(),
                    "skipped": "already_completed_today",
                    "note": (
                        "Idempotent skip: today's book-learning already succeeded; "
                        "skipping the redundant backup run to avoid duplicate work and "
                        "Claude CLI session-limit failures."
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    # Reconcile knowledge coverage BEFORE a consuming role reads it, so the
    # "every admitted macro card is classified" invariant holds path-independently.
    if args.role in PRE_RECONCILE_ROLES:
        try:
            run_command(
                ["python3", "scripts/knowledge_default_activation.py"], timeout=60
            )
        except Exception:
            pass  # best-effort; the coverage audit still catches genuine gaps

    prompt_path = PROMPT_DIR / f"{args.role}.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    run_started = datetime.now().astimezone().isoformat()

    result = raw_output = payload_text = used_model = None
    trace = {}
    last_exc: Exception | None = None
    attempts_made = 0
    for attempt in range(1, MAX_AGENT_ATTEMPTS + 1):
        attempts_made = attempt
        try:
            result, raw_output = run_agent(args.role, prompt, config)
            meta = result.get("meta") or {}
            trace = meta.get("executionTrace") or {}
            agent_meta = meta.get("agentMeta") or {}
            payload_text = "\n\n".join(
                item.get("text", "") for item in result.get("payloads", []) if item.get("text")
            ).strip()
            if not payload_text:
                raise RuntimeError("agent returned no text payload")

            provider = agent_meta.get("provider") or trace.get("winnerProvider")
            model = agent_meta.get("model") or trace.get("winnerModel")
            used_model = f"{provider}/{model}"
            required_prefix = config.get("require_model_prefix")
            if required_prefix and required_prefix not in used_model:
                raise RuntimeError(
                    f"model policy violation for {args.role}: expected {required_prefix}, got {used_model}"
                )
            last_exc = None
            break
        except Exception as exc:
            last_exc = exc
            transient = is_transient_error(str(exc))
            nonfatal_limit = is_nonfatal_book_limit(args.role, str(exc))
            sys.stderr.write(
                f"[runner] {args.role} attempt {attempt}/{MAX_AGENT_ATTEMPTS} failed "
                f"(transient={transient}): {str(exc)[-600:]}\n"
            )
            if nonfatal_limit:
                break
            if attempt < MAX_AGENT_ATTEMPTS and transient:
                time.sleep(RETRY_SLEEP_SECONDS)
                continue
            break

    if last_exc is not None:
        final_error = RuntimeError(
            f"all {attempts_made} attempt(s) failed for {args.role}; "
            f"last error:\n{str(last_exc)[-3500:]}"
        )
        if is_nonfatal_book_limit(args.role, str(final_error)):
            archive = archive_skip(args.role, str(final_error))
            print(
                json.dumps(
                    {
                        "status": "nonfatal_skip",
                        "role": args.role,
                        "run_started": run_started,
                        "attempts": attempts_made,
                        "archive": archive,
                        "reason": (
                            "Claude quota/rate limit blocked this optional daily "
                            "book-learning run; archived for retry instead of failing "
                            "the market closed loop."
                        ),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        archive = archive_failure(args.role, final_error, config)
        print(
            json.dumps(
                {
                    "status": "documented_failure",
                    "role": args.role,
                    "run_started": run_started,
                    "attempts": attempts_made,
                    "archive": archive,
                    "error": str(final_error)[-4000:],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    archive = archive_result(args.role, payload_text, config)

    # Roles that can admit new knowledge cards must default-classify any freshly
    # admitted macro card for the activation layer (stamp no_daily_activation;
    # never auto-arm an activation_trigger). This closes the admission->coverage
    # gap so a new structural macro card cannot silently trip coverage red.
    knowledge_default_result = None
    if args.role in CARD_ADMITTING_ROLES:
        try:
            knowledge_default_result = run_command(
                ["python3", "scripts/knowledge_default_activation.py"], timeout=60
            )
        except Exception as exc:  # best-effort; never fail the role on this
            knowledge_default_result = {"status": "error", "error": str(exc)[-500:]}

    delivery_result = None
    if config["deliver"]:
        delivery_result = send_message(payload_text)

    print(
        json.dumps(
            {
                "status": "ok",
                "role": args.role,
                "run_started": run_started,
                "attempts": attempts_made,
                "model": used_model,
                "fallback_used": bool(trace.get("fallbackUsed")),
                "delivered": bool(config["deliver"]),
                "delivery_result": delivery_result,
                "archive": archive,
                "knowledge_default_activation": knowledge_default_result,
                "text_chars": len(payload_text),
                "raw_output_tail_chars": len(raw_output[-4000:]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
