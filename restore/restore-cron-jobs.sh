#!/usr/bin/env bash
# restore-cron-jobs.sh — Review and optionally restore OpenClaw cron jobs
#
# SAFETY: This script ONLY prints the cron definitions. It does NOT create,
# enable, or schedule any tasks automatically. You must explicitly call the
# OpenClaw gateway API to add jobs, and they default to enabled=false.
#
# To actually register a job, use:
#   openclaw gateway cron.add --job '{ ... }' --enabled false
# Then enable individually after verifying credentials and system health.
#
# PREREQUISITES:
#   - restore-agent.sh completed successfully
#   - Set env vars: WORKSPACE_PATH, TELEGRAM_TARGET, OPENCLAW_ACCOUNT_ID

set -euo pipefail

WORKSPACE_PATH="${WORKSPACE_PATH:-$(cd "$(dirname "$0")/.." && pwd)}"
TELEGRAM_TARGET="${OPENCLAW_TELEGRAM_TARGET:-YOUR_TELEGRAM_CHAT_ID}"
OPENCLAW_ACCOUNT_ID="${OPENCLAW_ACCOUNT_ID:-us-market}"

echo "=== us-stock-monitor: Cron Job Restore Preview ==="
echo ""
echo "IMPORTANT: No jobs are created by running this script."
echo "This is a dry-run preview only."
echo ""
echo "Configuration to apply:"
echo "  Workspace:       $WORKSPACE_PATH"
echo "  Telegram target: $TELEGRAM_TARGET"
echo "  Account ID:      $OPENCLAW_ACCOUNT_ID"
echo ""
echo "=== Core Scheduled Tasks (9 total, all disabled by default) ==="
echo ""
echo "1. 美股盘前机构级情报 (Pre-market Intelligence)"
echo "   Schedule: 0 9 * * 1-5 America/New_York (Weekdays 09:00 ET)"
echo "   Role: premarket_prediction"
echo "   Delivers: Pre-market market intelligence report via Telegram"
echo ""
echo "2. 美股盘后预测与操作复盘 (Post-market Audit)"
echo "   Schedule: 20 16 * * 1-5 America/New_York (Weekdays 16:20 ET)"
echo "   Role: postmarket_audit"
echo "   Delivers: Post-market review and prediction accuracy audit"
echo ""
echo "3. 美股闭环健康巡检 (Closed-loop Health Check)"
echo "   Schedule: 5 17 * * 1-5 America/New_York (Weekdays 17:05 ET)"
echo "   Role: closed_loop_health"
echo "   Delivers: System health check via Telegram"
echo ""
echo "4. 美股学术与市场研究 (Academic & Market Research)"
echo "   Schedule: 30 20 * * 1,3,5 America/New_York (Mon/Wed/Fri 20:30 ET)"
echo "   Role: research_a"
echo "   Delivers: Silent research task, writes to research/logs/"
echo ""
echo "5. 周度知识蒸馏与反证审计 (Weekly Knowledge Distillation)"
echo "   Schedule: 0 10 * * 6 America/New_York (Saturday 10:00 ET)"
echo "   Role: weekly_distillation_b"
echo "   Delivers: Weekly research distillation"
echo ""
echo "6. 月度Prompt评测与受控优化 (Monthly Prompt Evaluation)"
echo "   Schedule: 0 11 * * 0#1 America/New_York (First Sunday 11:00 ET)"
echo "   Role: monthly_prompt_eval_c"
echo "   Delivers: Monthly prompt quality evaluation"
echo ""
echo "7. 每日Claude开放书籍学习 (Daily Book Learning)"
echo "   Schedule: 0 3,6 * * * America/New_York (Daily 03:00 and 06:00 ET)"
echo "   Role: daily_book_learning_claude"
echo "   Delivers: Silent research task, requires Claude Sonnet"
echo ""
echo "8. 美股盘中高流动性扫描 :33分 [HIGH-FREQUENCY, OPTIONAL]"
echo "   Schedule: 33 9-15 * * 1-5 America/New_York (Weekdays :33 each hour)"
echo "   Role: intraday_prediction_33"
echo "   NOTE: Runs up to 7x per trading day - significant model usage"
echo ""
echo "9. 美股盘中高流动性扫描 :03分 [HIGH-FREQUENCY, OPTIONAL]"
echo "   Schedule: 3 10-15 * * 1-5 America/New_York (Weekdays :03 each hour)"
echo "   Role: intraday_prediction_03"
echo "   NOTE: Runs up to 6x per trading day - significant model usage"
echo ""
echo "=== Full job definitions ==="
echo "See: cron-definitions/all-jobs.json"
echo ""
echo "=== To register a job (example) ==="
echo ""
echo "Replace YOUR_WORKSPACE below and run via openclaw gateway:"
cat <<'EXAMPLE'
openclaw gateway cron.add --job '{
  "name": "美股盘前机构级情报",
  "enabled": false,
  "agentId": "us-market",
  "schedule": {"kind": "cron", "expr": "0 9 * * 1-5", "tz": "America/New_York"},
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "command",
    "argv": ["sh", "-lc", "python3 scripts/us_market_cron_runner.py --role premarket_prediction"],
    "cwd": "/YOUR/WORKSPACE/PATH/workspace-us-market",
    "timeoutSeconds": 1500,
    "outputMaxBytes": 30000
  },
  "delivery": {"mode": "none", "channel": "telegram", "to": "YOUR_TELEGRAM_CHAT_ID", "accountId": "us-market"}
}'
EXAMPLE
echo ""
echo "After registering, enable with:"
echo "  openclaw gateway cron.update --jobId <id> --enabled true"
echo ""
echo "VERIFY before enabling: credentials are valid, workspace is configured."
