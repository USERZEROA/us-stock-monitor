# Structured Log Schema

Every market report should write the human-readable Markdown archive and one
machine-readable JSONL record. JSONL does not replace the report; it makes
audits, rule tracking, and monthly evaluation reliable.

## Paths

- Premarket: `reports/structured/premarket/YYYY-MM-DD.jsonl`
- Intraday: `reports/structured/intraday/YYYY-MM-DD.jsonl`
- Post-market: `reports/structured/postmarket/YYYY-MM-DD.jsonl`

Append one JSON object per run. Use UTF-8. Do not include credentials, raw
tokens, account IDs, or private API secrets.

If a scheduled market window fails before a final user-visible report is
generated, do not recreate a prediction after the fact. If local run/session
evidence exists, append a documented failure record with
`archive_status.status: "failed_backfilled_audit"`, empty `predictions`,
empty `position_reviews`, empty `action_drafts`, and a
`final_action_summary` that clearly says the original report failed and no
order was executed. This closes the audit gap without pretending the report
was delivered on time.

## Common Required Fields

```json
{
  "schema_version": "1.0",
  "run_time_et": "YYYY-MM-DD HH:MM:SS ET",
  "trading_date": "YYYY-MM-DD",
  "job_id": "cron id",
  "job_label": "premarket_09 | cron_03 | cron_33 | postmarket_1620",
  "report_type": "premarket | intraday | postmarket",
  "market_status": "open | closed | premarket | postmarket | holiday | skipped | unknown",
  "archive_status": {
    "markdown_path": "path",
    "jsonl_path": "path",
    "status": "success | failed | failed_backfilled_audit | backfilled_from_failed_session | documented_failure",
    "error": ""
  },
  "inputs": {
    "webull_portfolio_sync_status": "success | failed | skipped",
    "webull_order_sync_status": "success | failed | skipped",
    "market_data_sources": ["source names"],
    "knowledge_files_read": ["MARKET_KNOWLEDGE.md", "research/FAILED_IDEAS.md"]
  },
  "predictions": [],
  "position_reviews": [],
  "action_drafts": [],
  "order_lifecycle": {
    "order_drafts": [],
    "user_approvals": [],
    "execution_receipts": [],
    "approval_chain_status": "complete | incomplete | no_orders | not_available_in_wrapper_fallback",
    "notes": ""
  },
  "execution_cost_layers": {
    "broker_reported_fees": [],
    "estimated_fees": [],
    "fee_status": "final | provisional | no_fees | not_applicable",
    "notes": ""
  },
  "special_event_monitoring": {
    "active": false,
    "plan_source": "",
    "watched_tickers": [],
    "minute_monitor_status": "not_applicable | active | cron_restricted | failed",
    "thirty_minute_review_required": false,
    "next_review_et": "",
    "failure_reason": ""
  },
  "final_action_summary": "Final one-line buy/sell/hold/avoid summary shown at the end of the human report.",
  "risk_rules_applied": [],
  "failure_flags": [],
  "source_refs": []
}
```

## Prediction Object

```json
{
  "ticker": "QQQM",
  "direction": "buy | sell | hold | avoid | observe",
  "horizon": "intraday | 1-5d | 2-4w",
  "thesis": "short summary",
  "trigger": "price/event/volume condition",
  "invalidation": "condition that cancels thesis",
  "confidence": "low | medium | high",
  "position_context": "held | candidate | no_position"
}
```

## Position Review Object

```json
{
  "ticker": "QQQM",
  "position_context": "held | newly_bought | candidate",
  "holding_type": "broad_core_etf | growth_broad_etf | mega_cap_quality | event_recovery | biotech_high_volatility | low_quality_theme | other",
  "quantity": 2.61,
  "cost_basis": 263.28,
  "current_price": 286.31,
  "unrealized_pl_pct": 8.55,
	  "profit_audit_line_pct": 8,
	  "full_exit_line_pct": 15,
	  "loss_limit_pct": -8,
	  "loss_limit_price": 241.15,
	  "loss_limit_basis": "instrument type + six-month event window + peer/sector confirmation + concentration",
	  "profit_audit_triggered": true,
	  "full_exit_triggered": false,
	  "loss_limit_triggered": false,
	  "probability_edge_status": "intact | weakening | invalidated | unknown",
	  "recommended_action": "hold | trim | sell_70_to_100_pct | sell_all | add | avoid_add",
	  "moving_stop_or_invalidation": "price/event/risk condition",
  "requires_user_approval": true
}
```

Every report that has current holdings should include one `position_reviews`
object per held ticker. If a newly filled BUY appears in the order sync or user
context, the next report must mark that ticker as `newly_bought` and complete a
post-buy review.

`loss_limit_pct`, `loss_limit_price`, `loss_limit_basis`, and
`loss_limit_triggered` are required for new market reports whenever cost basis
and a current price are available. For non-US or manual holdings, use the
instrument's local currency and state the lot/liquidity basis in
`loss_limit_basis`.

## Special Event Monitoring Object

