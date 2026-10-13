# Knowledge Governance

This document controls long-run knowledge growth for the U.S. market system.
It prevents daily book learning, research, and prompt evaluation from turning
the system into an oversized, contradictory, or overfit rule pile.

## Architecture

Knowledge has four layers:

1. `research/books/` stores full daily book notes and page coverage ledgers.
2. `research/knowledge/cards/` stores machine-auditable JSON knowledge cards.
3. `research/knowledge/domains/` stores domain indexes used for routing and
   periodic review.
4. `MARKET_KNOWLEDGE.md` stores only admitted, currently usable durable
   rules, with applicability limits and revalidation triggers.

`research/BOOK_LEARNING_LATEST.md` is a latest-run digest only. It is not a
durable rule source by itself and must not override older stronger evidence.

## Admission Gate

Any new durable knowledge from books, papers, research, or postmarket review
must have a knowledge card before it is treated as admitted. A card must
include:

- `rule_id`
- `title`
- `status`
- `domain`
- `source_type`
- `source_title`
- `source_authors`
- `source_year`
- `source_path`
- `source_pages`
- `evidence_grade`
- `core_conclusion`
- `mechanism`
- `applicable_environment`
- `non_applicable_environment`
- `prohibited_use`
- `downstream_roles`
- `revalidation_trigger`
- `last_review_date`

Allowed `status` values:

- `candidate`: useful but not admitted.
- `admitted`: usable in market reports when applicable.
- `deprecated`: formerly admitted but no longer active.
- `rejected`: reviewed and should not be used.

Allowed domains:

- `methodology`
- `risk_management`
- `market_microstructure`
- `portfolio_construction`
- `equity_events`
- `macro`
- `derivatives`
- `accounting_valuation`
- `behavioral`
- `system_engineering`

## Permission Tiers

Automatic write allowed:

- daily book notes;
- research index entries;
- knowledge cards with `candidate` or `admitted` status;
- queue updates;
- contradiction notes;
- research logs.

Conditional write allowed:

- append-only `MARKET_KNOWLEDGE.md` entries that pass admission rules;
- domain index updates under `research/knowledge/domains/`;
- `research/rules/RULE_PERFORMANCE.md` updates after performance review.

Forbidden without explicit user approval:

- protected cron schedules or enabled state;
- Telegram delivery targets;
- broker/Webull authentication or execution permissions;
- model authentication, default model routing, or fallback chains;
- `AGENTS.md` security boundaries;
- any order placement, modification, cancellation, or automation.

## Topic Rotation

Daily book learning should avoid narrow topic lock-in. Over a rolling 30-book
window, target approximate coverage:

- 20% statistics, machine learning, or time series;
- 20% risk management, portfolio construction, and sizing;
- 20% market microstructure, liquidity, transaction costs, and execution;
- 15% accounting, valuation, earnings, and financial statements;
- 15% macro, rates, currency, commodities, and policy transmission;
- 10% behavioral finance, trading psychology, and system engineering.

The target is a guardrail, not a hard quota. Recent system failures can justify
temporary priority shifts.

## Latest-Knowledge Bias Guard

Market reports may cite the latest book digest only when it is relevant to the
current market question. The latest book must not dominate live facts, primary
sources, account state, event timing, risk limits, or stronger older rules.

If a latest digest conflicts with established durable knowledge, the report
must either follow the stronger evidence or mark the conflict for weekly review.

## Contradiction And Review

Before admitting a rule, check:

- `research/FAILED_IDEAS.md`;
- existing `MARKET_KNOWLEDGE.md`;
- domain indexes under `research/knowledge/domains/`;
- recent postmarket failures;
- known contrary evidence in the source itself.

Contradictions must be recorded under `research/contradictions/` or inside the
daily note. Do not silently overwrite older durable rules.

Every admitted card must define a revalidation trigger. Weekly and monthly
review tasks should downgrade, rewrite, or reject cards that repeatedly fail.

## Storage And Budget

- Save the legal-source PDF only when needed for auditability.
- Record SHA-256 when practical.
- Skip or request manual approval for a single PDF above 100 MB.
- Do not keep duplicate PDFs with the same SHA-256.
- If `research/books/` exceeds 2 GB, monthly evaluation must propose an archive
  or compression plan.
- Runner context must prefer indexes, latest digest, and domain summaries over
  dumping entire historical notes into every task.

## Audit Expectations

`scripts/knowledge_audit.py` is the machine gate. Closed-loop health must run
it. A red result means the system should not treat new knowledge as admitted
until fixed. A yellow result means the loop can continue, but weekly/monthly
review must handle warnings.
