#!/usr/bin/env python3
"""Validate daily closed-loop market archives and structured logs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "CLOSED_LOOP_MANIFEST.json"
HEALTH_DIR = ROOT / "reports" / "closed-loop-health"
PROFIT_TAKING_RULE_ID = "standing-profit-taking-lines"
POST_BUY_RULE_ID = "standing-post-buy-review"
SPECIAL_EVENT_RULE_ID = "standing-special-event-monitoring"
SPECIAL_EVENT_MONITOR_DIR = ROOT / "reports" / "special-event-monitoring"
CORE_PROMPT_MARKERS_BY_ROLE = {
    "premarket_prediction": {"KRE持仓风控/候选降级", "特殊事件监控", "防套锁利", "自洽检查"},
    "intraday_prediction_33": {"KRE持仓风控/候选降级", "特殊事件监控", "防套锁利", "自洽检查"},
    "intraday_prediction_03": {"KRE持仓风控/候选降级", "特殊事件监控", "防套锁利", "自洽检查"},
    "postmarket_audit": {"KRE持仓风控/候选降级"},
    "closed_loop_health": {"KRE持仓风控/候选降级"},
}

DOCUMENTED_FAILURE_STATUSES = {
    "failed_backfilled_audit",
    "backfilled_from_failed_session",
    "documented_failure",
    "manual_review_required",
}

NON_COVERAGE_MONITOR_STATUSES = {
    "documented_skip_outside_window",
    "manual_review_required",
}

EXPECTED_INTRADAY_WINDOWS = {
    "cron_33": [
        "09:33",
        "10:33",
        "11:33",
        "12:33",
        "13:33",
        "14:33",
        "15:33",
    ],
    "cron_03": ["10:03", "11:03", "12:03", "13:03", "14:03", "15:03"],
}
INTRADAY_WINDOW_GRACE_MINUTES = 10


STRUCTURED_SPECS = {
    "premarket": {
        "path": ROOT / "reports" / "structured" / "premarket",
        "expected_labels": {"premarket_09"},
        "required_fields": {
            "schema_version",
            "run_time_et",
            "trading_date",
            "job_id",
            "job_label",
            "report_type",
            "market_status",
            "archive_status",
            "inputs",
            "predictions",
            "position_reviews",
            "action_drafts",
            "final_action_summary",
            "risk_rules_applied",
            "failure_flags",
            "source_refs",
        },
    },
    "intraday": {
        "path": ROOT / "reports" / "structured" / "intraday",
        "expected_labels": {"cron_03", "cron_33"},
        "required_fields": {
            "schema_version",
            "run_time_et",
            "trading_date",
            "job_id",
            "job_label",
            "report_type",
            "market_status",
            "archive_status",
            "inputs",
            "predictions",
            "position_reviews",
            "action_drafts",
            "final_action_summary",
            "risk_rules_applied",
            "failure_flags",
            "source_refs",
        },
    },
    "postmarket": {
        "path": ROOT / "reports" / "structured" / "postmarket",
        "expected_labels": {"postmarket_1620"},
        "required_fields": {
            "schema_version",
            "run_time_et",
            "trading_date",
            "job_id",
            "job_label",
            "report_type",
            "market_status",
            "archive_status",
            "inputs",
            "predictions",
            "position_reviews",
            "action_drafts",
            "final_action_summary",
            "risk_rules_applied",
            "failure_flags",
            "source_refs",
            "audit_results",
            "operation_reviews",
            "rule_updates",
        },
    },
}


MARKDOWN_ARCHIVES = {
    "premarket": ROOT / "reports" / "premarket-predictions",
    "intraday": ROOT / "reports" / "intraday-predictions",
    "postmarket": ROOT / "reports" / "postmarket-reviews",
}


REPORT_ROLES = {
    "premarket": {"premarket_prediction"},
    "intraday": {"intraday_prediction_03", "intraday_prediction_33"},
    "postmarket": {"postmarket_audit"},
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {"_error": f"invalid json: {exc}"}


def file_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "nonempty": False, "size": 0}
    size = path.stat().st_size
    return {"path": str(path), "exists": True, "nonempty": size > 0, "size": size}


def applied_rule_ids(record: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for item in record.get("risk_rules_applied") or []:
        if isinstance(item, dict):
            rule_id = item.get("rule_id")
            if rule_id:
                ids.add(str(rule_id))
        elif isinstance(item, str):
            ids.add(item)
    return ids


def parse_run_time_et(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    for suffix in (" ET", " EDT", " EST"):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
            break
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    return None


def archive_status_value(record: dict[str, Any]) -> str:
    status = record.get("archive_status")
    if isinstance(status, dict):
        return str(status.get("status", ""))
    return ""


def validate_intraday_window_coverage(
    trading_date: str, records: list[dict[str, Any]]
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    coverage: dict[str, Any] = {}
    parsed_records: list[tuple[dict[str, Any], datetime]] = []
    for record in records:
        parsed_time = parse_run_time_et(record.get("run_time_et"))
        if parsed_time is not None:
            parsed_records.append((record, parsed_time))

    for label, times in EXPECTED_INTRADAY_WINDOWS.items():
        for time_text in times:
            expected = datetime.strptime(f"{trading_date} {time_text}", "%Y-%m-%d %H:%M")
            deadline = expected + timedelta(minutes=INTRADAY_WINDOW_GRACE_MINUTES)
            key = f"{label} {time_text} ET"
            matches = [
                record
                for record, parsed_time in parsed_records
                if str(record.get("job_label")) == label
                and expected <= parsed_time <= deadline
            ]
            if not matches:
                errors.append(f"missing intraday scheduled window: {key}")
                coverage[key] = {"status": "missing", "records": 0}
                continue

            statuses = [archive_status_value(record) for record in matches]
            if "success" in statuses:
                coverage[key] = {"status": "success", "records": len(matches)}
            elif any(status in DOCUMENTED_FAILURE_STATUSES for status in statuses):
                coverage[key] = {
                    "status": "documented_failure",
                    "records": len(matches),
                    "archive_statuses": statuses,
                }
            else:
                errors.append(f"intraday window has no success or documented failure: {key}")
                coverage[key] = {
                    "status": "unknown",
                    "records": len(matches),
                    "archive_statuses": statuses,
                }
    return errors, coverage


def validate_record_semantics(path: Path, number: int, record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    position_reviews = record.get("position_reviews")
    if position_reviews:
        if not isinstance(position_reviews, list):
            errors.append(f"{path}:{number}: position_reviews is not a list")
        if PROFIT_TAKING_RULE_ID not in applied_rule_ids(record):
            errors.append(
                f"{path}:{number}: position_reviews present but risk_rules_applied "
                f"does not include {PROFIT_TAKING_RULE_ID}"
            )
    if isinstance(position_reviews, list):
        newly_bought = [
            review
            for review in position_reviews
            if isinstance(review, dict) and review.get("position_context") == "newly_bought"
        ]
        if newly_bought and POST_BUY_RULE_ID not in applied_rule_ids(record):
            errors.append(
                f"{path}:{number}: newly_bought position review present but "
                f"risk_rules_applied does not include {POST_BUY_RULE_ID}"
            )
    special_event = record.get("special_event_monitoring")
    if isinstance(special_event, dict):
        watched = special_event.get("watched_tickers")
        has_watched = isinstance(watched, list) and len(watched) > 0
        if (special_event.get("active") or has_watched) and (
            SPECIAL_EVENT_RULE_ID not in applied_rule_ids(record)
        ):
            errors.append(
                f"{path}:{number}: special_event_monitoring present but "
                f"risk_rules_applied does not include {SPECIAL_EVENT_RULE_ID}"
            )
    order_lifecycle = record.get("order_lifecycle")
    if order_lifecycle is not None and not isinstance(order_lifecycle, dict):
        errors.append(f"{path}:{number}: order_lifecycle is not an object")
    if isinstance(order_lifecycle, dict):
        for field in ("order_drafts", "user_approvals", "execution_receipts"):
            if field in order_lifecycle and not isinstance(order_lifecycle[field], list):
                errors.append(f"{path}:{number}: order_lifecycle.{field} is not a list")
    execution_cost_layers = record.get("execution_cost_layers")
    if execution_cost_layers is not None and not isinstance(execution_cost_layers, dict):
        errors.append(f"{path}:{number}: execution_cost_layers is not an object")
    if isinstance(execution_cost_layers, dict):
        for field in ("broker_reported_fees", "estimated_fees"):
            if field in execution_cost_layers and not isinstance(execution_cost_layers[field], list):
                errors.append(f"{path}:{number}: execution_cost_layers.{field} is not a list")
    return errors


def validate_jsonl(
    path: Path,
    required_fields: set[str],
    expected_labels: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return records, [f"missing jsonl: {path}"]
    if path.stat().st_size == 0:
        return records, [f"empty jsonl: {path}"]
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{number}: invalid json: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{path}:{number}: record is not an object")
            continue
        job_label = str(record.get("job_label", ""))
        if expected_labels is None or job_label in expected_labels:
            missing = sorted(required_fields - set(record))
            if missing:
                errors.append(f"{path}:{number}: missing fields {missing}")
            errors.extend(validate_record_semantics(path, number, record))
        records.append(record)
    return records, errors


def load_jsonl_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size == 0:
        return records
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def is_active_special_event_record(record: dict[str, Any]) -> bool:
    special_event = record.get("special_event_monitoring")
    if not isinstance(special_event, dict):
        return False
    watched = special_event.get("watched_tickers")
    has_watched = isinstance(watched, list) and len(watched) > 0
    return bool(special_event.get("active") or has_watched)


def has_intraday_special_event_coverage(trading_date: str) -> bool:
    intraday_path = STRUCTURED_SPECS["intraday"]["path"] / f"{trading_date}.jsonl"
    for record in load_jsonl_records(intraday_path):
        if is_active_special_event_record(record):
            status = archive_status_value(record)
            if status == "success" or status in DOCUMENTED_FAILURE_STATUSES:
                return True

    monitor_path = SPECIAL_EVENT_MONITOR_DIR / f"{trading_date}.jsonl"
    return monitor_path.exists() and monitor_path.stat().st_size > 0


def special_event_monitor_artifact_status(trading_date: str) -> str:
    monitor_path = SPECIAL_EVENT_MONITOR_DIR / f"{trading_date}.jsonl"
    records = load_jsonl_records(monitor_path)
    if not records:
        return "missing"
    statuses = {str(record.get("status", "")) for record in records if isinstance(record, dict)}
    if statuses and statuses <= NON_COVERAGE_MONITOR_STATUSES:
        return "documented_non_coverage_only"
    return "coverage_or_mixed"


def active_special_event_sources(trading_date: str) -> list[str]:
    sources: list[str] = []
    for report_type in ("premarket", "postmarket"):
        path = STRUCTURED_SPECS[report_type]["path"] / f"{trading_date}.jsonl"
        for number, record in enumerate(load_jsonl_records(path), 1):
            if is_active_special_event_record(record):
                sources.append(f"{path}:{number}")
    return sources


def count_markdown_runs(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    labels = text.count("job_label")
    separators = text.count("---")
    return max(labels, separators)


def determine_level(issues: list[str], warnings: list[str]) -> str:
    if issues:
        return "red"
    if warnings:
        return "yellow"
    return "green"


def expected_enabled_roles(manifest: dict[str, Any]) -> set[str]:
    roles: set[str] = set()
    for job in manifest.get("required_jobs", []):
        if not isinstance(job, dict):
            continue
        role = str(job.get("role", ""))
        if bool(job.get("expected_enabled", True)):
            roles.add(role)
    return roles


def report_type_required(report_type: str, enabled_roles: set[str]) -> bool:
    roles = REPORT_ROLES.get(report_type)
    if not roles:
        return True
    return bool(roles & enabled_roles)


def expected_labels_for_report_type(report_type: str, labels: set[str], enabled_roles: set[str]) -> set[str]:
    if report_type != "intraday":
        return labels
    expected: set[str] = set()
    if "intraday_prediction_03" in enabled_roles:
        expected.add("cron_03")
    if "intraday_prediction_33" in enabled_roles:
        expected.add("cron_33")
    return expected


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Closed Loop Health - {result['trading_date']}",
        "",
        f"- Generated at: {result['generated_at']}",
        f"- Status: {result['status']}",
        "",
        "## Archive Files",
        "",
    ]
    for name, status in result["markdown_archives"].items():
        lines.append(
            f"- {name}: {'ok' if status['exists'] and status['nonempty'] else 'missing/empty'} "
            f"({status['path']}, {status['size']} bytes, runs={status.get('run_count', 0)})"
        )
    lines.extend(["", "## Structured Logs", ""])
    for name, status in result["structured_logs"].items():
        lines.append(
            f"- {name}: records={status['record_count']}, "
            f"errors={len(status['errors'])}, path={status['path']}"
        )
    lines.extend(["", "## Required Files", ""])
    for status in result["required_files"]:
        lines.append(
            f"- {status['relative_path']}: "
            f"{'ok' if status['exists'] and status['nonempty'] else 'missing/empty'} "
            f"({status['size']} bytes)"
        )
    if result["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in result["warnings"])
    if result["issues"]:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {item}" for item in result["issues"])
    lines.append("")
    return "\n".join(lines)


def validate(trading_date: str, require_all_archives: bool) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    manifest = load_json(MANIFEST_PATH)
    if manifest is None:
        issues.append(f"missing manifest: {MANIFEST_PATH}")
        manifest = {"required_paths": []}
    elif isinstance(manifest, dict) and manifest.get("_error"):
        issues.append(f"{MANIFEST_PATH}: {manifest['_error']}")
        manifest = {"required_paths": []}
    enabled_roles = expected_enabled_roles(manifest if isinstance(manifest, dict) else {})

    if isinstance(manifest, dict):
        jobs_by_role = {
            str(job.get("role")): job
            for job in manifest.get("required_jobs", [])
            if isinstance(job, dict)
        }
        for role, markers in CORE_PROMPT_MARKERS_BY_ROLE.items():
            job = jobs_by_role.get(role)
            if job is None:
                issues.append(f"manifest missing required job role: {role}")
                continue
            present = {str(marker) for marker in job.get("required_markers", [])}
            missing = sorted(markers - present)
            if missing:
                issues.append(f"manifest job {role} missing core prompt markers: {missing}")

    required_files = []
    for relative in manifest.get("required_paths", []):
        status = file_status(ROOT / relative)
        status["relative_path"] = relative
        required_files.append(status)
        if not status["exists"]:
            issues.append(f"required path missing: {relative}")
        elif not status["nonempty"] and not (ROOT / relative).is_dir():
            warnings.append(f"required file is empty: {relative}")

    markdown_archives: dict[str, dict[str, Any]] = {}
    for name, directory in MARKDOWN_ARCHIVES.items():
        path = directory / f"{trading_date}.md"
        status = file_status(path)
        status["run_count"] = count_markdown_runs(path)
        status["required"] = report_type_required(name, enabled_roles)
        markdown_archives[name] = status
        if status["required"] and require_all_archives and not (status["exists"] and status["nonempty"]):
            issues.append(f"{name} markdown archive missing or empty: {path}")
        elif status["required"] and not (status["exists"] and status["nonempty"]):
            warnings.append(f"{name} markdown archive not present yet: {path}")

    structured_logs: dict[str, dict[str, Any]] = {}
    for name, spec in STRUCTURED_SPECS.items():
        path = spec["path"] / f"{trading_date}.jsonl"
        required = report_type_required(name, enabled_roles)
        expected_labels = expected_labels_for_report_type(
            name, set(spec.get("expected_labels") or set()), enabled_roles
        )
        if not required and not path.exists():
            records, errors = [], []
        else:
            labels_to_validate = expected_labels if required else None
            records, errors = validate_jsonl(path, spec["required_fields"], labels_to_validate)
        labels = {str(record.get("job_label", "")) for record in records}
        missing_labels = sorted(expected_labels - labels)
        if required and require_all_archives and missing_labels:
            errors.append(f"missing expected job labels: {missing_labels}")
        elif required and missing_labels:
            warnings.append(f"{name} structured log missing labels so far: {missing_labels}")
        window_coverage: dict[str, Any] | None = None
        if name == "intraday" and expected_labels:
            window_errors, window_coverage = validate_intraday_window_coverage(
                trading_date, records
            )
            if require_all_archives:
                errors.extend(window_errors)
            else:
                warnings.extend(window_errors)
        if errors and require_all_archives:
            issues.extend(errors)
        elif errors:
            warnings.extend(errors)
        structured_log_status: dict[str, Any] = {
            "path": str(path),
            "record_count": len(records),
            "job_labels": sorted(labels),
            "errors": errors,
            "required": required,
            "expected_labels": sorted(expected_labels),
        }
        if window_coverage is not None:
            structured_log_status["window_coverage"] = window_coverage
        structured_logs[name] = structured_log_status

    intraday_expected = report_type_required("intraday", enabled_roles)
    special_sources = active_special_event_sources(trading_date)
    if special_sources and not intraday_expected and not has_intraday_special_event_coverage(trading_date):
        warnings.append(
            "active special_event_monitoring found while intraday cron roles are expected disabled; "
            "no intraday structured coverage or one-time special-event monitor archive found. "
            f"sources={special_sources}"
        )
    elif special_sources and not intraday_expected:
        monitor_status = special_event_monitor_artifact_status(trading_date)
        if monitor_status == "documented_non_coverage_only":
            warnings.append(
                "active special_event_monitoring has only documented skip/manual-review artifacts, "
                "not real intraday coverage. Treat as documented failure/yellow, not green."
            )

    result = {
        "schema_version": "1.0",
        "generated_at": datetime.now().astimezone().isoformat(),
        "trading_date": trading_date,
        "require_all_archives": require_all_archives,
        "status": determine_level(issues, warnings),
        "issues": issues,
        "warnings": warnings,
        "markdown_archives": markdown_archives,
        "structured_logs": structured_logs,
        "required_files": required_files,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.now().astimezone().strftime("%Y-%m-%d"))
    parser.add_argument("--require-all-archives", action="store_true")
    parser.add_argument("--write-health", action="store_true")
    parser.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = parser.parse_args()

    result = validate(args.date, args.require_all_archives)
    if args.write_health:
        HEALTH_DIR.mkdir(parents=True, exist_ok=True)
        path = HEALTH_DIR / f"{args.date}.md"
        path.write_text(render_markdown(result), encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 2 if result["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