Use this object when the report identifies a major earnings day, macro-policy
release day, Treasury auction, regulatory event, or confirmed abnormal move that
requires elevated monitoring. If no special event is active, omit the field or
set `"active": false`.

```json
{
  "active": true,
  "plan_source": "premarket_09 | manual | prior_intraday",
  "watched_tickers": ["GOOGL", "TSLA", "QQQM", "SMH"],
  "related_assets": ["QQQ", "SPY", "VIX"],
  "event_types": ["earnings", "read_through"],
  "minute_monitor_status": "active | cron_restricted | failed",
  "thirty_minute_review_required": true,
  "next_review_et": "2026-07-22 12:03 ET",
  "buy_triggers": ["QQQ reclaims VWAP and VIX < 18"],
  "sell_triggers": ["QQQ breaks day low while VIX makes day high"],
  "invalidation": ["official event time unconfirmed", "spread/volume unreliable"],
  "failure_reason": ""
}
```

If `active` is true or `watched_tickers` is non-empty, `risk_rules_applied`
must include `"rule_id": "standing-special-event-monitoring"`.
When `active` is false, `watched_tickers` must be `[]` if present. Do not use
ordinary holdings or position-review tickers as special-event watched tickers.

## Final Action Summary

Every human-readable report must end with one final action sentence:

`最终操作总结：本时间段买入0；卖出0；持有QQQM、VOO、PYPL、MSFT、KRE；回避AMC、DPZ；条件触发才考虑QQQM最多$150，否则不操作。`

The JSONL record should mirror that sentence in `final_action_summary`. It must
name tickers and quantities or max dollar amounts when applicable. If there is
no immediate trade, it must explicitly say buy 0 and sell 0.

For documented failed windows, `final_action_summary` must explicitly say the
window failed, was not delivered, and is not a recreated trading prediction.

## Action Draft Object

```json
{
  "ticker": "QQQM",
  "side": "BUY | SELL | HOLD",
  "max_usd": 100,
  "approx_shares": 0.35,
  "limit_price": 284.0,
  "requires_user_approval": true,
  "reason": "short summary",
  "invalidation": "condition"
}
```

## Order Lifecycle Object

Use this object to preserve the audit chain when a report discusses actual or
potential Webull orders. It is optional for older records, but new runner
fallback and documented-failure records include it.

```json
{
  "order_drafts": [
    {
      "order_draft_id": "local report id or stable text reference",
      "ticker": "AMZN",
      "side": "BUY | SELL",
      "quantity": 1,
      "limit_price": 255,
      "created_at_et": "YYYY-MM-DD HH:MM:SS ET",
      "requires_user_approval": true,
      "status": "draft | approved | rejected | expired | submitted"
    }
  ],
  "user_approvals": [
    {
      "user_approval_message_id": "telegram message id or local evidence id",
      "approved_order_draft_id": "matching order_draft_id",
      "approved_at_et": "YYYY-MM-DD HH:MM:SS ET",
      "approval_text_excerpt": "short non-sensitive excerpt"
    }
  ],
  "execution_receipts": [
    {
      "execution_receipt_id": "Webull order id or local receipt id",
      "approved_order_draft_id": "matching order_draft_id if known",
      "ticker": "AMZN",
      "side": "SELL",
      "quantity": 1,
      "filled_price": 271,
      "filled_at_et": "YYYY-MM-DD HH:MM:SS ET",
      "status": "filled | partial | open | rejected | canceled"
    }
  ],
  "approval_chain_status": "complete | incomplete | no_orders | not_available_in_wrapper_fallback",
  "notes": ""
}
```

## Execution Cost Layers Object

Use this object whenever a filled order or realized P/L is discussed. Broker
fees and regulatory fees are authoritative when returned by the API. If the API
has not returned fees, estimates must be labeled provisional.

```json
{
  "broker_reported_fees": [
    {
      "execution_receipt_id": "matching receipt id",
      "fee_type": "commission | regulatory | other",
      "amount": 0.01,
      "currency": "USD",
      "source": "webull_order_status_snapshot.json"
    }
  ],
  "estimated_fees": [
    {
      "execution_receipt_id": "matching receipt id",
      "amount": 0.02,
      "currency": "USD",
      "reason": "API fee field not returned; provisional small-order estimate"
    }
  ],
  "fee_status": "final | provisional | no_fees | not_applicable",
  "notes": ""
}
```

## Risk Rule Object

```json
{
  "rule_id": "RULE-YYYYMMDD-NN or standing-rule-name",
  "status": "applied | violated | not_applicable",
  "evidence": "short evidence"
}
```

If a record contains one or more `position_reviews`, `risk_rules_applied` must
include a rule object with `"rule_id": "standing-profit-taking-lines"`. If a
newly filled BUY is reviewed in that record, also include
`"rule_id": "standing-post-buy-review"`.

## Post-Market Additions

Post-market records should also include:

```json
{
  "audit_results": [],
  "operation_reviews": [],
  "rule_updates": [],
  "failures_written": ["research/queue/postmarket-failures.md"],
  "eval_cases_written": ["research/EVAL_CASES.md"]
}
```
