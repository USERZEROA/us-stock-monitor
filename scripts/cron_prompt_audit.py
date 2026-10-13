#!/usr/bin/env python3
"""Read-only audit of US-market cron wiring against the closed-loop manifest."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "CLOSED_LOOP_MANIFEST.json"
LOG_DIR = ROOT / "research" / "logs"
EXPECTED_AGENT_ID = "us-market"
EXPECTED_MODEL = "openai/gpt-5.5"
RUNNER = "scripts/us_market_cron_runner.py"
AGENTS_PATH = ROOT / "AGENTS.md"
AGENTS_CONTRACT_MARKERS = [
    "只读边界",
    "Webull",
    "不得下单",
    "用户明确批准",
    "America/New_York",
    "SOURCE HIERARCHY",
    "WEB SECURITY",
    "DECISION DISCIPLINE",
    "SPECIAL EVENT MONITORING",
    "PROFIT TAKING AND PER-POSITION REVIEW",
    "SELF-CONSISTENCY CHECK",
    "最终操作总结",
    "03/33",
    "enabled=false",
    "research/OPERATIONAL_CHECKLIST.md",
    "research/REPORT_TEMPLATE.md",
    "research/STRUCTURED_LOG_SCHEMA.md",
    "research/SYSTEM_STATE.md",
    "MARKET_KNOWLEDGE.md",
    "research/FAILED_IDEAS.md",
    "position_reviews",
    "final_action_summary",
    "order_lifecycle",
    "execution_cost_layers",
    "standing-special-event-monitoring",
    "standing-profit-taking-lines",
    "standing-post-buy-review",
    "standing-profit-lock-threshold",
    "KRE持仓风控/候选降级",
]
NONFATAL_BOOK_LEARNING_MARKERS = (
    "local_command_runner_nonfatal_skip",
    "You've hit your weekly limit",
    "reason=rate_limit",
    "Claude quota/rate limit",
)


def latest_role_log_text(role: str, max_chars: int = 8000) -> str:
    logs = sorted(LOG_DIR.glob(f"*-{role}.md"))
    if not logs:
        return ""
    try:
        return logs[-1].read_text(encoding="utf-8", errors="replace")[-max_chars:]
    except Exception:
        return ""


def has_nonfatal_book_learning_failure(role: str) -> bool:
    if role != "daily_book_learning_claude":
        return False
    text = latest_role_log_text(role)
    return any(marker in text for marker in NONFATAL_BOOK_LEARNING_MARKERS)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def get_job(job_id: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        output = subprocess.check_output(
            ["openclaw", "cron", "get", job_id],
            text=True,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
    except subprocess.CalledProcessError as exc:
        return None, exc.output.strip()
    except subprocess.TimeoutExpired:
        return None, "openclaw cron get timed out"
    try:
        return json.loads(output), None
    except json.JSONDecodeError as exc:
        return None, f"openclaw cron get returned invalid JSON: {exc}"


def expected_schedule_parts(schedule_text: str) -> tuple[str, str | None]:
    parts = schedule_text.rsplit(" ", 1)
    if len(parts) == 2 and "/" in parts[1]:
        return parts[0], parts[1]
    return schedule_text, None


def audit_job(spec: dict[str, Any]) -> dict[str, Any]:
    job_id = str(spec["id"])
    job, error = get_job(job_id)
    result: dict[str, Any] = {
        "id": job_id,
        "name": spec.get("name"),
        "role": spec.get("role"),
        "status": "green",
        "errors": [],
        "warnings": [],
    }
    if error or job is None:
        result["status"] = "red"
        result["errors"].append(error or "job not found")
        return result

    payload = job.get("payload") or {}
    payload_kind = payload.get("kind")
    command = str(payload.get("command") or " ".join(payload.get("argv") or []))
    prompt_path = ROOT / "research" / "cron_prompts" / f"{spec.get('role')}.md"
    if payload_kind == "command":
        try:
            message = prompt_path.read_text(encoding="utf-8")
        except Exception as exc:
            message = ""
            result["errors"].append(f"prompt file unreadable for command job: {prompt_path}: {exc}")
    else:
        message = str(payload.get("message") or payload.get("text") or "")
    schedule = job.get("schedule") or {}
    expected_expr, expected_tz = expected_schedule_parts(str(spec.get("schedule", "")))

    result.update(
        {
            "enabled": bool(job.get("enabled")),
            "agentId": job.get("agentId"),
            "payload_model": payload.get("model"),
            "payload_kind": payload_kind,
            "command": command,
            "sessionTarget": job.get("sessionTarget"),
            "schedule": schedule,
            "delivery_mode": (job.get("delivery") or {}).get("mode"),
            "lastRunStatus": (job.get("state") or {}).get("lastRunStatus"),
            "consecutiveErrors": int((job.get("state") or {}).get("consecutiveErrors") or 0),
            "message_len": len(message),
        }
    )

    expected_enabled = bool(spec.get("expected_enabled", True))
    result["expected_enabled"] = expected_enabled
    if bool(job.get("enabled")) != expected_enabled:
        result["errors"].append(
            f"enabled mismatch: expected {expected_enabled}, got {bool(job.get('enabled'))}"
        )
    nonfatal_book_failure = has_nonfatal_book_learning_failure(str(spec.get("role")))
    if expected_enabled:
        last_run_status = result.get("lastRunStatus")
        consecutive_errors = int(result.get("consecutiveErrors") or 0)
        if last_run_status and last_run_status != "ok":
            if nonfatal_book_failure:
                result["warnings"].append(
                    f"lastRunStatus is {last_run_status!r} due to documented external Claude quota; "
                    "market cron wiring remains intact"
                )
            else:
                result["errors"].append(f"lastRunStatus is {last_run_status!r}, not 'ok'")
        if consecutive_errors > 0:
            if nonfatal_book_failure:
                result["warnings"].append(
                    f"consecutiveErrors is {consecutive_errors} from documented optional book-learning quota limit"
                )
            else:
                result["errors"].append(f"consecutiveErrors is {consecutive_errors}, expected 0")
    if not expected_enabled:
        result["disabled_reason"] = spec.get("disabled_reason", "")
    if job.get("agentId") != EXPECTED_AGENT_ID:
        result["errors"].append(
            f"agentId mismatch: expected {EXPECTED_AGENT_ID}, got {job.get('agentId')}"
        )
    if payload_kind == "command":
        role = spec.get("role")
        if RUNNER not in command or f"--role {role}" not in command:
            result["errors"].append(
                f"command runner mismatch: expected {RUNNER} --role {role}, got {command}"
            )
        expected_runner_model = spec.get("expected_runner_model")
        if expected_runner_model:
            try:
                runner_text = (ROOT / RUNNER).read_text(encoding="utf-8")
            except Exception as exc:
                runner_text = ""
                result["errors"].append(f"runner unreadable for model audit: {exc}")
            if expected_runner_model not in runner_text or str(role) not in runner_text:
                result["errors"].append(
                    "runner model policy mismatch: "
                    f"expected role {role} to declare {expected_runner_model}"
                )
    elif payload.get("model") != EXPECTED_MODEL:
        result["errors"].append(
            f"payload model mismatch: expected {EXPECTED_MODEL}, got {payload.get('model')}"
        )
    if expected_expr and schedule.get("expr") != expected_expr:
        result["errors"].append(
            f"schedule expr mismatch: expected {expected_expr}, got {schedule.get('expr')}"
        )
    if expected_tz and schedule.get("tz") != expected_tz:
        result["errors"].append(
            f"schedule tz mismatch: expected {expected_tz}, got {schedule.get('tz')}"
        )
    if payload_kind != "command" and job.get("sessionTarget") != "isolated":
        result["warnings"].append(f"sessionTarget is {job.get('sessionTarget')}, not isolated")

    missing_markers = [
        marker for marker in spec.get("required_markers", []) if marker not in message
    ]
    result["missing_markers"] = missing_markers
    if missing_markers:
        result["errors"].append(f"missing prompt markers: {missing_markers}")

    result["status"] = "red" if result["errors"] else ("yellow" if result["warnings"] else "green")
    return result


def determine_status(results: list[dict[str, Any]]) -> str:
    if any(item["status"] == "red" for item in results):
        return "red"
    if any(item["status"] == "yellow" for item in results):
        return "yellow"
    return "green"


def audit_agents_contract() -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": str(AGENTS_PATH),
        "status": "green",
        "errors": [],
        "warnings": [],
        "missing_markers": [],
        "bytes": 0,
        "lines": 0,
    }
    try:
        text = AGENTS_PATH.read_text(encoding="utf-8")
    except Exception as exc:
        result["status"] = "red"
        result["errors"].append(f"AGENTS.md unreadable: {exc}")
        return result

    result["bytes"] = len(text.encode("utf-8"))
    result["lines"] = text.count("\n") + (0 if text.endswith("\n") else 1)
    missing = [marker for marker in AGENTS_CONTRACT_MARKERS if marker not in text]
    result["missing_markers"] = missing
    if missing:
        result["errors"].append(f"missing AGENTS contract markers: {missing}")
    if result["bytes"] > 20000:
        result["warnings"].append(
            f"AGENTS.md is {result['bytes']} bytes; target is under 20000 bytes"
        )
    result["status"] = "red" if result["errors"] else ("yellow" if result["warnings"] else "green")
    return result


def determine_report_status(jobs: list[dict[str, Any]], agents_contract: dict[str, Any]) -> str:
    statuses = [item["status"] for item in jobs] + [agents_contract["status"]]
    if "red" in statuses:
        return "red"
    if "yellow" in statuses:
        return "yellow"
    return "green"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Cron Prompt Audit - {report['generated_at']}",
        "",
        f"- Status: {report['status']}",
        f"- Manifest: {MANIFEST_PATH}",
        "",
        "## AGENTS Contract",
        "",
        f"- Status: {report['agents_contract']['status']}",
        f"- Path: {report['agents_contract']['path']}",
        f"- Size: {report['agents_contract']['bytes']} bytes, {report['agents_contract']['lines']} lines",
        f"- Missing: {report['agents_contract']['missing_markers']}",
        "",
        "## Jobs",
        "",
    ]
    for item in report["jobs"]:
        lines.append(
            f"- {item['role']}: {item['status']}, enabled={item.get('enabled')}, "
            f"expected_enabled={item.get('expected_enabled')}, "
            f"agent={item.get('agentId')}, kind={item.get('payload_kind')}, "
            f"model={item.get('payload_model')}, "
            f"target={item.get('sessionTarget')}, "
            f"lastRunStatus={item.get('lastRunStatus')}, "
            f"consecutiveErrors={item.get('consecutiveErrors')}, "
            f"missing={item.get('missing_markers', [])}"
        )
        for error in item["errors"]:
            lines.append(f"  - error: {error}")
        for warning in item["warnings"]:
            lines.append(f"  - warning: {warning}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest()
    jobs = [audit_job(spec) for spec in manifest.get("required_jobs", [])]
    agents_contract = audit_agents_contract()
    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now().astimezone().isoformat(),
        "status": determine_report_status(jobs, agents_contract),
        "agents_contract": agents_contract,
        "jobs": jobs,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 2 if report["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
