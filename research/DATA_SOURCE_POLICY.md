# Data Source Policy

This file controls recurring market-data source choices for us-market reports.
The goal is to avoid spending every intraday run on sources that repeatedly
return authorization, blocking, or missing-endpoint errors.

## Current Source Status

| Source | Status | Use | Reason / Last Review |
| --- | --- | --- | --- |
| Webull local snapshots | preferred_account | Account, cash, holdings, order status | Local read-only sync is the account baseline when successful. Reviewed 2026-07-28. |
| CNBC Quote Cache | preferred_market | ETF/equity/VIX/rates/commodities when available | Repeatedly succeeded on 2026-07-28 and provides broad live/near-live coverage. |
| Nasdaq quote API | preferred_equity | U.S. equity and ETF quotes | Repeatedly succeeded on 2026-07-28 for ticker snapshots. |
| Yahoo chart v8 | fallback_market | Intraday bars, VWAP-style context, proxy quotes | Worked when quote v7 failed; use after preferred sources or for chart/VWAP needs. |
| Cboe VIX pages/API | preferred_vix | VIX confirmation | Use for VIX cross-check, noting delays if present. |
| Fed, TreasuryDirect, SEC, company IR | preferred_events | Official events, filings, calendars, earnings | First-party event sources remain mandatory for event facts. |
| Yahoo quote v7 | disabled_intraday | Do not use in routine intraday runs | Repeated 401/429 in July 2026 reports. Revisit only during maintenance, not every cron. |
| Stooq CSV quote endpoint | disabled_intraday | Do not use in routine intraday runs | Repeated 404 for current ticker quote attempts. Revisit only during maintenance. |
| WSJ direct quote pages | disabled_intraday | Do not scrape in routine intraday runs | Repeated 401/direct-access failures. Use only as manually cited web/news source if accessible. |
| MarketWatch direct quote pages | disabled_intraday | Do not scrape in routine intraday runs | Repeated 401/403 direct-access failures. Use only as manually cited web/news source if accessible. |
| jq local CLI | disabled_runtime_helper | Do not use in routine local command snippets | `jq` is not installed in this workspace. Use `python3 -m json.tool` or a short Python JSON reader instead. Reviewed 2026-07-28. |

## Runtime Rule

- Intraday and premarket reports should start with preferred sources, then
  fallback sources.
- Disabled intraday sources must not be retried in every routine cron. If a
  disabled source is materially needed, write a short note that it is disabled
  due to repeated auth/blocking errors and use an approved fallback.
- If all preferred and fallback sources for a required data point fail, state
  that reliable real-time data is unavailable rather than trying many blocked
  webpages.
- Disabled runtime helpers such as missing CLIs should be replaced with an
  available local tool instead of retried. For JSON inspection, use Python.
- Any decision to re-enable a disabled source should happen in research or
  maintenance, after one explicit repair test proves it works again.
