# System State

Last updated: 2026-08-01 17:05 ET

## Existing Protected Premarket Task

- Name: 美股盘前机构级情报
- Job ID: 9b80bc8f-c054-4503-8d71-924b2861ed04
- Agent: us-market
- Schedule: `0 9 * * 1-5`
- Time zone: America/New_York
- Session target: isolated
- Delivery: Telegram announce to user id ending in `7498`
- Last observed status: ok
- Protection: do not change schedule, agent, payload, authentication, or delivery target without explicit user approval.

## Research Tasks

- Task A: 美股学术与市场研究
  - Job ID: 55b83de2-fddd-48dc-9c28-d75e037faec1
  - Agent: us-market
  - Schedule: `30 20 * * 1,3,5`
  - Time zone: America/New_York
  - Delivery: none
- Task B: 周度知识蒸馏与反证审计
  - Job ID: 45f8af1c-fda7-4100-9de0-67a3932eca36
  - Agent: us-market
  - Schedule: `0 10 * * 6`
  - Time zone: America/New_York
  - Delivery: Telegram announce to user id ending in `7498`
- Task C: 月度Prompt评测与受控优化
  - Job ID: f8d932bd-ad1f-4800-86a7-e520c6cb2a72
  - Agent: us-market
  - Schedule: `0 11 * * 0#1`
  - Time zone: America/New_York
  - Delivery: Telegram announce to user id ending in `7498`
- Daily book learning: 每日Claude开放书籍学习与系统成长
  - Job ID: 4fc3a69a-80f7-40c3-8a3e-088685fdca40
  - Agent: us-market
  - Schedule: `0 3,6 * * *`
  - Time zone: America/New_York
  - Delivery: none; failureAlert announces to Telegram after first failure
  - Model policy: runner role `daily_book_learning_claude` must request
    `anthropic/claude-sonnet-4-6`; actual runtime is verified to contain
    Claude, otherwise the runner records a documented failure.
  - Scope: legal open-access/public-domain/author-posted book PDFs only;
    one different book per day; full page-coverage ledger; no broker access,
    no Webull sync, no trading.

## Current Market Cron Mode

- User-requested mode as of 2026-07-30: premarket deep scan plus postmarket
  audit, with high-frequency intraday scans disabled unless explicitly
  re-enabled.
- Enabled:
  - 09:00 ET `美股盘前机构级情报`
  - 16:20 ET `美股盘后预测与操作复盘 每日16:20`
  - 17:05 ET `美股闭环健康巡检 每日17:05`
  - Research A, weekly distillation B, monthly evaluation C
- Disabled but retained:
  - `美股盘中高流动性扫描 每小时33分`
    (`ed297920-efc6-4001-9674-a5235b10c726`)
  - `美股盘中高流动性扫描 每小时03分`
    (`f00b7b64-8c16-475c-bda9-b5ae5019d0af`)
- Rationale: the user often has their own intraday judgment and does not want
  high-frequency automatic analysis noise or token usage.
- Replacement behavior: the 09:00 ET premarket task must perform a deeper event
  scan and create only necessary `deleteAfterRun=true` one-time event reminders
  for major same-day catalysts. If no precise event window exists, do not create
  mechanical reminders.
- Portfolio freshness: every cron role receives local context after attempting
  read-only `scripts/webull_portfolio_sync.py` and
  `scripts/webull_order_status.py`, so `PORTFOLIO_STATE.md` and
  `WEBULL_ORDER_STATUS.md` are refreshed before analysis when the API is
  available.

## Current Instruction Routing

- User-approved mode as of 2026-08-01: keep 03/33 high-frequency intraday cron
  disabled, and replace the oversized `AGENTS.md` entry file with a short
  contract plus explicit rule routing.
- `AGENTS.md` is the non-negotiable entry contract: read-only boundary,
  Webull read-only sync, time standard, source hierarchy, web security,
  decision discipline, special-event monitoring, profit-taking review,
  self-consistency, final action summary, and file routing.
- Daily operational details now live in `research/OPERATIONAL_CHECKLIST.md`.
- User-visible report structure now lives in `research/REPORT_TEMPLATE.md`.
- Structured JSONL requirements remain in `research/STRUCTURED_LOG_SCHEMA.md`.
- The pre-slimming snapshot is preserved at
  `research/prompt_versions/AGENTS_snapshot_20260801-132409_pre_slimming.md`.
- `scripts/us_market_cron_runner.py` injects role-specific context excerpts and
  includes a context budget report so oversized source files do not silently
  crowd out higher-priority operating rules.
- `daily_book_learning_claude` is a separate silent growth loop. It uses
  `research/BOOK_LEARNING_PROGRAM.md`, `research/BOOK_LEARNING_QUEUE.md`, and
  `research/books/` to study one legally sourced finance/quant/trading-related
  book per day and integrate only verified, bounded knowledge.
- Knowledge governance is the long-run growth control layer. It uses
  `research/KNOWLEDGE_GOVERNANCE.md`, machine-auditable JSON cards under
  `research/knowledge/cards/`, domain indexes under
  `research/knowledge/domains/`, and `scripts/knowledge_audit.py`. Newly
  admitted durable knowledge should have source pages, evidence grade,
  applicability, prohibited use, downstream roles, and a revalidation trigger.
  Latest book summaries must not override stronger older rules or live facts.

## Versions

- Knowledge base version: kb-20260801-knowledge-governance
- Prompt version: agents-slim-routing-20260801
- Research program version: research-program-20260713

## Last Successful Runs

- Lightweight research test: 2026-07-13, Daniel and Moskowitz "Momentum Crashes",
  initial evidence grade Medium
- Academic and market research: 2026-07-13, Dai-Medhat-Novy-Marx-Rizova
  reversal liquidity and Novy-Marx-Velikov anomaly trading-cost taxonomy,
  with contradiction note on implementation costs
- Academic and market research: 2026-07-15, Bernard-Thomas PEAD mechanism,
  with contradiction note on modern PEAD decay, liquidity, and transaction
  costs
- Weekly distillation: not yet run
- Monthly prompt evaluation: not yet run

## Open Exceptions

- Initial deployment was mistakenly created in `/home/openclaw/.openclaw/workspace`.
- Correction deployment migrated the research system to
  `/home/openclaw/.openclaw/workspace-us-market`.
- Main workspace copies are intentionally retained pending user instruction; do
  not delete them without approval.
- `MEMORY.md` did not exist during initial audit.
- `MARKET_KNOWLEDGE.md` was created empty except for admission rules.
- Current visible session is `main`, while protected premarket cron is bound to
  `us-market`.

## Temporary Validation Guard

Inactive as of 2026-07-15 21:15 ET after the one-paper Task A validation run
was completed and recorded in `research/daily/2026-07-15.md`.

Historical guard rule: the validation run studied at most one paper and did not
modify `AGENTS.md`, any cron job, Telegram settings, model settings, or
authentication settings.

## Secret Handling

No tokens, API keys, OAuth secrets, or credential file contents may be stored in
this file or in research logs.
