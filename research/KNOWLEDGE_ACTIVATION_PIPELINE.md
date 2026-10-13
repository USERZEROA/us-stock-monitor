# Knowledge Activation Pipeline

Closes the **knowledge → decision** gap: admitted knowledge cards no longer sit
in a silo. Machine-checkable `activation_trigger`s decide, from the day's real
market metrics, which cards MUST be consulted-and-cited in each report; a
coverage gate stops new cards from silently skipping the wire.

Status: prototype landed & self-verified 2026-08-23. Non-protected layer is
live. Protected prompt hooks below are **proposals awaiting user approval** —
not applied.

## Data flow (how the parts interconnect)

```
 daily_market_metrics.py ──► research/daily_market_metrics.json ──┐
   (FRED OAS + Yahoo VIX/KRE/SPY/JPY/MOVE)   (+ history.jsonl)     │
                                                                   ▼
 knowledge/cards/*.json (activation_trigger) ──► knowledge_activation_check.py
                                                     │        │
                                     must-cite list ─┘        └─ coverage audit
                                                                   │
 reports/{premarket,postmarket}/*.md ──► --audit-report ──► missing-citation red
                                                                   │
                        activation_backtest.py ──► threshold calibration verdicts
                                                                   │
             knowledge_activation_pipeline.py  ◄── single entry point wiring 1-4
```

## Scripts (all read-only over markets; none edit cards/prompts/cron/config)

| Script | Role |
|---|---|
| `scripts/daily_market_metrics.py` | Fetch 7 macro metrics → snapshot + history JSONL. Each metric independent; failures listed under `unavailable`, never crash. |
| `scripts/knowledge_activation_check.py` | Eval admitted-card triggers vs snapshot → must-cite list. `--audit-report` flags activated-but-not-cited. `--coverage-audit` flags admitted macro cards wired to neither trigger nor `no_daily_activation`. Defaults to the live snapshot when no metrics passed. |
| `scripts/activation_backtest.py` | `--reconstruct N` rebuilds N sessions from source and reports per-card fire rate + calibration verdict (never_fired / ok / TOO_FREQUENT). |
| `scripts/knowledge_activation_pipeline.py` | One entry point: collect → activation → coverage → optional report audit. Returns overall green/red. |

## Metric vocabulary

`vix`, `move_index`, `hy_oas_bps`, `ig_oas_bps`, `kre_drawdown_20d_pct`,
`spy_drawdown_20d_pct`, `usdjpy_1w_change_pct`.

## Card wiring (2026-08-23)

All 18 admitted macro cards covered: **9 with `activation_trigger`** (crisis /
credit / funding / intermediary), **9 tagged `no_daily_activation`** (conceptual
ERP / secular r* / QE-QT regime cards that are research-context by design).

## Calibration (60-session reconstruct, 2026-05-28..08-21)

USDJPY-driven cards (BIS-JPY-001, CGFS63-002, KR-001) fired 4/60 (6.7%, healthy).
The rest never fired — correct for a calm window (VIX never ≥25, KRE never ≤-8%,
HY never ≥450bps). Thresholds are defensible stress levels; recalibrate if a
future stress window shows a card that stays dark or one that spams (>40%).

**Reframe:** the historical "zero macro-card footprint" in trade reports was
*largely correct* — on calm days these crisis cards should not fire. The value
added is (a) forcing citation on the next stress day and (b) an auditable
"considered & not-applicable" record on calm days.

## Task wiring — IMPLEMENTED via runner injection (2026-08-23, user-approved)

Wired at the **runner** layer (`scripts/us_market_cron_runner.py :: build_context`)
instead of editing the protected premarket/postmarket/health prompt files. The
runner runs the pipeline as a read-only preflight and injects the JSON result
into `local_preflight_commands`, plus a mandatory directive in its trusted
context preamble. This needs no agent shell/toolsAllow access and touches no
protected schedule / routing / target / auth / cron-enabled state.

1. **premarket (09:00) & postmarket (16:20)** — `build_context` appends
   `knowledge_activation_pipeline.py --report-type <premarket|postmarket>`.
   Preamble directive: for each `stages.activation.activated_cards` the report
   must write adopt/exclude + reason; `activated_count=0` → "宏观激活卡：0（当日
   指标未触及压力阈值，已核对）"; citation ≠ order.

2. **closed-loop health (17:05)** — `build_context` appends
   `knowledge_activation_pipeline.py --report-type postmarket
   --audit-report reports/postmarket-reviews/<date>.md` (pipeline also runs the
   coverage audit). Preamble directive: if `missing_citations` non-empty OR
   `coverage.status=red` → health section marks RED.

3. **book-learning card governance** — NOT a separate prompt edit. Enforced
   transitively: an untagged new macro card makes `--coverage-audit` go red,
   which the 17:05 health injection surfaces as RED. Belt-and-suspenders only;
   add an explicit book-prompt line later if desired.

Verified 2026-08-23: build_context injects the pipeline (rc=0) for premarket /
postmarket / health; research_a and other roles are untouched;
`cron_prompt_audit` for the three prompts stays green (required markers intact).
Graceful degradation confirmed: missing report → `audit_error` surfaced, not a
crash; data-source outage → 0-activated green.
