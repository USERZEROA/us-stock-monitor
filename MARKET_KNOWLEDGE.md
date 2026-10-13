# Market Knowledge

This file stores only durable, reusable market knowledge that has passed the
admission rules in `research/RESEARCH_PROGRAM.md`.

Rules:

- Do not add a trading conclusion from a single weak paper.
- Do not add high-turnover results that ignore costs, liquidity, or slippage.
- Do not add sample-only rules without out-of-sample evidence or a mature
  methodology basis.
- Do not convert historical average effects into certain same-day predictions.
- Every entry must include support, contrary evidence, applicability limits,
  invalidation conditions, and a revalidation trigger.

## Admitted Entries

### Special Event Days Require Monitoring Cadence And Confirmation Gates

- Core conclusion: Major earnings days, macro-policy release days, Treasury
  auction days, and confirmed abnormal-move days require a higher monitoring
  cadence than ordinary market days, but the cadence is for evidence collection
  and timely review rather than automatic trading.
- Mechanism: Large scheduled events reprice stocks through guidance, discount
  rates, margins, capex, sector read-throughs, positioning, and liquidity. The
  first reaction can be incomplete or distorted by thin liquidity, while the
  30-minute regular-session reviews can test whether price, volume, VWAP, and
  sector confirmation support the initial interpretation.
- Supporting evidence: Mature event-study and earnings-announcement literature
  supports the idea that information arrives discretely and is incorporated
  through price and volume, while the PEAD entry below limits mechanical
  earnings-drift use. Market-microstructure practice supports separating
  event detection, quote monitoring, and execution approval.
- Contrary evidence: Highly liquid mega-cap events can be priced quickly, and
  too-frequent checks can overreact to noise, spreads, or after-hours prints.
  Minute-level observations without volume and sector confirmation can create
  false signals.
- Applicable environment: Confirmed special days involving current holdings,
  Magnificent Seven, S&P 100, market-cap leaders, high-liquidity event stocks,
  macro releases, Fed events, Treasury auctions, or sector-moving company
  disclosures.
- Non-applicable environment: Routine no-news trading, stale or unconfirmed
  event rumors, illiquid tickers, missing reliable quotes, or situations where
  the monitoring tool cannot verify timestamps and sources.
- Time scale: Event day through the next regular-session open for earnings
  released after market close.
- Use in premarket and intraday/event reports: Premarket reports must identify
  special-event tickers and produce a monitoring plan. As of 2026-07-30 the
  standing intraday 03/33-minute reports are intentionally disabled by user
  request, so active special-event days should use only a small number of
  deleteAfterRun=true one-time reminders or user-triggered manual reviews.
  If the 03/33 jobs are explicitly re-enabled later, they should again treat
  the plan as the first review queue while the event is active.
- Prohibited use: Do not trade automatically. Do not convert every minute move
  into a buy/sell call. Do not recommend buying an earnings beat or selling an
  earnings miss without guidance, liquidity, cost, price, volume, and sector
  confirmation.
- Evidence strength: Medium as an operating-risk framework; weak as a direct
  same-day forecast.
- Last review date: 2026-07-22.
- Revalidation trigger: Post-market audits show repeated missed earnings/Fed/
  macro turns, false alerts from minute noise, or repeated failures to create
  or consume special-event monitoring plans.

### Intraday Price Confirmation Requires Volume, Liquidity, And Cross-Market Checks

- Core conclusion: Premarket prints and early-session price moves are evidence,
  not final confirmation. A move becomes materially more reliable only when
  direct quote quality, volume, spread, VWAP/opening-range behavior, and related
  ETF or cross-asset confirmation all support the same interpretation. High
  volume alone is not liquidity, especially in VIX 18-20+ or market-wide stress
  regimes.
- Mechanism: Information accumulates outside regular hours, but trading costs
  and low volume can keep durable price discovery in the regular session. In
  liquid regular-session markets, fast traders can help prices incorporate
  permanent information and correct transitory errors, but passive displayed
  liquidity may be adversely selected or vanish under stress.
- Supporting evidence: Barclay and Hendershott (Journal of Empirical Finance,
  2008) find Nasdaq pre-open trading made opening prices more efficient as
  volume increased, but price discovery shifted from the regular day to the
  pre-open only for the highest-volume stocks. Brogaard, Hendershott, and
  Riordan (ECB Working Paper 1602; Review of Financial Studies, 2014) find HFTs
  generally facilitate price efficiency through liquidity-demanding orders in
  the direction of permanent price changes and against transitory errors.
- Contrary evidence: Barclay and Hendershott's related after-hours work reports
  significant but inefficient after-hours price discovery with much higher
  trading costs. Brogaard et al. (Journal of Financial Economics, 2018) find HFT
  liquidity provision is limited when many stocks have simultaneous extreme
  price moves. The SEC/CFTC Flash Crash report warns that high volume during
  significant volatility is not necessarily reliable evidence of liquidity.
- Applicable environment: Liquid U.S. stocks and ETFs with reliable timestamped
  quotes, direct volume data, bid/ask or spread visibility, VWAP/opening-range
  context, and related ETF or index confirmation.
- Non-applicable environment: Thin premarket or after-hours prints, stale
  quotes, missing direct volume/VWAP, source conflicts, wide or anomalous
  spreads, unconfirmed rumors, VIX 18-20+ stress without depth confirmation, or
  market-wide extreme moves where liquidity demand can dominate supply.
- Time scale: Premarket through intraday; strongest operational use is
  04:00-09:29 ET evidence grading and 09:30-09:45 ET price discovery checks.
- Use in premarket and intraday reports: Premarket reports should label price
  moves as confirmed, partly confirmed, or unconfirmed based on volume/spread
  quality and should write "regular-session confirmation pending" when
  necessary. Intraday reports should not upgrade early SMH/QQQ/QQQM or sector
  rebounds until they hold above VWAP or the opening range for at least 15
  minutes with direct volume and related ETF confirmation. If confirmation data
  are unavailable, lower confidence rather than inferring strength.
- Chinese marker summary for downstream health checks: `盘前价格不是确认信号`;
  `高成交量不等于流动性`; `早盘反弹必须通过15分钟VWAP/开盘区间、成交量和行业ETF确认`.
- Prohibited use: Do not buy, sell, or hold solely because a premarket print is
  favorable. Do not infer HFT support or durable liquidity from high volume
  alone. Do not treat a single early rebound as confirmation in a VIX 18-20+
  regime without VWAP, volume, spread, and ETF confirmation.
- Evidence strength: Medium as a market-microstructure operating rule; weak as
  a direct return forecast or mechanical intraday strategy.
- Last review date: 2026-07-25.
- Revalidation trigger: Live post-market reviews show repeated false positives
  from the 15-minute confirmation gate, repeated missed reversals despite full
  confirmation, structural changes in extended-hours trading quality, or new
  high-quality post-2020 evidence on overnight and opening price discovery.

### Profit Taking Uses Type-Specific Audit And Exit Lines

- Core conclusion: Profit-taking should be driven by type-specific expected
  value, remaining catalyst strength, trend confirmation, and drawdown risk,
  not by one universal profit percentage. Profit thresholds are mandatory audit
  triggers; after a profit audit line is reached, the system must actively
  protect gains with explicit lock-profit thresholds so a profitable position
  is not allowed to become a loss without a fresh, source-backed thesis. Profit
  thresholds become default large-reduction or full-exit triggers when
  probability advantage no longer clearly remains.
- Mechanism: Investors cannot know the exact bottom or top. Selling all winners
  too early can destroy momentum exposure, while holding event-driven or
  high-volatility names after the catalyst is priced can give back profits.
  A rule-based audit line reduces emotional decision-making and a separate
  full-exit line prevents indefinite holding after the expected-value edge fades.
- Supporting evidence: Odean (1998) and Barber/Odean research on the disposition
  effect show investors often sell winners too quickly while holding losers.
  Jegadeesh and Titman (1993) and Moskowitz, Ooi, and Pedersen (2012) support
  momentum/trend persistence as a reason not to automatically sell every winner.
  Kelly-style position sizing frames the decision around probability advantage
  and capital growth rather than top-ticking.
- Contrary evidence: Momentum can crash after stress and crowded winners can
  unwind. Event-driven gains can reverse when the event is fully priced,
  guidance disappoints, regulatory facts change, or liquidity deteriorates.
  High-volatility small caps can lose paper gains faster than broad ETFs.
- Applicable environment: Existing U.S. equity or ETF holdings with known cost
  basis, current price, unrealized P/L percentage, liquidity, spread, catalyst
  status, and market risk regime.
- Non-applicable environment: Missing cost basis, stale quotes, unverified
  premarket prints, illiquid names without reliable spread/volume data, or cases
  where tax/account constraints dominate the decision.
- Time scale: Intraday through 2-4 week account management; longer-term core
  allocation still requires separate portfolio planning.
- Use in premarket and intraday reports: For every held ticker, classify the
  holding type, show current unrealized P/L percentage, mark whether the
  profit-audit line or full-exit line is triggered, and give an explicit hold,
  trim, or sell-all draft. When the audit line is triggered, provide both an
  upside lock-profit sell threshold and a downside giveback/moving-stop sell
  threshold. For every newly filled BUY, run a separate post-buy ticker review
  in the next report.
- Chinese marker summary for downstream health checks: every current holding
  must be checked against its `止盈审计线` and `全卖线`; every newly filled BUY
  must trigger `买后判断` in the next report. Structured reports should include
  `position_reviews`, `standing-profit-taking-lines`, and, when applicable,
  `standing-post-buy-review`.
- Type-specific lines:
  - Broad core ETF such as VOO/SPY: audit +6% to +8%; full-exit review +12% to
    +15%.
  - Growth broad ETF such as QQQM/QQQ: audit +8% to +10%; full-exit review +15%
    to +18%.
  - Mega-cap quality stock such as MSFT: audit +8% to +12%; full-exit review
    +18% to +25%.
  - Event/recovery holding such as PYPL/KRE: audit +5% to +8%; full-exit review
    +12% to +18%.
  - KRE special guardrail: The user wants KRE watched closely and does not want
    losses to compound. If KRE weakens versus XLF and SPY, breaks the report's
    intraday/cost invalidation level, or the regional-bank thesis loses relative
    strength while rates/VIX are rising, reports should prioritize a full-position
    SELL KRE draft with quantity, limit/price condition, expected proceeds, and
    explicit user-approval requirement. Do not average down KRE while it is weak
    versus XLF/SPY.
  - Biotech, innovation-drug, or high-volatility thematic holding: audit +12% to
    +18%; full-exit review +25% to +40%, with earlier de-risking before binary
    clinical, FDA, or policy events.
  - Low-quality small cap or pure theme trade: audit +8% to +12%; full-exit
    review +15% to +25%.
- Full-exit default trigger: After a holding reaches its full-exit review line,
  default to a 70%-100% sell draft when trend weakens, volume confirms reversal,
  VIX breaks above 20 with QQQ/SPY weakness, the catalyst is fully priced without
  new upside evidence, the position becomes the account's dominant risk, or a
  higher expected-value replacement requires cash.
- Lock-profit default trigger: After a holding reaches its profit-audit line,
  do not let the report defer indefinitely. If the position gives back roughly
  one-third to one-half of its unrealized gain from the recent high, breaks the
  stated moving stop, loses ETF/sector confirmation, or the event thesis fails,
  default to a 25%-50% sell draft for ETFs/quality mega-caps and a 50%-100% sell
  draft for event/recovery or low-quality names. If the position accelerates
  into or above the full-exit line, default to a 70%-100% sell draft unless a
  new first-party catalyst improves the forward thesis.
- Prohibited use: Do not sell every winner solely because it is profitable. Do
  not hold an event or high-volatility winner indefinitely after the thesis is
  exhausted. Do not apply ETF thresholds to small biotech or event stocks.
- Evidence strength: Medium as a risk-management framework; not a deterministic
  price forecast.
- Last review date: 2026-07-19.
- Revalidation trigger: Live post-market reviews show repeated selling too early,
  repeated giveback after full-exit lines, materially changed volatility regime,
  or new high-quality research on rule-based profit taking.

### Loss Limits Must Be Instrument-Specific, Not One Universal Percent

- Core conclusion: A forced-sell / max-loss line should be set separately for
  each holding. It must combine instrument type, liquidity, volatility, account
  concentration, thesis horizon, six-month event risk, and peer/sector
  confirmation. A single fixed percentage across ETFs, mega-cap stocks, Hong
  Kong board-lot names, high-beta event trades, and financial-sector stress
  holdings is not acceptable.
- Mechanism: The same paper loss has different information content depending on
  the instrument. A broad ETF drawdown can be ordinary market beta; a low-volume
  Hong Kong consumer stock breaking a 52-week low may indicate structural
  liquidity/sector failure; a high-beta event trade can invalidate immediately
  after catalyst disappointment; a bank or credit-sensitive holding can compound
  through funding, rates, credit spreads, and peer weakness.
- Use in premarket, intraday, postmarket, and manual trading conversations: For
  every held ticker discussed, state the individualized `亏损上限` / forced-sell
  line and why it was chosen. The reason must cover: (1) holding type and
  liquidity/lot constraints, (2) material events in the next six months, (3)
  peer/sector/country or related-asset confirmation, and (4) account
  concentration/correlation. If the line is hit, produce a sell/trim draft that
  requires user approval; do not keep observing unless a fresh first-party
  catalyst explicitly resets the thesis.
- Non-US application: For Hong Kong stocks, use HKD price levels, board-lot
  constraints, local-market trading calendar, spread/turnover, peer group, and
  sector beta. A structural level such as 52-week low/IPO low/support break with
  volume can be more appropriate than importing a U.S. small-account stop percent.
- Evidence strength: Medium as a risk-management framework; it is a discipline
  for limiting loss compounding, not a standalone price forecast.
- Last review date: 2026-08-24.
- Revalidation trigger: Postmarket reviews show repeated stop-outs before thesis
  failure, repeated late exits after peer/sector deterioration, or new research
  on volatility-scaled / event-aware stop rules.

### Held Sector ETF Relative Weakness Requires Sell-Draft Escalation

- Core conclusion: For an already held liquid sector ETF, repeated relative
  weakness versus both its direct benchmark and the broad market is a
  risk-reduction trigger. If KRE or another approved held sector ETF is weaker
  than its sector benchmark and SPY for two consecutive delivered report
  windows, and no verified first-party positive catalyst offsets the weakness,
  the next report should escalate from "do not add" to a concrete sell draft.
- Mechanism: Intraday ETF price discovery can persist when opening information,
  inventory pressure, macro rates, or sector-specific risk keeps being processed
  through the session. Relative weakness in a held ETF also consumes risk budget:
  the decision is not to predict a crash, but to stop letting a weakening
  position wait indefinitely for a price stop.
- Supporting evidence: Gao, Han, Li, and Zhou (Journal of Financial Economics,
  2018) document intraday momentum in liquid ETFs and stronger effects on
  volatile, high-volume, macro-news days. Lesmond, Schill, and Zhou (Journal of
  Financial Economics, 2004) support adding transaction-cost, liquidity, spread,
  and turnover gates before using momentum or relative-strength findings. The
  2026-07-20 KRE postmarket review showed late escalation after repeated KRE
  weakness; the 2026-07-21 review found the next-day KRE sell discipline
  acceptable after KRE remained weak versus XLF/SPY.
- Contrary evidence: APAC ETF replication evidence shows intraday momentum is
  not universal and can fail when ETF trading is sparse or stale. The Gao et al.
  study is about market ETF intraday continuation, not a direct KRE sell rule.
  Korajczyk and Sadka show some momentum implementations can survive costs,
  limiting any blanket anti-momentum conclusion.
- Applicable environment: Existing long position in a liquid sector ETF, reliable
  timestamped quotes for the ETF, its direct sector benchmark, SPY, VIX/rates
  context, and enough bid/ask or price-source quality to draft an executable
  but approval-gated sell order.
- Non-applicable environment: No existing position, illiquid or stale quotes,
  ETF distribution/split/adjustment issues, wide unreliable spreads, or a new
  first-party catalyst that improves the held ETF thesis and is confirmed by
  price/volume.
- Time scale: Intraday risk control through the same-session close; can extend
  to the next open when the second weak window occurs near the close.
- Use in premarket and intraday reports: For KRE specifically, weak versus XLF
  and SPY for two consecutive windows, or one weak window plus rising 10Y/VIX
  stress, should produce a SELL KRE full-position draft with quantity, live or
  near-live price condition, estimated proceeds, fee status, invalidation, and
  explicit user-approval requirement. Do not wait for the price stop alone.
- Prohibited use: Do not short a sector ETF or buy an inverse ETF from this rule
  alone. Do not sell after one noisy print. Do not ignore quote-source failures,
  current first-party catalysts, spreads, fees, or user approval.
- Evidence strength: Medium as a risk-control framework for held liquid ETFs;
  weak as a deterministic same-day forecast.
- Last review date: 2026-07-25.
- Revalidation trigger: Three or more future sell-draft escalations are
  immediately reversed by validated relative-strength recovery, or structured
  logs show repeated false exits caused by stale quote feeds, excessive spread,
  or overreaction to one sector window.

### Factor Signals Require Cost, Liquidity, And Capacity Gates

- Core conclusion: Gross factor or anomaly returns are not usable market
  knowledge until turnover, spreads, market impact, shorting constraints,
  liquidity, and capacity have been checked.
- Mechanism: High turnover, wide spreads, price impact, and borrow constraints
  can erase statistically significant paper returns; cost-aware entry/hold
  rules can preserve some lower-turnover anomalies but do not remove
  implementation risk.
- Supporting evidence: Novy-Marx and Velikov (NBER 20721; Review of Financial
  Studies, 2016) show transaction costs reduce profitability and significance
  across anomalies, with cost mitigation most useful for lower-turnover signals.
  Edelen, Ince, and Kadlec (Journal of Financial Economics, 2020) estimate that
  typical mutual-fund implementation costs can eliminate much of momentum's
  paper profit. De Groot, Huij, and Zhou (Journal of Banking and Finance, 2012)
  show broad short-term reversal profits are smaller than likely trading costs.
- Contrary evidence: Frazzini, Israel, and Moskowitz (2012 working paper) use
  large live institutional trading data and find value and momentum more
  scalable than many cost estimates imply. This limits blanket pessimism but
  depends on unusually strong execution and scale.
- Applicable environment: Liquid U.S. equity universes, explicit turnover and
  cost estimates, cost-aware construction, and signals not dominated by
  microcaps or one-off news.
- Non-applicable environment: Thin premarket prints, high-turnover intraday
  trades, illiquid small caps, crowded rebalances, urgent execution, poor
  borrow, or strategies without spread/volume confirmation.
- Time scale: Multi-day to multi-year factor context; not a stand-alone intraday
  trade signal.
- Use in premarket reports: When a trade rationale depends on momentum,
  reversal, value, quality, low-volatility, or another factor narrative, require
  current catalyst, liquidity, spread, volume, and price-confirmation evidence.
- Prohibited use: Do not infer tradability from gross historical alpha or
  statistical significance alone. Do not recommend a same-day trade solely
  because it matches a factor.
- Evidence strength: Strong as a methodology principle; medium for specific
  live factor implementation.
- Last review date: 2026-07-13.
- Revalidation trigger: New high-quality post-2020 implementation evidence,
  major market-structure changes, sustained spread/liquidity regime shifts, or
  direct contradiction from live execution studies.

### Published Factor Narratives Need Out-Of-Sample, Decay, And Crowding Checks

- Core conclusion: Popular published anomalies and factor stories should be
  treated as context, not catalysts, unless they survive out-of-sample,
  post-publication, multiple-testing, crowding, liquidity, and cost checks.
- Mechanism: Publication and productization can attract arbitrage capital,
  reduce mispricing returns, raise common exposure, and increase unwind risk.
  Some apparent decay also reflects false discovery, microcap dependence, or
  stricter testing standards rather than investor learning alone.
- Supporting evidence: McLean and Pontiff (Journal of Finance, 2016) find 97
  published predictors have lower out-of-sample and post-publication returns.
  Chordia, Subrahmanyam, and Tong (Journal of Accounting and Economics, 2014)
  find many anomalies attenuated after decimalization. Hou, Xue, and Zhang
  (Review of Financial Studies, 2020) show most tested anomalies fail stricter
  replication hurdles. Linnainmaa and Roberts (Review of Financial Studies,
  2018) find many accounting anomalies are spurious in long out-of-sample
  histories.
- Contrary evidence: Some anomalies may reflect persistent risk premia or
  costly-to-arbitrage mispricing and can survive in low-liquidity or high
  idiosyncratic-risk stocks. Published decay does not prove every factor is
  dead.
- Applicable environment: Well-known factor narratives, factor ETFs or
  systematic products, crowded leadership themes, liquid markets where
  arbitrage capital can respond, and reports discussing positioning risk.
- Non-applicable environment: Private information, confirmed company-specific
  catalysts, hard-to-arbitrage illiquid names, structural risk premia, or cases
  where live first-party facts dominate historical factor behavior.
- Time scale: Research hygiene and risk framing across days to months; not a
  precise same-day timing tool.
- Use in premarket reports: Add decay/crowding caveats when action plans rely
  on heavily publicized factor stories such as momentum, AI leadership, low
  volatility, quality, or reversal.
- Prohibited use: Do not short a stock or factor solely because a narrative is
  popular. Do not treat average published-factor decay as a forecast for today's
  price move.
- Evidence strength: Strong for research hygiene; medium for practical factor
  allocation; weak for single-stock intraday timing.
- Last review date: 2026-07-13.
- Revalidation trigger: New replication meta-studies, new crowding/capacity
  evidence, major factor-product flow shifts, or durable contradiction in
  post-publication performance.

### Momentum And Reversal Evidence Are Conditional Risk Frames, Not Daily Catalysts

- Core conclusion: Momentum crash and reversal research can improve risk
  framing, but it should not be converted into mechanical same-day long/short
  calls.
- Mechanism: Momentum portfolios can suffer sharp losses after prior market
  stress when volatility is elevated and loser stocks rebound. Short-term
  reversal can reflect liquidity provision and temporary price pressure. Long-
  term reversal can reflect valuation, sentiment, size, value, distress, or
  methodology effects.
- Supporting evidence: Daniel and Moskowitz (NBER 20439; Journal of Financial
  Economics, 2016) document conditional momentum crash risk. Jegadeesh (Journal
  of Finance, 1990) documents short-horizon return autocorrelation in historical
  U.S. stocks. De Bondt and Thaler (Journal of Finance, 1985) document
  long-horizon overreaction evidence. Dai, Medhat, Novy-Marx, and Rizova (NBER
  30917; Financial Analysts Journal, 2024) link filtered short-run reversals to
  liquidity provision.
- Contrary evidence: Goetzmann and Huang find no comparable momentum crashes in
  Imperial Russia, suggesting market-structure dependence. Fama and French
  (Journal of Finance, 1996) weaken purely behavioral explanations of many
  anomalies. Short-term reversal evidence is fragile after costs and standard
  reversal definitions can be contaminated by PEAD and industry momentum.
- Applicable environment: Elevated volatility, prior market stress, crowded
  winner/loser dispersion, visible temporary price pressure, and confirmed
  regular-session liquidity recovery.
- Non-applicable environment: Calm low-volatility markets, confirmed earnings
  or guidance surprises, regulatory shocks, credit events, sector information
  updates, wide spreads, poor borrow, or unconfirmed thin premarket moves.
- Time scale: Premarket and opening risk framing for reversal/liquidity; days
  to months for factor leadership and momentum crash risk.
- Use in premarket reports: Warn against extrapolating crowded winners after
  stress and against treating thin premarket losers as automatic rebound buys.
  Require current catalyst, spread, volume, and price confirmation.
- Prohibited use: Do not say a momentum stock must crash today, a prior loser
  must rebound, or a long-term laggard is a buy solely because it is a loser.
- Evidence strength: Medium for risk framing; weak for direct live trade rules.
- Last review date: 2026-07-13.
- Revalidation trigger: Modern post-2016 momentum crash replications,
  transaction-cost-adjusted reversal studies, or live evidence that opening
  liquidity behavior has structurally changed.

### Earnings Surprises Need Guidance, Revision, Liquidity, And Cost Gates

- Core conclusion: Earnings surprises can create delayed information
  processing, but modern U.S. premarket reports should treat PEAD as an
  earnings-mechanism checklist, not as an automatic post-earnings buy or short
  rule.
- Mechanism: Investors may underprocess how current earnings imply future
  earnings, margins, cash flow, and guidance. Delayed analyst revisions and
  constrained trading can extend the reaction, especially when disclosure is
  complex or liquidity is weaker.
- Supporting evidence: Bernard and Thomas (Journal of Accounting and
  Economics, 1990) link current quarterly earnings surprises to predictable
  later earnings-announcement reactions. Fink (2021 review) summarizes PEAD as
  a durable literature pattern without one universal explanation. Ng,
  Rusticus, and Verdi (Journal of Accounting Research, 2008) support a
  transaction-frictions channel.
- Contrary evidence: Martineau (2022) argues PEAD has been non-existent for
  large stocks since 2006 and disappeared more recently for microcaps. Chordia,
  Goyal, Sadka, and Shivakumar (2009) find PEAD is concentrated in illiquid
  stocks and that transaction costs account for much of paper profits.
- Applicable environment: Confirmed earnings surprise reinforced by guidance,
  revenue quality, margins, cash flow, segment metrics, analyst revisions, and
  regular-session price/volume confirmation.
- Non-applicable environment: Liquid mega-cap releases where the information is
  quickly priced, one-off accounting/tax items, conflicting guidance, extreme
  premarket gaps, wide spreads, high borrow costs, or missing consensus
  baseline.
- Time scale: Earnings-day interpretation through the following weeks or
  quarters; not a stand-alone intraday trigger.
- Use in premarket reports: Use PEAD research to ask whether the market is
  still processing persistent forward-quarter implications, and require
  guidance, revision, liquidity, and cost checks before any action plan.
- Prohibited use: Do not recommend buying positive EPS surprises or shorting
  negative EPS surprises solely because historical PEAD exists. Do not apply
  1970s-1980s effect sizes mechanically to modern large caps.
- Evidence strength: Medium for earnings-processing mechanism; weak for direct
  modern same-day trading.
- Last review date: 2026-07-18.
- Revalidation trigger: New post-2022 PEAD studies, modern large-cap
  earnings-drift evidence, analyst-revision drift updates, or live evidence
  that announcement-day price discovery has structurally slowed.

### Fed Events Require Surprise, Path, Yield-Curve, And Cross-Asset Confirmation

- Core conclusion: Equity reactions to Fed events should be framed around the
  unexpected component of policy and the expected policy path, not the headline
  action alone.
- Mechanism: Fed news can reprice equities through the front-end rate path,
  the default-free yield curve, expected cash flows, risk premia, the dollar,
  credit, and sector duration/cyclicality. FOMC statements, SEP dots, minutes,
  speeches, and press conferences can matter more than the current target
  decision.
- Supporting evidence: Bernanke and Kuttner (NBER 10402; Journal of Finance,
  2005) estimate that broad equities respond to unanticipated policy shocks.
  Gurkaynak, Sack, and Swanson (Federal Reserve FEDS; IJCB, 2005) show that a
  current-target factor is insufficient and that a future-policy-path factor is
  central. SF Fed monetary-policy-surprise data and Bauer-Swanson updates keep
  high-frequency surprises useful with refined identification.
- Contrary evidence: Nagel and Xu (NBER 32884, 2024) argue FOMC equity
  reactions are explained mostly by default-free yield-curve movements rather
  than equity-premium changes. Davig and Gerlach (IJCB, 2006) find
  state-dependent and sometimes insignificant equity reactions. Raw surprises
  can be partly predictable from public pre-announcement information.
- Applicable environment: Scheduled or unscheduled Fed news that genuinely
  changes the target or path baseline, with confirmation from 2-year and
  10-year yields, the dollar, real rates, credit spreads, and sector behavior.
- Non-applicable environment: Fully priced decisions, ambiguous statements,
  conflicting cross-asset signals, thin liquidity, simultaneous macro shocks,
  growth-scare easings, inflation/term-premium shocks, or FOMC reactions
  dominated by positioning.
- Time scale: FOMC release window, same day, and 1-5 trading days for rate-path
  repricing; medium term only when the path change persists.
- Use in premarket reports: Separate target surprise, path surprise, yield
  curve movement, and sector transmission before labeling Fed news bullish or
  bearish.
- Prohibited use: Do not say rate cuts are automatically bullish, hikes are
  automatically bearish, or a hold is neutral without checking expectations,
  path language, yields, dollar, credit, and growth/inflation context.
- Evidence strength: Medium for Fed-event mechanism and report checklist; weak
  for direct post-announcement trading rules.
- Last review date: 2026-07-18.
- Revalidation trigger: New post-2024 high-frequency Fed-shock studies,
  structural changes to FOMC communication, persistent QE/QT regime shifts, or
  evidence that yield-curve confirmation no longer explains equity responses.

### Extended-Hours Trading Requires Whole-Share Orders, No Fractional Shares

- Core conclusion: After the regular U.S. market session closes (16:00 ET),
  fractional-share orders cannot be executed. All extended-hours (post-market
  and pre-market) trade drafts must be in whole-share quantities only, minimum
  1 share. Any fractional-share draft that targets post-market execution is
  invalid and must be rounded or withdrawn.
- Mechanism: U.S. broker extended-hours trading (typically 04:00–09:30 ET
  pre-market and 16:00–20:00 ET post-market) does not support fractional-share
  orders. Fractional shares are a regular-session-only feature. Attempting to
  place a fractional order in extended hours will be rejected or silently
  rounded by the broker. User confirmed on 2026-07-22: after regular market
  close, fractional shares cannot be traded, minimum 1 share.
- Applicable environment: Any trade draft intended for post-market (after 16:00
  ET) or pre-market (before 09:30 ET) execution.
- Non-applicable environment: Regular session (09:30–16:00 ET), where
  fractional-share orders are supported by most retail brokers.
- Required behavior in reports:
  - If market is closed at report time and a sell draft is proposed, all
    quantities must be rounded to the nearest whole share (≥1).
  - Do not propose fractional-quantity drafts (e.g., 0.50 shares, 0.40 shares,
    0.80 shares) for post-market execution.
  - If the desired trim size is less than 1 share, defer to the next regular
    session or propose 1 whole share with explicit user approval.
  - State session status (open / post-market / pre-market) when presenting a
    trade draft, and flag if the quantity had to be adjusted for extended-hours
    compliance.
- Prohibited use: Do not draft 0.x share orders for post-market submission. Do
  not assume the broker will fill fractional quantities after 16:00 ET.
- Evidence strength: Hard platform constraint confirmed by user on 2026-07-22.
  No contrary evidence; this is a broker rule, not a research inference.
- Last review date: 2026-07-22.
- Revalidation trigger: Broker policy change that explicitly enables fractional
  share orders during extended hours, confirmed in writing from broker support.

### Quantitative Trade Evaluation: Kelly Criterion, Expected Value, And ATR-Based Position Sizing

- Core conclusion: Every trade draft must pass a mathematical gate before
  qualifying for a user-approval request. A trade with negative expected
  value (EV ≤ 0) or estimated win rate below the mathematical break-even
  threshold is rejected regardless of how compelling the qualitative
  narrative sounds. Math overrides story. The two required tools are
  `scripts/position_math.py` (Kelly + EV + position size) and
  `scripts/probability_lookup.py` (empirical base-rate win rates from
  calibration data). Both are installed in the us-market workspace.

- Five required formulas for every trade draft:

  (1) BREAK-EVEN WIN RATE — minimum W for positive EV:
      W_min = 1 / (1 + R)
      where R = reward/risk ratio = target_gain_pct / stop_loss_pct
      Derivation: solve EV = W·gain - (1-W)·loss > 0 for W, with gain = R·loss.
      Example: Target +4%, Stop -2% → R=2 → W_min = 1/3 = 33.3%
      Interpretation: any strategy where our estimated W < W_min is a
      guaranteed negative-EV trade and must NOT be drafted.

  (2) EXPECTED VALUE PER DOLLAR INVESTED:
      EV = W · gain_frac - (1-W) · loss_frac
      where gain_frac = stop_frac · R and loss_frac = stop_frac.
      Example: W=0.57, R=2, stop=2% → EV = 0.57·0.04 - 0.43·0.02 = +1.58%
      A positive EV means the strategy is profitable in expectation.
      EV must be computed in each report that proposes a draft order.

  (3) KELLY FRACTION — optimal allocation fraction:
      f* = W - (1-W)/R   [full Kelly]
      Use half-Kelly in practice: f_half = f*/2
      Signal-adjusted Kelly: f_adj = f_half · (confirmation_score/10)
      where confirmation_score ∈ {0,...,10} = number of independent signals confirmed.
      Final position size = min(f_adj, max_cap) · account_value
      Hard caps: single stock/ETF ≤ 20%; inverse ETFs ≤ 9% total.
      Full Kelly derivation: maximise E[ln(wealth)] = W·ln(1+f·R) + (1-W)·ln(1-f)
      Taking derivative and setting to zero: f* = W - (1-W)/R.
      Note: full Kelly has large drawdowns (~50% Kelly fraction = 50% drawdown risk);
      half-Kelly trades drawdown magnitude for geometric growth stability.

  (4) EXPECTED LOG GROWTH RATE — comparing position size choices:
      g(f) = W·ln(1 + f·R) + (1-W)·ln(1 - f)
      Positive g means wealth compounds upward; g(0) = 0 (no trade baseline).
      At full Kelly, g is maximised. Below full Kelly, g decreases but so
      does variance. Use this to compare "full Kelly vs half Kelly vs 10% cap".

  (5) SORTINO PROXY — single-trade quality:
      Sortino_proxy = EV / (downside_std)
      where downside_std ≈ (1-W) · loss_frac (expected loss contribution)
      Ratio > 1.0 means expected gain exceeds the downside deviation.
      Ratio < 0.5 means poor risk/reward even with positive EV.

- Calibrated empirical win rates (from SPY/MSFT/PYPL calibration CSVs,
  2000-2026, computed by `scripts/probability_lookup.py`):

  SPY empirical P(up) by VIX regime:
  | VIX regime | 1-day W | 5-day W | 10-day W | 20-day W |
  |------------|---------|---------|----------|----------|
  | < 18 (open gate) | 55.4% | 59.7% | 63.5% | 66.9% |
  | 18-20 (reduced) | 52.4% | 56.9% | 59.1% | 60.9% |
  | > 20 (paused) | 53.8% | 56.4% | 58.3% | 62.1% |
  | > 30 (crisis) | 54.9% | 57.3% | 62.1% | 69.3% |

  MSFT empirical P(up) by VIX regime (2000-2026):
  | VIX regime | 1-day W | 5-day W | 10-day W | 20-day W |
  |------------|---------|---------|----------|----------|
  | < 18 | 50.9% | 55.0% | 57.5% | 61.8% |
  | 18-20 | 50.6% | 54.3% | 56.9% | 60.9% |
  | > 20 | 51.5% | 56.3% | 59.6% | 64.3% |

  Key insight: single-stock win rates are lower than index win rates for the
  same VIX regime, because stock-specific risk adds variance without adding
  directional edge from broad market conditions alone. SPY at VIX<18 has
  55.4% 1-day W; MSFT has only 50.9%. Individual stock selection adds ±5-10%
  to the base rate depending on catalysts — this is where research quality
  matters most.

  Run `python3 scripts/probability_lookup.py --ticker TICKER --vix CURRENT_VIX`
  to get real-time regime-specific win rates for any ticker with calibration CSV.

- Confirmation score rubric (each signal below earns +1, max 10):
  1. VIX gate: current VIX is in the open (< 18) regime
  2. Price above 20-day MA and above VWAP at scan time
  3. Volume above 20-day average volume (> 1.0×)
  4. Sector ETF confirming (SMH/XLF/XLK trending same direction)
  5. NYSE A/D ratio > 1.5 (breadth confirming)
  6. Macro calendar clear (no major data release within 24 hours)
  7. News catalyst is confirmed (≥1 first-party or two-media-source backing)
  8. KRE (if applicable) not flagging relative weakness vs XLF
  9. Earnings risk clear (no earnings within 5 trading days for this ticker)
  10. Prior standing-profit-lock-threshold is not endangered by this new position
  Proceed gate: confirmation_score ≥ 5 (half of available signals).
  At score 3-4: reduce to quarter-Kelly.
  At score 0-2: do not draft.

- How to invoke the math tools (required before any buy draft):

  Step A — Look up base-rate win rate:
    python3 scripts/probability_lookup.py --ticker TICKER --vix CURRENT_VIX
    Use the `current_regime_summary.win_rates_in_current_regime.fwd_5d` value
    as the base-rate W for trades with 3-7 day holding period.
    Adjust up by up to +5% for strong confirmed catalyst, down by up to -5%
    for weak/contested narrative.

  Step B — Compute Kelly and EV:
    python3 scripts/position_math.py \
      --ticker TICKER \
      --win-rate [from Step A, adjusted] \
      --reward-ratio [target_gain_pct / stop_loss_pct] \
      --stop-pct [stop distance as %] \
      --price [current market price] \
      --confirmation-score [0-10 count]
    Read `position_math_last.json` for the output.

  Step C — Include in draft order:
    Every buy draft must include a one-line math block:
    `[MATH] W=57.0% | R=2.0 | EV=+1.58% | Kelly_adj=13.8% | Shares=2 | Risk=$8.62`

- Applicable environment: before any buy or add-to-position draft.
  Also before sizing an inverse ETF position.
  Not required for standing sell triggers (profit-lock, stop-loss) where
  the position already exists and the question is exit, not entry.

- Non-applicable environment: Do not run Kelly when the position is already
  open and you are deciding whether to hold. Kelly governs entry sizing only.
  Do not use Kelly fraction as a HOLD signal — it is an ENTRY sizing tool.

- Prohibited use:
  - Do not draft a buy order without showing the EV calculation in the report.
  - Do not use win rate estimates above 65% for single stocks without two
    independent quantitative or confirmed fundamental reasons.
  - Do not use win rates sourced from "gut feel" or narrative quality.
    Win rates must come from either (a) probability_lookup.py calibration data
    or (b) a specific documented catalyst with cited research backing.
  - Do not use full Kelly (f*) directly — always use half-Kelly or smaller.
  - Do not apply Kelly to hypothetical future positions without a specific entry
    trigger; Kelly is a sizing tool, not a screening tool.
  - Do not override the EV gate because "the story sounds compelling." A trade
    where EV ≤ 0 is prohibited regardless of qualitative conviction.

- Evidence strength: Strong for Kelly optimality under log-utility assumptions
  (Kelly 1956, Shannon information theory derivation); Strong for EV math
  (arithmetic probability theory); Medium for optimal fraction choice in
  practice (full Kelly overestimates when win rate estimates are uncertain);
  Strong for empirical win rates (direct computation from 26 years of data);
  Weak for individual stock win rate adjustments (catalyst quality is
  inherently qualitative and hard to quantify precisely).

- Last review date: 2026-07-23.
- Revalidation trigger: New calibration CSV run (quarterly via
  `fetch_calibration_data.py`) that changes SPY or held-ticker win rates by
  more than ±3% in any VIX regime; user instruction to change Kelly fraction;
  live evidence that confirmation score rubric is poorly calibrated (e.g.,
  score 5 drafts are failing at > 55% rate).

### Inverse ETFs Provide Bounded Downside Exposure But Decay Rapidly With Daily Rebalancing

- Core conclusion: Leveraged and unleveraged inverse ETFs allow downside
  positioning without a margin account or securities borrowing. For a small
  account (~$3,000–$4,000), inverse ETFs are safer than shorting individual
  stocks because losses are capped at the investment amount and there is no
  short-squeeze or margin-call risk. However, 3x leveraged inverse ETFs suffer
  severe path-dependent decay when markets are choppy: a flat or oscillating
  index erodes 3x inverse ETF value even when the final level is unchanged.
  Primary instruments: SQQQ (3x inverse QQQ), SPXS (3x inverse S&P 500),
  SRTY (3x inverse Russell 2000), TECS (3x inverse XLK). For longer hedges
  in confirmed downtrends, 1x instruments (SH, PSQ, RWM) are preferable.
  User approved inverse ETF as the account's downside hedging mechanism on
  2026-07-23.
- Mechanism: Daily rebalancing creates compounding path dependency. For 3x
  inverse ETFs, when the index moves -n% then +n% on consecutive days, the
  ETF value after both days is (1+3n)(1-3n) = 1-9n² < 1. This decay is
  purely mathematical and accelerates with realized volatility. At 1% daily
  index volatility, a 3x inverse ETF loses approximately 4.5% per week in a
  range-bound market regardless of direction. At 2% daily volatility, decay
  is approximately 18% per week. Conversely, in a sustained one-directional
  trend the compounding works in the holder's favor: a market down 1% per
  day for 10 days produces gains exceeding 3× the index loss.
- Supporting evidence: SEC investor alert "Leveraged and Inverse ETFs:
  Specialized Products with Extra Risks for Buy-and-Hold Investors" (2009)
  explicitly warns that 3x ETFs held more than one day can diverge from the
  expected multiple due to daily compounding. Avellaneda and Zhang (Journal
  of Investment Management, 2010) derive closed-form volatility decay for
  leveraged ETFs and show that at 20% annualized daily volatility, a 3x
  inverse ETF loses roughly 45% of NAV per year to decay in a flat market.
  No-margin structure confirmed: inverse ETFs do not require a margin account,
  cannot be short-squeezed (the ETF itself), and have fixed maximum loss.
- Contrary evidence: In sustained downtrends (more than 5 consecutive down
  days), 3x inverse ETFs can produce returns exceeding 3× the index move
  due to positive compounding — making them attractive for strong trend
  environments. However, identifying sustained trends in advance is
  unreliable. VIX spikes (>30) historically precede reversals 60%+ of the
  time within 5 days, making deep-decay inverse ETF holds through VIX spikes
  particularly risky. Tax treatment: 3x leveraged ETF gains are often
  treated as short-term capital gains regardless of holding period due to
  regulated investment company rules; consult tax advisor.
- Applicable environment (all gates must be satisfied for a draft order):
  (a) VIX > 20 AND rising on 2+ consecutive sessions;
  (b) SPY or QQQ below the 20-day MA with 2 consecutive closes below;
  (c) NYSE Advance/Decline ratio < 1.0 for 2+ days (breadth confirming);
  (d) Clear macro catalyst or technical breakdown (not VIX alone);
  (e) Sentiment composite RISK-OFF from us-market-sentiment skill.
  Instrument selection: SQQQ if Nasdaq leading decline; SPXS for broad
  market; TECS if tech sector distribution confirmed; SRTY if small-cap
  / credit stress is the driver.
- Non-applicable environment: VIX below 20; choppy or oscillating markets
  without directional trend; V-shaped recovery in progress (SPY gap-up ≥2%,
  NYSE A/D ratio > 2.0 with volume confirmation); confirmed bullish macro
  catalyst (surprise Fed pivot, strong NFP below consensus, CPI miss);
  SPY/QQQ back above 20-day MA with breadth recovery. Any of these
  invalidates an existing inverse ETF position.
- Time scale and position sizing:
  - 3x inverse ETFs: max hold 2–5 trading days without full trend
    re-confirmation. Re-check all entry gates daily.
  - 1x inverse ETFs: acceptable hold up to 10 trading days in confirmed
    downtrends.
  - Max allocation: 8–10% of total portfolio in all inverse ETF positions
    combined. For a $3,600 account: max ~$300–$360 across all inverse names.
  - Never stack multiple inverse ETFs (e.g., both SQQQ and SPXS) in
    simultaneous positions — they share market-direction correlation without
    diversification benefit.
- Profit-taking protocol for inverse ETF positions:
  - Index down 2–3% from entry: capture 50%+ of position (≈6–9% on 3x)
  - Index down 4–5% from entry: capture 80% (≈12–15% on 3x)
  - Full-exit trigger: VIX reverses below 18, OR SPY/QQQ gaps up ≥2%
    on volume, OR NYSE A/D ratio recovers above 2.0 for one full session.
  - Never hold through a confirmed reversal signal waiting for more gains.
- Required behavior in reports: When proposing an inverse ETF draft order,
  explicitly cite which of the applicable-environment gates are satisfied.
  If any gate is missing, the draft must be withheld. The `standing-inverse-
  etf-conditions` rule governs this check.
- Prohibited use:
  - Do not hold any 3x inverse ETF through a confirmed market reversal signal.
  - Do not use inverse ETFs when VIX < 20 — decay will erode gains faster
    than any move.
  - Do not stack multiple inverse ETFs simultaneously.
  - Do not average down on inverse ETFs during a market recovery.
  - Do not treat inverse ETFs as cash equivalents or as passive hedges.
  - Do not enter large inverse positions pre/post-market on thin liquidity.
- Evidence strength: Strong for daily rebalancing decay mechanism
  (mathematical). Medium for entry gate calibration (based on VIX
  calibration data). Weak for precise profit-taking thresholds (empirical
  guidelines only; market structure changes can invalidate them quickly).
- Last review date: 2026-07-23.
- Revalidation trigger: Live evidence that VIX-gated entries are poorly
  calibrated vs CALIBRATION_SUMMARY.md distributions; sustained trending
  markets where 3x holds outperform the gate rule; structural changes to
  SQQQ/SPXS/SRTY/TECS AUM or liquidity; SEC rule changes affecting daily
  rebalancing requirements for leveraged ETFs.

### Official VIX And Implied Volatility Are Risk-State Inputs, Not Directional Trade Signals

- Core conclusion: For premarket and intraday risk-state classification, a
  timestamped official Cboe VIX value, or a reliable vendor carrying official
  VIX, should outrank prior-session VIX, stale sidebar quotes, and unlabeled
  proxies. If official real-time VIX is unavailable, VX futures, VIX term
  structure, UVXY/VIXY, ES/NQ futures, and other instruments may be used only
  as explicitly labeled proxies with a confidence downgrade. VIX can set risk
  budget, max size, and confirmation gates; it cannot by itself create an
  immediate buy or sell draft.
- Mechanism: VIX-style measures extract risk-neutral expected volatility from
  index option prices. Because option markets aggregate hedging demand,
  expectations, and risk premia before and during the cash session, current
  implied volatility is generally more informative about ex ante market risk
  than stale historical volatility. But the same risk premia and hedging demand
  make VIX a biased volatility forecast and not a same-day direction signal.
- Supporting evidence: Cboe states that VIX is calculated from real-time SPX
  option bid/ask quotes, targets a constant 30-day expected volatility measure,
  and is disseminated during GTH and RTH windows. Fleming (Journal of Empirical
  Finance, 1998) finds S&P 100 option-implied volatility is upward biased but
  contains relevant information and dominates historical volatility in ex ante
  forecasting power. Jiang and Tian (Review of Financial Studies, 2005) find
  model-free implied volatility from SPX options subsumes Black-Scholes implied
  volatility and past realized volatility in forecasting future realized
  volatility. The 2026-07-23 live failure, where premarket VIX was estimated
  near 17 while open VIX was about 19.27, shows stale/proxy source error can
  materially misclassify the risk state.
- Contrary evidence: Fleming's evidence also shows implied volatility tends to
  overstate future realized volatility, and the bias is not a trading-profit
  signal. VIX futures are not spot VIX; they contain term-structure, carry,
  convexity, liquidity, and risk-premium effects. VIX ETFs/ETNs add roll and
  product-construction mechanics. Modern weekly and 0DTE SPX option activity
  may alter intraday behavior relative to older samples.
- Applicable environment:
  - Premarket, intraday, and postmarket reports that classify VIX risk state.
  - Special-event days when VIX gates affect buy/sell draft eligibility.
  - Any report using VIX thresholds such as <18, 18-20, or >20.
- Non-applicable environment:
  - Direct VIX-product trading, which requires separate roll, decay, spread,
    and execution-cost analysis.
  - Single-stock direction calls without price, volume, catalyst, and sector
    confirmation.
  - Cases where official VIX is unavailable and no timestamped proxy exists;
    report reliable real-time VIX unavailable.
- Required behavior in reports:
  - Record the VIX source type: official, vendor official, VX futures proxy,
    ETF/ETN proxy, stale, or unavailable.
  - Record the timestamp and ET session context.
  - If source is proxy, avoid hard spot-VIX language and downgrade confidence.
  - In postmarket audit, compare premarket VIX/proxy against official open VIX;
    review >1 point errors and treat >2 point errors as material source/risk
    failures.
  - Continue applying `standing-vix-permission-not-order`: VIX below a
    threshold permits only conditional risk-taking and cannot create an
    immediate order.
- Prohibited use:
  - Do not use prior-session VIX as live premarket VIX.
  - Do not present VX futures, UVXY, VIXY, or other proxies as exact spot VIX.
  - Do not write "VIX <18 means buy" or "VIX >20 means sell."
  - Do not override price/volume/VWAP/breadth/catalyst gates because VIX is
    favorable.
- Evidence strength: Medium-to-Strong for model-free/index-option implied
  volatility as a volatility information source; Medium for the live reporting
  source hierarchy; Weak for any direct equity direction signal.
- Last review date: 2026-07-26.
- Revalidation trigger: Structured logs show repeated official/proxy VIX gaps;
  09:00 proxy-to-open VIX error exceeds 2 points more than twice in a month;
  Cboe changes VIX calculation or dissemination schedule; live calibration
  shows current proxy hierarchy is inferior to another timestamped source.

### Closing Auctions Are Official Reference Marks, Not Standalone Direction Signals

- Core conclusion: In liquid U.S. stocks and ETFs, official closing prices set
  through closing auctions are valid postmarket accounting and audit reference
  marks when the source is reliable and timestamped. But closing-auction volume,
  imbalance, or a late auction price move is not a standalone next-session
  directional signal. If a scheduled postmarket report failed to capture the
  close on time, the system must mark the missing close data and any late source
  explicitly; it must not recreate missed trading predictions from later data.
- Mechanism: Closing auctions concentrate benchmark, passive, ETF, and
  liquidity-motivated orders at one clearing price. This concentration can
  reduce price impact for many nonmicrocap stocks and make the official close a
  useful reference. The same concentration can also create temporary deviations
  from nearby continuous-market prices, especially around index events, options
  expiry, imbalances, or thin names.
- Supporting evidence: Bogousslavsky and Muravyev (Journal of Financial
  Markets, 2023) report that U.S. closing auctions accounted for 7.5% of daily
  volume in 2018 versus 3.1% in 2010, that closing prices usually match nearby
  bid/ask prices, and that average auction price deviations revert quickly.
  Goyal, Jegadeesh, and Wu (Journal of Financial and Quantitative Analysis,
  2026) use CRSP, TAQ, and NYSE/Nasdaq auction data from 2012-2021 and find
  closing-auction price impact is lower than continuous-market impact for all
  groups except Nasdaq microcaps; opening auctions are illiquid. NYSE reports
  Q2 2024 U.S. closing auctions matched $55.5B/day and 9.44% of total notional.
- Contrary evidence: Closing prices can attract manipulation or benchmark
  pressure when the close is economically valuable; Hillion and Suominen
  (Journal of Financial Markets, 2004) is the classic warning. Passive investing
  can concentrate liquidity at the close and may reduce continuous-session shock
  absorption, as noted by the ECB's 2024 financial-stability discussion.
  Auction deviations that quickly reverse are evidence against using close moves
  as a simple next-day momentum signal.
- Applicable environment:
  - Postmarket reports that need official close prices for SPY/QQQ/IWM/DIA,
    VIX-linked context, sector ETFs, and held tickers.
  - 15:30-16:00 ET intraday windows where close-flow pressure may affect
    lock-profit or risk-reduction reviews.
  - Large-cap stocks and liquid ETFs with reliable official or vendor close
    data.
- Non-applicable environment:
  - Nasdaq microcaps, thin stocks, halts, corporate actions, or abnormal auction
    imbalances without direct source confirmation.
  - Opening auction and first-print trades; the opening auction is a separate,
    less liquid regime.
  - Any attempt to infer next-day direction from close volume alone.
- Required behavior in reports:
  - Separate "official close", "tail quote", "premarket quote", and "broker
    position mark."
  - If official/reliable close data are unavailable, write that clearly instead
    of substituting a stale 15:33 quote.
  - Opening trade drafts require 15-30 minutes of regular-session confirmation,
    VWAP/opening range, spread/volume, and sector/ETF confirmation.
  - A failed postmarket window remains `failed_backfilled_audit`; later close
    data can repair accounting, not recreate missed predictions.
- Prohibited use:
  - Do not treat a closing-auction spike as proof of next-day buying pressure.
  - Do not use a first print or opening auction price as stable fair value.
  - Do not cite lower closing-auction impact as permission to trade without EV,
    catalyst, risk-rule, and user-approval gates.
  - Do not use closing-auction cost evidence to replace Webull's actual fee
    finalization for realized P/L.
- Evidence strength: Medium-to-Strong for liquid-stock/ETF close-price
  reference and auction liquidity mechanism; Medium for execution-cost context;
  Weak for direction.
- Last review date: 2026-07-26.
- Revalidation trigger: Structured logs show repeated close-to-next-open
  directional failures, missing close snapshots persist despite redundant
  sources, NYSE/Nasdaq auction mechanics materially change, or live data show
  tail quotes routinely outperform official close for postmarket audit.

### Realized P/L Requires Fee Finalization And Execution-Cost Layering

- Core conclusion: Filled sell-order recaps must separate gross P/L,
  broker-returned fees, official regulatory-fee estimates, spread/slippage,
  market-impact/delay context, cost-basis source, and finalization status. A
  broker fee field returned by Webull is the final account source when
  available. If the fee is missing, a regulatory or `$0.02` small-order
  estimate may be used only as provisional.
- Mechanism: Implementation shortfall compares the paper decision with the
  actual implemented portfolio. Explicit fees are only one cost layer; spread,
  slippage, market impact, delay, and unfilled opportunity cost are distinct
  execution layers. Realized account P/L, however, should be finalized from the
  broker's actual order and fee records, not from a spread proxy.
- Supporting evidence: Perold (Journal of Portfolio Management, 1988) provides
  the implementation-shortfall framework for paper-vs-actual execution.
  Hasbrouck (Journal of Finance, 2009) validates daily effective-cost estimates
  against TAQ transaction-level estimates with about 0.965 correlation in the
  1993-2005 validation sample, while noting effective cost is not full
  multi-trade implementation shortfall. SEC Section 31 guidance states the fee
  obligation applies to SROs and the FY2026 rate from 2026-04-04 is $20.60 per
  $1,000,000 of covered sales; FINRA lists covered equity Trading Activity Fee
  at $0.000166 per share, subject to caps and exemptions.
- Contrary evidence: Harris (Journal of Finance, 1990) shows Roll-style
  serial-covariance spread estimates are noisy and biased; Goyenko, Holden, and
  Trzcinka (Journal of Financial Economics, 2009) show liquidity proxy quality
  varies against TAQ and Rule 605 benchmarks. Rule 605 reports and spread
  proxies are execution-quality context, not individual broker statements.
- Applicable environment: Postmarket and intraday order recaps, Webull fee
  finalization, filled sells, partial fills, sold positions whose current
  holding cost basis disappeared, and small-account fee estimates.
- Non-applicable environment: Tax-lot accounting, wash sales, broker statement
  disputes, option exercise/assignment, corporate actions, or trades where fill
  price, quantity, or cost basis cannot be verified.
- Time scale: Accounting/audit workflow; not a trade-timing signal.
- Required behavior in reports:
  - If broker fees are returned, use them and mark realized P/L final.
  - If broker fees are missing but fill price, quantity, and cost basis are
    known, report gross P/L and provisional net P/L using official regulatory
    estimates or the approved `$0.02` fallback; label final broker record as
    controlling.
  - If cost basis is missing, do not compute net P/L unless citing a prior
    structured log or user-confirmed statement as the cost source.
  - Keep spread/slippage/market-impact discussion separate from broker fee
    finalization.
- Prohibited use:
  - Do not call estimated net P/L final while Webull fees remain empty.
  - Do not replace broker fees with Rule 605, spread, or Roll/Gibbs estimates.
  - Do not use missing fees to avoid reviewing filled sell orders.
  - Do not use implementation-shortfall or effective-spread evidence as a
    same-day buy/sell signal.
- Evidence strength: Strong as transaction-cost accounting and audit workflow;
  Medium for modern retail fee-estimate calibration; Weak for direction.
- Last review date: 2026-07-29.
- Revalidation trigger: Webull fee fields begin returning final fees reliably,
  structured logs show repeated cost-basis corruption after sells, broker
  statements contradict the `$0.02` provisional estimate on multiple small
  orders, SEC/FINRA fee schedules change, or the schema adds validated
  `execution_cost_layers`.

### Event Dates And Remaining Trading Sessions Must Be Verified Before Drafts

- Core conclusion: Any event-driven buy, sell, trim, or hold draft must verify
  the official event date, weekday, release/session timing, and number of
  remaining regular trading sessions before using urgency language such as
  "last trading day" or "before earnings." A calendar/date mismatch blocks the
  draft until the date is corrected or clearly downgraded.
- Mechanism: Event-risk decisions are path dependent. One extra regular
  session before an earnings release, FOMC decision, macro print, FDA date, or
  court/regulatory event can materially change the right action because the
  system can wait for more price, volume, spread, and news confirmation.
- Supporting evidence: The 2026-07-26 postmarket audit found that several
  2026-07-24 PYPL windows mislabeled 2026-07-28 as Monday; it is Tuesday. If
  PYPL earnings are before market on 2026-07-28, then 2026-07-27 remains a
  regular session, so the 2026-07-24 "final window" urgency and full-sell
  draft were too aggressive. This was added to
  `research/queue/postmarket-failures.md` and `research/EVAL_CASES.md`.
- Contrary evidence: Date verification does not decide direction and does not
  replace price, volume, guidance, filing, or company-IR checks. A verified
  near-term event can still justify a risk-reduction draft when the position
  breaks its invalidation level, liquidity disappears, or the official event
  itself introduces binary risk the user does not want to hold.
- Applicable environment:
  - Earnings, conference calls, FOMC, CPI/PCE/NFP/ISM, Treasury auctions,
    FDA/regulatory/court dates, and any event used to justify a trade draft.
  - Premarket, intraday, postmarket, and weekend reports that discuss events in
    the next five regular trading sessions.
- Non-applicable environment:
  - Pure accounting updates with no trade draft or urgency claim.
  - Long-term background dates that are explicitly not used for action.
- Required behavior in reports:
  - Verify weekday locally or from an official source before writing event
    urgency.
  - Separate event release time, call time, premarket/after-hours reaction, and
    next regular-session price discovery.
  - If the official time is unavailable, write "specific time unconfirmed" and
    do not invent a minute.
  - If a date error is found, correct the event plan and reduce or remove any
    urgency-based order draft.
- Prohibited use:
  - Do not infer the weekday from memory or from a stale report.
  - Do not call a day the "last trading day" before checking the calendar.
  - Do not force a full sell solely because earnings are near when another
    regular session remains and no price/information failure has triggered.
- Evidence strength: Strong as a reporting and audit-control principle; Medium
  for event-risk sizing discipline; Weak as any direct direction signal.
- Last review date: 2026-07-26.
- Revalidation trigger: Any future postmarket audit finds a weekday/date error,
  official IR calendar changes after a report, or monthly prompt canaries show
  event-date parsing remains unstable.

### Real Interest Rates And Growth Equity Duration Are Structurally Related, Not Daily Signals

- Core conclusion: Growth-tilted ETFs (QQQM/QQQ) have materially longer effective
  cash-flow duration than core/value ETFs (VOO/SPY). When TIPS-implied real interest
  rates rise in a sustained fashion (weeks to months), growth stocks face a
  discount-rate headwind that is structurally larger than the headwind for value or
  blended-market stocks. This effect operates over rate cycles, NOT intraday or
  day-to-day.
- Mechanism: In a standard DCF framework, stocks whose expected cash flows arrive
  further in the future (high P/E, low near-term earnings yield, reinvestment-heavy
  businesses) have longer "duration." A 1-percentage-point rise in the discount rate
  creates a larger present-value reduction for a 15-year-duration stock than for a
  5-year-duration stock, analogous to a long-duration bond vs. a short-duration bond.
  The TIPS 10-year real yield is the relevant rate channel for equity duration, not
  the nominal yield alone. The nominal yield contains an inflation premium that does
  not directly affect real asset valuations in the same direction.
- Supporting evidence:
  - Lettau, Martin and Wachter, Jessica A. (2007), "Why Is Long-Horizon Equity
    Less Risky? A Duration-Based Explanation of the Value Premium," Journal of
    Finance, Vol. 62, No. 1, pp. 55–92. DOI: 10.1111/j.1540-6261.2006.01012.x.
    Shows growth stocks have longer duration and are disproportionately exposed to
    discount-rate (real rate) shocks. Model fits the value premium and cross-section
    of returns over a 50+ year U.S. sample. Source: Tier 2 (JF); full text not
    accessed in live session 2026-07-31 (ScienceDirect/journal access blocked);
    treated as established training-data knowledge.
  - Weber, Michael (2018), "Cash Flow Duration and the Term Structure of Equity
    Returns," Journal of Financial Economics, Vol. 128, No. 3, pp. 486–503.
    DOI: 10.1016/j.jfineco.2018.02.003. Empirically measures cash-flow duration
    from analyst EPS forecast data; finds a ~5.2% annual return gap between short-
    and long-duration quintiles; the premium survives FF5 factor controls. The 2022
    rate shock (TIPS real yield surging, QQQ -33%) provides a post-sample
    confirmation. Source: Tier 2 (JFE); full text not accessed in live session
    2026-07-31 (ScienceDirect blocked); treated as established training-data knowledge.
- Contrary evidence:
  - The AI earnings cycle (2023–2025) showed that strong cash-flow growth can more
    than offset duration headwinds. NVDA, MSFT, and AMZN delivered earnings growth
    large enough to dominate the 4%+ real rate environment. This weakens the model's
    near-term predictive power in extreme earnings-acceleration environments.
  - The value premium partially reflects distress risk (Fama-French), not only
    duration. Competing explanations exist.
  - Rising real rates sometimes signal economic strength, which lifts earnings,
    partially offsetting valuation compression. The direction is ambiguous in
    early-expansion environments.
  - Duration operates in the cross-section on average; individual stocks deviate
    widely.
- Applicable environment:
  - QQQM/QQQ add-on sizing decisions when TIPS 10Y real yield is sustainably above
    2.0% and rising (weeks of confirmed upward trend, not one-day moves).
  - Macro-calendar framing: when FOMC is in a hawkish cycle or NFP/CPI data reprices
    the rate path materially higher, QQQM faces duration headwind vs. VOO.
  - Portfolio construction: QQQM vs. VOO relative weighting in rate-rising vs.
    rate-falling environments.
- Non-applicable environment:
  - Intraday or single-session trading; duration does not operate on this timescale.
  - Days when a single 10Y yield move of a few basis points is the only input;
    bps-level moves are noise relative to the cycle-level duration mechanism.
  - Environments where earnings growth clearly dominates (AI capex boom without
    rate signal reversal).
  - Do not apply to individual stock selection within the QQQM basket; QQQM-level
    duration analysis is appropriate, stock-by-stock variation is wide.
- Required behavior in reports:
  - When 10Y real (TIPS) yield is rising in a sustained cycle, add a context note
    for QQQM: "structural duration headwind; apply normal-to-tighter sizing gates."
  - Distinguish nominal 10Y yield (4.714% on 2026-07-31) from real 10Y yield
    (TIPS-implied, approximately 2.1–2.3% in mid-2026). Only the real yield
    is the primary duration channel.
  - Do not generate a QQQM sell draft solely because nominal yields rose in a day.
  - When rate environment improves (real rates falling), upgrade QQQM sizing to
    standard rather than tighter.
- Prohibited use:
  - Do not convert daily nominal yield moves into same-day QQQM sell signals.
  - Do not equate a nominal yield rise with a real rate rise without checking
    the TIPS breakeven component.
  - Do not apply the duration premium as a same-session momentum trade trigger.
  - Do not use this mechanism to recommend inverse ETFs without meeting all five
    inverse-ETF gates in MARKET_KNOWLEDGE.md.
- Evidence strength: Strong for the theoretical mechanism and the historical
  regularity (value/growth duration differential well-replicated); Medium for live
  premarket application (rate cycles ≠ daily triggers; earnings growth can overwhelm).
- Last review date: 2026-07-31.
- Revalidation trigger: TIPS real yield data systematically unavailable in live
  sessions (requiring proxy rethink); AI earnings cycle shows sustained evidence that
  duration mechanism no longer holds in current market structure; Fed changes how it
  communicates real rate path.

### Industry Peer Earnings Transfer Partially Reduces But Does Not Eliminate Pre-Announcement Binary Risk

- Core conclusion: When a closely-correlated industry peer announces strong earnings
  results for a specific business segment that overlaps materially with an upcoming
  reporter's revenue mix, this constitutes partial information transfer that
  legitimately reduces (but does not eliminate) the binary-event risk of holding
  through the subsequent announcement. The strength of the risk reduction depends on:
  (1) the revenue-segment overlap fraction; (2) whether the peer's outperformance was
  revenue-driven vs. mix/margin-driven; (3) whether other non-overlapping segments
  of the subsequent reporter remain uncertain.
- Mechanism:
  - Firms in the same industry face correlated macro and demand conditions; a peer's
    announcement reveals information about the shared environment (Freeman and Tse,
    1992 JAE).
  - Stocks earn a positive earnings announcement premium on average (~2.1–2.5%
    excess return in the announcement week), suggesting that holding through
    announcements has positive expected value in aggregate (Frazzini and Lamont,
    2007 JFE).
  - Combining both: strong peer read-through shifts the pre-announcement expected
    value upward, reducing the probability of a large negative surprise in the
    overlapping segment. This justifies a lower urgency for pre-announcement risk
    reduction (trim to half size or move stop to cost, rather than full exit).
- Supporting evidence:
  - Freeman, Robert N. and Tse, Senyo Y. (1992), "An Earnings Prediction Approach
    to Examining Intercompany Information Transfers," Journal of Accounting and
    Economics, Vol. 15, No. 4, pp. 509–523. DOI: 10.1016/0165-4101(92)90009-V.
    Shows peer earnings predict subsequent reporters; effect is stronger in
    homogeneous industries. Source: Tier 2 (JAE); full text not accessed in live
    session 2026-07-31; treated as training-data knowledge.
  - Frazzini, Andrea and Lamont, Owen A. (2007), "The Earnings Announcement Premium
    and Trading Volume," Journal of Financial Economics, Vol. 86, No. 3, pp. 548–573.
    DOI: 10.1016/j.jfineco.2007.01.008. Documents a statistically significant ~2.5%
    excess return around earnings announcement weeks; premium survives factor
    controls; higher for high-attention stocks. Source: Tier 2 (JFE); full text not
    accessed in live session 2026-07-31; treated as training-data knowledge.
- Contrary evidence:
  - For conglomerates with low segment-level overlap, the information transfer is
    weak. AMZN's AWS segment (~17% of total revenue in 2025) means MSFT Azure
    results explain only part of AMZN's total earnings outcome; retail, advertising,
    and subscriptions remain binary.
  - Modern large-cap announcement premiums may have weakened (see Martineau 2022 in
    FAILED_IDEAS.md); algorithmic trading and same-day options settlement may have
    compressed the premium for mega-cap stocks.
  - Options-implied straddle pricing: when the straddle is fairly priced at the
    expected announcement move, stock holders do not systematically earn the premium —
    options sellers capture it.
  - Competitive dynamics can invert the transfer: if MSFT gained cloud market share
    at AMZN's expense, MSFT's strong Azure results would be a negative signal for AWS.
- Applicable environment:
  - Holding a position through earnings when all of the following are true:
    (a) A closely-correlated peer (same primary business segment, revenue overlap
    >50% of the upcoming reporter's total revenue) has reported with meaningful
    upside in that segment.
    (b) The peer's outperformance was revenue-driven, not purely margin/mix-driven.
    (c) The position size is ≤ 15% of account equity (small enough that a -15% miss
    does not cause unacceptable loss).
    (d) No adverse price action or unusual options market behavior pre-announcement.
  - When these criteria are met, the default is: trim to 50% or move stop to cost
    basis, do NOT full-exit preemptively.
- Non-applicable environment:
  - Position is a conglomerate where the peer covers <30% of total revenue mix.
  - Position is already above the profit-audit line (take-profit logic supersedes
    announcement premium argument).
  - Peer's read-through is ambiguous or mixed (e.g., peer beat on revenue but missed
    on margin, with uncertain implications for the subsequent reporter).
  - Any event with binary regulatory, legal, or macro risk unrelated to the peer's
    earnings (FDA ruling, DOJ action, macro shock).
  - Large accounts where the announcement exposure represents >20% of equity.
- Required behavior in reports:
  - When a pre-earnings risk review is triggered, explicitly assess:
    (1) Which peers have already reported? What was their primary-segment surprise?
    (2) What fraction of the upcoming reporter's revenue does this segment represent?
    (3) Is the peer's outperformance revenue-driven or margin-driven?
    (4) What is the current position size as a fraction of account equity?
  - If peer read-through meets the applicability conditions above, downgrade binary
    risk from "high" to "moderate" and change the default draft from "full pre-exit"
    to "trim to 50% or move stop to cost basis."
  - Still issue a reduced-size sell draft if the position is above the profit-audit
    line; profit protection logic takes precedence over announcement premium.
- Prohibited use:
  - Do not use the announcement premium to justify holding any position through
    any earnings, regardless of size or concentration.
  - Do not use peer read-through to eliminate the binary event risk entirely.
  - Do not cite this rule as justification for holding a position that has already
    triggered its full-exit line.
  - Do not apply this framework to non-earnings binary events (FDA rulings, FOMC,
    litigation outcomes).
- Evidence strength: Medium for industry information transfer mechanism (Freeman-Tse
  1992, well-cited); Medium for announcement premium (Frazzini-Lamont 2007, well-
  cited but modern large-cap applicability uncertain); Weak for same-stock single-
  announcement prediction.
- Last review date: 2026-07-31.
- Revalidation trigger: Martineau (2022) decay evidence is confirmed in postmarket
  audits (hold-through-earnings systematically underperforms vs. sell-before model);
  a future postmarket failure shows peer read-through was used to justify a hold that
  resulted in a large loss; or monthly prompt evaluation finds the dual-path rule
  creates confusion in final-action summaries.

### High-Priced Whole-Share Orders Require Account-Percentage Sizing Gates

- Core conclusion: In a small account, a single share of a high-priced stock can
  create excessive concentration even when the ticker is liquid and the catalyst is
  real. Whole-share minimums, especially in extended hours, must be translated into
  account-equity percentage before any order draft is shown.
- Mechanism:
  - A $700-$900 single share can represent 15%-25% of a ~$3,500-$4,000 account.
  - High concentration increases forced-decision risk: a position may have to be
    sold early to reduce exposure even when the underlying thesis continues to work.
  - Fractional-share restrictions outside regular hours can make the smallest
    executable order larger than the desired risk unit.
- Supporting evidence:
  - Mature portfolio-construction principle: position sizing should be based on
    portfolio risk and loss tolerance, not only on ticker quality.
  - Local postmarket audit on 2026-07-30: BUY MU 1 share near $850 was about 23%
    of account equity; it was sold quickly for a tiny gain before MU continued
    higher, showing that oversize whole-share exposure can create both
    concentration risk and premature-exit risk.
  - `Extended-Hours Trading Requires Whole-Share Orders, No Fractional Shares`
    already requires whole shares in premarket/postmarket drafts; this entry adds
    the sizing overlay when one whole share is too large.
- Contrary evidence:
  - For exceptionally high-conviction, first-party confirmed catalysts, a larger
    single-share position can still be acceptable if the user explicitly approves
    the concentration and downside amount.
  - Very liquid mega-cap stocks have low spread/slippage; the issue is account
    concentration, not market liquidity.
- Applicable environment:
  - Any trade draft where one whole share is greater than 15% of account equity.
  - Premarket/postmarket drafts where fractional shares are not executable.
  - High-volatility earnings, semiconductor, biotech, or event-driven names where
    gap risk is large relative to account equity.
- Non-applicable environment:
  - Fractional regular-session drafts where the proposed notional is below the
    account risk cap.
  - Existing positions already approved by the user, though they still require
    profit-taking and invalidation review.
- Required behavior in reports:
  - Before drafting a high-priced whole-share BUY, compute one-share notional as a
    percentage of account equity and cash.
  - If one share exceeds 15% of account equity, default action is buy 0 unless the
    catalyst is first-party confirmed, price/volume gates are met, and the draft
    explicitly labels the oversized concentration.
  - If one share exceeds 20% of account equity, require an "oversized whole-share"
    warning and prefer waiting for regular-session fractional execution or a lower
    notional alternative.
  - Do not use a profitable one-off outcome to loosen this gate.
- Prohibited use:
  - Do not draft high-priced whole-share buys solely because a name is liquid,
    high quality, or moving on earnings.
  - Do not hide the account-percentage impact in a generic "small position" phrase.
  - Do not treat an oversized whole-share trade as equivalent to a $100-$300 staged
    ETF tranche.
- Evidence strength: Strong as a mature risk-sizing principle; Medium for this
  account-specific operational gate based on live audit evidence; Weak as any
  ticker-direction signal.
- Last review date: 2026-08-01.
- Revalidation trigger: account equity materially increases so one share of the
  relevant high-priced stocks is below 10%-15% of equity; broker enables reliable
  fractional extended-hours execution; or repeated audited cases show the gate
  blocks higher-quality opportunities without reducing drawdown or forced exits.

### Multiple Testing Requires FDR Control; Raw P-Values Without Correction Inflate False Discoveries

- Knowledge card: `KG-20260801-ISL-FDR-001`.
- Core conclusion: When testing m signals, factors, or strategies simultaneously
  at significance level α, expected false positives ≈ α × m (for independent
  tests where all nulls are true). Testing 100 candidate factors at p < 0.05
  without correction expects 5 false discoveries even if no factor is real.
  The Benjamini-Hochberg (BH) procedure controls the False Discovery Rate (FDR
  ≤ q) while remaining far more powerful than the Bonferroni correction for
  large m. FDR control should be applied to any factor-screening, signal-selection,
  or multi-strategy comparison exercise.
- Mechanism: Multiple testing inflates the family-wise probability of at least one
  false rejection. Bonferroni corrects by using threshold α/m per test — correct
  but extremely conservative (very low power for m > 20). BH works by ranking
  p-values p_(1) ≤ p_(2) ≤ … ≤ p_(m) and setting the rejection threshold
  adaptively: reject all H₀ⱼ with pⱼ ≤ p_(L) where L = max{j: p_(j) < q·j/m}.
  This guarantees FDR ≤ q regardless of how many nulls are true and regardless
  of the p-value distribution of false nulls, provided tests are independent or
  only mildly dependent. The rejection threshold is data-dependent (cannot be
  pre-specified), unlike Bonferroni.
- Supporting evidence: Benjamini & Hochberg (1995, Journal of the Royal
  Statistical Society Series B — Tier 2) is the foundational paper; proven
  result with guarantees under independence and positive regression dependence.
  James et al. (2021, ISL 2nd ed, Springer) provide textbook treatment confirming
  the procedure. McLean & Pontiff (2016, Journal of Finance — already in
  RESEARCH_INDEX.md) attribute part of factor decay to false discovery in original
  studies: many published "significant" factors were found without adequate
  multiple-testing correction.
- Contrary evidence: BH assumes tests are independent or positively dependent.
  When tests are strongly negatively dependent, BH may not control FDR at the
  stated level (though this is rare in practice). BH also assumes p-values are
  uniformly distributed under the true nulls — violated when there is residual
  data snooping or p-value hacking before the final test. The BY procedure
  (Benjamini & Yekutieli 2001) extends BH to arbitrary dependence at the cost
  of a log(m) penalty.
- Applicable environment: Any factor research or signal-selection workflow where
  m ≥ 10 candidates are evaluated and the goal is to select a subset that
  outperforms chance. Backtesting a single strategy is a special case of multiple
  testing if many variants were tried before the final specification. Journal-style
  hypothesis tests on factor alphas. Side-by-side comparison of K models.
- Non-applicable environment: Testing a single pre-specified hypothesis with no
  data dredging. Live trading decision on a single identified catalyst. When
  the number of tests m is 1-2 and tests are independent.
- Time scale: Research-phase methodology; applies before any factor enters
  MARKET_KNOWLEDGE.md or becomes a trading rule.
- Use in research and premarket reports: Any multi-factor screen reported in
  the research system should state whether FDR or Bonferroni correction was
  applied. Reports should never present raw p-values from a multi-factor
  scan as "statistically significant" without noting the multiple-testing
  correction (or lack thereof). When evaluating anomaly papers or factor
  research, check whether the paper tested many signals and whether
  multiple-testing correction was applied.
- Prohibited use: Do not treat a raw p < 0.05 from a scan of 20+ factors as
  confirmed statistical significance without FDR correction. Do not apply
  the one-test framework to an exercise that tested many variants of the same
  signal. Do not interpret BH "rejection" as certainty — FDR control at 10%
  still implies 10% of discoveries are false on average.
- Evidence strength: Strong as a statistical methodology principle; directly
  applicable to the factor research program; weak as a same-day trading signal.
- Last review date: 2026-08-01.
- Revalidation trigger: New high-quality methodology paper changes the
  recommended FDR threshold for financial factor research, or the standard
  dependency structure of financial test statistics is shown to materially
  violate BH assumptions in ways that affect the research system.
- Source: ISL 2nd ed Ch 13 (James et al., Springer 2021); Benjamini &
  Hochberg (JRSS-B, 1995); McLean & Pontiff (Journal of Finance, 2016).

### Overfitting Prevention Requires Bias-Variance Management and Out-Of-Sample Validation

- Knowledge card: `KG-20260801-ISL-OOS-002`.
- Core conclusion: Training error (in-sample MSE, in-sample R²) always
  decreases as model complexity increases and is not a valid estimate of
  generalization performance. Expected test MSE = Bias²(f̂) + Var(f̂) + Var(ε).
  Adding predictors, hidden layers, or interaction terms reduces bias but
  increases variance; the optimal complexity minimizes their sum. Cross-
  validation (k-fold or rolling-origin for time series) is the required tool
  for estimating test error and selecting hyperparameters. LASSO and Ridge
  regularization reduce variance via explicit coefficient penalization; LASSO
  additionally performs variable selection (exact zero coefficients) and is
  preferred for sparse signals. Random forests and boosting have internal
  OOB/CV estimates; boosting CAN overfit and requires CV to select B (n trees).
- Mechanism:
  - Bias: error from approximating complex reality with a simpler model.
    Increases when model is too inflexible; linear regression on a non-linear f.
  - Variance: sensitivity of f̂ to training data perturbations. Increases when
    model is too flexible (overfitting); a decision tree that memorizes training data.
  - Irreducible error Var(ε): noise floor; cannot be reduced by any model.
  - k-fold CV: divide data into k folds; train on k-1, validate on 1; average
    k validation errors. 10-fold preferred over LOOCV because lower variance
    (LOOCV outputs are highly correlated across the n near-identical training sets).
  - LASSO (ℓ₁ penalty): minimize RSS + λΣ|βⱼ|; forces sparse solutions (exact
    zeros); select λ via k-fold CV; one-SE rule prefers simpler models within
    one SE of minimum CV error; must standardize predictors.
  - Ridge (ℓ₂ penalty): minimize RSS + λΣβⱼ²; shrinks all coefficients toward
    0 but retains all; best when signal is spread across many small effects.
  - Random Forest: OOB (out-of-bag) error ≈ LOOCV error; reliable without a
    separate test set. Decorrelated trees via m ≈ √p features per split.
    Does not overfit with large B. Variable importance = total RSS/Gini reduction.
  - Boosting: sequential residual fitting with learning rate λ; CAN overfit
    (unlike RF); select B (n trees) via k-fold CV. Three hyperparameters (B, λ, d).
- Supporting evidence: Core statistical theory (Geman et al. 1992 for
  bias-variance; Stone 1974 for CV — Tier 2 / foundational). Tibshirani (1996,
  JRSS-B — Tier 2) for LASSO; Hoerl & Kennard (1970) for Ridge. Breiman (2001,
  Machine Learning — Tier 2) for Random Forests. James et al. (2021, ISL 2nd ed,
  Springer) confirm and integrate all of the above. Mature methodologies, each
  with decades of cross-domain validation.
- Contrary evidence: CV error is a noisy estimate of true test MSE for small n;
  the estimated optimal complexity can be off by several fold. For strongly
  autocorrelated time series, naive k-fold CV (random split) leaks future
  information — rolling-origin or blocked CV is required (see FPP3 run). LASSO
  can fail when true betas are not exactly sparse; Ridge may be preferred. OOB
  error slightly underestimates test error in some settings. Boosting with very
  small λ may require B > 10,000 trees, which can be computationally prohibitive.
- Applicable environment: Factor-model building, signal-selection with multiple
  candidate predictors, hyperparameter tuning for any ML model used in the
  research system, backtesting validation design.
- Non-applicable environment: Pure live-catalyst decisions where no multi-feature
  model is involved. Known structural risk premia not requiring out-of-sample
  validation (e.g., risk-free rate plus equity risk premium as approximate
  forward return framework). Single-equation models with pre-specified coefficients
  and no data-dependent tuning.
- Time scale: Research-phase methodology; applies before any model or signal
  is admitted to live trading.
- Use in research reports: Any model reported in the research system must
  state the validation methodology (what CV scheme was used, what the OOS
  metric was). In-sample R² or training error must NOT be presented as
  evidence of predictive power. For time-series signals, rolling-origin CV
  is required; for cross-sectional factor research, standard k-fold CV is
  acceptable for non-autocorrelated test statistics. LASSO/Ridge λ selection
  must specify the CV fold count and whether the one-SE rule was applied.
- Prohibited use: Do not report in-sample backtest Sharpe or R² as the
  primary evidence of strategy quality. Do not tune any hyperparameter on the
  same data used to report strategy performance. Do not compare k strategies
  and pick the best without applying FDR correction to the selection p-value.
  Do not use default single-split train/test if the split is not disclosed
  and the test set was viewed during development.
- Evidence strength: Strong as statistical methodology; directly applicable to
  the research system's signal-validation and model-selection workflow; weak
  as a same-day directional signal.
- Last review date: 2026-08-01.
- Revalidation trigger: New high-quality evidence shows a specific alternative
  validation framework outperforms k-fold CV for financial returns data; or
  a new meta-study changes the recommended value of k for financial time series.
- Source: ISL 2nd ed Chs 2, 5, 6, 8 (James et al., Springer 2021); Geman et al.
  (1992); Stone (1974); Tibshirani (1996); Breiman (2001). See also FPP3
  candidate note (`research/books/2026-08-01-forecasting-principles-practice-fpp3.md`)
  for the time-series rolling-origin CV analog.

### When Features Greatly Outnumber Observations (p >> N), Aggressive Regularization Is Required

- Knowledge card: `KG-20260802-ESL-HDP-001`.
- Core conclusion: When the number of candidate features p greatly exceeds the
  number of observations N, models with moderate or no regularization massively
  overfit and produce poor out-of-sample predictions. Aggressive regularization
  (heavy shrinkage, near-zero effective degrees of freedom relative to p) is
  required and outperforms moderate regularization across all method families
  (Ridge, LASSO, LDA, logistic regression, SVM). The optimal amount of
  regularization increases with the ratio p/N; when p/N is large, almost all
  coefficients should be shrunk nearly to zero even if many are non-zero in
  the true model, because there is insufficient data to estimate them.
- Mechanism:
  - When p > N, OLS is undefined; even when p < N but p/N is high, OLS is
    near-singular and highly variable.
  - Ridge regression SVD solution: β̂ridge = V(D²+λI)⁻¹Dᵀu; effective df =
    Σdⱼ²/(dⱼ²+λ). High λ → few effective df → strong shrinkage.
  - Simulation (ESL Ch 18, Figure 18.1): p=1000, N=100. Ridge with λ→small
    (99 effective df) is nearly OLS; vastly underperforms ridge with λ→large
    (43 effective df), which shrinks almost all coefficients to near zero.
  - Intuition: with N=100 observations and p=1000 features, the sample
    covariance matrix is rank-100 at best; the remaining 900 directions are
    estimated from noise. Heavy shrinkage ignores those noise dimensions.
  - Feature selection methods (LASSO, nearest shrunken centroids) also work
    in p >> N by discarding noisy features; shrinkage and selection are
    complementary, not alternatives.
  - Diagonal LDA / independence rule (assumes zero within-class correlations)
    often outperforms full LDA when p >> N because there is insufficient data
    to reliably estimate the p×p covariance matrix.
  - Supervised PCA: filter features by univariate score, then PCA on selected
    subset. The unfiltered leading PC is contaminated by p-N noise features
    and is inconsistent for the latent factor; the supervised PC is consistent.
- Supporting evidence: Hastie, Tibshirani & Friedman (2009, ESL 2nd ed,
  Springer — Tier 2), Ch 18, pp 649–698. Mature methodological principle with
  theoretical guarantees and simulation validation. Bickel & Levina (2004)
  provide theoretical support for the independence rule in high dimensions.
  Bair et al. (2006) validate supervised PCA in survival modeling.
- Contrary evidence: When p/N is small (p < N/10 roughly), aggressive
  regularization can introduce unnecessary bias; moderate or no regularization
  may be preferred. LASSO/ridge may fail to distinguish signal from noise
  when correlation among features is very high (multicollinearity) — grouped
  LASSO or elastic net preferred. The p >> N principle assumes that most
  features are noise; if domain knowledge confirms most are signal, lighter
  shrinkage may be appropriate.
- Applicable environment: Factor-model building when the number of candidate
  signals (p) substantially exceeds the number of trading days / observations
  (N) in the estimation window. Testing 50+ factors on a 3-month (63-day)
  rolling window. Building any predictor with more features than observations.
  Classification with p >> N (e.g., many candidate signals for a binary
  prediction target like "up day" or "earnings beat").
- Non-applicable environment: Single pre-specified signal with theoretical
  backing and no data-driven feature selection. Fundamental factor models
  where a small number of well-understood factors (value, momentum, quality)
  are fit with N >> p. Macro forecasting with 3–5 well-understood predictors
  and long time series.
- Time scale: Research-phase methodology; applies during model building and
  signal-development stages, before any model enters live trading.
- Use in research and premarket reports: Any multi-factor or ML signal
  reported in the research system must state the p/N ratio of the estimation
  window. If p > N/5, the report must document that heavy regularization
  (high λ Ridge/LASSO) was used and that the regularization parameter was
  selected via time-series CV (rolling-origin), not in-sample. Reports must
  not present results from OLS or lightly regularized models when p/N > 0.5.
- Prohibited use: Do not fit OLS with more features than observations and
  present the in-sample results as evidence of predictive power. Do not use
  the number of significant coefficients from OLS in a p > N setting as
  evidence of real signal. Do not apply the p << N regularization intuition
  (e.g., "small ridge penalty is better") when the feature-to-observation
  ratio is high.
- Evidence strength: Strong as statistical methodology; directly applicable
  to the research system's signal-selection and model-building workflow;
  weak as a same-day directional signal.
- Last review date: 2026-08-02.
- Revalidation trigger: New research demonstrates that a specific alternative
  approach (e.g., neural network with implicit regularization, or a principled
  sparse Bayesian method) reliably outperforms heavy-shrinkage Ridge/LASSO
  in p >> N financial factor selection settings.
- Source: ESL 2nd ed Ch 18 (Hastie, Tibshirani & Friedman, Springer 2009);
  Bickel & Levina (2004) for independence rule theory; Bair et al. (2006)
  for supervised PCA.

### Yen Carry Trade Unwinding Tightens US Financial Conditions

- Knowledge card: `KG-20260802-BIS-JPY-001`.
- Core conclusion: When yen-funded leveraged carry trades unwind rapidly —
  triggered by BOJ tightening or sudden yen appreciation — investors who
  borrowed cheaply in yen and invested in USD assets are forced to sell
  those USD assets to repay yen obligations. This deleveraging tightens US
  financial conditions (lower equities, higher yields, VIX spike) even though
  the origin is Japanese monetary policy, not a domestic US shock.
- Mechanism: Carry trade setup: borrow yen at low cost (via FX swap or
  outright forward) → sell yen spot for USD → invest in higher-yielding USD
  assets. Net exposure: long USD assets, short yen (unhedged). When BOJ
  raises rates or yen appreciates unexpectedly: yen short becomes a loss →
  forced unwind → sell USD assets → US financial conditions tighten.
  Amplified by leverage (often 10x+). August 2024 episode: BOJ signals
  tightened → USD/JPY fell sharply → leveraged yen carry positions unwound
  → US equities fell, VIX spiked, US financial conditions tightened.
- Supporting evidence: BIS Annual Economic Report 2025, Chapter II (Tier 1
  source; BIS is explicitly listed as Tier 1 in RESEARCH_PROGRAM.md);
  empirical cross-country analysis, Graph 12 (yen carry trade mechanics),
  August 2024 episode documentation. BIS OTC derivative statistics tracking
  yen FX swap volumes corroborate the timing and magnitude of the transmission.
- Contrary evidence: Not all BOJ rate hikes cause US market disruption —
  depends on size of carry position build-up. If the carry trade is small or
  positions are already reduced, BOJ tightening has limited US spillover.
  Orderly/expected BOJ moves allow gradual position reduction without
  forced selling.
- Applicable environment: BOJ signals or delivers rate hikes; sudden USD/JPY
  reversal (yen appreciation acceleration); yen FX swap volumes declining;
  CIP deviation (JPY-USD) narrowing toward zero; prior sustained period of
  yen depreciation and BOJ ultra-loose policy (carry build-up phase).
- Non-applicable environment: BOJ in active easing mode (yen depreciating →
  carry trade build-up, not unwind); US-driven risk-off not related to FX
  carry; normal USD/JPY ranges without concentrated carry positions; gradual
  and expected yen appreciation where positions can be reduced orderly.
- Time scale: Event-driven; activation requires BOJ policy shift or acute
  USD/JPY reversal; effect can develop over days to weeks.
- Use in premarket reports: When BOJ is scheduled to meet or USD/JPY moves
  more than 2% intraday, flag yen carry unwind risk as a potential amplifier
  of US equity sell-offs and VIX spikes. Do NOT treat as a mandatory sell
  trigger; it is a risk-state modifier requiring confirmation.
- Prohibited use: Do not treat any yen strengthening as automatically causing
  US equity decline. Do not use as a standalone buy or sell signal. Do not
  project magnitude or duration without evidence of position size.
- Evidence strength: Strong as macro risk mechanism; empirically supported
  by the August 2024 episode and BIS cross-country analysis (Tier 1 source).
  Moderate as a premarket prediction tool (requires confirming indicators).
- Last review date: 2026-08-02.
- Revalidation trigger: BOJ normalizes fully to neutral/hawkish policy and
  yen FX swap volumes plateau at structurally lower level, reducing carry
  build-up potential; or a new BIS empirical study revises the August 2024
  transmission channel analysis.
- Source: BIS Annual Economic Report 2025, Ch II, pp 63–75 (BIS, June 2025).

### NBFI Treasury Basis Trade Creates Systemic Fragility

- Knowledge card: `KG-20260802-BIS-NBF-002`.
- Core conclusion: Hedge funds run large leveraged positions in the Treasury
  "basis trade" (buy cash bonds, short futures, repo-financed at near-zero
  haircut). The trade requires extreme leverage to be profitable on a small
  spread. A small increase in repo haircuts forces rapid deleveraging —
  simultaneous Treasury selling by many basis traders causes yield spikes and
  Treasury market dislocations that spread to credit and equities.
- Mechanism: Cash Treasury bonds trade at a slight discount to fair value
  implied by futures → buy cash bond, short futures, capture basis. Finance
  cash bond via repo (pledge bond as collateral). At zero or near-zero
  haircut: borrow up to 100% of bond value → leverage 50–100x is common.
  Profitability requires this leverage to make the small spread meaningful.
  Risk: if repo haircuts increase even 1–2%, forced position reduction.
  With 50x leverage, a 2% haircut increase requires selling ~half the
  position. In stress, many basis traders deleverage simultaneously →
  Treasury selling wave → yields spike. Downstream: sovereign bond losses
  create bank/NBFI balance sheet pressure → credit tightening feedback loop.
  Historical precedent: March 2020 COVID "dash for cash" — basis trade
  deleveraging was central to the Treasury market dislocation requiring
  Fed intervention.
- Supporting evidence: BIS Annual Economic Report 2025, Chapter I (Tier 1
  source); BIS documents this as a structural vulnerability. March 2020
  Treasury market stress provides historical out-of-sample validation.
  Academic literature on basis trade fragility (prior BIS/Fed research).
- Contrary evidence: Fed emergency repo operations in March 2020 prevented
  permanent dislocation; central bank backstops reduce but do not eliminate
  the risk. Basel III capital reforms reduce some bank leverage, but basis
  trades are primarily HF, not bank, positions.
- Applicable environment: Simultaneous VIX spike + Treasury yield spike +
  credit spread widening (all three together suggest basis trade deleveraging
  signature); repo market stress (GCF repo rates rising, haircuts widening);
  Treasury bid-ask spreads widening; financial stress events across all
  asset classes simultaneously.
- Non-applicable environment: Normal Treasury market functioning with stable
  repo haircuts; isolated equity sell-offs not accompanied by Treasury yield
  spikes; Fed actively buying Treasuries (backstops the market); episodes
  where only one of VIX/yields/spreads is elevated (not systemic pattern).
- Time scale: Event-driven; acute basis trade deleveraging can develop in
  hours to days once triggered by a repo haircut increase or liquidity shock.
- Use in premarket reports: When VIX is surging AND Treasury yields are also
  spiking simultaneously, flag potential basis trade deleveraging as a risk
  amplifier. For KRE holdings: if basis trade stress is severe, bank
  collateral values and repo access may be affected — consider applying full
  KRE guardrail and elevated scrutiny. Do not reduce KRE position on basis
  trade risk alone without other confirming signals.
- Prohibited use: Do not use as a directional trading signal for Treasury
  yields in normal conditions. Do not model precise deleveraging timing.
  Do not confuse basis trade profitability analysis with systemic risk analysis.
- Evidence strength: Strong as a structural vulnerability; empirically
  validated by March 2020 episode and documented by BIS (Tier 1 source).
  Weak as a precise timing tool for specific yield moves.
- Last review date: 2026-08-02.
- Revalidation trigger: Regulatory reform mandating minimum repo haircuts for
  Treasury repo (e.g., via central clearing) substantially reduces leverage;
  update this entry to reflect lower fragility; or a major stress episode
  occurs with a different mechanism (non-repo-driven).
- Source: BIS Annual Economic Report 2025, Ch I, pp 27–37 (BIS, June 2025).

### Stock-Bond Correlation Turns Positive in Inflationary Regimes

- Knowledge card: `KG-20260802-BIS-SBC-003`.
- Core conclusion: The traditional negative stock-bond correlation (bonds
  serve as equity hedge via flight-to-safety) was a feature of the 2002–2021
  low-inflation environment. Post-2022, the correlation became structurally
  positive: adverse shocks raise inflation expectations AND risk aversion
  simultaneously → stocks and bonds fall together. The bonds-as-equity-hedge
  assumption and standard 60/40 portfolio diversification are unreliable
  during inflationary supply-shock regimes.
- Mechanism: In deflationary/low-inflation regime: adverse shock → central
  bank cuts rates (bonds appreciate) + flight to safety (bonds appreciate) →
  bonds rally while stocks fall → negative correlation. In inflationary
  regime: adverse supply shock (tariffs, energy, geopolitics) → raises
  inflation expectations (bonds lose value as fixed income) AND raises risk
  aversion (stocks fall) → both assets decline → positive correlation.
  The correlation sign flips when the dominant risk driver is supply/inflation
  rather than demand/growth. Additionally, the "convenience yield" (liquidity
  premium investors pay for Treasuries) declined: diversification benefits
  from Treasuries are reduced.
- Supporting evidence: BIS Annual Economic Report 2025, Chapter I, Graph
  11.C (Tier 1 source; empirical documentation of post-2022 structural break).
  Consistent with academic literature on the macroeconomic regime-dependence
  of stock-bond correlation (e.g., Baele et al., Campbell et al.).
- Contrary evidence: The correlation reverted toward negative in 2024 and
  early 2025 as inflation approached targets. The regime-dependence means
  the positive correlation is not permanent. Deflationary shocks (demand
  collapse, recession fear without inflation) can restore negative correlation.
  Short-duration bonds (T-bills, <2yr) have lower duration risk and may still
  serve as partial hedges even in inflationary regimes.
- Applicable environment: Supply-shock-driven risk events (tariff
  announcements, energy price spikes, geopolitical disruptions); high and
  volatile inflation environment (CPI above target, uncertain expectations);
  inflationary stagflation scenarios; portfolio hedging decisions when
  inflation uncertainty dominates growth uncertainty.
- Non-applicable environment: Demand-shock recessions where central banks
  cut aggressively (GFC 2008, COVID 2020 initial phase) — bonds still hedge;
  well-anchored inflation expectations with CB credibility intact (correlation
  can revert negative); short-duration bond exposure (<1yr maturity) less
  affected by inflation regime; active QE context (Fed buying bonds).
- Time scale: Regime-level: the correlation regime persists over months to
  years. Not a single-day signal; requires assessment of current inflation
  regime before applying.
- Use in premarket and research reports: When evaluating portfolio composition
  during supply-shock events (tariff announcements, energy spikes), do not
  assume TLT/IEF will serve as reliable equity hedges. In research, any
  multi-asset strategy assuming negative stock-bond correlation must condition
  on the inflation regime. For position-level risk, assess whether current
  environment is inflationary-supply or deflationary-demand before assigning
  bond hedge effectiveness.
- Prohibited use: Do not assume positive stock-bond correlation is permanent;
  it is regime-dependent. Do not use TLT/IEF as equity hedges during confirmed
  inflationary supply shocks without acknowledging this entry's conditions.
  Do not use this to eliminate bonds from all portfolios — bonds still serve
  as hedges in deflationary scenarios.
- Evidence strength: Strong as a structural observation with Tier 1 source
  documentation; moderate as a real-time signal (requires regime identification
  first); revalidation needed if inflation durably returns to 2% and stabilizes.
- Last review date: 2026-08-02.
- Revalidation trigger: Sustained return to sub-2% inflation with
  well-anchored expectations for 2+ years → re-assess whether correlation
  has reverted to negative regime. If Fed returns to zero-bound policy,
  deflationary regime properties likely re-emerge.
- Source: BIS Annual Economic Report 2025, Ch I, pp 33–35, Graph 11.C
  (BIS, June 2025).

### Geopolitical Risk Events Cause Persistent Equity Declines; Energy and Defense Hedge

- Knowledge card: `KG-20260803-GFSR-GPR-001`.
- Core conclusion: Major geopolitical risk (GPR) events cause aggregate equity
  markets to decline approximately 0.3% per GPR shock unit on average, with the
  effect persisting for 6+ months. Military conflicts produce larger declines
  (1990 Gulf War: Kuwait equities -50%; 1973 Arab Oil Embargo: -70% for affected
  markets). EM sovereign CDS spreads rise 50–200 bps after domestic military
  conflicts. Energy, defense, and commodity exporter sectors generally benefit.
  Safe-haven advanced-economy sovereign yields decline (flight-to-safety). Investors
  partially price GPR ex-ante via equity beta and options markets (put protection
  costs rise before and during major events).
- Mechanism: Two transmission channels. (1) Market sentiment: GPR raises uncertainty
  and risk aversion; investors sell risky assets and buy safe havens; equities fall,
  VIX spikes, AE bond yields decline, USD strengthens. (2) Economic: supply chain
  disruptions (tariffs, sanctions, physical damage to infrastructure) affect corporate
  revenues sector-specifically. Energy benefits from oil price increases caused by
  supply disruption; commodity importers, retail, and utilities suffer from higher
  input costs and demand uncertainty. The market sentiment channel typically dominates
  in the first days to weeks; the economic channel drives persistence over months.
- Supporting evidence: IMF Global Financial Stability Report April 2025, Chapter 2
  (Tier 1 source; cross-country panel study using Caldara-Iacoviello GPR index,
  Fama-MacBeth regression, decile portfolio analysis). Multiple out-of-sample episodes
  used: Russia-Ukraine 2022 invasion (firm-level stock returns, subsidiary exposure,
  options pricing); US-China tariff announcements 2018–19 (both Chinese and US firms);
  historical events since WWII (aggregate stock market reaction database).
- Contrary evidence: Average effect of ~0.3% masks extreme heterogeneity across events;
  many minor geopolitical events have no statistically significant market impact.
  Short-lived geopolitical events can reverse quickly (e.g., some Middle East military
  incidents resolved within days). Markets can partially anticipate major conflicts
  before they materialize (Russian troop movements → Feb 2022 invasion: options market
  priced risk early). For advanced economy safe-havens (US, Germany, Japan), sovereign
  bond yields often decline on GPR (opposite of EM), reducing GPR's applicability
  to AE fixed income in a uniform way.
- Applicable environment: Active military conflict in a major economy or
  energy-producing region; US tariff escalation or trade war announcements; GPR
  index (Caldara-Iacoviello) spiking materially above recent average; VIX spike
  associated with geopolitical news rather than domestic economic data; EM sovereign
  CDS spreads widening without concurrent domestic macro deterioration; premarket
  monitoring on days with major geopolitical news.
- Non-applicable environment: Short-lived domestic political events with no
  economic transmission (elections, minor diplomacy); advanced economy safe-haven
  sovereign yields (these often rally on GPR, not fall); day-trading horizons
  (average GPR effect accumulates over weeks to months); GPR events where no
  plausible oil supply disruption exists.
- Time scale: Persistent over weeks to months for major events; not a same-day
  intraday signal. Average effect ~0.3% accumulates over 6+ months; major military
  conflicts produce larger and faster declines.
- Use in premarket reports: When major GPR events are in focus (military conflict,
  tariff escalation, energy-supply disruption), flag energy and defense as potential
  relative outperformers. Flag retail, utilities, and commodity importers as under
  pressure. For EM positions: expect CDS spread widening and capital outflow risk.
  For KRE (regional banks): GPR can tighten financial conditions → bank credit risk
  increases → apply standard KRE guardrail criteria. Do not treat as a directional
  buy or sell signal without live price confirmation.
- Prohibited use: Do not use GPR index as precision entry/exit timing for intraday
  or day trades. Do not assume energy always benefits — requires oil supply disruption
  specifically. Do not apply AE safe-haven sovereign bond rules to EM. Do not treat
  the ~0.3% average as a point estimate for any specific event.
- Evidence strength: Strong — Tier 1 source (IMF GFSR April 2025) with multiple
  confirmed out-of-sample episodes (Russia 2022, US-China 2018-19, WWII+ history).
  Quantification (0.3% per shock) is an average with wide dispersion.
- Last review date: 2026-08-03.
- Revalidation trigger: Major new geopolitical event produces statistically
  insignificant market response across multiple independent studies; or structural
  de-globalization reduces cross-border GPR transmission materially.
- Source: IMF Global Financial Stability Report, April 2025, Ch 2, pp 43–85
  (IMF, April 2025). Caldara-Iacoviello GPR index (AER 2022) referenced.

### Treasury Market Has Outgrown Dealer Balance Sheets; Repo Rate Sensitive to Issuance

- Knowledge card: `KG-20260803-GFSR-TDL-002`.
- Core conclusion: The US Treasury market has grown 500%+ since the GFC, but
  broker-dealer balance sheets have grown much more slowly (constrained by Basel III
  supplementary leverage ratio and capital rules). When Treasury issuance spikes,
  GC repo rates rise disproportionately and Treasury market liquidity deteriorates
  (wider bid-ask spreads for 2y/10y/30y). Dealers are shifting from fixed-income
  repo to higher-margin equity margin loans, further reducing their Treasury
  intermediation capacity. Cross-border: ECB quantitative tightening has pushed
  euro area banks into the US dollar repo market, creating dollar funding concentration
  and rollover risks (signaled by EUR/JPY/GBP cross-currency basis widening).
- Mechanism: Primary dealers must absorb Treasury auction supply and intermediate
  the secondary market. Post-GFC Basel III SLR rules limit repo book growth relative
  to Treasury market expansion. Treasury outstanding ~$10T → $30T+ since GFC; dealer
  capacity did not keep pace. When auction supply spikes: dealers cannot absorb →
  repo rates rise to attract marginal buyers → GC repo/SOFR/EFFR basis spreads widen
  → market liquidity deteriorates (wider bid-ask spreads, reduced depth). In stress,
  this chain amplifies: higher repo rates → basis trade margin calls (see
  KG-20260802-BIS-NBF-002) → forced Treasury selling → yield spike → credit
  tightening feedback loop. March 2020 "dash-for-cash" episode is the historical
  out-of-sample validation (required Fed emergency intervention).
- Supporting evidence: IMF Global Financial Stability Report April 2025, Chapter 1,
  Figure 1.19 (Tier 1 source; direct empirical scatter of repo rate sensitivity
  to issuance; Treasury market vs dealer balance sheet divergence chart; bid-ask
  spread vs dealer constraint chart). Corroborated by BIS Annual Economic Report 2025
  (Tier 1 source; Ch I documents basis trade fragility using the same dealer capacity
  constraint). March 2020 historical precedent validated by both sources.
- Contrary evidence: Fed emergency repo operations and subsequent QE in March 2020
  prevented permanent dislocation; central bank backstops reduce but do not eliminate
  the risk. New SEC central clearing mandate for Treasury repo (if implemented) would
  materially increase effective dealer capacity. Some studies argue repo market
  innovations (sponsored repo, FICC clearing) partially offset SLR constraints.
  Short-term T-bill markets are less affected than long-duration coupon bond markets.
- Applicable environment: Periods of high Treasury issuance (large deficits,
  post-debt-ceiling resolution, front-loaded quarterly settlements); GC repo rates
  (SOFR, GCF) rising relative to EFFR/IORB benchmark; 10y or 30y Treasury bid-ask
  spreads widening beyond normal seasonal ranges; VIX spike coinciding with Treasury
  yield spike simultaneously (both moving up = basis trade + dealer capacity double
  stress); cross-currency basis (EUR/JPY/GBP vs USD) widening significantly.
- Non-applicable environment: Fed actively buying Treasuries via QE or emergency
  purchase programs; SOFR/EFFR spread stable and narrow; normal Treasury issuance
  calendar with no unusual supply spikes; short-term T-bill issuance.
- Time scale: Event-driven and structural. The structural constraint (dealer
  capacity vs Treasury market size) is persistent and grows gradually. The acute
  stress (repo rates spiking on issuance) can develop within days of a large
  auction or market event.
- Use in premarket reports: When monitoring financial stress, use repo rate vs
  SOFR/EFFR spread and 10y/30y Treasury bid-ask spreads as real-time indicators
  of dealer capacity constraint. When VIX and Treasury yields spike together, flag
  both basis trade amplification (KG-20260802-BIS-NBF-002) and dealer capacity
  constraint as compounding mechanisms. For KRE/bank sector: dealer capacity
  constraints can amplify bank funding costs via repo market stress.
- Prohibited use: Do not treat every repo rate increase as dealer capacity stress
  — can be seasonal or technical. Do not model precise timing of market dislocation
  from dealer capacity alone. Do not assume Fed will not backstop — but March 2020
  required emergency action before stabilization.
- Evidence strength: Strong for the structural observation and direction; moderate
  as a real-time signal (requires monitoring actual repo/SOFR spreads and bid-ask
  spreads). Two independent Tier-1 sources (IMF GFSR Apr 2025 + BIS AR 2025) and
  March 2020 historical validation.
- Last review date: 2026-08-03.
- Revalidation trigger: SEC/FINRA central clearing mandate for Treasury repo
  materially increases effective dealer intermediation capacity; or SLR reform
  exempts US Treasuries (briefly exempted 2020-21); or Fed resumes QE.
- Source: IMF Global Financial Stability Report, April 2025, Ch 1, pp 39–42,
  Figure 1.19 (IMF, April 2025); corroborated by BIS Annual Economic Report 2025,
  Ch I (BIS, June 2025).

---

## KG-20260803-IASB-CF-001: Amortized Cost Measurement Hides Fair Value Changes from P&L and OCI; FVOCI Routes Losses to Equity Only — Bank Bond Portfolio Unrealized Loss Risk

- Rule ID: KG-20260803-IASB-CF-001
- Domain: accounting_valuation
- Applicability: Bank and insurance company balance sheet analysis; KRE and regional bank holding review; periods when interest rates have risen and fixed-income portfolios have depreciated in value.
- Core principle: When financial assets (bonds, loan portfolios classified as "hold-to-collect") are measured at **amortized cost** (historical cost basis updated for payments, accrued interest, and impairment), fair value changes are **not recognized in either P&L or OCI**. Unrealized losses accumulate silently — invisible to the income statement and also absent from OCI. Only an impairment event (or sale) forces recognition. Under **FVOCI** (fair value through other comprehensive income), value changes hit equity (AOCI — accumulated other comprehensive income) but do NOT flow through P&L; interest income and impairment remain in P&L. Under **FVPL** (fair value through profit or loss), all value changes recognized in P&L immediately.
- Mechanism: IASB Conceptual Framework Ch 6 (§6.4–6.86) establishes that different measurement bases capture different information: historical cost is verifiable and well-understood but stale; fair value is current but may have measurement uncertainty. When the balance sheet measurement basis differs from the income statement measurement basis, the CF requires income/expenses to be split between P&L and OCI (§6.83–6.86). For amortized cost instruments (hold-to-collect business model under IFRS 9 / HTM under US GAAP ASC 320), this split means ALL fair value changes are excluded from BOTH P&L and OCI — only impairment (an exception) enters the income statement. For FVOCI instruments (hold-to-collect-and-sell model / AFS under US GAAP), fair value changes accumulate in AOCI.
- Premarket use: When KRE or any regional bank holding is under review, check: (1) What proportion of the securities portfolio is HTM/amortized cost vs AFS/FVOCI vs trading/FVPL? (2) What is the current AOCI balance (negative = cumulative unrealized losses on AFS portfolio)? (3) For large HTM portfolios: look for the fair value footnote disclosure — GAAP/IFRS require fair value disclosure even for amortized-cost portfolios. Large discrepancy between amortized cost carrying value and disclosed fair value = latent capital risk that materializes only on forced sale. The SVB/SIVB March 2023 failure pattern was the extreme version of this mechanism: large HTM portfolio with massive unrealized losses, forced to sell when deposit flight triggered liquidity crisis.
- Non-applicable environment: Companies with no significant financial instrument portfolios; banks that classify most instruments as trading/FVPL; when interest rates are stable or declining so fair value losses are not accumulating; when HTM portfolio is small relative to total capital.
- Prohibited use: Do not assume amortized cost automatically means hidden losses without checking actual fair value footnote disclosures (IFRS/GAAP require fair value disclosures for all financial instruments). Do not conflate IFRS terminology (FVOCI/FVPL) with US GAAP terminology (AFS/HTM/Trading) without accounting for recycling-rule differences. Do not claim all off-P&L fair value changes are "hidden" — AOCI is publicly disclosed in the equity section of the balance sheet.
- Time scale: Slow-building risk (interest rate cycle timescale — months to years of accumulation); rapid materialization on forced sale or confidence-driven deposit flight.
- Evidence strength: Mature methodological principle; IASB official Tier-1 standard-setter; endorsed in IFRS 9 and US GAAP ASC 320; externally validated by the 2023 regional banking crisis episode (SVB, Signature, FRC).
- Last review date: 2026-08-03.
- Revalidation trigger: Major revision to IFRS 9 or ASC 320 eliminating the amortized cost category; widespread adoption of fair value option by banks making the issue irrelevant in practice.
- Source: IASB Conceptual Framework for Financial Reporting (March 2018), Ch 6 §6.4–6.86, Table 6.1; IFRS Foundation open-access PDF; 86 pages fully read 2026-08-03.

---

## KG-20260803-IASB-CF-002: Off-Balance-Sheet Transfers Require Loss of Control; Retained First-Loss Positions and Agent Arrangements Preserve Balance Sheet Exposure

- Rule ID: KG-20260803-IASB-CF-002
- Domain: accounting_valuation
- Applicability: Bank balance sheet analysis when large off-balance-sheet commitments or securitization programs disclosed; REIT and mortgage REIT analysis; evaluating whether disclosed "off-balance-sheet" items represent real economic risk.
- Core principle: Under IASB CF, an **asset** is recognized only when an entity **controls** an economic resource — has the present ability to direct its use, obtain benefits from it, and prevent others from doing so (§4.19–4.25). **Derecognition** requires loss of control, not merely legal transfer (§5.26–5.31). If an entity transfers an asset to an SPV but **retains exposure to significant positive or negative variations** in that asset's economic benefits (e.g., via first-loss tranche, guarantee, call option, retained interest), this indicates continued control and the asset stays on the reporting entity's balance sheet. Similarly, if an asset is transferred to an agent acting on behalf of the transferor, the transferor retains control. **"Off-balance-sheet" ≠ "off-risk."**
- Mechanism: The CF control test (§4.19) requires: (1) present ability to direct the resource's use; (2) ability to obtain economic benefits; (3) ability to prevent others from directing use/obtaining benefits. If a bank securitizes loans into an SPV but retains the first-loss tranche (absorbing initial credit losses), it retains significant economic exposure and likely retains control, requiring consolidation of the SPV. The specific accounting standards (IFRS 10 — Consolidated Financial Statements; US GAAP ASC 810 — Variable Interest Entities) implement this control concept. The CF provides the conceptual foundation; the standards provide the detailed implementation rules.
- Premarket use: When MD&A or risk factor disclosures mention off-balance-sheet exposures, securitization programs, conduit facilities, CLO structures, or special-purpose entities: determine whether the entity retains first-loss protection, guarantees, residual interests, or other forms of economic exposure. If yes → the off-balance-sheet label may understate true balance sheet risk. Relevant particularly for: (a) banks with large loan securitization programs during credit-tightening periods; (b) mortgage REITs with complex agency/non-agency structures; (c) commercial real estate lenders in originate-to-distribute models.
- Non-applicable environment: True-sale securitizations where originator holds no residual interest and has no ongoing obligation; simple operational off-balance-sheet items (operating lease commitments pre-IFRS 16, purchase commitments) which are a different category from control-based consolidation.
- Prohibited use: Do not assume all disclosed off-balance-sheet items represent hidden balance sheet risk — many are genuine arm's-length transfers with no residual exposure. Do not apply CF principles without checking the actual consolidation disclosure in the financial statement notes (IFRS 10 / ASC 810 analysis is disclosed and audited). Do not conflate different types of off-balance-sheet items (loan commitments, guarantees, operating leases, securitization structures) — each has distinct recognition rules.
- Time scale: Structural/permanent consideration; becomes acute during liquidity or credit crises when off-balance-sheet vehicles face stress and are pulled back onto balance sheet.
- Evidence strength: Mature methodological principle; IASB official Tier-1 standard-setter; externally validated by 2008 GFC when conduits and SIVs (structured investment vehicles) were pulled back onto bank balance sheets when liquidity support facilities were triggered.
- Last review date: 2026-08-03.
- Revalidation trigger: Fundamental revision to IFRS 10 or ASC 810 changing the control definition; major enforcement actions establishing new precedent on what constitutes retained control for securitization purposes.
- Source: IASB Conceptual Framework for Financial Reporting (March 2018), Ch 4 §4.3–4.25, Ch 5 §5.26–5.35; IFRS Foundation open-access PDF; 86 pages fully read 2026-08-03.

---

## KG-20260803-HLZ-MP-001: Research Hygiene Gate for New Factor, Trading-Rule, and Prompt-Rule Claims

- Rule ID: KG-20260803-HLZ-MP-001
- Domain: methodology
- Applicability: Factor screens; new trading rules proposed from repeated
  postmarket failures; monthly prompt-evaluation candidates; structured-log
  mining across many windows/tickers; public factor narratives; any backtest
  with many tried variants.
- Core principle: A candidate market factor, trading rule, or prompt rule
  discovered from many tested variants, repeated report failures, or historical
  backtests is not durable knowledge until it passes multiple-testing,
  out-of-sample/holdout, publication-decay/crowding, transaction-cost/liquidity,
  point-in-time-data, and audit-chain checks.
- Mechanism: When many signals or rule variants are searched, ordinary
  single-test thresholds create false discoveries. Harvey-Liu-Zhu show that a
  factor-zoo setting requires materially higher evidence hurdles than t > 2.0,
  with published/NBER summaries indicating a new factor needs t > 3.0 and the
  extracted working-paper thresholds around 2.78-3.18 depending on hidden-test
  assumptions. McLean-Pontiff show that published predictors decay after the
  original sample and further after publication, consistent with a mix of
  statistical bias and informed trading/crowding. Replication evidence from
  Hou-Xue-Zhang further shows microcaps, equal weighting, and lax thresholds can
  inflate many anomaly returns. Therefore rule admission must separate
  statistical discovery from operational tradability and auditability.
- Supporting evidence: Harvey, Liu, Zhu (Review of Financial Studies, 2016;
  NBER WP 20592) on multiple testing in the cross-section of expected returns;
  McLean and Pontiff (Journal of Finance, 2016) on out-of-sample and
  post-publication return decay. This workspace's 2026-08-03 failure queue
  shows practical need: special-event archive gaps, approval-chain gaps,
  high-concentration trade gate failures, and fee-finalization lag are real
  repeated failures but should not be converted into standing prompt/trading
  rules from one case alone.
- Contrary evidence: Hou-Xue-Zhang (RFS 2020) supports skepticism but attributes
  much anomaly weakness to replication design, microcaps, and value weighting,
  not only publication learning. Andrew Y. Chen (2024 Federal Reserve Board
  working paper draft; author views only) argues many claimed findings may be
  true under FDR bounds, so the system must not equate "fails a stringent
  hurdle" with "economically false." Transaction-cost evidence remains a
  separate gate: a real factor can still be untradable, and a weak factor can
  still describe useful risk context.
- Applicable environment: Evaluating a proposed standing rule after repeated
  report failures; monthly prompt candidates; multi-factor screens; public
  factor and style narratives; historical backtests; structured-log mining.
- Non-applicable environment: Single verified official event time, filing fact,
  live price, Webull cash/position/order/fee field, or direct archive existence
  check. Those are factual/audit items and must be verified directly.
- Time scale: Research and prompt-governance horizon; days to months. Not an
  intraday timing tool.
- Use in premarket reports: If a thesis relies on a factor/backtest/newly
  promoted rule, briefly state whether it has FDR/OOS/holdout/cost/liquidity
  support or downgrade it to context. Do not let public factor narratives
  override current first-party facts, live prices, filings, or account risk.
- Use in postmarket and monthly evaluation: When converting failures into new
  standing rules, require non-overlapping development and holdout cases, tested
  variant count or FDR statement, direct audit-chain evidence, and no one-case
  evidence-grade upgrade.
- Prohibited use: Do not use this card as a buy, sell, short, or avoid signal.
  Do not claim every published factor is false. Do not upgrade a rule because
  one forecast worked once. Do not finalize broker fees, approvals, or archive
  statuses statistically; those require direct local or broker evidence.
- Evidence strength: Strong as methodology and governance principle; medium for
  factor-context interpretation; weak as any same-day trading signal.
- Last review date: 2026-08-03.
- Revalidation trigger: New high-quality replication evidence materially changes
  factor-zoo false discovery estimates; monthly prompt evaluation proposes a
  protected rule from fewer than five independent cases; factor screens lack
  FDR/OOS metadata; or market-structure changes materially alter transaction
  costs and arbitrage capacity.
- Source: `research/daily/2026-08-03.md`; Harvey-Liu-Zhu (RFS 2016/NBER WP
  20592); McLean-Pontiff (Journal of Finance 2016); contradiction note
  `research/contradictions/2026-08-03-research-hygiene-factor-zoo.md`.

---

## KG-20260804-BIS-B3-001: Basel III Output Floor at 72.5% Prevents IRB Capital Optimization; CET1 Ratios More Comparable Across Jurisdictions Post-2025

- Rule ID: KG-20260804-BIS-B3-001
- Domain: risk_management
- Applicability: Comparing CET1 capital adequacy across banks in different jurisdictions (especially European IRB-using banks vs US SA-constrained banks); understanding post-2022 bank capital trends; bank sector analysis including KRE comparisons.
- Core principle: Banks using internal ratings-based (IRB) approach for credit risk or internal models for market risk must hold capital against at least **72.5% of what standardized approaches (SA) would require**. Pre-Basel III finalisation, European G-SIBs using IRB could report very high CET1 ratios based on modeled RWAs that were sometimes 30-60% lower than what SA would produce. The 72.5% output floor, fully phased in by January 2027, substantially compresses this gap: `RWA_floored = max(RWA_modeled, 72.5% × RWA_SA)`.
- Mechanism: Phase-in schedule: 50% (Jan 2022), 55% (Jan 2023), 60% (Jan 2024), 65% (Jan 2025), 70% (Jan 2026), 72.5% (Jan 2027 — final). The floor applies to the aggregate RWA across credit risk, counterparty credit risk, market risk (FRTB SA), op risk (new standardized), and CVA (SA-CVA). Banks must disclose modeled vs. SA RWA during phase-in, making the gap transparent. A bank whose models produce RWA = 40% of SA RWA must now hold capital against ~72.5% × SA_RWA — near-doubling the previously modeled requirement for such banks.
- Supporting evidence: BIS BCBS d424 (December 2017), Output Floor section pp 137-139, §§1-10; Tier-1 regulatory standard.
- Contrary evidence: Some research suggests the floor may not be universally binding — large US banks were already at or near SA levels and are less affected. European banks may have raised capital proactively in anticipation. Additionally, national discretion allows supervisors to cap incremental floor-driven RWA increases during phase-in. Implementation timing varies by jurisdiction (EU vs US).
- Applicable environment: Cross-jurisdictional bank capital comparisons (especially European vs US); evaluating whether a European bank's high CET1 is genuinely equivalent to a US bank's CET1; understanding why some banks' capital ratios appear to decline as the floor phases in (not actual capital losses — floor binding constraining model benefit); bank M&A analysis comparing balance sheet strength.
- Non-applicable environment: Banks that only use SA (floor is non-binding — they already hold against 100% of SA requirement); NBFI entities; periods before Jan 2022 implementation.
- Time scale: Structural/regulatory (decades); floor fully phased in by Jan 2027; then permanent.
- Use in premarket reports: When evaluating KRE relative to European banks, note that European bank CET1 ratios have been converging toward US-comparable levels since 2022 due to output floor — previously published CET1 ratios pre-2022 for European banks systematically overstated comparability. Do not treat high European bank CET1 ratios pre-2022 as equivalent to comparable US bank ratios.
- Prohibited use: Do not use the output floor to predict specific bank capital raising needs without checking the bank's own disclosure of modeled vs. SA RWA. Do not assume 72.5% floor means all banks' ratios are now identical — significant differences remain within the SA component itself (risk weights, conservatism choices). Do not assume US and EU implementation timelines are synchronized.
- Evidence strength: Strong — official Tier-1 regulatory standard (BCBS d424); fully binding as of 2022-2027 phase-in.
- Last review date: 2026-08-04.
- Revalidation trigger: Major revision to Basel III output floor level; new BCBS guidance materially changing SA risk weights used in the floor.
- Source: BIS BCBS, Basel III: Finalising Post-Crisis Reforms, December 2017, Output Floor section pp 137-139 (BIS d424).

---

## KG-20260804-BIS-B3-002: Basel III Leverage Ratio Requires Gross SFT Exposure (Sale-Accounting Reversed); Directly Explains Why SLR Hard-Caps Dealer Repo Book Expansion

- Rule ID: KG-20260804-BIS-B3-002
- Domain: risk_management
- Applicability: Understanding why Treasury dealer capacity is constrained by SLR/leverage ratio even when net economic risk from repo is minimal; evaluating KRE and G-SIB dealer bank capacity constraints; analyzing why Fed's temporary SLR exemption in 2020-2021 mattered.
- Core principle: The Basel III leverage ratio (US implementation: Supplementary Leverage Ratio / SLR) requires Tier 1 Capital / Total Exposure Measure ≥ **3%** (G-SIBs: 3% + leverage ratio buffer = 50% × risk-weighted higher-loss absorbency buffer; e.g., a G-SIB with 2% risk-weighted buffer faces 4% minimum). The exposure measure is **gross**: (a) no netting of loans vs. deposits; (b) **SFTs (repo/reverse repo) at gross — §52 explicitly requires that banks reverse sale-accounting entries for SFTs** even if GAAP/IFRS permits sale accounting, calculating exposure as financing; (c) derivatives at SA-CCR (RC + 1.4 × PFE); (d) OBS items at SA CCFs (minimum 10% for unconditional cancellable commitments).
- Mechanism: A bank with a $500bn gross repo book (even if economically net-zero via offsetting reverses) must add ~$500bn+ to the leverage ratio exposure denominator. With a 3-4% minimum ratio, each $100bn of repo exposure requires $3-4bn of Tier 1 capital backing it. Pre-Basel III finalisation, banks could sometimes achieve repo netting under their accounting frameworks; §52 closes this loophole. This is the specific regulatory mechanism behind the dealer capacity constraint documented in KG-20260803-GFSR-TDL-002 — it is not just "Basel III constrains balance sheets" but specifically that gross repo must be counted even if economically matched. The Fed's 2020-2021 temporary SLR exemption (which excluded US Treasuries and Fed deposits from the exposure denominator) was the targeted relief that enabled dealer expansion during COVID stress.
- Supporting evidence: BIS BCBS d424 (December 2017), Leverage Ratio section pp 140-158 (esp. §52); Tier-1 regulatory standard. Corroborated by KG-20260803-GFSR-TDL-002 (IMF GFSR Apr 2025 empirical observation that dealers have shifted to equity margin lending as the market-observed consequence of this constraint).
- Contrary evidence: Some academic research argues that the leverage ratio constraint may be less binding than commonly assumed for most banks, with risk-based capital requirements being the binding constraint in practice. Additionally, sponsored repo and FICC clearing partially mitigate the gross SFT exposure by allowing netting under certain conditions. The 2021 SLR exemption expiration did NOT produce the Treasury market dislocation some feared, suggesting the constraint may have been partially offset by other factors.
- Applicable environment: When SOFR/GC repo spreads widen beyond normal seasonal ranges; when Treasury auction settlement puts sudden demand on dealer balance sheets; when Fed considers QT acceleration that increases T-bill/note supply requiring dealer intermediation; when assessing whether KRE or large bank dealer subsidiaries can absorb Treasury auction issuance; G-SIB leverage ratio buffer discussions; any analysis of the basis trade / Treasury market fragility chain.
- Non-applicable environment: Non-bank market makers (hedge funds, prop trading firms) that face no regulatory leverage ratio; foreign banks without US G-SIB status that may have lower SLR requirements; NBFI entities.
- Time scale: Structural/permanent (regulatory requirement is ongoing); becomes acute during Treasury issuance surges or market stress when dealer balance sheets are already under pressure.
- Use in premarket reports: When Treasury market stress indicators emerge (repo rate vs SOFR spread widening, Treasury bid-ask spread widening, basis trade spreads), use KG-20260804-BIS-B3-002 as the regulatory mechanism explanation for why dealer capacity is structurally constrained. Tie to KG-20260803-GFSR-TDL-002 for empirical market evidence. For KRE/bank sector: leverage ratio pressure can amplify funding cost increases.
- Prohibited use: Do not claim all large banks are constrained by leverage ratio — many have substantial Tier 1 capital cushion and are not at the binding minimum. Do not use this as a timing trigger without also checking actual SOFR/repo spreads and bid-ask indicators. Do not conflate regulatory leverage ratio (Tier 1/Exposure) with economic leverage (which can be reduced through hedges).
- Evidence strength: Strong — official Tier-1 regulatory standard (BCBS d424, §52); the gross SFT treatment is the specific mechanism; corroborated by IMF GFSR Apr 2025 market observation and BIS AR2025.
- Last review date: 2026-08-04.
- Revalidation trigger: Fed permanently exempts Treasuries/reserves from SLR; BCBS revises SFT netting rules for leverage ratio allowing economic netting; G-SIB leverage ratio buffer structure changes materially.
- Source: BIS BCBS, Basel III: Finalising Post-Crisis Reforms, December 2017, Leverage Ratio section pp 140-158 (BIS d424), especially §§20-21, §33, §52, §§9-10.

---

## KG-20260804-PFMI-001: CCP Default Waterfall and Cover-2 Requirement Structurally Reduce Bilateral Credit Risk; Explains Why Basel III Exempts CCP-Cleared OTC Derivatives from CVA Capital

- Rule ID: KG-20260804-PFMI-001
- Domain: risk_management
- Applicability: Understanding why post-GFC regulatory reform (Dodd-Frank, EMIR) mandated CCP clearing for standardized OTC derivatives; evaluating systemic risk in cleared derivatives markets; KRE and G-SIB sector analysis (clearing member default fund exposure); interpreting rare CCP stress events.
- Core principle: Systemically important CCPs must satisfy a **Cover-2** standard: maintain sufficient financial resources to absorb simultaneous default of the **two largest clearing members** (and their affiliates) in extreme but plausible conditions. The financial resource **waterfall** absorbs losses sequentially: **(1)** defaulter's initial margin (sized to cover PFE over liquidation period); **(2)** defaulter's prefunded default fund contribution; **(3)** CCP's own capital ("skin in the game"); **(4)** surviving clearing members' mutualized default fund contributions ("assessment powers"). This structure means CCP clearing converts bilateral counterparty credit risk into collectively-mutualized and pre-funded risk, which is why Basel III d424 exempts CCP-cleared trades from CVA capital requirements (see KG-20260804-BIS-B3-001 and KG-20260804-BIS-B3-002 for the regulatory capital side of this equation).
- Mechanism: In a bilateral OTC derivatives transaction, each party bears the full replacement cost if the counterparty defaults. CCP novation eliminates this: the CCP becomes buyer to every seller and seller to every buyer. The CCP's Cover-2 standard, waterfall, and daily (or intraday) variation margin collection ensure that even the simultaneous default of the two largest members is absorbed without loss to surviving participants. Systemically important CCPs (SIFMU in the US: LCH, CME, DTCC) are assessed against PFMI standards by the Fed, CFTC, and SEC. A CCP that meets PFMI requirements qualifies as a "Qualifying CCP" (QCCP) under Basel III, entitling clearing members to preferential capital treatment on their CCP exposures. The regulatory chain is: PFMI → QCCP designation → Basel III CVA exemption → bank incentive to clear OTC derivatives centrally.
- Supporting evidence: BIS CPMI-IOSCO PFMI (April 2012), Principle 4 (Credit risk, pp. 36-45), Principle 6 (Margin, pp. 50-56), Principle 13 (Default rules), Principle 14 (Segregation/portability); Tier-1 joint BIS+IOSCO standard. Corroborated by BIS Basel III d424 (December 2017), CVA section — CCP exemption presupposes PFMI compliance. Also corroborated by FSB mandate for CCP clearing of standardized OTC derivatives (Pittsburgh G20 commitment, 2009).
- Contrary evidence: Some academic research (eg. Duffie and Zhu 2011) showed that CCP clearing can reduce systemic risk for standardized products but may *increase* aggregate collateral requirements and introduce wrong-way risk if the clearing member and the reference entity are correlated. Additionally, multi-CCP fragmentation (different CCPs for different products) can prevent netting benefits that bilateral networks with common exposures could achieve. CCP itself can fail — a CCP failure would be a tail-risk systemic event not covered by the waterfall.
- Applicable environment: Evaluating systemic risk implications when a large clearing member faces stress (eg. Credit Suisse March 2023, LME nickel March 2022); understanding why Basel III incentivized CCP clearing; KRE sector analysis when assessing bank exposure to CCP default fund contributions; interpreting market stress where cleared OTC derivatives markets are involved.
- Non-applicable environment: Exchange-listed equity and ETF trading where DTCC/NSCC guarantee is automatic background infrastructure; bilateral uncleared derivatives (exempted sovereign, end-user); equity securities (which settle under DvP regime, not CCP derivatives waterfall).
- Time scale: Structural/regulatory (CCP clearing mandate is permanent post-GFC; PFMI standards are ongoing); default waterfall is a standing structural feature.
- Use in premarket reports: When assessing whether a financial sector stress event involves derivatives clearing chains, cite PFMI waterfall to explain why the risk is structured and mutualized rather than solely bilateral. When evaluating KRE stress (clearing member banks): note that banks contribute to CCP default funds; in extreme events, these can be "called" (assessment powers). For KRE analysis: clearing member banks' CCP default fund exposure is typically small relative to total capital and is secured by initial margin, but it represents a contingent liability.
- Prohibited use: Do not claim CCP clearing eliminates all counterparty risk — CCPs themselves can fail (eg. if more than Cover-2 members default simultaneously); residual tail risk exists. Do not assume all cleared derivatives trades are at a QCCP — verify QCCP designation status. Do not conflate the CCP default waterfall with individual clearing member default margin calculations visible in daily risk reports.
- Evidence strength: Strong — official Tier-1 joint regulatory standard (CPMI-IOSCO PFMI); implemented globally; corroborated by Basel III CVA capital treatment (BIS d424) and FSB clearing mandate.
- Last review date: 2026-08-04.
- Revalidation trigger: PFMI materially revised; QCCP definition or CVA capital treatment in Basel III changes; major SIFMU (LCH, CME, DTCC) fails or is placed into recovery.
- Source: BIS CPMI-IOSCO, Principles for Financial Market Infrastructures, April 2012, Principles 4, 6, 13, 14 (BIS cpmi/publ/d101a.pdf).

---

## KG-20260805-FCIC-001: CDS Without Capital Reserves and OTC Derivatives Opacity Were the Root Mechanisms of AIG-Style Systemic Risk; Empirical Basis for Dodd-Frank/PFMI Central Clearing Mandate

- Rule ID: KG-20260805-FCIC-001
- Domain: derivatives
- Applicability: Understanding why post-GFC regulatory reform (Dodd-Frank Title VII, EMIR) mandated CCP clearing for standardized OTC derivatives; interpreting CDS spread widening on major financial institutions as collateral trigger signal; evaluating KRE/G-SIB exposure to derivatives counterparty risk; contextualizing PFMI Cover-2 and Basel III CVA exemption requirements.
- Core principle: The FCIC (US government investigation with subpoena authority) documents the definitive empirical case for why unregulated bilateral OTC CDS without capital reserves created systemic risk. AIG Financial Products wrote $440B+ in CDS protection on CDO tranches earning periodic premiums without posting capital reserves (CDS escaped insurance regulation under CFMA 2000). CDS contracts required AIG to post cash collateral equal to mark-to-market losses on referenced CDO tranches (not just on actual credit events). When CDO valuations fell 2007-2008, collateral demands reached $14.5B by August 2008. S&P downgrading AIG 3 notches in September 2008 triggered rating-linked collateral clauses → an additional $14B immediately → Goldman alone demanded $8.4B → AIG insolvent within days. The Fed ultimately committed >$182B. Simultaneously: AIG's $2.7T OTC derivatives book was invisible to regulators because bilateral OTC required no trade reporting. Regulators were "straining to understand an unknown battlefield" (FCIC conclusions). European banks had bought AIG CDS to reduce Basel regulatory capital requirements; AIG failure would have triggered ~$30B in European bank capital needs. Regulatory chain confirmed by congressional response: AIG failure → Dodd-Frank Title VII → CCP clearing mandate → PFMI standards (KG-20260804-PFMI-001) → Basel III QCCP CVA exemption (KG-20260804-BIS-B3-001).
- Mechanism: Three interlocking failures: (1) No capital reserves: AIG sold CDS protection earning premiums but posted no capital, creating an asymmetric payoff (small upside, enormous tail risk); insurance regulators had no authority under CFMA 2000. (2) Mark-to-market collateral posting: CDS contracts had Credit Support Annexes (CSAs) requiring posting of cash collateral based on mark-to-market losses on referenced CDOs, not just on actual defaults — so falling CDO prices (even without default) triggered cash demands. (3) OTC opacity: no exchange reporting, counterparty exposure invisible; when AIG's failure became possible, "every bank and dealer has exposure to them" (NY Fed 2008) but nobody knew the magnitude. This combination is WHY CCP clearing solves the problem: CCPs require initial margin (capital reserves) from day one, collect variation margin daily (PFMI Cover-2), and provide transparent position reporting. Dodd-Frank mandated CCPs for standardized OTC derivatives precisely because the AIG model proved bilateral OTC unworkable at systemic scale.
- Supporting evidence: FCIC Report (2011), Chapter 3 (CDS mechanics, pp. 77-79), Chapter 8 (AIG within CDO machine, pp. 169-171), Chapter 19 (AIG bailout, pp. 372-395), Chapter 20 (AIG counterparty payments, pp. 405-408), Conclusions pp. 24-25. US government investigation with subpoena authority; cross-confirmed by PFMI (BIS/IOSCO Tier-1, KG-20260804-PFMI-001) which specifies the regulatory solution; cross-confirmed by LTCM case (Chapter 4, pp. 84-87): $1.25T notional derivatives, $2.2B equity, near-collapse when correlations spiked (1998 precursor of same mechanism). AIG counterparty payments at par (Goldman $8.4B, Deutsche $8.5B, SocGen $16.5B, Barclays $7B) documented with specific figures.
- Contrary evidence: Some AIG defenders argued mark-to-market collateral calls were unjustified because the underlying mortgages had not yet defaulted (dispute with Goldman over marks in 2007). The FCIC acknowledged that some collateral demands may have been aggressive; however, the structural problem (no reserves, no CCP, OTC opacity) remains valid regardless of specific valuation disputes. Post-crisis critique: Dodd-Frank clearing mandates may have concentrated risk at CCPs (solving bilateral opacity but creating new TBTF-style systemic concentration); however, PFMI Cover-2 requirements address this.
- Applicable environment: Evaluating major financial institution stress where CDS spreads widen sharply (CDS spread > 300 bps on large bank or insurer = market pricing in serious failure risk); assessing KRE/bank sector when large counterparties are under stress (KRE clearing member banks are exposed through CCP default funds, but this is structurally very different from bilateral AIG-style exposure); interpreting Dodd-Frank clearing mandates and PFMI compliance as risk-reduction infrastructure; any analysis where derivatives counterparty exposure is discussed.
- Non-applicable environment: Exchange-listed equity options and futures (already cleared through DTCC/CME since before Dodd-Frank); standardized interest rate swaps and CDS index products (CDX, iTraxx) cleared post-Dodd-Frank through LCH/CME — PFMI waterfall applies; US regional bank sector in normal conditions (KRE constituents are clearing members with structured CCP protections, not uncleared CDS sellers at AIG's scale).
- Time scale: Historical/structural (documents why 2007-2010 regulatory response was designed as it was); relevant when assessing current OTC derivatives risk (residual bilateral uncleared OTC still exists for customized/non-standardized products).
- Use in premarket reports: When discussing major financial institution stress involving derivatives (eg. hedge fund blowup, large bank CDS spread widening, commodity trading firm margin calls), cite FCIC-001 mechanism to explain why OTC derivatives exposure can be larger and more interconnected than publicly disclosed. When assessing KRE sector exposure: note that CCP clearing (post-Dodd-Frank) has reduced but not eliminated counterparty risk; CCP default fund contributions remain a contingent liability (see KG-20260804-PFMI-001). When interpreting PFMI compliance news for SIFMU (LCH, CME, DTCC), reference FCIC-001 as the empirical motivation for the PFMI standards.
- Prohibited use: Do not claim current financial system has the same OTC opacity as pre-2010; Dodd-Frank trade repositories and CCP clearing mandates have significantly reduced (though not eliminated) bilateral OTC opacity for standardized products. Do not use FCIC evidence to claim CDS markets are inherently dangerous; exchange-cleared or CCP-cleared CDS (CDX, iTraxx) with PFMI-compliant waterfall is structurally very different from AIG's uncleared bilateral book. Do not conflate 'large notional OTC derivatives' with net economic exposure — LTCM's $1.25T notional vs. $2.2B equity illustrates that notional can overstate gross exposure but can understate crisis fragility when correlations spike and close-out netting fails.
- Evidence strength: Strong — US government investigation with subpoena authority and full access to internal documents; specific dollar amounts and timelines documented; legislative/regulatory response (Dodd-Frank Title VII, PFMI) confirms the causal diagnosis; cross-confirmed by LTCM precedent in same document.
- Last review date: 2026-08-05.
- Revalidation trigger: Major revision of Dodd-Frank Title VII clearing mandates; significant change in PFMI standards; new empirical study revising the causal chain from OTC opacity to systemic risk; major CCP failure that changes assessment of whether clearing mandates solved the problem.
- Source: Financial Crisis Inquiry Commission, "The Financial Crisis Inquiry Report," January 2011. US government public domain publication. Stanford Law mirror: fcic-static.law.stanford.edu/cdn_media/fcic-reports/fcic_final_report_full.pdf. Local: research/books/fcic_final_report_2011.pdf (662 pages, 4.9 MB, SHA-256: f22f0961f686e866d8b358154734e7d814cf06ee1af0ed6f52693f5c6d12c4ff).

---

## KG-20260805-CGFS44-001: LDI Duration Matching — Institutional Fixed Income Portfolios Close the Duration Gap via Interest Rate Swap Overlays; Long-End Rate Moves Generate Predictable Structural Hedging Demand

- Rule ID: KG-20260805-CGFS44-001
- Domain: portfolio_construction
- Applicability: Interpreting large-scale institutional demand for long-duration government bonds; explaining why long-end yields face structural demand that compresses term premiums; understanding KRE/bank sector risk in sustained low-rate environments (insurer profitability channel); contextualizing unusual long-end yield moves and preferred habitat effects.
- Core principle: Life insurance companies and pension funds face a structural **duration gap**: their liabilities (pension payments, annuity cash flows) have modified durations of 20-40 years, while bond markets rarely provide securities with matching duration (practical bond market ceiling ~15 years). **Liability-Driven Investment (LDI)** strategies close this gap by using **interest rate swap overlays** — receiving fixed, paying floating (LIBOR/SOFR) — to synthetically extend effective asset duration beyond what the physical bond portfolio can provide. The $40 trillion life insurance and pension fund sector across OECD markets uses this approach at scale. LDI creates a structural demand for long-duration government bonds and interest rate swaps that is predictable and recurring rather than tactical: it is driven by the accounting/regulatory requirement to match asset and liability interest rate sensitivity, not by short-term market views. Two LDI variants: **(1) Duration matching (partial immunisation):** align modified duration of asset portfolio with modified duration of liability portfolio; reduces but does not eliminate interest rate risk; **(2) Cash flow matching (complete immunisation):** match specific cash flows from assets to specific liability payment dates; eliminates interest rate risk but requires exact cash flow timing — difficult for longevity-uncertain pension/insurance liabilities.
- Mechanism: Modified duration of liabilities (D_L) typically exceeds modified duration of assets (D_A): D_L ~20-40 years vs. D_A (physical bond portfolio) ~10-15 years. The duration gap = D_L − D_A creates an interest rate sensitivity mismatch: when rates fall, the present value of liabilities rises *more* than the present value of assets → funding deficit emerges. LDI closes the gap by: **(a)** lengthening asset duration via long-maturity government bonds (30-year Treasuries, Gilts, Bunds); **(b)** interest rate swap overlay: the institution enters a receive-fixed 30-year interest rate swap, receiving a fixed coupon and paying floating LIBOR/SOFR. This synthetically adds fixed-income duration without additional bond purchases. Inflation-linked liabilities require inflation swaps. The swap overlay creates a **positive feedback loop** during long-end rallies: rate declines increase PV of liabilities → funding gap widens → institutions add more swap hedging demand → more buying pressure on long-end fixed-rate instruments. At end-2009, OECD pension funds and life insurers held 28-80% of assets in fixed income depending on jurisdiction (Table 2 in CGFS44: Netherlands pension 60%, Japan life 80%, US pension 28%, UK pension 40%). Solvency II capital charges (effective 2016) add a regulatory overlay: EEA government bonds carry 0% SCR (Solvency Capital Requirement) while equity carries 35-40% — further biasing the institutional fixed income allocation toward government bonds.
- Supporting evidence: BIS Committee on the Global Financial System (CGFS) Papers No. 44, July 2011; survey of 60+ major insurance companies and pension funds across US, UK, EUR, Japan, and other major markets; Table 2 (10-country asset allocation), Sections 2.3 (ALM), 4.4 (LDI derivatives strategy), 5.2.3 (LDI financial system implications); also Section 5.2.4 (procyclicality via LDI hedging demand). CGFS is the BIS committee of central bank research directors — highest Tier-1 classification. Source cross-confirmed by general market knowledge of LDI use (UK pension LDI crisis 2022 demonstrated scale of LDI swap market in practice; Bank of England emergency gilt purchases were triggered by LDI margin calls on pension funds).
- Contrary evidence: (1) Post-2022 rate spike: the sharp rise in long-end rates 2021-2023 created significant losses for LDI-heavy pension funds (UK gilt crisis September-October 2022; US pension funding improved while asset values fell). In rising-rate environments, LDI increases losses relative to unhedged portfolios. (2) Shift toward DC plans: defined contribution pension plans, where investment risk is borne by employees, do not require LDI — the trend toward DC reduces the share of assets subject to LDI. (3) Liability-matching alternatives: some insurers use buy-and-maintain credit portfolios (not swaps) to match liability cash flows, reducing dependence on derivative overlays. (4) Data age: CGFS44 data is end-2009, before Solvency II implementation (2016) and the post-2022 rate spike shifted allocations substantially.
- Applicable environment: (1) Long-end yield curve moves (particularly UST 10-30Y and EUR 10-30Y rates) where institutional LDI hedging demand creates directional flow; long-end rate declines typically worsen funding ratios → more hedging demand; (2) KRE or bank sector analysis where sustained low rates affect insurer/pension fund profitability and product pricing (negative margin risk per Japanese 1997-2001 precedent); (3) Interpreting large-scale demand for long-duration government bonds (flat/inverted long end of curve) where preferred habitat from LDI mechanics provides structural buying; (4) Understanding why institutional investors absorb long-maturity bonds at seemingly low yields.
- Non-applicable environment: (1) US domestic equity investing in normal conditions — LDI flow is slow-moving strategic rebalancing, not intraday or week-by-week; (2) Short-duration fixed income or money market analysis — LDI mechanism operates at 10-30Y duration; (3) Predicting intraday price moves — LDI execution is scheduled asset-liability management, not reactive to intraday data; (4) DC pension plan analysis — no LDI at plan level; (5) Japanese insurance market pre-2005 — cross-shareholding accounting/regulatory structure differed substantially.
- Time scale: Structural / multi-year (LDI strategies are set by annual or triennial asset-liability reviews, not by daily market moves; immediate tactical impact only in funding-ratio crisis events like UK 2022).
- Use in premarket reports: (1) When long-end rates decline significantly (UST 30Y down >15 bps): mention structural LDI hedging demand as a mechanism that reinforces long-end rate moves (not just a flow observation but a structural feedback loop); (2) When analyzing KRE sector: sustained low rates reduce insurer profitability and product pricing ability — note Japanese precedent as a tail risk context for 5-10 year horizon; (3) When interpreting unusual demand for long-duration Treasuries or swaps: LDI mechanics explain preferred habitat at 20-30Y that is not driven by near-term total return expectations; (4) During potential stress: if pension fund or insurer funding ratios deteriorate sharply (equity+bond simultaneous decline as in 2022 UK), LDI collateral calls can force rapid long-duration bond selling — cite CGFS44-003 (candidate) for the doom loop mechanism.
- Prohibited use: (1) Do not predict specific insurer or pension fund trades without verifying current LDI ratios and the specific regulatory regime applicable to them; (2) Do not assume all institutional fixed income buying is LDI-driven — credit spread carry, yield enhancement, and index replication are also significant motives; (3) Do not conflate European Solvency II capital incentives with US NAIC RBC or Japanese FSA frameworks — capital charges differ significantly by jurisdiction; (4) Do not extrapolate 2009 asset allocation data as current — Solvency II implementation (2016), low-rate experience (2013-2021), and post-2022 rate spike have shifted allocations substantially.
- Evidence strength: Strong — official Tier-1 BIS/CGFS committee report based on 60+ institutional investor interviews; mechanism well-established in asset-liability management literature; 2022 UK LDI crisis provides out-of-sample episode consistent with mechanism.
- Last review date: 2026-08-05.
- Revalidation trigger: Major change in US ERISA pension funding rules; Solvency II fundamental revision; significant shift in long-end yield curve structure altering LDI economics; major insurer/pension fund failure due to duration gap mismanagement; second Tier-1 source quantifying current LDI swap notional outstanding.
- Source: Committee on the Global Financial System (CGFS), "Fixed income strategies of insurance companies and pension funds," BIS CGFS Papers No. 44, July 2011. Free open-access PDF at bis.org/publ/cgfs44.pdf. Local: research/books/bis_cgfs44_2011.pdf (67 pages, 398 KB, SHA-256: 40ef63cae9e2d25707e4de619b89613f31763daa88e58c05bc48d3cfad8da7e6).

---

## KG-20260805-AUDIT-CHAIN-001: Audit-Chain Evidence Binding for Local Market Reports

- Rule ID: KG-20260805-AUDIT-CHAIN-001
- Domain: system_engineering
- Applicability: Account-baseline, order-lifecycle, special-event-monitoring,
  structured-log, approval-chain, and fee-finalization audits in this workspace.
- Core principle: A local market-report system should not treat an account
  baseline, order audit, special-event review, or realized P/L as complete
  merely because one artifact exists. The relevant artifacts must be linked by
  compatible scope and stable local IDs: portfolio account, order account,
  report archive, structured JSONL record, order draft, user approval, broker
  execution receipt, and broker-final or explicitly provisional fee status.
- Mechanism: NIST log-management guidance treats logs as a managed process
  requiring infrastructure, review, protection, and retention rather than raw
  collection alone. SEC CAT architecture creates auditability by linking order
  receipt/origination, routing, execution, modification, and cancellation events
  through identifiers. SEC broker-dealer books-and-records rules require
  account/order identity, timing, terms, execution/cancellation state, and
  preservation. Applied locally: a Webull fill proves execution but not local
  approval-chain completeness; a special-event collector proves data capture but
  not user-visible report delivery; a portfolio snapshot proves selected account
  scope only unless reconciled with the order snapshot; empty broker fee arrays
  require provisional cost status.
- Supporting evidence: NIST SP 800-92 "Guide to Computer Security Log
  Management" (2006); SEC Rule 613 / Consolidated Audit Trail overview and 2026
  CAT concept release; current eCFR/SEC materials for Exchange Act Rules 17a-3
  and 17a-4. Local stress cases: 2026-08-05 Webull portfolio/order account
  mismatch; 2026-08-04 AMD/SPCX/ANET fills without complete local
  draft/math/approval chain; 2026-08-03 through 2026-08-05 special-event
  collector/report mismatch; repeated Webull fee arrays remaining empty after
  filled sells.
- Contrary evidence: CAT-style linkage is costly and privacy-sensitive; local
  implementation must use minimal redacted/stable IDs and must not store tokens,
  credentials, or full private account identifiers. NIST guidance is not a
  trading alpha standard. SEC broker-dealer rules apply to broker-dealers, not
  to this workspace; the workspace borrows the audit principle and must not
  claim regulatory compliance. More logs can create false confidence if link
  status is not reviewed.
- Applicable environment: (1) Webull portfolio and order sync outputs disagree
  on account ID, account type, selected account, or consolidation scope; (2)
  Webull shows an actual filled order but local files lack matching order draft,
  math block, approval message/time, or execution receipt; (3)
  `reports/special-event-monitoring/YYYY-MM-DD.jsonl` exists without a matching
  user-visible intraday Markdown/structured report; (4) structured JSONL fields
  conflict with Markdown archives; (5) broker fees are missing and P/L is
  provisional.
- Non-applicable environment: Same-day market direction, ticker selection,
  standalone buy/sell/hold/avoid decisions, or single verified official
  filing/event facts that do not depend on local account or order state.
- Time scale: Standing operational guardrail; active in every premarket,
  intraday, postmarket, Webull fee review, and monthly prompt-evaluation audit.
- Use in premarket reports: Degrade account baseline when account IDs or
  snapshot scopes conflict; do not rank cash/holdings as verified consolidated
  facts until the scripts agree or a user-confirmed account baseline is present.
- Use in intraday and special-event reports: Mark data-only collectors as
  collection evidence, not complete user-visible reviews, unless a matching
  Markdown/structured intraday report exists or a documented skip/manual-review
  warning is written.
- Use in postmarket reports: Require linked order draft, approval, execution,
  account scope, archive, and fee-status fields before calling an order audit
  complete. Broker fills remain authoritative execution records, but local
  approval-chain completeness is unverified without matching local artifacts.
- Use in Webull fee review: Keep `broker_reported_fees`, `estimated_fees`, and
  `fee_status` separate; never finalize realized P/L from provisional estimates.
- Use in monthly prompt evaluation: Add canaries for account mismatch,
  fill-without-local-approval-chain, collector/report mismatch, and
  provisional-vs-final fee wording.
- Prohibited use: Do not use this rule as a market signal. Do not store raw
  tokens, credentials, full private account IDs, or unnecessary personal data.
  Do not recreate a missing prediction after the fact; write
  `documented_failure` or `failed_backfilled_audit` status. Do not treat a
  broker fill as proof that the local research system preserved approval. Do
  not finalize fees from estimates.
- Evidence strength: Strong for system-engineering/audit-process use; no
  evidence strength for directional trading.
- Last review date: 2026-08-05.
- Revalidation trigger: Webull sync scripts output a verified multi-account
  consolidated baseline; structured schema adds mandatory lifecycle-link
  validation; CAT/SEC recordkeeping rules materially change; privacy/storage
  review requires fewer retained link fields.
- Source: `research/daily/2026-08-05.md`;
  `research/knowledge/cards/KG-20260805-AUDIT-CHAIN-001.json`;
  NIST SP 800-92 https://csrc.nist.gov/pubs/sp/800/92/final ;
  SEC Rule 613/CAT https://www.sec.gov/about/divisions-offices/division-trading-markets/rule-613-consolidated-audit-trail ;
  Federal Register CAT concept release
  https://www.federalregister.gov/documents/2026/04/20/2026-07651/concept-release-on-consolidated-audit-trail-and-other-audit-trails-and-data-sources ;
  eCFR Rule 17a-3 and Rule 17a-4.

---

## KG-20260806-CGFS52-001: Bond Market Liquidity Bifurcation — Dealer Capacity Constraints Drive Structural Fragmentation Between Sovereign Benchmarks and Corporate/Off-the-Run Securities; Faster and Deeper Dealer Retrenchment in Stress Episodes

- Rule ID: KG-20260806-CGFS52-001
- Domain: market_microstructure
- Applicability: Bond ETF analysis (LQD, HYG corporate bond ETFs more vulnerable
  than TLT sovereign ETF — bifurcation is between asset classes); interpreting
  simultaneous VIX spike + Treasury yield spike + credit spread widening as
  consistent with dealer inventory retrenchment; KRE/bank sector stress events
  where dealer bank subsidiary balance sheet contraction coincides with AFS bond
  mark-to-market losses (SVB-type risk chain); primary dealer net position data
  (NY Fed weekly) as leading indicator of dealer capacity stress; monetary policy
  normalization events (rate hikes, taper announcements) that trigger correlated
  bond fund outflows.
- Core principle: Bond market liquidity is structurally bifurcated between
  most-liquid/on-the-run sovereign benchmark instruments (liquidity recovered
  to near pre-crisis levels by 2014) and less-liquid instruments including
  corporate bonds and off-the-run securities (bid-ask spreads remained wider;
  turnover ratios collapsed — share of US corporate bonds with ≥50% annual
  turnover fell from 20% to <5%). During stress episodes, dealer retrenchment
  is faster and deeper than pre-crisis because VaR measures give more weight to
  recent observations: volatility rises → VaR rises faster → dealers reduce
  exposures more aggressively → wider bid-ask spreads → more volatility
  (feedback loop).
- Mechanism: Market-maker P&L: revenues (bid-ask spread + ancillary services)
  minus costs (inventory VaR + capital cost + funding cost + hedging cost +
  operational cost). Post-crisis regulatory constraints compress dealer capacity:
  (1) Leverage ratio (Basel III §52: gross SFT exposure, no netting) — #1
  regulatory impact on market-making per 84-institution CGFS survey covering 40
  advanced economy and 44 emerging market institutions — constrains high-volume
  sovereign bond repo and other large-gross/low-margin activities; (2) Capital
  requirements (Basel 2.5 Incremental Risk Charge + stressed VaR) increase
  inventory costs specifically for traded credit; (3) LCR reallocates inventory
  toward HQLA, disadvantaging corporate bonds. Bid-ask spread = expected
  inventory VaR + adverse selection risk (Glosten-Milgrom 1985: probability
  quote is hit by more-informed trader) + capital and funding costs. Corporate
  bonds require warehousing (longer search for offsetting demand) → higher
  inventory cost → worse capital-adjusted return → dealer exit or service
  reduction. Sovereign benchmarks: high turnover, hedgeable with liquid
  futures/swaps, acceptable cost-capital ratio → retain dealer commitment (at
  reduced capacity vs pre-crisis). Primary Dealer (PD) system: sovereign
  market-making obligations in exchange for preferential central bank facility
  access + auction access; PD net and gross fixed income positions declined
  sharply in May-July 2013 episode (Box 3): 10Y UST yield rose 1.63% → 2.74%;
  dealers reduced inventory confirming retrenchment mechanism. OTC bond markets
  are quote-driven (request-for-quote/RFQ model); dealers are the sole liquidity
  providers; this is structurally different from exchange-based order-driven
  equity markets where multiple participants provide two-way liquidity
  continuously.
- Supporting evidence: BIS CGFS Papers No. 52 (November 2014) — Committee on
  the Global Financial System, 84-institution market-making survey (40 AE + 44
  EM), cross-asset liquidity metrics (Graphs 3/4/5), dealer inventory data,
  Graph 6 turnover ratio collapse, May-July 2013 case study (Box 3), regulatory
  drivers survey (Table 1: >50% attributed at least moderate decline to leverage
  ratio). Corroborated by: KG-20260803-GFSR-TDL-002 (IMF Tier-1 April 2025:
  Treasury market grown 500%+ since GFC; dealer balance sheets constrained by
  SLR; repo rates increasingly sensitive to issuance); KG-20260804-BIS-B3-002
  (BIS Basel III d424 Tier-1: §52 gross SFT exposure treatment — the specific
  mechanism behind leverage-ratio dealer constraint). Two independent Tier-1
  sources confirm the mechanism.
- Contrary evidence: Non-bank market-makers (Citadel Securities, Virtu, Jane
  Street) have partially filled the dealer gap in standardized instruments and
  electronic trading platforms (MarketAxess, Tradeweb) have increased corporate
  bond electronic trading. Sovereign benchmark liquidity substantially recovered
  by 2014. Total effect may be smaller in most-liquid segments of corporate
  bond market by 2025 than 2014 data indicates.
- Applicable environment: (1) Corporate bond ETF monitoring (LQD, HYG) during
  rate volatility or credit stress events; (2) Interpreting simultaneous VIX +
  yield + spread spike as dealer retrenchment signature; (3) KRE stress review
  where dealer subsidiary balance sheet reduction is observable; (4) Primary
  dealer net position (NY Fed) data interpretation; (5) Fixed income market
  functioning assessment during monetary policy normalization.
- Non-applicable environment: Exchange-listed equity markets (order-driven, not
  quote-driven; multiple liquidity providers; dealer inventory model does not
  apply); most-liquid on-the-run UST 2/5/10/30Y benchmarks in normal
  conditions; intraday short-term equity ETF trading (SPY, QQQ); directional
  bond price forecasting without corroborating observable evidence.
- Time scale: Structural mechanism (multi-year regime since post-crisis
  regulatory implementation 2012-2015); retrenchment dynamic operates intraday
  to weekly during stress episodes.
- Use in premarket reports: When monitoring Treasury market stress, use repo
  rate vs SOFR/EFFR spread and 10Y/30Y bid-ask spreads as real-time indicators.
  When VIX and yields spike simultaneously, apply this card alongside
  KG-20260802-BIS-NBF-002 (NBFI basis trade fragility) — complementary
  mechanisms for the same stress episode. For bond ETF analysis: flag LQD/HYG
  ETF premium/discount to NAV widening as consistent with authorized participant
  constraints in underlying OTC market. For KRE: dealer bank subsidiary
  inventory reduction can cause AFS mark-to-market losses → AOCI pressure.
- Prohibited use: Do not claim all bond markets are equally impaired — sovereign
  benchmarks largely recovered; bifurcation is between asset classes. Do not use
  as directional bond price signal without corroborating observable evidence
  (primary dealer data, fund flow data, actual spread widening). Do not assume
  non-bank market-makers have not partially filled the dealer gap in standardized
  instruments — they have in some segments as of 2025. Do not treat 2014
  inventory and turnover data as current without updating from primary dealer
  data (NY Fed) or BIS.
- Evidence strength: Strong (Tier-1 BIS CGFS committee report + 84-institution
  survey + May-July 2013 OOS case study + two independent Tier-1 source
  corroboration from IMF GFSR April 2025 and BIS Basel III d424).
- Last review date: 2026-08-06.
- Revalidation trigger: Second Tier-1 study confirming corporate bond bid-ask
  spreads or dealer inventories materially recovered from post-crisis impairment;
  major structural change to Basel III leverage ratio treatment; Federal Reserve
  or BIS report showing primary dealer inventories recovered relative to
  outstanding bond supply; major non-bank market-maker study showing effective
  replacement of dealer intermediation in corporate bonds.
- Source: Committee on the Global Financial System (CGFS), "Market-making and
  proprietary trading: industry trends, drivers and policy implications," BIS
  CGFS Papers No. 52, November 2014. https://www.bis.org/publ/cgfs52.pdf.
  Local: research/books/bis_cgfs52_2014.pdf (59 pages, 567 KB, SHA-256:
  6d18d350d2c487f5fd24f99f342d6bca3317e82db880fd7891fefd47d6e1a1bb).

---

## KG-20260806-CGFS55-001: Fixed Income Market Liquidity Hidden Deterioration — Quantity Metrics (Depth, Price Impact) Reveal Structural Fragility Behind Stable Bid-Ask Spreads; PTF Liquidity Categorically Different From Dealer Liquidity in Stress

- Rule ID: KG-20260806-CGFS55-001
- Domain: market_microstructure
- Applicability: Any fixed income market fragility assessment; bond ETF premium/discount
  to NAV monitoring; US Treasury or sovereign bond flash event analysis; KRE stress episodes
  involving dealer bank VaR-duration amplifier; evaluating whether PTF/HFT presence in
  sovereign bond markets substitutes adequately for dealer large-trade capacity (it does not).
- Core principle: The main margin of adjustment in fixed income market liquidity is through
  QUANTITIES, not PRICES. Bid-ask spreads (price-based metrics) remain near pre-crisis levels
  for sovereign benchmark bonds, but quantity-based metrics reveal severe structural
  deterioration: quoted depth for 2-year US Treasury notes declined by MORE THAN 65% since
  peak in early 2013; price impact of large trades has increased significantly; US primary
  dealer net Treasury positions fell ~80% since 2013; average transaction sizes declined.
  Bid-ask spread alone is an INSUFFICIENT and LAGGING indicator of fixed income fragility.
  PTFs (principal trading firms) provide narrow spreads through instantaneous order-flow-based
  quoting but do not commit to warehousing large inventory. In stress (Oct 15, 2014 flash
  rally): PTFs cut depth while dealers widened spreads; BOTH became net aggressive sellers
  as prices fell simultaneously. "Markets where non-dealer market-makers play a major role
  seem to be at LEAST AS SUSCEPTIBLE to abrupt bouts of liquidity deterioration as markets
  that rely on dealer intermediation."
- Mechanism: Two mechanisms extending CGFS52-001: (1) QUANTITY-BEFORE-PRICE
  DETERIORATION: Market-makers first reduce QUANTITIES (depth, inventory) before widening
  spreads because widening spreads signals poor market quality and loses clients; in acute
  stress, both happen simultaneously. Quoted depth is the EARLY WARNING signal: when depth
  falls while spreads look tight, the market is approaching a fragility threshold. (2) PTF
  LIQUIDITY ASYMMETRY: PTFs provide tight spreads via instantaneous algorithmic quoting
  based on order flow information acquisition, not commitment to large-trade capacity.
  PTF-provided spreads signal informational speed, not willingness to absorb inventory.
  In the Oct 15, 2014 flash rally: PTFs maintained tight spreads but DECISIVELY CUT BACK
  depth; bank-dealers WIDENED spreads (both pulled back from large-trade accommodation);
  self-trading surged (~$160M net buyer imbalance from self-trades in 12 minutes).
  Self-reinforcing dynamics: individual dealer withdrawal → fewer intermediation alternatives
  → higher cost for remaining dealers → more withdrawal; total liquidity decline MORE THAN
  PROPORTIONAL to initial trigger. VaR-duration amplifier (from CGFS52): at high duration
  levels, small yield increases → large mark-to-market losses → VaR rise → dealer retrenchment
  → wider bid-ask → more volatility.
- Supporting evidence: BIS CGFS Papers No. 55 (January 2016) — Study Group of 25 central
  banks chaired by Bank of France (Denis Beau); direct follow-up to CGFS52; Box 4 survey of
  40+ market-making firms from 11 jurisdictions; Oct 15, 2014 US Treasury flash rally case
  study (US Joint Staff Report, five agencies: Treasury, Fed, FRBNY, SEC, CFTC); May 2015
  German bund yield reversal case study; Graph 2 (UST depth -65%); Graph 3 (dealer inventory
  trends); Graph 4 (bond fund $7.4T AUM). Corroborated by: KG-20260806-CGFS52-001 (BIS 2014,
  same domain, independent Study Group); KG-20260803-GFSR-TDL-002 (IMF Tier-1); IMF GFSR
  Oct 2015 referenced within CGFS55 as independent confirmation.
- Contrary evidence: Electronic trading platforms (MarketAxess, Tradeweb, Bloomberg) have
  continued to grow post-2016 and now cover a wider range of bond maturities and credit
  qualities, potentially partially restoring depth in some segments. Some PTF participation
  in corporate bonds has grown since 2016. Depth and inventory data from 2016 may not reflect
  current 2025 market structure without checking NY Fed primary dealer data.
- Applicable environment: (1) Fixed income market fragility check: monitor depth AND
  price impact, not just bid-ask spreads; depth collapse with tight spreads = early fragility
  signal. (2) Bond ETF analysis (LQD, HYG, TLT): depth in underlying OTC bonds = key
  signal for authorized participant redemption cost and ETF NAV divergence risk. (3) Flash
  rally/flash crash identification: no fundamental trigger + VIX spike + yield move = apply
  PTF+dealer simultaneous withdrawal mechanism. (4) KRE/bank stress: high duration + rising
  rates → VaR-duration amplifier → dealer bank trading revenue squeeze + AFS AOCI losses
  simultaneously. (5) PTF/non-bank presence assessment: PTF presence does NOT substitute
  for dealer large-trade capacity.
- Non-applicable environment: Normal market conditions with low volatility (bid-ask spreads
  and depth are both adequate in calm periods); exchange-listed equity markets with formal
  market-maker obligations and circuit breakers; very short-duration sovereign bonds;
  intraday short-term equity ETF trading (SPY, QQQ — order-driven markets, different structure).
- Time scale: Structural mechanism (multi-year) for quantity deterioration; retrenchment
  dynamic operates intraday to weekly in stress episodes; flash events can develop in
  12 minutes (Oct 15, 2014 precedent).
- Use in premarket reports: When assessing fixed income market health: check depth and
  price impact data (NY Fed primary dealer data, Bloomberg depth quotes) alongside spreads.
  When yield volatility surges intraday with no macro trigger: apply PTF liquidity asymmetry
  (depth will have fallen while spreads look tight). For KRE: at high duration + rising rates,
  expect VaR-duration amplifier to activate dealer retrenchment faster than spreads suggest.
  For bond ETF monitoring: ETF premium/discount to NAV is a lagging indicator; depth and
  transaction size data are leading indicators.
- Prohibited use: Do not use PTF presence in a sovereign bond market as evidence of
  adequate large-trade dealer substitution — CGFS55 explicitly says PTF markets are equally
  susceptible to abrupt liquidity deterioration. Do not rely on bid-ask spread data alone to
  assess bond market liquidity health. Do not treat Oct 2014 flash rally or May 2015 bund
  as a tradable pattern — they illustrate fragility conditions, not recurring timing signals.
  Do not benchmark current market-making costs against pre-crisis levels — pre-crisis liquidity
  was structurally under-priced due to implicit public sector backstop (CGFS55 Section 4).
  Do not treat 2016 depth/inventory data as current without updating from NY Fed or BIS.
- Evidence strength: Strong (Tier-1 BIS CGFS committee report; Study Group of 25 central
  banks; Box 4 survey 40+ market-making firms; two OOS case studies with official multi-agency
  data; second Tier-1 source corroborating CGFS52-001 pattern with new 2015-2016 data).
- Last review date: 2026-08-06.
- Revalidation trigger: Formal Tier-1 study showing depth metrics materially recovered in US
  or European sovereign bond markets post-2020; PTF study showing effective large-trade
  capacity substitution in corporate bonds; structural change to US Treasury market
  microstructure (RFQ → CLOB for large trades); Fed/BIS report on post-2022 normalization
  impact on bond market fragility confirming or denying the mechanism.
- Source: Committee on the Global Financial System (CGFS), "Fixed income market liquidity,"
  BIS CGFS Papers No. 55, January 2016. https://www.bis.org/publ/cgfs55.pdf.
  Local: research/books/bis_cgfs55_2016.pdf (35 pages, 447 KB, SHA-256:
  226372398dd7d68e07f26f9dadc312f55e260f6427046d842170780f23f278b0).

---

## KG-20260807-CGFS27-001: Regulatory ALM Feedback Mechanism — Fair Value Accounting and Risk-Based Solvency Create Structural Price-Inelastic Demand for Long-Duration Assets; DB Pension Demand-Supply Imbalance Self-Reinforces When Yields Fall

- Rule ID: KG-20260807-CGFS27-001
- Domain: portfolio_construction
- Applicability: Analyzing structural demand for long-duration sovereign bonds (TLT, IEF, long-end
  Treasuries, gilts) from DB pension funds and life insurers; understanding why long-end yields
  sometimes fall below macro fundamentals during stress; KRE bank stress involving LDI swap
  counterparty flows; regulatory events affecting major DB pension systems (FTK reviews, Solvency II
  implementation, US FASB pension accounting changes); interpreting demand-supply imbalances in
  long-maturity bond markets.
- Core principle: Fair value accounting requirements (FRS 17/IAS 19/FASB 158) and risk-based
  solvency regimes (FTK/Solvency II/traffic-light models) force DB pension funds and life insurers to
  hold long-duration assets to reduce balance sheet volatility. This demand is PRICE-INELASTIC: funds
  must buy regardless of yield levels to meet regulatory compliance. When many institutions act
  simultaneously, a self-reinforcing feedback loop develops: LDI buying → yields fall → liability NPV
  rises at lower discount rate → funding gap persists or widens → more LDI buying → more yield
  compression. Potential demand substantially exceeds available supply: US $290-300B; UK ~35% of
  long-term bond market (2006 estimates; funding ratios changed post-2022 rate rise).
- Mechanism: Three interlocking components: (1) REGULATORY TRIGGER: fair value accounting
  exposes sponsor balance sheets to visible pension surplus/deficit volatility; risk-based solvency
  requires buffers against adverse market scenarios. Combined, they create regulatory pressure to
  minimize funding volatility through duration matching and swap overlays. (2) PRICE INELASTICITY:
  the more urgent the solvency compliance requirement (e.g., UK PPF mandated 10-year deficit
  elimination), the less sensitive demand is to prevailing yield levels. Boots pension fund case study:
  entire £2.3B moved into long gilts over 15 months regardless of price. (3) FEEDBACK LOOP: LDI
  buying compresses long yields → at lower discount rate, liability NPV rises MORE than asset values
  → funding gap persists → renewed buying. UK market participants confirmed this mechanism was a
  key driver of gilt market dynamics 2004-2006. Forward real rates at 30-year maturity fell to ~0.5%
  while growth expectations remained stable — implying the excess demand was the primary driver.
  Supply response: governments issued 50-year bonds (France, UK); 40-year (Japan agency); 30-year
  (Germany, US reintroduction); but outstanding supply remained small vs potential demand; swap
  market provides more liquid alternative but counterparty exposure flows through bank balance sheets.
- Supporting evidence: BIS CGFS Papers No. 27 (February 2007) — Study Group of 25 central banks,
  chair José Viñals (Bank of Spain); interviews with 45 institutional investors across 17 countries.
  (i) UK empirical validation: 30/50-year index-linked gilt yields compressed to 0.9-0.7% in early
  2006 (Graph 4); forward real rates at 25-year maturity near 0.5% while UK growth expectations
  stable (Graph 5). BOE and multiple market participants confirmed LDI mechanism as key driver.
  (ii) Canada validation: real return bond (RRB) demand exceeded supply; BEIR distorted in H2 2004.
  (iii) Denmark: 2001 mark-to-market rule change → significant shift to euro bonds within 3 months.
  (iv) Netherlands: duration extension of bond portfolios after FTK announcement (though no large
  equity-bond shift due to healthy funding ratios and large euro bond supply).
  (v) Demand-supply estimates from multiple independent sources: OECD, IMF GFSR, Goldman
  Sachs, UBS, US Treasury ($290-300B US; 35% UK market), JP Morgan, Bank of Spain — all
  converging on large imbalances.
  Corroborated by: KG-20260805-CGFS44-001 (LDI mechanics and swap overlay structure);
  KG-20260806-CGFS52-001 (reduced dealer capacity compounds price impact of institutional demand);
  KG-20260806-CGFS55-001 (quantity-before-price deterioration amplifies forced-buying price impact).
- Contrary evidence: Outside UK and Canada, effects on long-term interest rates were limited as of
  2007 — Netherlands, Sweden, US/Europe had smaller demand-supply imbalances or more gradual
  implementation. After the 2022-2023 rate normalization cycle, US and European DB funding ratios
  improved materially (higher discount rates reduced liability NPV), reducing the urgency of LDI
  buying and the strength of the feedback. Post-2022 context: mechanism is structurally intact but
  acute pressure is lower than 2004-2006. CRITICAL FAILURE CONDITION: in rapidly RISING yield
  environments with leveraged LDI overlays, margin calls can force SELLING of gilts/Treasuries
  (UK LDI crisis, September-October 2022 — Bank of England emergency gilt purchase program
  required). The 2007 paper analyzed only the falling-yield phase of the feedback loop.
- Applicable environment: Periods when long-end yields are declining or have been low; when major
  DB pension systems face pending regulatory implementation of fair value requirements; when LDI
  swap overlay positions are large relative to gilt/Treasury market float; when yield curve is flattening
  driven by long-end demand rather than short-end rate cuts; KRE assessment when bank subsidiary
  LDI swap exposure is material.
- Non-applicable environment: Short-duration sovereign bonds (LDI focuses on 10-50 year maturities);
  DC pension plans (no price-inelastic demand mechanism); corporate bonds (secondary to government
  bonds for ALM due to credit risk and supply irregularity); rapidly rising yield environments unless
  studying the REVERSE mechanism (LDI margin calls → forced selling → yield spike amplification);
  countries with small DB pension sectors relative to local bond supply; current post-2022 period
  without verifying current DB funding ratios and LDI overlay leverage.
- Time scale: Structural mechanism operates on multi-year horizons; acute episodes develop over
  weeks-to-months following major regulatory announcements (Denmark: 3 months; UK: 2004-2006
  sustained; 2022 UK reverse: developed over weeks). Intraday signals not applicable.
- Use in premarket reports: When 10Y+ Treasury or gilt yields decline significantly without macro
  trigger: consider structural LDI demand as a contributor (not just monetary policy or safe-haven
  flows). When KRE/regional banks face long-duration mark-to-market losses: their LDI swap
  counterparty positions compound the stress via bilateral flows. When major regulatory events
  affecting EU/UK/US pension systems occur: flag potential for structural demand wave. NOTE: verify
  current DB funding ratios — post-2022 improved funding means less acute near-term pressure than
  the 2004-2006 UK episode.
- Prohibited use: Do not treat LDI demand as a permanent floor on long-end yields — 2022 UK
  crisis shows LDI can amplify yield spikes (forced selling) rather than dampen them. Do not use
  2007-vintage demand-supply estimates ($290-300B US) as current — funding ratios changed
  materially after 2022 rate rise; obtain current estimates before applying to sizing. Do not assume
  all DB pension systems behave like the UK (which had the most acute implementation + the smallest
  long-bond market relative to DB AUM); Dutch funds had very different experience. Do not treat as a
  short-term trading signal for long-end bonds — it is a multi-year structural mechanism.
- Evidence strength: Strong (Tier-1 BIS CGFS committee report; Study Group of 25 central banks;
  45 institutional interviews; UK OOS case study with observable yield compression; cross-country
  corroboration from Canada/Denmark/Netherlands; multi-source demand-supply estimates; extends
  CGFS44-001 with regulatory trigger + feedback mechanism).
- Last review date: 2026-08-07.
- Revalidation trigger: Formal Tier-1 study (BIS, IMF, BOE, FSB) documenting the 2022 UK LDI
  crisis as the reverse-feedback episode (forced gilt selling under margin calls → BOE intervention);
  updated demand-supply imbalance estimates for major DB markets post-2022 rate normalization;
  IASB/FASB changes to pension accounting standards that weaken the mark-to-market pressure
  mechanism; formal empirical study linking LDI structural demand to long-end yield term premium
  post-2022.
- Source: Committee on the Global Financial System (CGFS), "Institutional investors, global savings
  and asset allocation," BIS CGFS Papers No. 27, February 2007. https://www.bis.org/publ/cgfs27.pdf.
  Local: research/books/bis_cgfs27_2003.pdf (58 pages, 486 KB, SHA-256:
  5447fa763773b7d3dc8dc0ef9e3c47fe9811a77fd4e431d41907032704b72933).

### Single-Stock Earnings Transmits To A Sector ETF Only Via Its Systematic Component, Scaled By Index Weight

- rule_id: KG-20260807-ITSF-001
- Core conclusion: A sector-ETF constituent's earnings surprise predicts the sector
  ETF's (e.g., SMH) direction only through its industry-common (systematic)
  component, and its mechanical contribution is bounded by the reporter's index
  weight. A large idiosyncratic move in a low-weight or sub-segment constituent
  (e.g., a pure memory/NAND name in a compute/GPU-dominated semiconductor ETF) is
  not a reliable sector-direction signal and must not be transferred one-for-one.
- Mechanism:
  - A cap-weighted ETF return is, by construction, `r_ETF ≈ Σ_i w_i · r_i`
    (plus fees/tracking error). A single constituent's contribution is bounded by
    its index weight times its return.
  - Intra-industry information transfer (Foster 1981) is real but second-order:
    only the industry-common component of an announcer's surprise informs peers,
    and the transfer can be contagion (same sign) OR competitive (opposite sign,
    when a rival's weakness reflects share/margin shifts rather than end-demand).
  - Individual-stock returns are mostly idiosyncratic (Roll 1988, low R²), so a
    constituent's earnings-day move maps only partially onto the systematic
    component that could re-rate the ETF's large weights.
- Supporting evidence:
  - Foster, George (1981), "Intra-Industry Information Transfers Associated with
    Earnings Releases," Journal of Accounting and Economics 3(3), pp. 201-232.
    DOI: 10.1016/0165-4101(81)90004-7. Documents statistically significant but
    small same-direction peer reactions to an industry member's earnings; transfer
    rises with industry homogeneity. Source: Tier 2 (JAE); full text not accessed
    in live session 2026-08-07 (ScienceDirect 403); published-literature knowledge.
  - Roll, Richard (1988), "R²," The Journal of Finance 43(3), pp. 541-566.
    DOI: 10.1111/j.1540-6261.1988.tb04591.x. Shows individual-stock returns have
    low R² against market/industry factors; the majority of single-stock variance
    is idiosyncratic and even explicit public firm-specific news explains only a
    small part of large moves. Source: Tier 2 (JF); full text not accessed in live
    session 2026-08-07 (Wiley 403); published-literature knowledge.
  - Mechanical cap-weight identity (definitional, not empirical): confirms the
    weight-scaling bound above.
  - Live corroboration: 2026-08-06 premarket predicted SMH -0.40% from SNDK/WDC
    (low-weight memory names) earnings; SMH closed +0.31%. The idiosyncratic
    single-stock shock did not transmit to the cap-weighted ETF.
- Contrary evidence:
  - Contagion is not universal: a rival's miss can be neutral/positive for
    share-gaining peers (competitive transfer), so even the sign is not guaranteed.
  - In risk-off/stress regimes, cross-sectional correlations spike toward 1 and the
    low-R² insulation weakens; small names can co-move with the sector. Condition on
    the volatility regime (tie to standing-vix-layering).
  - Bellwether exception: an early-reporting, economically-central constituent
    (dominant foundry/GPU/analog name) carries far more sector information than a
    peripheral name of similar weight (Ramnath 2002).
  - Modern large-cap announcement/PEAD decay (Martineau 2022; see FAILED_IDEAS.md):
    any tradable edge is small after costs — use to scale confidence, not to trade.
- Applicable environment:
  - Premarket/intraday sector-ETF (SMH/XLK/SMH-like) directional framing when one
    or more constituents report earnings.
  - Postmarket audit grading of sector read-through predictions.
- Non-applicable environment:
  - Predicting an individual constituent's own reaction (this rule is about the ETF).
  - Stress/crash regimes where correlations spike (systematic risk dominates).
  - Broad macro shocks that move the whole sector regardless of single-name earnings.
- Time scale: Event window (announcement day to next regular session); not a
  multi-day drift or long-horizon signal.
- Required behavior in reports:
  - Score a constituent's earnings→sector effect as roughly
    P(systematic | surprise) x (reporter index weight) x (contagion sign), and state
    the reporter's approximate sector role (bellwether vs. sub-segment) explicitly.
  - Give low-weight, sub-segment, or firm-specific reporters near-zero
    sector-direction weight; do not write a sector directional call off them alone.
  - Any resulting action still requires the standing-smh-confirmation gate
    (15-minute VWAP/volume) before it can influence a trade draft.
  - In elevated-volatility/correlation regimes, note that co-movement risk is higher
    and the insulation is weaker.
- Prohibited use:
  - Do not transfer a single low-weight constituent's earnings surprise one-for-one
    (or by sign) to the sector ETF direction.
  - Do not ignore the competitive (opposite-sign) possibility for rival misses.
  - Do not treat firm-specific/sub-segment misses as sector signals.
  - Do not use this rule as a standalone buy/sell signal; it only calibrates a
    directional prior that must still pass confirmation and quant-math gates.
- Evidence strength: Medium-to-Strong for existence of intra-industry transfer
  (Foster 1981) and for idiosyncratic dominance (Roll 1988); Medium for premarket
  application; Weak for any single-name → index one-for-one move.
- Last review date: 2026-08-07.
- Revalidation trigger: A future postmarket audit finds a sector read-through miss
  in the opposite direction (a systematic, high-weight reporter that failed to
  transmit); live SMH constituent-weight data becomes available to make the
  weight-scaling quantitative; a stress-regime episode shows the low-R² insulation
  broke as expected (confirming the regime caveat); or new replication materially
  changes the intra-industry transfer estimates.
- Source: Foster (1981) JAE 3(3):201-232 and Roll (1988) JF 43(3):541-566, plus
  the cap-weight accounting identity. Documented in research/daily/2026-08-07.md;
  full journal text not accessed live (ScienceDirect/Wiley 403).

## KG-20260809-CFAEV-001: Grossman-Stiglitz Equilibrium: Markets Cannot Be Fully Efficient; Informational Inefficiency Is an Economic Necessity

- Rule ID: KG-20260809-CFAEV-001

- Core conclusion: If prices were fully informationally efficient, fundamental research would earn zero returns, so rational investors would stop doing it. But without research, prices would diverge from fundamental value, making research profitable again. Markets must remain sufficiently inefficient to allow sophisticated fundamental investors a fair return on their information-gathering costs. As passive investing grows, fewer fundamental investors participate → prices diverge more → research becomes more profitable → equilibrium re-established. This is a structural mechanism, not a temporary anomaly.
- Mechanism: Grossman-Stiglitz (1980): In an Arrow-Debreu economy, if price reflects all information, informed investors have no incentive to acquire costly information. But without informed traders, prices cannot incorporate information. Contradiction → markets must be in equilibrium where the return to information gathering equals its cost. Cornell (2016) extension: passive share grew from 16% to 34% of US mutual fund/ETF assets between 2006-2016. While no observable change in market efficiency was detected (too much volatility to measure), equilibrium theory predicts some inefficiency must persist.
- Key distinction from Sharpe's arithmetic: Sharpe's arithmetic (active as a group must underperform passive after costs — arithmetic identity) and G-S equilibrium coexist. G-S explains why a subset of better-informed investors can outperform; Sharpe explains why the average cannot. Both are true simultaneously.
- Supporting evidence: Grossman & Stiglitz (1980, AER, vol. 70, no. 3: 393-408) — foundational theoretical result, highly cited; Cornell & Roll (1981, Bell Journal) — related competitive framework; Cornell (2016) — empirical update on passive-share era; Derrien & Kecskés (2013) — companies losing analyst coverage decrease investment/financing by up to 2% of total assets, confirming fundamental analysts have a real economic function.
- Contrary evidence: In practice, the bar for achieving material informational advantage over institutional consensus in US mega-cap stocks has risen sharply as AI, alternative data, and NLP tools have spread. G-S equilibrium says the opportunity level is positive; it does not specify its magnitude or guarantee any individual's ability to exploit it.
- Applicable environment: Fundamental analysis of under-covered securities (small-cap US, mid-cap US, emerging market equities with limited analyst coverage); situations where local knowledge, proprietary data access, or processing advantage over the marginal investor is achievable.
- Non-applicable environment: Heavily covered US large-cap / Magnificent Seven / S&P 100 stocks where institutional consensus forms rapidly; situations where the proposed information edge is already widely distributed (commercially available data, published factor, screener-accessible metric).
- Time scale: The equilibrium mechanism operates continuously; it does not provide short-term timing signals.
- Use in reports: When evaluating whether fundamental research is worth conducting on a specific name, note analyst coverage density. Thin coverage → wider G-S gap → higher expected alpha from research effort. Dense coverage → narrow G-S gap → research effort competes against institutional consensus.
- Prohibited use: Do not treat G-S equilibrium as a guarantee that any specific analyst or fund will outperform. Do not use it as a trading signal. Do not use it to justify ignoring Sharpe's arithmetic when evaluating active fund choices.
- Evidence strength: Strong for the theoretical mechanism (Grossman-Stiglitz 1980 AER); Medium for empirical magnitude in the current passive-share era.
- Last review date: 2026-08-09.
- Revalidation trigger: Evidence emerges that passive-share growth beyond ~50% of AUM causes measurable degradation in market efficiency (wider bid-ask spreads, larger post-announcement drift, slower information incorporation); or new study replicates Derrien-Kecskés finding on a more recent sample confirming analyst-coverage economic value.
- Source: Grossman & Stiglitz (1980, AER); Cornell (2016); Derrien & Kecskés (2013, JF). Via CFA RF Equity Valuation (2017), Ch 6, pp. 109-111. Full daily note: research/books/2026-08-09-cfa-rf-equity-valuation-science-art-craft.md.

## KG-20260809-CFAEV-002: Active Management Systematic Underperformance: SPIVA Evidence and Sharpe's Arithmetic Identity

- Rule ID: KG-20260809-CFAEV-002

- Core conclusion: Active investors as a group must underperform passive investors after costs — this is an arithmetic identity, not a statement about market efficiency. Empirical SPIVA data confirms the prediction across multiple geographies, cap-sizes, and multi-year horizons. Performance persistence is extremely low: fewer than 3% of top-quartile funds remain top-quartile over a 2-year period. Default to low-cost index ETFs as core portfolio vehicles; require demonstrated exceptional skill before preferring active over passive.
- Mechanism: Sharpe's arithmetic (1991): Let passive investors hold the market index and active investors hold the complement. If the market returns 10%, passive earns 10%. Since passive + active = market, active investors as a group also earn 10% pre-cost. Because active investors incur higher costs (management fees, trading spreads, research expenses) than passive investors, active as a group must underperform passive after costs. This result is independent of market efficiency — it holds even in highly inefficient markets.
- SPIVA 2016 data (S&P Dow Jones Indices; periods ending 31 December 2016): Europe large-cap vs. S&P Europe 350: 80%/74%/74% underperform at 1/3/5yr. Japan large-cap vs. S&P TOPIX 150: 64%/60%/74%. USA large-cap vs. S&P 500: 66%/93%/88%. USA midcap vs. S&P MidCap 400: 89%/94%/90%. USA small-cap vs. S&P SmallCap 600: 86%/96%/97%. Active underperformance is worse in mid- and small-cap, and worse over longer time horizons.
- Persistence (Soe & Poirier 2016): Of 631 domestic equity funds in the top quartile as of September 2014, only 2.85% remained top-quartile at September 2016. Less than 1% of large-cap funds maintained top-quartile status through 3 consecutive 12-month periods. An inverse relationship exists between measurement horizon and ability to maintain top status.
- Supporting evidence: Sharpe (1991, FAJ vol. 47, no. 1) — arithmetic identity, foundational; SPIVA 2016 (S&P Dow Jones) — multi-country, multi-period empirical confirmation; Soe & Poirier (2016, S&P Dow Jones) — persistence scorecard; Jensen (1968, JF vol. 23, no. 2) — original active fund study.
- Contrary evidence: G-S equilibrium (see entry above) shows that a subset of sophisticated investors with genuine informational advantages can outperform. Malkiel (2016) noted Chinese local equity market as the one exception where insider-trading prevalence enables active outperformance. EM equities generally offer wider opportunities than developed markets. Harvey et al. (2013): Asian (Japanese) analysts outperform European/US analysts on both buy and sell recommendations — suggesting skill and/or informational advantages exist for some participants.
- Applicable environment: Evaluating whether to use actively managed mutual funds vs. low-cost ETFs for core equity exposure; evaluating any trading strategy that claims systematic alpha; evaluating persistence claims by fund managers.
- Non-applicable environment: Does not apply to individual stock selection where informational advantages may exist (G-S); does not preclude all active management — it constrains the average. Does not apply to non-competitive vehicles (private equity, proprietary trading desks with exclusive order flow).
- Time scale: Short-term outperformance is possible but not persistent; long-horizon (3-5yr) underperformance is the dominant outcome.
- Use in reports: When proposing use of an actively managed vehicle or a systematic factor strategy, state the cost-adjusted expected return and acknowledge the SPIVA base rate. When holding an ETF or index vehicle, this entry provides the baseline justification.
- Prohibited use: Do not treat this as a prohibition on fundamental analysis (G-S coexists). Do not apply it to single-stock analysis. Do not use it to justify ignoring research — research is what maintains the G-S equilibrium.
- Evidence strength: Strong — arithmetic identity (Sharpe 1991) + multi-country, multi-period SPIVA data + persistence evidence.
- Last review date: 2026-08-09.
- Revalidation trigger: SPIVA releases data showing sustained reversal (>40% of US large-cap active funds outperforming over 10-year horizons after fees); or a structural change in the cost of passive investing makes the arithmetic advantage smaller.
- Source: Sharpe (1991, FAJ); SPIVA 2016 (S&P Dow Jones); Soe & Poirier (2016). Via CFA RF Equity Valuation (2017), Ch 6, pp. 105-109. Full daily note: research/books/2026-08-09-cfa-rf-equity-valuation-science-art-craft.md.

## KG-20260809-CFAEV-004: Total Payout Yield (Dividends Plus Buybacks) Is the Correct Return Driver in the Buyback Era; DDM Dividend-Only Yields Understate Shareholder Returns

- Rule ID: KG-20260809-CFAEV-004

- Core conclusion: Traditional dividend discount models (DDM) and Gordon Growth Model treat only dividends as the shareholder return mechanism. In the 2000-2016 era, US corporate buybacks were massive ($6.1T on S&P 500 2005-2016) and often exceeded dividends as a return vehicle. Using dividend yield alone understates the total return stream to equity holders. Straehl & Ibbotson (2015) show total payout yield (dividends + net buybacks) better explains actual US stock returns in this era. Separately, EPS growth driven by share-count reduction is not organic earnings growth and must be decomposed.
- Mechanism: Buybacks reduce share count → each remaining share represents a larger fraction of unchanged total earnings → EPS rises mechanically. Cash returns to shareholders who tender/sell, and to remaining shareholders through ownership concentration. Both mechanisms return value, neither shows up in dividend yield. The supply-side return decomposition (Ibbotson framework) must include buyback yield to match realized returns since 2000.
- Key data: S&P 500 buybacks $536B in 2016; $6.1T total 2005-2016 (Birinyi Associates). S&P 500 Q4 2016 buybacks: $135.3B (S&P 2017). Approximately 1% US excise tax on buybacks (IRA 2022, effective 2023) added modest cost without materially reducing buyback volumes.
- Supporting evidence: Straehl & Ibbotson (2015, Morningstar WP) — total payout decomposition; Birinyi Associates and S&P aggregate buyback data (Tier 2 institutional) — magnitude confirmation; Brettell et al. (2015 Reuters investigative series "The Cannibalized Company") — buyback quality risk (corporate timing is poor; debt-financed buybacks can destroy value).
- Contrary evidence: Buybacks are discretionary and cyclical — S&P 500 buybacks declined in 2016 from 2015 peak; cannot be projected as stable. Brettell et al. (2015): managements have poor market timing, often buying high; some companies reduced R&D or capital investment to fund buybacks, potentially harming long-run earnings power. Debt-financed buybacks increase leverage → refinancing risk under rate stress.
- Applicable environment: Valuing US large-cap equities using discounted cash flow or DDM; assessing EPS growth quality in earnings reports; computing the appropriate return expectation for S&P 500 index ETFs; comparing dividend-paying vs. buyback-focused firms.
- Non-applicable environment: International markets where buybacks are less common (European dividend culture, Japanese gradually adopting); pre-2000 era where dividends dominated; regulated industries (banks under capital constraints may restrict both dividends and buybacks simultaneously).
- Time scale: Return measurement over full cycles (3-5+ years); quarter-to-quarter buyback variability is high.
- Use in reports: When reviewing EPS growth as a bullish driver, explicitly decompose organic earnings growth vs. share count reduction effect. When using any P/E or DDM-based valuation, note whether dividend yield or total payout yield is the appropriate denominator. When KRE or bank holdings reduce buybacks under capital pressure, note that total payout yield may compress.
- Prohibited use: Do not project historical buyback rates as guaranteed future return components. Do not treat debt-financed buybacks as equivalent to organic cash generation. Do not use buyback volume alone as a bullish signal without checking the financing source and the price paid.
- Evidence strength: Strong for mechanism and magnitude (multiple institutional data sources); Medium for the Straehl-Ibbotson working paper (not yet formally journal-published at time of reading, 2017).
- Last review date: 2026-08-09.
- Revalidation trigger: Buyback tax significantly reduces buyback volumes (e.g., rate raised to 4%+); or regulatory change restricts buybacks (e.g., mandatory employee-investment requirements before buybacks); or Straehl-Ibbotson paper is formally published and findings updated.
- Source: Straehl & Ibbotson (2015, Morningstar WP); S&P (2017); Birinyi Associates data. Via CFA RF Equity Valuation (2017), Ch 4, pp. 78-90. Full daily note: research/books/2026-08-09-cfa-rf-equity-valuation-science-art-craft.md.

## KG-20260809-BISQR-001: Private Credit Growth Is Driven by Three Macro Factors — Policy Rate, Banking Sector Efficiency, and Regulatory Stringency (45-Country Panel, 2010–2019)

- Rule ID: KG-20260809-BISQR-001

- Core conclusion: Private credit origination volume is significantly driven by three macro factors: (1) lower policy rates (+12% originations per -1SD of 4.14%); (2) less efficient/capable banking sector, measured by the IMF financial institutions (FI) index (+33% per -1SD in FI index — the largest driver; represents ~half the AE vs. EME gap); (3) more stringent bank regulation (+7% per +1SD in World Bank bank regulatory stringency index). Non-financial corporate leverage is not significant. Supply factors (low rates attracting institutional capital, declining BDC cost of capital) dominated private credit growth 2010–2019. BDC WACC converged with bank WACC by ~250bp over 2010–2019, eroding banks' initial funding advantage. Private credit AUM: $0.2T (early 2000s) → $2.5T+ (2024).
- Mechanism: Three structural channels: (a) Rate channel: lower policy rates reduce BDC wholesale funding costs (BDCs lack sticky deposits and reprice fully with policy rate), and expand institutional investor demand for yield-seeking assets. (b) Banking efficiency channel: when domestic banks are less capable of serving loan demand (low profitability, thin branch/ATM network, high spreads), firms pivot to private credit alternatives; this effect is empirically largest. (c) Regulatory stringency: tighter bank capital requirements reduce banks' willingness to extend credit to riskier middle-market and LBO borrowers. Cost-of-capital secondary mechanism for BDCs: BDC cost of equity fell post-GFC as institutional familiarity and portfolio performance improved; BDC D/E leverage rose from ~0.4 to >1.0+ (2011-present), reducing blended WACC via debt tax shield and debt-over-equity substitution.
- Key data: Panel regression: N=1,523 observations; 45 countries; Q1 2010–Q4 2019. Policy rate SD: 4.14%; FI index SD: 0.174; bank stringency SD: 0.104. BDC sample: 11 banks + 55 BDCs, Bloomberg WACC (Graph 4.A-C in article). Private credit AUM: $2.5T+ as of 2025. SVAR decomposition: US data Q1 2004–Q3 2024.
- Supporting evidence: BIS Quarterly Review March 2025 Article 1 (Tier-1, peer-reviewed BIS); supply/demand SVAR decomposition (Box A) consistent with main regression; BDC CoC analysis uses Bloomberg WACC data (Tier-2). IMF GFSR April 2024 (cited in article) — confirms private credit risks from financial stability perspective.
- Contrary evidence: Post-2019 data is not in the regression; the 2022-2024 hiking cycle may have partially reversed the rate-channel contribution. Rising BDC leverage also creates fragility: higher D/E amplifies losses in a credit downturn. Retail investor entry via open-ended private credit structures (noted as a risk by the authors) could introduce liquidity mismatches that banks do not face.
- Applicable environment: Analyzing private credit cycle dynamics vs. bank lending cycle; assessing BDC sector exposure as an alternative credit vehicle; evaluating banking sector competitive pressure from private credit; monitoring whether rate cuts (Fed easing cycle) are likely to re-accelerate private credit supply expansion; comparing AE vs. EME private credit penetration (EME banking inefficiency suggests structural private credit demand potential).
- Non-applicable environment: Short-term deal volume fluctuations (seasonal, M&A calendar); individual BDC stock selection; private credit defaults or recovery rates (article covers origination volume, not credit quality); post-2019 dynamics not captured in regression (described descriptively only).
- Use in reports: When private credit market conditions are cited as a risk factor for banks or a competing force for credit quality, apply this card to assess whether macro drivers (rate cycle phase, banking sector stress) are supporting or contracting private credit supply. When BDC sector stocks appear as candidates, note the WACC convergence thesis and its rate-cycle sensitivity.
- Prohibited use: Do not use +12%/+33%/+7% effect sizes to forecast specific private credit AUM levels — these are panel averages across 45 countries. Do not infer that higher policy rates alone will shrink private credit — supply and demand factors interact. Do not treat BDC WACC convergence as permanent.
- Evidence strength: Strong — large multi-country panel (45 countries, 9 years) with country and time fixed effects; BIS Tier-1 source; three mechanisms each independently significant with stable cross-specification coefficients (R-squared 0.864–0.867).
- Last review date: 2026-08-09.
- Revalidation trigger: Updated BIS/IMF cross-country panel covering post-2019 data confirms or revises the three-factor model under different rate regimes; or BDC sector stress event challenging the WACC convergence narrative.
- Source: BIS Quarterly Review, March 2025, pp. 23–40, "The global drivers of private credit." Full daily note: research/books/2026-08-09-bis-qr-march-2025.md.

## KG-20260809-BISQR-002: Bank-Fund Stress Commonality — Bond MFs Destabilize in High-Pressure Banking Episodes; Bond ETFs Are a Stabilizing Force

- Rule ID: KG-20260809-BISQR-002

- Core conclusion: When market pressure in the banking sector is elevated and sustained (top 10% of 4-month bank CDS spread changes), all three major investment fund types show declining net flows (strain commonality). However, bond ETFs remain in net inflow territory — functioning as a stabilizing force — while open-ended bond mutual funds (MFs) experience outflows 75% of the time. Bond MF strain commonality with banking stress rose from ~0% correlation (2006–13) to ~80% correlation (2014–24). Low-cash-buffer bond MFs facing outflows increase their cash holdings in response (cash hoarding), confirming they sell illiquid assets simultaneously — amplifying bond market stress precisely when banks are already under pressure. Simulated bond MF outflows at a 1SD bank CDS shock reach ~50% of March 2020 (Covid) peak outflow magnitude.
- Mechanism: Common investor base creates linkage: when bank CDS spreads rise (reflecting credit risk repricing), investors holding both bank liabilities and bond fund shares simultaneously retrench from both, generating correlated stress. Bond ETF business model reduces run incentives: (1) Authorised Participants (APs) — small number means each AP internalizes the price impact of redemptions on own ETF holdings; (2) in-kind redemptions — ETF sponsors select less attractive redemption baskets during stress, reducing incentive to redeem for cash; (3) secondary market premium/discount mechanism — bargain hunters buy discounted ETFs, stabilizing price without requiring underlying asset sales. Bond MFs lack these mechanisms: direct cash redemptions force illiquid asset sales; first-mover advantage creates run incentive; low-cash-buffer funds both receive larger outflows AND hoard cash, doubling the fire-sale pressure.
- Key data: 53 large banks, 15 jurisdictions; top 500 global bond ETFs; top 500 global bond MFs; top 500 US prime MMFs; Jan 2006–Aug 2024. High-pressure episodes: GFC (2008–09), European sovereign debt crisis (2010–12), Covid shock (2020), 2016 G-SIB stress, 2022 credit risk spikes. Bond MF high-pressure correlation (2014-24): ~80%. Bond ETF high-pressure correlation: >50% (but flows remain positive). Bond MF outflow frequency in high-pressure episodes: 75%. Shocked bond MF outflow (1SD bank CDS shock): ~50% of March 2020 peak.
- Supporting evidence: BIS Quarterly Review March 2025 Article 4 (Tier-1; Aquilina, Cornelli, Tarashev). Consistent with KG-20260806-CGFS52-002 (bond fund liquidity illusion — bond fund redemptions amplify bond market dislocations). Morris-Shim-Shin (2017, JME) on redemption risk and cash hoarding confirmed in Box A. FSB (2023) and IOSCO (2024) recommendations on open-ended fund liquidity management validate the systemic risk framing.
- Contrary evidence: March–April 2023 (SVB/Credit Suisse) banking stress was severe but short-lived and did not meet the 4-month sustained criterion — bond MF flows did not show the predicted pattern. The mechanism requires sustained bank CDS pressure, not abrupt spikes. Prime MMF sector risk is lower since 2016 US reform shifted prime MMF investors toward government MMFs (safer assets).
- Applicable environment: Monitoring systemic risk when banking sector CDS spreads rise on a sustained (4-month) basis — triggering the high-pressure regime; interpreting bond ETF vs. bond MF flow divergence during banking stress as a systemic signal; assessing whether bond market conditions are being amplified by NBFI fire sales during banking stress; evaluating structural resilience of bond ETF vs. bond MF as portfolio vehicles during financial stress; cross-referencing with KG-20260802-BIS-NBF-002 (NBFI basis trade) and KG-20260804-BIS-B3-002 (leverage ratio constraint) during severe banking stress scenarios.
- Non-applicable environment: Short-lived banking stress spikes (like SVB/Credit Suisse March 2023) that do not sustain 4 months; government money market funds (different risk profile from prime MMFs); equity funds; individual bond ETF products with unique AP or portfolio structures.
- Use in reports: When a high-pressure banking episode is identified (sustained bank CDS spread rise), flag the bond MF fire-sale amplification risk on bond market conditions. When a bond ETF is held in the portfolio, note its relative resilience vs. bond MFs during banking stress. When evaluating KRE holdings during banking stress: the bond MF channel can tighten credit conditions further even if the KRE-specific fundamentals are stable.
- Prohibited use: Do not use bond ETF inflows during banking stress as a guarantee that ETF prices will hold — extreme stress (like March 2020) still caused ETF premium/discount dislocations requiring Fed intervention. Do not use this to make buy/sell timing signals — the finding describes flows and systemic risk, not prices or alpha. Do not treat 80% correlation as a precise forecast for any specific episode.
- Evidence strength: Strong — 18-year dataset; 53 banks + 1,500+ funds; two subperiods for structural comparison; identified mechanism (ETF vs. MF business model difference); consistent with existing CGFS and FSB findings.
- Last review date: 2026-08-09.
- Revalidation trigger: New sustained high-pressure banking episode (2025+) where bond MF/ETF flow patterns can be compared to predictions; structural change in bond ETF in-kind redemption rules; FSB/IOSCO reform implementing swing pricing or anti-dilution levies on bond MFs that changes incentive structure.
- Source: BIS Quarterly Review, March 2025, pp. 83–98, "Commonality under pressure: banks and funds." Full daily note: research/books/2026-08-09-bis-qr-march-2025.md.

## KG-20260810-BFSG-001: Disposition Effect — Investors Sell Winners Too Early and Hold Losers Too Long

- Rule ID: KG-20260810-BFSG-001

- Core conclusion: Investors systematically sell winning positions too early (to lock in the feeling of pride) while holding losing positions too long (to avoid the regret of realizing a loss). This asymmetry is the disposition effect. Magnitude: individual brokerage data (Odean 1998, 10,000 accounts): winners sold 1.68x more often than losers; proportional trading rates: 14.8% for winners vs. 9.8% for losers. The effect is documented in professional mutual fund managers (Frazzini 2006, JF) and across multiple international markets. Net result: investors retain tax-inefficient realized-gain positions too short and loss positions too long, producing systematic below-market returns from a timing drag even when their stock selection is random.
- Mechanism: Kahneman-Tversky prospect theory value function. In the gain domain (position above purchase price), marginal utility of additional gains is concave (diminishing), creating strong incentive to realize the gain before it shrinks — locking in pride. In the loss domain (position below purchase price), marginal utility is convex (diminishing marginal disutility of additional losses), creating incentive to hold and hope for breakeven rather than realize the loss and feel regret. Mental accounting reinforces this: each position is tracked in its own mental account with purchase price as reference point, preventing portfolio-level netting that would rationalize loss realization.
- Professional mitigation: explicit stop-loss rules (e.g., mandatory sale if position falls 10% from cost), end-of-day or end-of-period forced realization, "tax harvesting" reframing (re-labels loss realization as a tax benefit, reducing the emotional cost of loss recognition). Professionals exhibit the disposition effect but overcome it more effectively than amateurs through these rule-based self-control tools.
- Key data: Odean (1998, JF): 10,000 brokerage accounts 1987-1993; proportional selling: 14.8% winners, 9.8% losers. Shefrin-Statman (1985, JF): original theory and event study evidence. Frazzini (2006, JF): fund manager disposition effect in quarterly holdings data — managers with high disposition effect underperform. Multiple country replications (UK, Australia, Taiwan, India).
- Supporting evidence: Shefrin & Statman 1985 (original, JF); Odean 1998 (JF large brokerage data); Frazzini 2006 (JF, mutual fund managers); Barber & Odean 2000 (JF, trading frequency and underperformance). Monograph source: Statman 2019, CFA RF "Behavioral Finance: The Second Generation," Conclusion, pp. 183-186.
- Contrary evidence: High-frequency traders and algorithmic systems mechanically execute stop-losses — the disposition effect may be diminished in markets dominated by algorithmic participants. Tax-loss harvesting services (e.g., Betterment, Wealthfront) systematically reverse the loss-holding behavior for clients using these tools.
- Applicable environment: Post-entry position review — each time a position has declined from entry price, check whether the hold decision reflects a genuine revised thesis or mere regret-aversion (no thesis update); when a position has risen substantially and there is hesitation to take profits without a specific fundamental reason; evaluating active fund managers for disposition effect drag (systematic loss-holding is a red flag); standing post-buy review for every newly filled buy order (define stop-loss level at time of entry to prevent future disposition-effect trap).
- Non-applicable environment: Tax-loss harvesting decisions (the behavioral frame is explicitly managed); intraday scalps without reference-point anchoring; positions with automated stop-loss systems already in place; cases where genuine thesis revision justifies holding a loss position.
- Use in reports: Apply as a self-consistency check in each position review: "Is this position being held because the fundamental thesis remains intact, or because realizing the loss feels emotionally costly?" If the latter, disposition effect is active. Flag for the standing-post-buy-review protocol.
- Prohibited use: Do not use disposition effect as a mandate to always close losing positions — it is a bias check, not a trading signal. Do not conclude that every loss-making position is held due to disposition effect; thesis revision is legitimate.
- Evidence strength: Strong — multiple Tier-1 studies over multiple decades, multiple markets, multiple investor types (retail and professional). Effect size is robust and statistically significant.
- Last review date: 2026-08-10.
- Revalidation trigger: Large-scale brokerage study post-2020 showing disposition effect has been substantially weakened by algorithmic/robo-advisor adoption; or formal meta-analysis showing effect size is no longer economically significant for institutional portfolios.
- Source: Shefrin & Statman (1985, JF); Odean (1998, JF); Frazzini (2006, JF); via Statman (2019) "Behavioral Finance: The Second Generation," CFA RF, pp. 183-186. Full daily note: research/books/2026-08-10-behavioral-finance-statman-2019.md.

## KG-20260810-BFSG-002: Admired vs. Spurned Stocks — Stocks of 'Good Companies' Yield Lower Returns Due to Affect Heuristic Overvaluation

- Rule ID: KG-20260810-BFSG-002

- Core conclusion: Stocks of companies highly ranked in Fortune's 'Most Admired Companies' survey consistently yield lower future returns than stocks of companies with low rankings (disliked/spurned companies) over multi-year holding periods. The mechanism is the affect heuristic: when investors hold strong positive feelings about a company, they simultaneously overestimate expected returns AND underestimate risk for that company's stock — the opposite of the rational risk-return trade-off. This bidding-up of admired stocks raises their prices above fundamental value, reducing subsequent returns. Supporting: cross-country study found that populations rating a country's stock market as "attractive" simultaneously rate it as "low risk" — confirming the affect heuristic's simultaneous distortion of both risk and return assessments. The "accepted-shunned" factor (Statman's behaviorally-augmented BAPM): the Vice Fund (sin sector stocks) outperformed the Vanguard FTSE Social Index Fund (accepted/ESG stocks) over 2002-2012, with alpha of approximately 1% annually.
- Mechanism: Affect heuristic (Slovic, Finucane): holistic like/dislike judgment creates a halo that contaminates both risk assessment and return expectation. Investors who like a company (Apple, Amazon, Nike) believe it simultaneously offers higher expected returns AND lower risk — two errors in the same direction. Since they overvalue expected returns and underestimate risk, they bid the stock price above fair value, leaving future return below fair compensation for the actual risk borne. Two reinforcing channels: (1) Cognitive-errors channel: investors incorrectly extrapolate past sales, earnings, and quality metrics into future stock returns (representativeness error); "good company with great products" → "good stock with high returns" is a category error; (2) Expressive/emotional-benefits channel: investors who want to own shares of companies they admire (for social status, values alignment, consumer brand love) are willing to accept lower utilitarian returns for these non-utilitarian benefits — willingly paying a premium.
- Key data: Statman & Shefrin (1995): initial "Good Companies, Bad Stocks" finding. Statman, Fisher, Anginer: multi-study replication using Fortune Most Admired annual survey (1983-ongoing). Cross-country affect study: two groups rated 40+ country stock indexes — one for expected return, one for expected risk; positive correlation found (admired countries expected both high return and low risk) rather than the rational positive risk-return trade-off. Vice Fund vs. Vanguard FTSE Social Index Fund (2002-2012): Vice Fund alpha ~1%; accepted-shunned factor beta: +0.20 (Vanguard FTSE), -0.46 (Vice Fund) in 5-factor model. Employee satisfaction portfolio ("100 Best Companies to Work For"): +3.5% annual abnormal return 1984-2009 — consistent with markets undervaluing intangible quality not captured by admired-company affect.
- Supporting evidence: Statman & Shefrin (1995); Fortune Most Admired Companies data (Tier-2 survey, but used consistently in peer-reviewed Statman studies); Hong & Kacperczyk (2009, JFE): tobacco/alcohol/gambling earn higher returns, consistent with demand-reduction mechanism for sin sectors. Edmans (2011, JFE): employee satisfaction → abnormal returns, consistent with cognitive-errors hypothesis for intangible quality. Monograph: Statman (2019) "Behavioral Finance: The Second Generation," Ch 8, pp. 141-157.
- Contrary evidence: Some period-specific results may reflect omitted risk factors (quality, profitability, investment factors in the 5-factor model) partially explaining the admired-company premium; the causal identification is not as clean as a randomized experiment. ESG investing growth post-2018 may have already largely repriced the sin-stock discount in the "accepted-shunned" factor.
- Applicable environment: When buy thesis is primarily based on company brand reputation, product quality, or consumer appeal rather than specific valuation metrics — positive affect may already be fully priced in; when evaluating sector tilts (growth/technology/consumer discretionary vs. tobacco/alcohol/defense) for multi-year holding; post-earnings analysis for widely beloved companies where sentiment is universally positive — check for affect overshoot.
- Non-applicable environment: Same-day or short-term momentum — affect mispricing operates over 1-5+ year horizons; macro-driven sector moves (risk-off/risk-on) where all stocks move together; cases where admired-company status reflects genuinely superior informational signals (insider knowledge, product pipeline) not yet in public prices.
- Use in reports: When a candidate stock is a widely admired market leader in a consumer-facing or technology sector, flag the affect-heuristic risk: "Admired company status is a valuation risk factor — check P/E, P/S, P/FCF relative to sector median." Do not use as a standalone contrarian short signal; the effect operates over long horizons.
- Prohibited use: Do not short a stock solely because it is widely admired — long-horizon effect, high risk of momentum continuing before reversal. Do not apply mechanically: "Fortune Most Admired companies always underperform" — the effect requires excess valuation from affect-driven demand, which must be verified in current metrics.
- Evidence strength: Strong — multiple Tier-1 studies using consistent Fortune Most Admired survey data over 30+ years; cross-country affect study confirms mechanism; accepted-shunned factor documented in a formal behaviorally-augmented asset pricing model.
- Last review date: 2026-08-10.
- Revalidation trigger: Post-2020 study of Fortune Most Admired vs. spurned returns accounting for ESG AUM growth; or large-scale factor analysis showing the premium disappears after controlling for profitability and quality factors (which would shift the explanation from affect to omitted risk factor).
- Source: Statman & Shefrin (1995); Statman, Fisher, Anginer (multiple); Hong & Kacperczyk (2009, JFE); Edmans (2011, JFE); via Statman (2019) "Behavioral Finance: The Second Generation," CFA RF, Ch 8, pp. 141-157. Full daily note: research/books/2026-08-10-behavioral-finance-statman-2019.md.

## KG-20260810-BFSG-003: Attention-Driven Buying — Hot News, Abnormal Volume, Extreme Returns, and Search Interest Create Retail Buy Pressure

- Rule ID: KG-20260810-BFSG-003

- Core conclusion: Retail investors are disproportionately likely to buy stocks that have recently caught their attention through news, abnormal volume, extreme one-day returns, or direct search interest. Barber and Odean (2008, RFS) show that individual investors are net buyers of attention-grabbing stocks while professional investors are less influenced by attention. Da, Engelberg, and Gao (2011, JF) validate the mechanism with Google Search Volume Index (SVI) for Russell 3000 stocks from 2004-2008: abnormal SVI is distinct from older attention proxies, likely reflects retail attention, predicts higher stock prices over the next two weeks, and predicts eventual reversal within the year. The usable conclusion for this system is a risk-control gate: hot-news/gap/high-volume names are more vulnerable to attention-driven overpaying and must pass valuation, confirmation, and concentration checks before any buy draft.
- Mechanism: Availability heuristic and constrained search. When retail investors choose what to buy, they face thousands of possible stocks and tend to consider the subset made salient by news, volume, extreme returns, or search/social attention. When they sell, they mostly choose from holdings they already own; short selling is rare. Attention therefore produces asymmetric retail buy pressure rather than symmetric buy/sell pressure. Da/Engelberg/Gao add a direct attention proxy: elevated Google SVI captures retail attention more timely than news/volume/return proxies and is consistent with temporary attention-induced price pressure followed by slower reversal.
- Key data: Barber/Odean RFS 21(2), pp. 785-818, DOI 10.1093/rfs/hhm079; SSRN/web-search abstract records the hypothesis and confirms individual investors are net buyers of stocks in the news, stocks with high abnormal trading volume, and stocks with extreme one-day returns. Da/Engelberg/Gao JF 66(5), pp. 1461-1499, DOI 10.1111/j.1540-6261.2011.01679.x; Wiley/Crossref abstract records Russell 3000 sample from 2004-2008; 834,627 firm-week observations with 468,413 valid SVI observations; SVI predicts next-two-week price pressure and eventual one-year reversal.
- Supporting evidence: Two independent Tier-2 peer-reviewed studies: Barber/Odean (2008, RFS) uses account-level buy/sell behavior and indirect attention proxies; Da/Engelberg/Gao (2011, JF) uses a direct Google search proxy in a later Russell 3000 sample and explicitly tests the Barber/Odean pressure-and-reversal mechanism. Statman (2019) CFA RF behavioral-finance digest provides the availability-heuristic framing.
- Contrary evidence: Da/Engelberg/Gao itself is a caution against immediate contrarian trading: high attention predicts higher prices for the next two weeks before eventual reversal. News, volume, extreme returns, and SVI can reflect genuine information arrival rather than pure bias. Google Trends coverage is incomplete for low-search tickers. Both core samples predate zero-commission trading, fractional shares, TikTok/Reddit-style social flows, and post-2020 retail options intensity.
- Applicable environment: Premarket or intraday buy candidates with mainstream news, abnormal volume, large gap moves, extreme one-day returns, FDA/earnings/AI/meme/short-squeeze narratives, IPO attention, or obvious retail/social search attention; postmarket audit of newly bought positions whose cost basis is above the regular-session close after an attention-catching move; small-account position sizing where the stock is visible and exciting but concentration risk is high.
- Non-applicable environment: Attention caused by verified fundamental information that materially changes fair value and is supported by filings, company IR, or official data; institutional-dominated liquidity events where retail attention is not a meaningful share of demand; broad index ETF decisions where single-name retail attention is not the driver; already-confirmed pullback/retest setups where price has reset and the buy thesis is no longer a chase of the initial event.
- Time scale: Intraday to two-week continuation risk, with medium-term reversal risk up to one year; exact timing is not tradable from the literature alone.
- Use in reports: Apply as a risk and audit gate, not as a price target. If a same-day buy candidate is hot-news/gap/high-volume/search-attention driven, require at least one hard non-attention reason before any buy draft: valuation reset, confirmed pullback/retest, official earnings/filing evidence, liquidity/spread confirmation, or portfolio concentration below the standing limit. If a new buy has cost basis above the regular-session close after a high-attention move, postmarket audit should label it attention-chase unless a documented non-attention thesis exists.
- Prohibited use: Do not use attention as a standalone buy signal. Do not short or sell mechanically solely because attention is high; short-term continuation can precede reversal. Do not conflate retail attention with institutional informed buying. Do not apply exact timing/effect sizes to modern social-media and zero-commission markets without fresh evidence.
- Evidence strength: Medium-to-Strong — two independent Tier-2 peer-reviewed U.S. studies with different proxies and sample windows; limited by pre-social-media samples and by the mixed timing result.
- Last review date: 2026-08-10.
- Revalidation trigger: Post-2020 study using social media/search/options-retail-flow data shows the attention pressure-and-reversal pattern has disappeared, or shows that algorithmic/institutional liquidity now fully absorbs retail attention demand without overpayment.

## KG-20260811-AIAMS-001: Hierarchical Risk Parity (HRP) — Clustering-Based Recursive Inverse-Variance Allocation Addresses MVO Instability and Concentration

- Rule ID: KG-20260811-AIAMS-001

- Core conclusion: Mean-variance optimization (MVO) suffers from three structural weaknesses: instability (portfolios are highly sensitive to small changes in expected-return estimates, producing wildly different weights across periods), concentration (MVO tends to allocate extreme weights to one or a few assets when estimation error aligns with extreme covariance entries), and out-of-sample underperformance (these flaws cause MVO portfolios to underperform simpler alternatives when evaluated on data not used for optimization). Hierarchical Risk Parity (HRP) addresses all three by replacing matrix inversion with a three-step algorithm: (1) Compute pairwise distance d(i,j) = √(2(1−ρ(i,j))) and apply agglomerative clustering to produce a dendrogram; (2) Quasi-diagonalize the covariance matrix by reordering assets per the dendrogram so similar assets appear adjacent; (3) Traverse the dendrogram top-down and at each split allocate the cluster's weight between sub-clusters in inverse proportion to sub-cluster variance (using only diagonal terms, avoiding ill-conditioned matrix inversion). The result diversifies across clusters rather than individual assets.
- Mechanism: HRP avoids the fundamental computational problem with MVO — inverting an ill-conditioned covariance matrix when N (number of assets) is small relative to the estimation window or when assets are highly correlated. By working with the hierarchical tree rather than the full covariance inverse, HRP produces portfolio weights that are robust to small data perturbations. It requires no expected-return estimates, eliminating the most error-prone input to MVO. Diversification operates at two levels simultaneously: within each cluster (assets that behave similarly) and across clusters (different market segments). This multi-level diversification reduces both idiosyncratic concentration and cluster-level concentration.
- Key data and sources: López de Prado (2016, Journal of Portfolio Management 42(4):59-69): introduced the algorithm and tested it out-of-sample over multiple asset classes; HRP outperformed equal-weight, min-variance, and MVO in OOS tests. Confirmed as a well-established investment application in CFA Institute Research Foundation monograph (2025) "AI in Asset Management: Tools, Applications, and Frontiers," Ch 1 (Simonian), pp. 1–26. The algorithm has been independently extended in Raffinot (2017) and cited in dozens of empirical portfolio construction papers.
- Practical application for this system: When reviewing multi-ETF holdings (MSFT, SMCI, PLTR in tech growth cluster; VRTX in healthcare; KRE in regional financials), HRP informs the intuition that holding MSFT and PLTR simultaneously does not provide as much diversification as holding MSFT and VRTX or MSFT and KRE. The cluster structure suggests: tech-growth exposures (MSFT, PLTR, SMCI, QQQM) belong to one cluster; healthcare (VRTX) to a second; regional banking (KRE) to a third; broad market ETFs (SPY, QQQM) overlap clusters. HRP would reduce aggregate tech-growth exposure relative to equal-weight. This is an analytical framework for reviewing concentration, not a mechanical order-sizing instruction.
- Contrary evidence: Some studies find that HRP underperforms equal-weight and min-variance portfolios in equity-only bull-market environments where expected returns are reliably positive and well-estimated from trailing data. The advantage is specifically largest when expected-return uncertainty is high and asset relationships are genuinely hierarchical. In concentrated small-account portfolios (3–5 positions), the hierarchical tree has minimal structure; the method degenerates toward naive equal-weight.
- Applicable environment: Multi-asset-class or multi-sector ETF portfolios where expected-return uncertainty is high; concentration risk review when holdings span multiple correlated tech or sector positions; periodic portfolio review as an alternative to arbitrary equal-weight sizing; use when MVO would require inverting a near-singular covariance matrix (fewer than 30 observations per asset).
- Non-applicable environment: Single-stock sizing within a position; high-conviction alpha strategies with reliable expected-return estimates; very short-term tactical trading; portfolios of fewer than 4–5 assets where hierarchical structure is trivial; severe market stress where correlation structure shifts significantly from the estimation period.
- Prohibited use: Do not use HRP portfolio weights as hard rules for placing specific buy/sell orders without explicit user review and approval. Do not represent HRP as guaranteed outperformance over MVO in any specific environment. Do not apply it to cryptocurrency or highly illiquid assets where correlation estimates are unreliable.
- Evidence strength: Strong — Tier-2 peer-reviewed Journal of Portfolio Management study with OOS testing; mathematically rigorous mechanism; confirmed adoption in CFA RF open-access monograph; independently extended in subsequent academic literature.
- Last review date: 2026-08-11.
- Revalidation trigger: Post-2020 empirical study specifically comparing HRP to equal-weight and min-variance in a concentrated ETF small-account universe similar to current holdings, showing that HRP's advantage over equal-weight has disappeared or reversed.
- Source: López de Prado (2016, JPM 42(4):59-69); via Simonian in CFA RF "AI in Asset Management" (2025), Ch 1, pp. 1–26. Full daily note: research/books/2026-08-11-ai-in-asset-management-cfa-rf-2025.md.
- Source: Barber & Odean (2008, Review of Financial Studies); Da, Engelberg & Gao (2011, Journal of Finance); Statman (2019) "Behavioral Finance: The Second Generation." Full daily note: research/daily/2026-08-10.md.

## KG-20260811-CGFS59-001: Quarter-End Repo Window-Dressing — Banks with Period-End Snapshot Reporting Sharply Contract Repo Intermediation at Q/Y-Ends

- Rule ID: KG-20260811-CGFS59-001

- Core conclusion: Banks subject to period-end (point-in-time snapshot) leverage ratio and G-SIB/SRF reporting sharply contract repo intermediation at quarter-ends and year-ends to "window-dress" their balance sheets, causing predictable pricing discontinuities and quantity restrictions that reverse after the reporting date. Banks subject to period-average leverage ratio reporting (primarily US domestic banks and UK banks post-Q1 2017) reduce repo intermediation more continuously and persistently, producing lower but more stable volumes. Key evidence: euro area banks sharply contracted US triparty repo volumes at Q-ends while US/UK period-average reporters showed stable patterns. Annex 4 BCBS monitoring data (2013-2016H1): banks with leverage ratio < 3% in 2014H1 reduced repo/exposure ratio from 6.51% to 3.95% by 2016H1 — tightest banks adjusted most. At Q-ends in euro area, repo rates for German/French high-quality collateral fell sharply (excess cash seeking scarce CCP-eligible assets); Italian/Spanish repo rates spiked upward. UK overnight repo rates fell to -23 bp at year-end 2016. US: Fed RRP facility absorbed up to $475B at Q-ends (over $300B from money market funds) — direct evidence of cash seeking repo that dealers refused.

- Mechanism: Leverage ratio is measured at period-end reporting date → banks minimize balance sheet size on that date → repo (which expands balance sheet on both sides) is reduced or rejected → cash investors face outright refusal at any price over reporting dates → rates spike or collapse depending on whether excess cash or excess collateral dominates. Additional compounding mechanisms at year-end: G-SIB surcharge assessed annually at year-end (bucket-crossing creates cliff effect on entire balance sheet); SRF levy calculated on year-end liabilities (euro area banks). Three simultaneous drivers at December 31 = most severe episodes. Reporting frequency asymmetry: period-average requirement (US/UK) prevents the sharp Q-end contraction but creates sustained lower intermediation pressure throughout the quarter.

- Key data and sources: CGFS59 (BIS Tier-1, April 2017, Study Group of 25 central banks); Munyan (2015, OFR Working Paper No. 22) empirically confirms cross-border Q-end repo retrenchment; Cipriani, Louria, Martin (2017, FRBNY Staff Reports) provides econometric analysis of different jurisdictional behavior. BCBS monitoring exercises (six consecutive periods 2013H2-2016H1) in Annex 4: North American banks average ~8% repo/exposure ratio (higher than global average ~4%); European banks have largest absolute share (~46% of global repo book).

- Applicable environment: Quarter-ends and year-ends for monitoring repo market functioning; assessing whether Treasury market stress at Q-end reflects regulatory window-dressing vs. fundamental deterioration; understanding KRE bank sector behavior around reporting dates; distinguishing euro area banks (period-end reporters) from US/UK banks (period-average reporters) in triparty or bilateral repo markets.

- Non-applicable environment: Intra-quarter (non-period-end) repo market dynamics; jurisdictions that have adopted period-average reporting throughout; as a persistent directional trading signal (window-dressing behavior reverses after reporting date).

- Prohibited use: Do not interpret Q-end repo rate spikes or collapses as fundamental credit or solvency deterioration — they are regulatory behavioral artifacts that normalize after the reporting date. Do not extrapolate from Q-end repo conditions to normal (non-period-end) market functioning. Do not conflate repo rate spikes with general credit stress without checking calendar context.

- Evidence strength: Strong — BIS CGFS Tier-1 source (25 central banks); two independent corroborating academic/official studies (Munyan 2015 OFR WP; Cipriani et al. 2017 FRBNY SR); BCBS monitoring data across six periods; cross-jurisdictional comparison of period-end vs. period-average reporters consistent with mechanism.

- Last review date: 2026-08-11.

- Revalidation trigger: Regulatory shift to mandatory period-average reporting for all major repo market jurisdictions (would eliminate Q-end asymmetry); or empirical evidence (post-2020 data) that window-dressing behavior has changed materially.

- Source: BIS CGFS Papers No. 59 (April 2017), chaired by Sir Jon Cunliffe; Munyan (2015, OFR WP 22); Cipriani et al. (2017, FRBNY SR). Full daily note: research/books/2026-08-11-bis-cgfs59-repo-market-functioning.md.

## KG-20260811-CGFS59-002: QE Collateral Scarcity — Central Bank Asset Purchases Reduce High-Quality Sovereign Bond Float, Pushing Specific Collateral Repo Rates Below Policy Rates

- Rule ID: KG-20260811-CGFS59-002

- Core conclusion: Large-scale central bank asset purchases (QE/LSAP) remove high-quality government bonds from the market float available for repo collateral. This creates two observable effects: (1) specific (named) collateral repo rates fall below the official policy rate or deposit facility rate — even turning negative — because borrowers must pay a premium to obtain scarce securities in repo; (2) at Q-ends, holders of scarce collateral refuse to lend it via repo because bank balance sheet constraints prevent them from reinvesting resulting cash, creating a mutually reinforcing scarcity episode. In euro area since mid-2015: German and French sovereign-specific repo rates fell significantly below ECB deposit facility rate due to PSPP purchases. At 2016 year-end: all euro area sovereign GC repo rates fell sharply while Italian-German repo spread widened to approximately 5%. ECB established Eurosystem Securities Lending Programme to partially mitigate by re-lending purchased bonds into the repo market.

- Mechanism: Central bank buys government bonds → removes those bonds from the circulating float available as repo collateral → market participants who need specific bonds (to cover short positions, post deliverable margin, fulfill settlement obligations) must pay higher rates to borrow them → collateral-specific repo rate = cash lending rate minus scarcity premium → scarcity premium can be large enough to push the rate below zero (cash lender effectively pays to lend against scarce collateral). Simultaneously: QE creates reserves throughout banking system → bank balance sheets expand → leverage ratio pressure increases → banks less willing to accept cash in repo over Q-ends → cash investors can't place cash → excess cash pushes Q-end rates for cash-seeking investors sharply downward. Both channels compound at Q-ends. Securities lending programs (UK DMO, BOJ, ECB) partially mitigate by returning purchased bonds to the market.

- Key data and sources: CGFS59 (BIS Tier-1); ECB GC Pooling and RepoFunds rate data (show overnight repo below deposit facility rate for German/French collateral since mid-2015); BOJ tiered reserve and GC repo arbitrage data; UK Treasury bill yields to -25 bp at 2016 year-end; Bucalossi-Scalia (2016, Bank of Italy Occasional Papers No. 347) corroborates euro area leverage ratio impact on repo rates.

- Applicable environment: During active large-scale QE programs; when specific sovereign bond repo rates are trading below official policy rate (diagnostic signal of collateral scarcity, not credit stress); when assessing impact of QT/balance sheet normalization on collateral availability and repo rates; when evaluating why Treasury-specific repo rates are below SOFR/EFFR during periods of Fed asset holdings.

- Non-applicable environment: When central bank has fully normalized balance sheet and asset holdings are minimal; markets where central bank purchases are small relative to outstanding government bond float; as a price prediction for any individual sovereign bond repo rate — too many market-specific factors.

- Prohibited use: Do not interpret collateral scarcity and below-policy repo rates solely as market dysfunction — they are an observable (sometimes intended) side-effect of QE policy. Do not use negative repo rates as a standalone trading signal without verifying central bank asset holdings as the driver. Do not assume QE scarcity effects persist indefinitely — they reverse with QT and can be partially offset by securities lending programs.

- Evidence strength: Strong — BIS CGFS Tier-1 source; ECB, BOJ, and CGFS multi-jurisdictional data; Bank of Italy corroboration; mechanism quantitatively consistent with observable market data across multiple jurisdictions and QE episodes.

- Last review date: 2026-08-11.

- Revalidation trigger: QT normalization study showing that repo rates did NOT normalize above policy rate as predicted by collateral scarcity resolution; or evidence that the mechanism operates fundamentally differently in post-2022 rate environment.

- Source: BIS CGFS Papers No. 59 (April 2017), chaired by Sir Jon Cunliffe; Bucalossi-Scalia (2016, Bank of Italy OP No. 347); ECB, BOJ, and CGFS monitoring data. Full daily note: research/books/2026-08-11-bis-cgfs59-repo-market-functioning.md.

## KG-20260811-CGFS59-003: CCP Netting Reduces Leverage Ratio Constraint for Repo — Matched Inter-Dealer Books Net to Zero Balance Sheet; End-User Triparty Markets Are Excluded

- Rule ID: KG-20260811-CGFS59-003

- Core conclusion: Routing both the repo and reverse repo leg of a matched book through a central counterparty (CCP) allows repo market dealers to net positions to a single CCP counterparty — eliminating the net balance sheet impact of the matched book and removing the associated leverage ratio cost. Euro area government bond repo: CCP usage reached 50-60% of market volume by 2017, driven primarily by this incentive. At Q-ends in the euro area, the spread between CCP-cleared and bilateral repo rates can reach hundreds of basis points — CCP-cleared pricing is far more stable. This netting benefit is NOT available in US triparty repo markets, where end users (money market funds, hedge funds, insurers) are typically not CCP members. A distressed institution needing directional (one-sided, non-nettable) repo funding faces full leverage ratio cost even if it accesses the CCP.

- Mechanism: CCP becomes counterparty to both legs of the matched book → dealer faces a single counterparty for both the repo (lending cash, receiving collateral) and the reverse repo (receiving cash, returning collateral) → bilateral netting: combined net exposure to CCP = $0 → zero incremental leverage ratio denominator → no capital charge for the matched book. For end-user intermediation (triparty: dealer stands between MMF and hedge fund), CCP netting requires both clients to be CCP members, which is uncommon due to membership economics (liquidity resource requirements and regulatory capital for committed CCP liquidity). Attempts to expand US CCP membership have had mixed success.

- Key data: CGFS59 Box B (mathematical netting illustration); Annex 1 euro area: CCP share of repo market 50-60% by 2017; Q-end CCP vs bilateral repo spread: hundreds of bps. PFMI framework confirms CCP structures reduce bilateral credit risk (KG-20260804-PFMI-001). Two corroborating Tier-1 sources for the CCP mechanism (CGFS59 + PFMI).

- Applicable environment: Analyzing repo market structure and why euro area repo is more stable than US triparty at Q-ends; evaluating CCP clearing policy proposals; assessing whether dealer capacity improvements via CCP expansion are feasible in specific jurisdictions; understanding why CCP pricing and bilateral pricing diverge sharply at Q-ends.

- Non-applicable environment: US triparty repo markets (end users typically non-CCP members → no matched-book netting for client intermediation); directional (one-sided) repo trades even via CCP — these retain full leverage ratio cost; as a solution to EF5 (asset monetization) repo needs in stress — CCP netting requires matching, not directional trades.

- Prohibited use: Do not assume CCP clearing resolves dealer capacity constraints universally; the matched-book netting benefit is limited to inter-dealer transactions. Do not assume CCP membership expansion is economically straightforward — membership costs are material barriers.

- Evidence strength: Strong — BIS CGFS Tier-1 (25 central banks); mathematical mechanism incontrovertible (balance sheet netting); empirical CCP usage data consistent with mechanism; extends and corroborates KG-20260804-PFMI-001 (CCP infrastructure) from a repo-specific balance sheet perspective.

- Last review date: 2026-08-11.

- Revalidation trigger: Successful expansion of CCP membership to major end-users in US triparty market (would change applicability conditions); or regulatory removal of netting recognition for CCP-cleared repos.

- Source: BIS CGFS Papers No. 59 (April 2017), Box B and Section 3. Full daily note: research/books/2026-08-11-bis-cgfs59-repo-market-functioning.md.

## KG-20260812-CGFS63-001: QE/APP Yield Compression — Cross-Country Evidence: LSAP1 -90-120 bp, ECB APP -100 bp, BoE QE -50-100 bp, BoJ QQE -10-25 bp; Portfolio Rebalancing Elevates Risk-Asset Valuations; Repo Collateral Scarcity Side Effect

- Rule ID: KG-20260812-CGFS63-001

- Core conclusion: Cross-country meta-analysis of 37 academic studies and a survey of 23 central banks establishes that large-scale asset purchase programs reduce 10-year sovereign yields by 50-120 bp depending on program design: Fed LSAP1 (agency MBS + Treasuries) -90 to -120 bp; Fed LSAP2/MEP (Treasuries only) ~-30 to -40 bp; ECB APP (cumulative, multi-asset) ~-100 bp on 10-year sovereign yields; BoE QE1+QE2 -50 to -100 bp on gilts; BoJ QQE -10 to -25 bp (event study) / ~-90 bp (BoJ regression). Domestic currency depreciation: 4-6% for QE1/LSAP1/ECB APP/QQE. Portfolio rebalancing channel: CB removes safe-asset supply → investors substitute into riskier assets → equity prices rise, corporate spreads compress. Critical side effect: APPs generate collateral scarcity in repo markets (BoJ: lower volumes/yield volatility; Riksbank: market liquidity deterioration; BoE: price dislocations in specific bonds) — mitigated by securities lending programs and per-security holdings caps. GDP peak effects 0-4 pp (25 studies); inflation effects positive but slow.

- Mechanism: Three channels. (1) Portfolio rebalancing: CB absorbs duration and safe-asset supply → remaining investors must substitute into riskier assets (equities, corporate bonds, EM assets) → risk premia compress, equity P/E ratios expand. (2) Signaling: APPs signal CB commitment to low-for-long policy → forward rate expectations fall → term premia compress; FG amplifies this channel. (3) Bank lending: CB purchases raise bank security portfolio values and reduce bank funding costs → banks expand lending → credit conditions ease. Collateral scarcity side effect: as CB accumulates large share of sovereign bond supply, remaining market float shrinks → specific repo rates fall below policy rate (cross-reference CGFS59-002); securities lending programs partially reintroduce purchased bonds to repo market.

- Key cross-reference: CGFS63 independently corroborates CGFS59-002 (QE collateral scarcity in repo). Two Tier-1 sources now confirm this mechanism.

- Applicable environment: When major CB (Fed, ECB, BoE, BoJ) announces or expands QE/APP: sovereign yields likely to compress by 50-120 bp range for 10Y (program design matters — MBS-targeted outperforms Treasuries-only; open-ended/outcome-based outperforms fixed-size). When evaluating equity valuation in QE context: P/E expansion is partially mechanical (portfolio rebalancing); not entirely earnings-driven. When assessing repo conditions during QT: as APPs unwind, collateral scarcity resolves → repo rates normalize upward → SOFR-EFFR spread may widen before normalizing.

- Non-applicable environment: Flow effects smaller than stock/announcement effects and fade quickly; agency MBS purchases more effective at reducing mortgage rates than Treasury-only; QE less effective against structural deflationary forces (BoJ QQE did not achieve inflation target despite extraordinary scale). QT yield effects may not be symmetric to QE.

- Prohibited use: Do not assume linear scaling (larger programs not proportionally more effective; diminishing returns documented). Do not equate QE announcement effect with lasting flow effect. Do not assume symmetric QT reversal.

- Evidence strength: Strong — Tier-1 BIS CGFS meta-analysis; 37 academic studies; 23-CB survey; multiple independent corroborating studies per program and CB.

- Last review date: 2026-08-12.

- Revalidation trigger: Post-2022 empirical study on whether QT-era yield movements follow the inverse of QE-era compression at comparable balance sheet magnitudes; whether 2022 normalization episode showed structural breaks.

- Source: BIS CGFS Papers No. 63 (October 2019), Section 2.3; Annex 2; Graph 8 (yield effects, 37 studies); Graph 9 (macro effects, 25 studies). Full daily note: research/books/2026-08-12-bis-cgfs63-ump-cross-country.md.

## KG-20260812-CGFS63-002: CIP Deviation as USD Funding Stress Indicator — Cross-Currency Basis Widening Signals Acute Dollar Shortage; Fed Swap Lines Are Systemic Backstop; Swap Line Announcements Reduce CIP Deviations by ~5 bp

- Rule ID: KG-20260812-CGFS63-002

- Core conclusion: During the GFC, European banks had expanded large USD-denominated assets (loans, bonds, securities) funded through FX swap markets. Post-Lehman, both interbank and FX swap markets froze: effective maturity of dollar funding shortened while dollar assets became illiquid — creating acute global USD shortage. Observable diagnostic: cross-currency basis (FX-implied USD rate vs. LIBOR/SOFR) widened sharply as dollar borrowers paid above-CIP rates. Systemic backstop: Fed established USD swap lines with 14 central banks by October 2008; standing arrangements with no pre-set limit since October 2013 (BoC, BoE, BoJ, ECB, Fed, SNB). Empirical evidence: Baba-Packer (2009) — USD auctions based on swap lines reduced FX swap spread level and volatility; Coffey et al. (2009) — swap line announcements reduced CIP deviations by ~5 bp on average. This knowledge card promotes the existing macro.md candidate "FX swap market amplification of financial conditions" — CGFS63 is the second independent Tier-1 source confirming the mechanism.

- Mechanism: Banks fund USD assets by selling domestic currency (eg EUR) spot and buying USD, with an agreement to sell USD back at the forward rate. When dollar supply dries up in FX swap markets: (a) FX-implied cost of USD rises above LIBOR → CIP fails → cross-currency basis widens; (b) banks face maturity mismatch: USD assets remain; USD funding dries up → acute solvency risk if basis widens enough. CB swap line: foreign CB borrows USD from Fed → distributes via USD auction to local banks → banks obtain dollar funding without private FX swap market → basis compresses. Signaling: mere establishment of swap line reduces stress even before use, as banks know backstop exists (option value of the facility).

- Key data: Coffey et al. (2009): swap line announcements → ~5 bp CIP deviation reduction on average. Ivashina et al. (2015): euro area banks most dependent on wholesale dollar funding cut lending most. Bahaj-Reis (2018): swap lines significantly reduced USD funding risk for banks with access. CGFS63 (2019): 14 CBs assessed swap lines as effective in normalizing FX swap spreads, reducing risk premia, improving foreign currency borrowing.

- Second source: Cross-reference KG-20260803-GFSR-TDL-002 (cross-border dollar funding stress via cross-currency basis — IMF GFSR April 2025, Tier-1). Two independent Tier-1 sources now confirm: (1) the CIP deviation / cross-currency basis as USD funding stress indicator; (2) the FX swap market as the primary cross-border dollar funding channel.

- Applicable environment: When EUR/USD or USD/JPY cross-currency basis (3M or longer) widens significantly (>20 bp = high stress; >5-10 bp = rising tension): interpret as dollar funding stress — not just risk-off or credit concerns. When USD appreciates sharply + VIX spikes: check cross-currency basis to confirm if dollar funding stress is a driver vs. pure risk-off. When global bank stocks fall alongside USD strength: foreign banks with large USD balance sheets face dollar funding risk — systemic stress indicator.

- Non-applicable environment: Normal markets where CIP holds approximately (basis near zero = no acute dollar stress). Does not apply to localized bank idiosyncratic stress. Post-2013 standing swap line arrangements mean extreme GFC-level dollar shortage (100+ bp CIP deviations) is less likely — backstop now established and pre-committed. Small persistent CIP deviations (5-15 bp) in post-2015 markets partly reflect regulatory frictions (leverage ratio, capital charges), not pure dollar stress.

- Prohibited use: Do not treat regulatory-friction-driven post-2015 CIP deviations (~5-15 bp) as equivalent to GFC-level dollar funding stress — different mechanism (regulation vs. acute shortage). Do not conflate cross-currency basis with EME credit risk or sovereign fiscal stress.

- Evidence strength: Strong — Tier-1 BIS CGFS (23 CBs); Baba-Packer (2009); Coffey et al. (2009); Bahaj-Reis (2018); Ivashina et al. (2015). Multiple independent empirical sources on multiple dimensions.

- Last review date: 2026-08-12.

- Revalidation trigger: Evidence that post-2013 standing swap line arrangements have so thoroughly backstopped dollar funding stress that cross-currency basis no longer provides early warning; or new USD funding stress episode (eg non-bank dollar borrowers, digital asset dollar settlement) outside swap line coverage.

- Source: BIS CGFS Papers No. 63 (October 2019), Box B (pp. 30-31). Full daily note: research/books/2026-08-12-bis-cgfs63-ump-cross-country.md. Second source: GFSR April 2025.

## KG-20260812-NBER-QT-001: QT-QE Asymmetry in Announcement Effects — QT Announcements Raise Yields by +4-8 bp per Event (+20-26 bp Cumulative), Far Less Than QE Compression (50-120 bp); Active QT > Passive QT on Long-End

- Rule ID: KG-20260812-NBER-QT-001

- Core conclusion: Cross-country event study of 48 QT announcements across 7 advanced economies (Australia, Canada, Euro area, New Zealand, Sweden, UK, US) shows QT announcement effects on government bond yields are far smaller than QE effects in reverse. Individual Main Announcement: +4-8 bps at 1-year and longer maturities (statistically significant). Cumulative across 2021-2023 tightening cycle: +20-26 bps average (heterogeneous across countries). By comparison, QE programs during stressed periods compressed yields by -50 to -120 bp (per established literature; also see KG-20260812-CGFS63-001). Active QT (bond sales) has larger yield effects than passive QT (roll-off), especially at longer maturities — active QT steepens the yield curve. Passive QT primarily affects short-term yields and works mainly through signaling tighter monetary policy. Preliminary Discussions (vague, no specific details): no significant effect on yields. Main Announcements (concrete start dates/magnitudes): drive the yield response. QT announcement effects on equities, exchange rate, and inflation compensation are in the expected direction (tightening) but statistically insignificant, EXCEPT: corporate bond index (significant decline) and government bond convenience yield (significant decline).

- Mechanism: Two channels. (1) Signaling: QT announcements signal CB commitment to tighter policy → short-rate expectations rise → short-term yields increase; passive QT primarily works this way. (2) Duration/supply channel: active QT increases net private supply of long-duration bonds → term premium rises → yield curve steepens; active QT works more strongly through this channel. Part of the yield response to QT announcements may reflect accompanying forward guidance language about tighter policy (not purely balance sheet mechanics). Very limited spillovers to other countries — unlike QE during stressed periods which had large global effects.

- Cross-reference: QT-QE asymmetry: compare to CGFS63-001 (QE yield compression -50 to -120bp) — QT announcement effects are 4-10x smaller than QE effects with opposite sign. Corroborates Smith-Valcarcel (2023) who found minimal US QT1 announcement effects.

- Applicable environment: When a major CB (Fed, ECB, BoE) announces a new or expanded QT program: expect +4-8 bp in government bond yields per Main Announcement at 1yr+ horizons. When evaluating QT contribution to tightening cycle: cumulative +20-26 bp is the expected range for a full QT program. When active QT announced or expanded (active bond sales): expect yield curve steepening — larger effect at 10-year+ maturities relative to short-term. When passive QT only: smaller yield effects, primarily short-term, mainly via signaling.

- Non-applicable environment: Results from post-pandemic tightening cycle where liquidity was still ample at QT onset. May not apply if QT begins when reserve scarcity is already present (could have amplified effects), or when government debt supply is not already elevated. Announcement effects do not equal implementation effects (no significant same-day pricing impact on QT transaction dates).

- Prohibited use: Do not assume QT reverses QE yield compression symmetrically — effects are far smaller. Do not treat QT announcement dates as analogous to QE announcement dates for position sizing. Do not assume QT has effects comparable to QE-scale events on equities or credit spreads.

- Evidence strength: Moderate — NBER Tier-1 working paper (not yet peer-reviewed); 7-CB cross-country design provides internal validation; multiple methods (event study panel regression); corroborated by Smith-Valcarcel (2023) for US QT1. Promoted to admitted despite single-paper basis because: cross-country design, clear mechanism, corroboration from prior US study, and consistent with established QE asymmetry evidence.

- Last review date: 2026-08-12.

- Revalidation trigger: Peer-reviewed publication of Du-Forbes-Luzzetti (2024) with substantially different results; OR a QT episode producing yield effects comparable to QE (suggesting the "water boiling" transition has occurred and standard estimates no longer apply).

- Source: NBER Working Paper No. 32321 (Du, Forbes, Luzzetti, April 2024), Sections 3-4; Table 3.7 (pp. 1-61). Full daily note: research/books/2026-08-12-nber-qt-around-globe-2024.md.

## KG-20260812-CONC-001: Single-Name Concentration Must Be Limited in a Small Retail Account Without a Demonstrated Edge — Individual-Stock Lifetime Returns Are Severely Positively Skewed (57.4% Underperform T-Bills; Top 4.3% of Firms Create ALL Net Wealth), and Concentration Paid Only for Informed Investors in Local/Non-Index Names With Large Accounts (and Even Then at a Lower Sharpe)

- Rule ID: KG-20260812-CONC-001

- Core conclusion: Two independent peer-reviewed studies jointly support enforcing a single-name concentration limit for a small retail account that has not demonstrated a genuine informational edge. (1) BASE RATE — Bessembinder (2018): over July 1926–December 2016, of 25,967 individual U.S. common stocks, 57.4% had a lifetime buy-and-hold return BELOW one-month Treasury bills (negative cross-sectional median), and net lifetime shareholder wealth creation (~$35T) is extremely right-skewed — the top 90 firms (0.33%) produced HALF and the top 1,092 firms (4.3%) produced ALL of it, while the remaining ~95.7% only matched T-bills. A few-name portfolio is thus a bet against a positively skewed distribution in which the typical stock underperforms cash; diversification is what converts the market's positive mean (carried by a tiny minority of winners) into a reliable expected outcome. (2) BOUNDARY — Ivković, Sialm & Weisbenner (2008): concentrated households (1–2 stocks) DID outperform diversified ones (3+) by ~16 bps/month (~0.8–4.8%/yr) in MEAN return, but the effect was stronger in non-S&P-500 and LOCAL stocks (information-asymmetry exploitation), was concentrated among LARGE accounts (small accounts did not reliably show it), and came with HIGHER total risk and LOWER Sharpe ratios. Net: concentration is justified only under a demonstrable edge in the right names; absent that, the Bessembinder base rate dominates and the limit must be enforced.

- Mechanism: Positive skewness of single-stock returns — monthly-return skewness amplified by multiplicative compounding — means lifetime outcomes are dominated by a handful of extreme winners while the median stock decays vs. cash. Holding 1–3 names maximizes exposure to this unfavorable base rate and to idiosyncratic (diversifiable, unrewarded) risk. The Ivković et al. exception runs through a different channel: private/local information lets skilled concentrators select from the favorable tail, but requires an information edge, names where such an edge exists (local/non-index), and enough capital to act; even then higher mean comes with lower Sharpe. A small account in large-cap index constituents with documented chase-entry behavior sits in the base-rate regime, not the informed-concentration regime. De-risking whole shares here costs ~$0.02/order (negligible), so cost cannot justify leaving a breached limit un-executed.

- Applicable environment: Small retail account where a single-name notional is a large % of equity and no documented informational edge exists; holdings are large-cap/broad-index constituents (e.g., MSFT, PLTR); a single position breaches the desk red line (>15% oversized warning; >20% default de-risk/buy-0); two names together dominate equity (e.g., MSFT+PLTR ~60%); sizing a new single-stock buy or reducing an over-weight ahead of an event/overnight macro. Grounds RULE-20260810-* (>20% → buy 0), RULE-20260811-03 (pre-macro de-risk draft), RULE-20260812-01 (up-day relative-weakness de-risk), and FAILED_IDEAS 2026-08-01 (one-share-notional % sizing).

- Non-applicable environment: Investors with a demonstrable documented edge in specific names (informed-concentration regime); concentration in local/non-S&P-500 names in a large sophisticated account; diversified index-ETF sizing (VOO/QQQM/SPY — the skewness argument is about single-name concentration, not broad baskets); mandates that explicitly accept lower Sharpe for higher mean and can bear the idiosyncratic drawdown.

- Prohibited use: Do not generate a directional buy/sell signal for any ticker — this governs SIZING/concentration limits only. Do not read Bessembinder as "individual stocks are bad" (the market's positive mean is real; it is just carried by a few names). Do not cite Ivković et al. to relax the limit for this account (its outperformance requires a demonstrated edge, local/non-index names, and large accounts, and still carries lower Sharpe). Do not treat the limit as satisfied by merely "advising" de-risk; when breached, produce a concrete share+limit de-risk draft (still user-approval-gated).

- Evidence strength: Strong — two independent Tier-2 peer-reviewed journals (JFE 2018; JFQA 2008), a clear mechanism (positive skewness / information-conditioned concentration), and out-of-sample/global corroboration (Bessembinder et al. 2019/2023 ~64,000 global stocks: skewness even more extreme internationally). Boundary condition explicitly carved out and recorded in a contradiction note.

- Last review date: 2026-08-12.

- Revalidation trigger: Peer-reviewed evidence that individual-stock lifetime-return skewness has materially attenuated in the modern era; OR credible evidence that this account has developed a demonstrable informational edge (then the Ivković-Sialm-Weisbenner informed-concentration regime, with its lower-Sharpe caveat, would apply); OR a change in desk policy on the >15%/>20% single-name limits.

- Source: Bessembinder, "Do Stocks Outperform Treasury Bills?", Journal of Financial Economics 129(3):440–457 (2018); Ivković, Sialm & Weisbenner, "Portfolio Concentration and the Performance of Individual Investors", Journal of Financial and Quantitative Analysis 43(3):613–655 (2008) (NBER WP 10675). Full daily note: research/daily/2026-08-12.md. Contradiction note: research/contradictions/2026-08-12-concentration-limit-vs-informed-concentration.md.


## KG-20260814-DMS-001: Global ERP Is Not Fixed and Varies Substantially Across Countries and Time Periods: The US Historical Equity Premium Is an Outlier Subject to Success Bias

- Rule ID: KG-20260814-DMS-001

- Core conclusion: The global equity risk premium (vs. cash bills) over 1900–2023 is 4.3% per year (35 DMS countries). The US equity premium of 4.7% vs. bills is the highest of all 35 countries and reflects extraordinary US economic and geopolitical success: the US went from ~0% of world equity market capitalization in the 1800s to 60.5% today — an outcome impossible to forecast ex-ante. World ex-US equity real return is 4.3% (in USD), 2.2 pp below US, compounding to a terminal wealth gap exceeding 12:1 over 124 years. Switzerland's equity premium vs. bills is 2.6% — 2.1 pp below the US figure. Investors who rely exclusively on US historical ERP as the forward-looking baseline commit "success bias": they implicitly assume the US will replicate its trajectory, when the more defensible prior for a global investor is the global average of ~4.3% vs. bills.

- Mechanism: The US equity premium is elevated for three compounding structural reasons: (1) Ex-post winner selection: the US is selected for study because it did well — the 21 countries with 124-year DMS data include markets that suffered severe political/military disruptions (Germany, Japan, Russia/Austria-Hungary), which automatically causes survivorship bias in favor of US returns. (2) Reserve currency exceptionalism: the USD became the world's reserve currency post-1944, systematically biasing USD-denominated returns upward vs. non-reserve-currency markets. (3) Geopolitical stability: the US was never invaded or occupied in the 20th century; capital infrastructure and rule of law remained intact through both World Wars. None of these factors can be assumed constant for the next 100 years, nor do they apply to other markets. The 2.2 pp annual gap between US and World ex-US returns compounds over 124 years to a 12:1 terminal wealth ratio — a magnitude that is a historical anomaly, not the base case for a forward-looking global investor.

- Key data: Global equity premium vs cash: 4.3% per year (DMS 35-country dataset, 1900–2023; executive summary p. 5). US real equity return: 6.5% per year (highest of 35 DMS countries, 1900–2023); EP vs bills: 4.7%; EP vs bonds: 3.5%. Switzerland real equity return: 4.5%; EP vs bills: 2.6%. World ex-US real return (USD): 4.3%; terminal wealth gap vs US-only: >12x after 124 years. Japan peaked at 41% of world equity index (late 1980s); fell to 6% by 2024 and remains below 1989 peak — worst DMS market from 1990–2023.

- Supporting evidence: DMS Global Investment Returns Yearbook 2024 Summary Edition (Dimson, Marsh, Staunton). Corroborates KG-20260813-FIE-002 (No Fixed ERP) from a different mechanism (country selection bias vs. TWIG regime dependence): both independently argue against using US historical ERP as a universal or stable forward-looking anchor.

- Applicable environment: When setting portfolio return assumptions for equity: use global DMS evidence (~4.3% real, ~4.7% nominal above bills globally) as the baseline, not US-only historical data (6.5% real). When evaluating whether a stock is "cheap vs. historical ERP": note that the relevant comparison depends on which country's ERP history is cited; US-only figures overstate global expectations. When constructing globally diversified portfolios: 4.3% global equity premium vs cash is the defensible long-run anchor; anything materially above this requires a country-specific or structural justification.

- Non-applicable environment: Does not provide a better point estimate of the FORWARD-LOOKING ERP — DMS explicitly cautions that even the global historical average may not equal future returns. Not applicable to short-term market timing or options pricing. Does not address within-country variation (sector, size, style premiums). Does not argue that US equities will underperform going forward — only that using US historical ERP as the forward-looking universal estimate overstates precision.

- Prohibited use: Do not use to claim US stocks are definitely overvalued at current valuations. Do not use the global 4.3% figure as a fixed annualized target without acknowledging regime and country dependence. Do not cite to discourage international diversification — World ex-US returns are still positive; the point is that US outperformance was not guaranteed ex-ante and may not repeat.

- Evidence strength: Strong — DMS is a 25-year, 35-market, academic-authored dataset; Dimson, Marsh, and Staunton are PhD-level finance researchers at Cambridge and LBS whose work is published in JF, JFE, RFS, and JPM; DMS dataset is standard in institutional and academic asset-class return research. Cross-country variation and success bias warning are replicated across multiple editions of the Yearbook. Second independent source for KG-20260813-FIE-002.

- Last review date: 2026-08-14.

- Revalidation trigger: Update when a newer DMS Yearbook edition (2025 or later) provides updated cross-country return tables; or when the full 2024 Yearbook becomes publicly available (Chapters 2, 6 have comprehensive multi-country ERP tables not in the Summary Edition).

- Source: Dimson, Marsh, Staunton. "UBS Global Investment Returns Yearbook 2024 — Summary Edition." UBS AG, 2024. Full daily note: research/books/2026-08-14-dms-global-investment-returns-yearbook-2024.md.


## KG-20260814-RERP-001: ERP Is Time-Varying; Rolling 20-Year US Excess Returns Range +20.7% to -10.1%, and Forward ERP Must Be Recomputed From Current Valuation and Real-Rate Inputs

- Rule ID: KG-20260814-RERP-001

- Core conclusion: The equity risk premium is not a fixed historical constant. The CFA Research Foundation monograph "Rethinking the Equity Risk Premium" records that rolling 20-year US stock-bond excess returns ranged from +20.7% to -10.1% between 1900 and 2010, and consecutive 10-year excess returns had -38% serial correlation. Ilmanen cites Cochrane's 2011 Journal of Finance presidential address for the modern consensus reversal: variation in price-dividend ratios is attributed to expected-return/discount-rate variation, not dividend-growth forecasts. Forward ERP should be estimated from current inputs, not copied from a 5-6% historical average: ERP = D/P + buybacks + real EPS growth - real bond yield.

- Mechanism: Starting valuation dominates 5-10 year forward equity returns because a high price paid for each dollar of cyclically adjusted earnings mechanically lowers future returns. DDM components vary with dividend/buyback yield, real growth expectations, and real yields. Investor risk aversion also varies across crash and bull-market regimes. Inflation affects valuations nonlinearly: P/E10 is highest around the 1-4% inflation "sweet spot" and contracts under deflation or inflation above roughly 5%.

- Applicable environment: Long-horizon portfolio return assumptions; market-wide valuation context; reports that cite "historical ERP" as a reason to buy or hold equities; inflation-regime valuation discussion; CAPE/E10-P based 5-10 year return framing. Use current dividend yield, buyback yield, real EPS growth, and real Treasury/TIPS inputs when making ERP statements.

- Non-applicable environment: Short-term trading windows measured in days or weeks; single-stock entry/exit decisions; options pricing; any report that needs a precise point estimate without uncertainty bands.

- Prohibited use: Do not use the rolling 20-year range as a direct buy/sell signal. Do not conclude stocks are automatically cheap because a prior 30-year realized excess return was low. Do not apply the 2011 DDM estimate directly to current markets without recomputing the inputs.

- Evidence strength: Strong — CFA Research Foundation monograph with named institutional contributors and peer-reviewed corroboration from Cochrane (2011, Journal of Finance).

- Last review date: 2026-08-14.

- Revalidation trigger: Update when newer long-run ERP research revises the rolling ERP range, serial correlation, or DDM forward ERP framework; recompute numerical forward ERP assumptions with current D/P, buybacks, real EPS growth, and real yields.

- Source: Hammond, Leibowitz, and Siegel, eds., "Rethinking the Equity Risk Premium," CFA Research Foundation, 2011; chapters by Arnott, Ilmanen, Dimson/Marsh/Staunton, Mehra, and Siegel; Cochrane, "Discount Rates," Journal of Finance 66(4):1047-1108 (2011). Full card: research/knowledge/cards/KG-20260814-RERP-001.json.


## KG-20260814-DMS-002: Corporate Credit Risk Premium: US IG Annualized Premium 0.76% Over 124 Years; HY 2.0% Above IG; Credit Has Statistically Significant Alpha vs Duration and Equity Premiums

- Rule ID: KG-20260814-DMS-002

- Core conclusion: US investment-grade corporate bonds have earned a net credit risk premium of approximately 0.76% per year over duration-matched Treasuries across 124 years (1900–2024). High-yield bonds earned approximately 2.0% above IG (1988–2014). Critically, the credit premium carries a statistically significant alpha after controlling for bond maturity premium and equity premium — it is a genuinely distinct return source, not an artifact of duration or equity risk loading. Loss rates (not default rates) are the correct measure: IG ~0.2%; HY ~2.7% per year. The fallen angels anomaly (IG→HY downgraded bonds outperforming) has persisted for 10+ years post-publication. The credit spread average (1.58%) and its standard deviation (0.73%) provide reference points for interpreting premarket spread moves.

- Mechanism: Corporate bonds trade at yield spreads above equivalent-maturity government bonds to compensate for: (1) expected credit loss = default probability × (1 - recovery rate); (2) credit risk premium = compensation for uncertainty about future credit losses, which cluster in recessions and equity bear markets (serial default correlation ρ=0.63). The net credit premium equals the yield spread minus expected credit loss rate (spread ~1.58%, loss ~1.0% historically → net ~0.58-0.76% empirically). Asvanunt and Richardson (2017) confirmed a statistically significant alpha after regressing credit excess returns on both the bond maturity premium and the equity premium — credit is a genuinely distinct factor. Fallen angels mechanism: IG-mandate funds are forced to sell bonds after downgrade regardless of valuation → price pressure → subsequent mean reversion favors buyers.

- Key data: US IG credit spread (1865–2023): average 1.58%, standard deviation 0.73% (GLSS 2011 updated). US IG credit premium (1900–2024, 124 years): 0.76% annualized; arithmetic mean excess return 0.69%; standard deviation 4.2%; year-by-year range: -17.1% (2008) to +17.9% (2009). Loss rates (Moody's 1983–2022): IG ~0.2%; HY ~2.7%; all corporate ~1.0%. HY credit premium above IG (Bloomberg-Barclays 1988–2014): 2.0%. Optimal mean-variance credit weight (Asvanunt-Richardson, in-sample): ~48% (vs. 35% Treasuries, 17% equities). Fallen angels: ~6.6% annual underperformance in 2 years post-downgrade; effect persists 10+ years post-Ilmanen (2011). Worst single-year default cluster: 1873-75 railroads (36% cumulative 3-year); worse than Great Depression (13% worst 3-year).

- Supporting evidence: Multi-source: (1) Giesecke-Longstaff-Schaefer-Strebulaev (2011, "Corporate Bond Default Risk: A 150-Year Perspective"): US credit spread and default data 1865–2010, updated to 2023 in DMS. (2) Moody's (2023): credit loss rates 1983–2022, by rating tier. (3) Coyle-Turnbull UK data, updated to 2023: UK corporate bond returns since 1860. (4) Bloomberg-Barclays US Corporate High Yield Index (1988–2014). (5) Asvanunt-Richardson (2017): alpha test, mean-variance weights. (6) Ilmanen (2011, 2022): fallen angels anomaly persistence. Multiple independent datasets, multiple time periods, multiple countries.

- Applicable environment: When evaluating expected return contribution from a corporate bond allocation: IG adds ~0.76% per year above Treasuries (gross, before transaction costs); HY adds ~2.0% above IG (gross). When interpreting credit spread moves in premarket: the average US IG spread is ~1.58% historically (std 0.73%); widen >2.3% (1 std dev above mean) = elevated credit stress; contraction below 0.85% = compression/tight conditions. When assessing fallen angels: post-downgrade recovery creates a return pattern that institutional mandates cannot capture but retail investors can (price pressure → mean reversion).

- Non-applicable environment: The 0.76% credit premium is for a well-diversified IG corporate bond portfolio — single-issuer credit risk has much higher variance and idiosyncratic default risk. The mean-variance optimal weight of 48% credit is in-sample optimization and likely overstated out-of-sample. Credit premium estimates require duration-adjusted returns; if comparing corporate bonds to government bonds without duration matching, the credit premium estimate is contaminated by the maturity premium.

- Prohibited use: Do not use the 0.76% credit premium or 1.58% average spread as a fixed constant to mechanically judge current portfolio yield contribution — current spread levels may be well above or below the long-run average and reflect current cycle positioning. Do not use the 48% mean-variance credit weight as a direct portfolio recommendation (in-sample only; credit crises produced -17.1% year credit excess return in 2008). Do not use fallen angels anomaly for single-issuer bets — documented for diversified baskets, not individual fallen angel bonds.

- Evidence strength: Strong — multiple independent datasets (GLSS US 1865-2023; UK 1860-2023; Moody's 1983-2022; Bloomberg-Barclays 1988-2014; Asvanunt-Richardson alpha test). Multi-source confirmation across multiple countries and time periods meets the two-source standard. DMS synthesis of this evidence is authoritative (25-year Yearbook, LBS/Cambridge authors).

- Last review date: 2026-08-14.

- Revalidation trigger: Update if a post-2024 long-run credit study shows the 0.76% IG credit premium has changed materially; or if a new multi-country credit premium meta-analysis revises the global estimate. Credit spread reference level (1.58% avg, 0.73% std) should be verified annually against updated GLSS/Moody's/Bloomberg-Barclays data.

- Source: Dimson, Marsh, Staunton. "UBS Global Investment Returns Yearbook 2024 — Summary Edition," Chapter 9/10. UBS AG, 2024. Synthesizes GLSS (2011), Moody's (2023), Coyle-Turnbull UK data, Bloomberg-Barclays HY, and Asvanunt-Richardson (2017). Full daily note: research/books/2026-08-14-dms-global-investment-returns-yearbook-2024.md.

## KG-20260817-BEHAV-OT-001: Individual-Investor Overtrading Systematically Erodes NET Returns (Turnover + Aggressive Orders + Transaction Costs); A Profitable Plan-Violating Round-Trip Is Outcome Bias, Not Evidence That Active Trading/Adding Pays

- Rule ID: KG-20260817-BEHAV-OT-001

- Core conclusion: Active trading by individual investors systematically destroys NET (after-cost) returns, and the loss traces to turnover and aggressive (liquidity-demanding) orders rather than to bad stock picks. (1) Barber & Odean (2000): across 66,465 U.S. discount-broker households (1991–1996), GROSS returns were roughly market-level, but the average household earned NET 16.4%/yr vs. the market's 17.9%, and the households that traded MOST earned only NET 11.4%/yr vs. 17.9% — a ~6.5 pp gap driven almost entirely by transaction costs (commissions + bid-ask spread); average turnover ~75%/yr; overconfidence drives the excess trading. (2) Barber, Lee, Liu & Odean (2009): using the COMPLETE population of Taiwan investors (1995–1999), the aggregate individual portfolio suffered a 3.8 pp/yr penalty (~2.2% of Taiwan GDP), virtually all traceable to AGGRESSIVE (marketable) orders, while institutions gained +1.5 pp/yr — losses transfer from individuals to institutions. Corollary (outcome-bias / "resulting" guard): because the base-rate distribution of active individual round-trips is net-negative, a single profitable plan-violating trade is a favorable draw, NOT evidence that trading or adding pays; discipline must be rule-based and must not be updated by one lucky outcome.

- Mechanism: Overconfidence → excessive trading and aggressive marketable orders. Each round-trip pays bid-ask spread + commissions + market impact; since gross returns are ~market-level, these costs compound directly into net underperformance that scales with turnover. Aggressive orders additionally suffer adverse selection (demanding liquidity from better-informed counterparties). Cumulative cost drag grows with trading frequency, independent of any single trade's outcome; treating one winning violation as validation is outcome bias.

- Applicable environment: Small retail account weighing an impulsive/same-day round-trip or an add outside the pre-committed plan; auditing a profitable trade that violated a premarket decision (e.g., buy 0 / no-add on an over-concentrated name — grounds RULE-20260817-01, re-run of FAILED_IDEAS 2026-08-01 MU concentration lesson); judging whether high turnover adds value (default: net cost drag absent a demonstrated edge); enforcing the rule-based buy gate (standing-quant-math-gate — impulse trades without an EV/Kelly math block are exactly this pattern); postmarket separation of net-of-cost outcome from decision quality.

- Non-applicable environment: Rule-based low-frequency risk management (concentration de-risk trims, invalidation-level exits, profit-lock sells) — plan-consistent, not overtrading, and not to be discouraged; investors with a demonstrated documented edge (a minority show skill/persistence — Coval-Hirshleifer-Teoh; Ivković-Sialm-Weisbenner informed concentration); institutional / passive limit-order (liquidity-providing) strategies, which the Taiwan study finds profitable; scheduled long-horizon rebalancing.

- Prohibited use: Not a directional buy/sell or market-timing signal (it governs TRADING FREQUENCY / discipline). Do not let a profitable plan-violating trade relax the no-trade/no-add/concentration discipline (outcome bias). Do not read as "never trade" — disciplined rule-based de-risking and invalidation exits are encouraged; the target is impulsive, overconfident, aggressive-order overtrading. Do not apply the penalty to institutions or a demonstrated-edge strategy.

- Contrary evidence: A minority of individuals show skill/persistence (Coval-Hirshleifer-Teoh; Ivković-Sialm-Weisbenner informed concentration), and some high trading frequency can be rational for the informed — but conditioned on a demonstrated edge; the aggregate/average result is robust and losses concentrate in aggressive orders. Contradiction note: research/contradictions/2026-08-17-overtrading-vs-informed-trading.md.

- Evidence strength: Strong — two independent Tier-2 peer-reviewed studies (JF 2000; RFS 2009), clear cost mechanism, out-of-sample confirmation (Taiwan whole population; also Barber-Odean 2001 "Boys Will Be Boys" within the US).

- Last review date: 2026-08-17.

- Revalidation trigger: Peer-reviewed evidence that individual-investor net trading losses have materially reversed in the modern zero-commission era (post-2019); OR credible evidence this account has a demonstrated intraday/active-trading edge (then the informed-trader boundary applies). Zero commissions remove one cost layer but bid-ask spread, market impact of aggressive orders, and adverse selection remain — verify before relaxing.

- Source: Barber & Odean, "Trading Is Hazardous to Your Wealth: The Common Stock Investment Performance of Individual Investors", Journal of Finance 55(2):773–806 (2000); Barber, Lee, Liu & Odean, "Just How Much Do Individual Investors Lose by Trading?", Review of Financial Studies 22(2):609–632 (2009). Full daily note: research/daily/2026-08-17.md.

## KG-20260818-COCH-001 / KG-20260813-FIE-002 (admitted 2026-08-18): Equity Risk Premiums Are Substantially Time-Varying; P/D Ratio Predicts Multi-Year Excess Returns; All Price-Dividend Variation Corresponds to Discount-Rate Variation; There Is No Fixed ERP

- Rule IDs: KG-20260818-COCH-001 (Cochrane 2011 mechanism card); KG-20260813-FIE-002 (FIE-002 upgraded to admitted)

- Core conclusion: Expected equity risk premiums (ERPs) vary substantially over time — by as much as their long-run mean — and are regime-dependent. Key empirical facts from three independent sources: (1) Cochrane (2011, Journal of Finance): The aggregate dividend yield (D/P ratio) forecasts excess U.S. stock market returns at 1yr and 5yr horizons: R²=0.09 at 1yr (b=3.8, t=2.6); R²=0.28 at 5yr (b=20.6, t=3.4); σ[E_t(R^e)] ≈ 5.46%/yr — as large as the historical equity premium mean of ~6%. All P/D ratio variation corresponds to discount-rate variation (long-run return forecast coefficient b_r ≈ 1.0); none corresponds to expected dividend growth variation (b_Δd ≈ 0). The same pattern holds across ALL asset classes: Treasury bonds, corporate bonds, foreign exchange, sovereign debt, and housing. Business cycle association: low prices/high ERP in bad times (high unemployment, contracting output); high prices/low ERP in expansions. (2) Dimson, Marsh, Staunton (2024): Cross-country ERP variation — US ERP vs bills = 4.7%, Switzerland = 2.6%, global = 4.3%; US went from 0% to 60.5% of world market cap, confirming success bias in long-run historical average. (3) Taylor (2026, CFA RF): Historical 900yr/25-country ERP variation by macro regime; realized US 10yr ERP ranged from +20% (1950s) to -10% (early 2000s), returning to double digits in 2020s. Conclusion: There is no single, stable equity risk premium; using a fixed long-run historical average as the forward-looking ERP is unreliable and regime-inappropriate.

- Mechanism: ERP variation reflects time-varying risk aversion driven by the macroeconomic cycle. Campbell-Cochrane (1999) habit formation: when consumption declines near the habit level, the surplus-consumption ratio falls, risk aversion rises sharply, investors demand a higher equity premium — generating the countercyclical ERP pattern. The present-value identity (Campbell-Shiller 1988) forces all P/D variation = discount-rate variation because dividend growth has near-zero predictability from the D/P ratio. In bad economic times, the ERP spikes; in expansions it compresses. Coordination across asset classes (credit spreads + equity ERP spike together during 2008) is consistent with macro risk-aversion explanation and inconsistent with purely behavioral or segmented-market explanations.

- Quantitative benchmarks: σ[E_t(R^e)] ≈ 5.46%/yr (as large as the 6% ERP mean); 5yr return R² = 0.28; US ERP vs bills: 4.7% (DMS 2024, 1900–2023); global ERP vs cash: 4.3% (35 countries). Realized US 10yr ERP ranged +20% to −10% by decade.

- Applicable environment: (1) Multi-year valuation regime context: when current market P/E or D/P is at historically extreme levels, the forward-looking multi-year ERP is correspondingly elevated or depressed — use as regime-awareness context for 1-5yr expected returns. (2) When market reports cite a fixed "6% equity premium" as a constant input — flag that it spans multiple distinct regimes and is unreliable at any specific point in time. (3) When evaluating long-run equity return assumptions in portfolio construction or macro regime analysis. (4) Credit spreads (BAA-AAA, HY-IG) widening simultaneous with equity declines → consistent with coordinated macro ERP spike (see COCH-002, now admitted 2026-08-19).

- Non-applicable environment: Intraday or monthly timing — ERP predictability operates at 1-5yr horizons (R² near zero at sub-6-month horizons). Does not provide a better ERP estimate to replace the historical average — it constrains overconfidence in any single estimate. Not a mechanism for predicting specific earnings or cashflow changes.

- Time scale: Multi-year valuation and regime context (1–5yr horizon). Not a same-day or monthly timing tool.

- Use in premarket reports: Use current P/D, E/P, or yield-spread context to identify whether the market is in a high-ERP (high forward expected returns) or low-ERP (low expected returns) regime. Do not override intraday price action or event catalysts based on multi-year ERP context. Do not assert a specific ERP number as the expected forward return — present as a range and regime-dependent estimate.

- Prohibited use: Do not use current P/D or P/E ratios as a short-term buy or sell trigger — evidence applies to 1-5yr horizons only. Do not declare markets "cheap" or "expensive" in premarket reports without noting the multi-year horizon caveat and the regime-dependence. Do not let ERP regime context override current position risk limits, concentration rules, or invalidation-level exits.

- Evidence strength: Strong — three independent multi-source supporting studies: Cochrane (2011) JF peer-reviewed presidential address (cross-asset OOS validation across stocks/bonds/FX/houses); Dimson-Marsh-Staunton (2024) 35-country 124-year institutional study; Taylor (2026) 900yr/25-country historical dataset. Two conditions satisfied: (a) two or more independent reliable studies; (b) one high-quality study (Cochrane 2011) with clear OOS validation across multiple asset classes and plausible mechanism.

- Contrary evidence: Welch and Goyal (2008, Review of Financial Studies) argue that most return predictors fail OOS in real-time forecasting exercises. Cochrane (2011) addresses this: the economic significance (σ[E_t(R^e)] ≈ 6%) is robust even when individual OOS R² is low; the question is "how much do expected returns vary?" not "can we beat a naive forecast?". Goyal-Welch OOS failures do not negate the existence of ERP variation; they constrain the precision of any specific quantitative forecast.

- Last review date: 2026-08-18.

- Revalidation trigger: Peer-reviewed study showing P/D ratio return predictability has broken down in the modern era (post-2010 passive-dominated, zero-commission markets) — verify σ[E_t(R^e)] is still ≈ its historical mean. OR credible meta-analysis showing historical ERP has stabilized (e.g., structural break test finding regime homogeneity post-2000).

- Sources: Cochrane, John H. "Presidential Address: Discount Rates." Journal of Finance 66(4):1047–1108 (2011). Author-posted PDF at johnhcochrane.com. Full daily note: research/books/2026-08-18-cochrane-discount-rates-jf-2011.md. Independent corroboration: Dimson, Marsh, Staunton (DMS-001 / KG-20260814-DMS-001); Taylor (FIE-002 / KG-20260813-FIE-002).

## KG-20260818-COCH-002 (admitted 2026-08-19): Cross-Asset ERP Coordination During Macro Crises — Simultaneous Credit Spread Widening, Equity Risk Premium Spike, and Macro Contraction Reflect Financial Intermediary Capital Impairment, Not Isolated Market Failures

- Rule ID: KG-20260818-COCH-002

- Core conclusion: During severe macro crises, risk premiums spike simultaneously across credit markets, equity markets, and (with single-source documentation) FX/sovereign markets. This coordination is not a coincidence of isolated sector failures — it reflects a common underlying driver: a sharp rise in macro risk aversion and/or financial intermediary capital impairment. Two independent Tier-2 peer-reviewed sources confirm the credit-equity-macro coordination dimension: (1) Cochrane (JF 2011): Figures 12-14 document that the BAA-AAA credit spread and the S&P 500 P/D ratio move together sharply during the 2008 financial crisis; CDS-Treasury basis violations and covered interest parity failures confirm cross-market linkages consistent with macro risk-aversion models. (2) Gilchrist-Zakrajšek (AER 2012): a VAR shows that a 20 bps shock to the Excess Bond Premium (EBP — the non-default component of credit spreads) causes GDP to fall 0.5 pp below trend at 5 quarters AND the equity market to decline 7 pp cumulative; EBP explains >10% of output variation and >25% of investment variation at business cycle frequencies. Broker-dealer CDS spreads co-move closely with EBP (Figure 8), confirming the financial intermediary transmission channel. Scope boundary: FX/sovereign coordination (CIP failures, covered interest parity violations during 2008) is documented by Cochrane (2011) alone and is not independently quantified in GZ (2012); apply with lower confidence for FX-specific coordination claims.

- Mechanism: Two complementary channels operate simultaneously in macro crises. (a) Macro risk-aversion channel (Campbell-Cochrane 1999 habit formation): when consumption falls toward the habit level, surplus-consumption ratio falls, risk aversion rises sharply across all investor types, raising the stochastic discount factor volatility and driving up ERP for all risky assets at once — the coordinated spike is a structural property of the pricing kernel, not individual market failures. (b) Financial intermediary capital impairment channel (Bernanke-Gertler 1989; Kiyotaki-Moore 1997; He-Krishnamurthy 2010): when intermediaries face capital impairment (losses, deleveraging, funding stress), their effective risk-bearing capacity falls, they demand higher compensation above expected default loss (EBP rises), reduce credit supply, and sell assets across markets simultaneously — creating coordinated price moves in credit and equity. Both channels generate the same cross-asset signature; macro risk-aversion explains the scale and macro co-movement; intermediary frictions amplify and accelerate the coordination.

- Quantitative benchmarks: (a) 1 SD EBP shock (~20 bps) → cumulative equity market decline of ~7 pp (VAR, Gilchrist-Zakrajšek 2012); (b) EBP peak of 275 bps in October 2008 (Lehman Brothers collapse); (c) EBP explains >10% of output variance, >25% investment variance at business cycle frequencies; (d) EBP correlates with broker-dealer 1yr CDS spreads through 2003-2010 (Figure 8, striking comovement); (e) BAA-AAA spread and S&P 500 P/D ratio spike together in 2008 (Cochrane 2011, Figure 12); (f) the overall scale of coordinated cross-asset ERP moves (σ[E_t(R^e)] ≈ 5.46%/yr per COCH-001) is too large to explain by intermediary frictions alone — macro risk-aversion is required.

- Applicable environment: (1) When multiple simultaneous signals appear — equity P/E spike, credit spread widening (BAA-AAA or HY-IG widening beyond what rising default risk alone justifies), FX basis widening (EUR/USD or USD/JPY cross-currency basis >20 bps), AND VIX surge — treat as macro ERP event requiring review of ALL holdings, not just the triggering asset. (2) When premarket observes equity weakness AND credit spread widening simultaneously: weight economic slowdown risk significantly, increase position scrutiny. (3) When distinguishing sector-specific shocks (single asset class moves) from macro shocks (credit + equity + economic activity all worsen together). (4) Supports interpretation of EBP-type widening: if Baa-Aaa rises faster than VIX or default risk alone explains, the excess is consistent with a macro ERP event.

- Non-applicable environment: Idiosyncratic sector shocks — if only equity moves but credit is calm, not a macro coordination event. Central bank intervention periods — Fed swap lines and QE can suppress cross-asset coordination by injecting liquidity and reducing intermediary stress (swap lines standing since Oct 2013 with major CBs; see CGFS63-002). Moderate volatility regimes — cross-asset coordination is diagnostic in severe drawdown environments (VIX >30, Baa-Aaa >200 bps); mild widening is not reliable. Intraday or day-trading — the coordinated ERP spike develops over weeks to quarters.

- Time scale: Crisis onset diagnosis and multi-week to multi-quarter position review. Not an intraday or daily timing tool.

- Use in premarket reports: When multiple asset classes show simultaneous stress (equity + credit + FX), identify this as a possible macro ERP event and recommend reviewing all concentrated positions. Do not declare a macro ERP event from equity weakness alone — require corroborating credit and/or FX evidence. Do not use as a mechanical sell trigger without checking whether central bank intervention has already begun to suppress the coordination signal.

- Prohibited use: Do not apply as a mechanical sell trigger (e.g., "BAA-AAA widens by X bps → sell all positions") without additional confirmation of context. Do not confuse the Baa-Aaa spread with the EBP — they are related but different; Baa-Aaa contains expected-default risk that EBP explicitly strips out. Do not treat the cross-asset coordination pattern as permanent — it mean-reverts as macro conditions stabilize.

- Evidence strength: Strong — two independent Tier-2 peer-reviewed sources with complementary methods: Cochrane (2011) JF Presidential Address (cross-asset descriptive analysis, theoretical mechanism, 2008 crisis documentation); Gilchrist-Zakrajšek (2012) AER (VAR quantification of EBP-equity-GDP coordination over 37 years, 7 recession cycles, with financial intermediary transmission evidence). Two conditions satisfied: (a) two or more independent reliable studies; (b) both provide plausible, theoretically consistent mechanisms. Scope limitation: FX/sovereign coordination remains single-source (Cochrane 2011).

- Contrary evidence: Philippon (2009, "Bond Market's q") argues that credit spreads can predict economic activity through a frictionless fundamental-signal channel (bond prices incorporate future cashflow news better than equity); however, GZ (2012) directly addresses this by showing the non-default component (EBP) drives most prediction, which is inconsistent with a purely frictionless cashflow-signal story and more consistent with the credit-supply/intermediary channel. Cochrane (2011) notes that intermediary frictions contribute to cross-asset spikes but cannot drive the overall scale of coordinated ERP moves — both channels are needed.

- Last review date: 2026-08-19.

- Revalidation trigger: Peer-reviewed study showing the credit-equity-macro coordination pattern has broken down in passive-dominated or post-2015 markets (e.g., Fed backstops permanently suppress the signal); OR second peer-reviewed study quantifying FX/sovereign ERP coordination magnitude in a post-2010 macro crisis.

- Sources: (1) Cochrane, John H. "Presidential Address: Discount Rates." Journal of Finance 66(4):1072-1079 (2011). Full daily note: research/books/2026-08-18-cochrane-discount-rates-jf-2011.md. (2) Gilchrist, Simon, and Egon Zakrajšek. "Credit Spreads and Business Cycle Fluctuations." American Economic Review 102(4):1692-1720 (2012). Full daily note: research/books/2026-08-19-gilchrist-zakrajsek-credit-spreads-2012.md. Cross-references: KG-20260818-COCH-001 (ERP time-variation mechanism); KG-20260819-GZ-001 (EBP measure candidate); KG-20260812-CGFS63-002 (CIP deviation mechanism).

## KG-20260812-CGFS63-003 (admitted 2026-08-19): Structural Natural Rate of Interest Decline — Trend r* Has Declined ~1-2 pp from Historical Average; Two Tier-1 Sources Confirm Pattern Persisted Through 2022:Q4; Era of Historically Low r* Has Not Ended as of End-2022

- Rule ID: KG-20260812-CGFS63-003

- Core conclusion: The natural rate of interest (r*) in the United States and other advanced economies experienced a structural decline of approximately 1-2 percentage points from its pre-2007 historical average. This decline — driven by demographic aging, productivity slowdown, and increased safe-asset demand — was not reversed by the COVID-19 pandemic or the subsequent 2022-2023 rate normalization cycle. Two independent Tier-1 sources confirm the structural decline: (1) BIS CGFS Papers No. 63 (2019): a 23-central-bank working group study cited Holston-Laubach-Williams (2017) estimates showing US r* fell from ~2.5% (pre-GFC) to approximately -0.26 to 1.4% by Q4 2018; Kiley-Roberts (2017) and Chung et al. (2019) estimated ELB binding probability at 20-40% per recession at that level of r*. (2) Holston, Laubach & Williams (2023) FRBNY Staff Report No. 1063: COVID-adjusted HLW model estimated through 2022:Q4 finds: US r* = 0.8% (end-2022) vs. 0.9% (end-2019) — change of -0.2 pp, within estimation error; Canada r* = 1.5% vs. 1.7% (-0.2 pp); Euro Area r* = 0.7% vs. 0.6% (+0.1 pp). Direct quote: "We do not find evidence that the era of historically low estimated natural rates of interest has ended." Five robustness specifications confirm this finding. Scope: covers US, Canada, and Euro Area. UK was dropped from HLW estimation post-2023 due to weakened IS curve reliability.

- Mechanism: Three structural forces drive r* lower: (a) Demographic shifts — aging populations have higher desired savings and lower consumption-smoothing demand for credit, reducing the equilibrium real return on capital. (b) Productivity growth slowdown — lower trend GDP growth (US: 3.3% in 1990 → 1.8% in 2022) reduces the marginal return on investment, lowering r* directly through the growth channel (r* = c·g + z in the HLW model; estimated c ≈ 1.1 for US). (c) Safe-asset demand — global demand for US Treasury securities (reserve currency status, global insurance motive) compresses the z component of r*. The HLW (2023) finding that r* did not rise in 2019-2022 despite large fiscal stimulus and rising government debt implies the z channel was offset by the g decline: lower trend growth partially offset any upward fiscal demand pressure on r*.

- Quantitative benchmarks: US r* secular path: 3.6% (1990) → 2.5% (2007) → 0.9% (2019) → 0.8% (2022). Trend growth: 3.3% (1990) → 2.8% (2007) → 2.1% (2019) → 1.8% (2022). Standard errors on r* are large: US σ ≈ ±1.14-1.57 pp (sample-average to end-sample SE), meaning r* plausibly ranges from approximately -0.76% to 2.36% at end-2022. Previous US recessions required ~5 pp of rate cuts; at r* ≈ 0.8% with 2% inflation target, the maximum conventional-policy easing space is approximately (0.8% + 2%) - 0% = 2.8% — well below the 5 pp historical requirement.

- Applicable environment: (1) When evaluating whether the Fed can handle a future recession with conventional tools only: lower r* implies the ELB binds much sooner than in prior cycles — UMPs (QE, forward guidance) remain necessary toolkit items (cross-reference CGFS63-001). (2) When analyzing long-duration asset valuations: structurally lower r* supports higher P/E multiples because the discount rate for future earnings is lower; a P/E of 20-25x is less extreme vs. fundamentals than it appears using pre-2007 discount rate assumptions. (3) When evaluating KRE/regional bank sector: persistent low r* compresses net interest margins over the long run even if rate normalization provides temporary NIM relief; structural pressure on bank earnings returns when rates eventually re-normalize lower. (4) When comparing current FOMC dot plots (long-run FFR ≈ 2.5-3.5%) to historical averages (pre-2007 long-run FFR ≈ 4-4.5%): the difference largely reflects structural r* decline, not permanent monetary tightening.

- Non-applicable environment: Precise trading signals — r* is a medium-run (5-10 year horizon) latent variable estimated with large uncertainty; it cannot support quarter-to-quarter trading decisions. Current cycle peak: the 2022-2024 rate normalization shows the Fed successfully raised the FFR to 5.25-5.5% without ELB binding, suggesting r* may be temporarily higher than 0.8% due to fiscal stimulus or inflation-risk premium; the admitted finding applies to the structural trend, not to the short-run level. Post-2022:Q4 data gap: HLW (2023) covers through 2022:Q4; any material development in 2023-2026 (AI productivity boom, sustained fiscal expansion, demographic shift reversal) could alter the structural r* path.

- Time scale: Multi-year to multi-decade structural context for portfolio construction, discount rate assumptions, and central bank policy analysis. Not a same-day market signal.

- Use in premarket reports: When Fed communication references the long-run neutral rate or r*: if FFR is materially above 0.8% + 2% inflation = 2.8% real neutral, the stance is restrictive and rate cuts are the eventual path. When evaluating bank sector (KRE) earnings sustainability: low structural r* = NIM compression risk re-emerges when rates normalize back toward structural neutral. Do not use to override live Fed policy signals or current yield curve data.

- Prohibited use: Do not treat 0.8% as a precise r* level — the HLW standard error means the true structural r* could be anywhere from approximately -0.8% to 2.4% for the US at end-2022. Do not use as a definitive argument that FFR must return to zero — post-pandemic fiscal stance, green investment, or AI-driven productivity gains could raise r* in the 2023-2030 period. Do not cite CGFS63 (2019) data alone for current r* estimates — that data ends in 2018; HLW (2023) through 2022:Q4 is the current model estimate.

- Evidence strength: Strong — two independent Tier-1 sources with complementary evidence bases: (1) BIS CGFS63 (2019): 23-central-bank working group meta-analysis citing HLW (2017) and academic ELB studies; (2) Holston-Laubach-Williams (2023) FRBNY SR-1063: primary model developers' post-COVID re-estimation through 2022:Q4, five robustness specifications, two-model check (HLW and LW). Two conditions satisfied: (a) two or more independent Tier-1 reliable studies; (b) both supported by plausible structural mechanisms with cross-economy validation.

- Contrary evidence: Obstfeld (2023) argues fiscal expansion and rising government debt may have permanently raised the neutral rate; the IMF WEO (2023) also noted uncertainty about r* post-pandemic. HLW (2023) model results are inconsistent with a material r* increase through 2022:Q4 — the decline in trend growth offset any z increase from fiscal channels. The debate continues for post-2023 data. Additionally, using the CBO's measure of potential output (rather than the HLW model's endogenous y*) produces substantially more negative r* estimates for 2010-2022, suggesting the HLW baseline may be the more optimistic (higher) r* estimate.

- Last review date: 2026-08-19.

- Revalidation trigger: Federal Reserve, BIS, or IMF published study estimating trend-r* using post-2023 data (2024-2025 vintage) and assessing whether the structural decline persists or whether post-pandemic fiscal expansion, deglobalization, or AI-driven investment demand has permanently raised r*. NY Fed quarterly HLW model data updates are available (next update: Aug 27, 2026) but are not a published validation — monitor for material shift >50 bps in US r* vs. 2022 baseline of 0.8%.

- Sources: (1) BIS CGFS Papers No. 63. "Unconventional Monetary Policy Tools: A Cross-Country Analysis." October 2019 (23 central banks). (2) Holston, Kathryn, Thomas Laubach, and John C. Williams. "Measuring the Natural Rate of Interest After COVID-19." Federal Reserve Bank of New York Staff Report No. 1063. June 2023. Full daily note: research/books/2026-08-19-holston-laubach-williams-rstar-covid-2023.md. Cross-references: KG-20260812-CGFS63-001 (QE/APP toolkit — low r* is the structural rationale); KG-20260819-HLW-001 (complementary: COVID permanently lowered y* level, separate from r* channel); KG-20260814-DMS-001 (global ERP variation; low r* is one mechanism compressing safe yields and supporting equity risk premium).

## KG-20260819-DCA-001: Idle Cash Carries a Systematic Opportunity Cost (Forgone Equity Risk Premium); Lump-Sum Deployment Beats Prolonged Dollar-Cost Averaging On Average (~2/3 of the Time) — But Staging Is a Legitimate Risk-Tolerance Compromise and Must Not Override Risk Gates

- Rule ID: KG-20260819-DCA-001

- Core conclusion: A large idle cash balance imposes a systematic opportunity cost equal to the forgone equity risk premium (ERP), and when cash is to be deployed toward a target allocation, deploying sooner (lump-sum, LSI) is on average superior to spreading it out via prolonged dollar-cost averaging (DCA). (1) Constantinides (1979) proves DCA is a deterministic, state-independent policy that is suboptimal under standard expected-utility assumptions (it ignores arriving information and delays exposure to a positive-expected-return asset). (2) Rozeff (1994) shows that, after risk adjustment, LSI is superior to DCA whenever the ERP is positive, and the longer the averaging period the larger the DCA underperformance. Empirical corroboration: Williams & Bacon (1993) — LSI beat DCA for ALL S&P 500 periods 1926–1991 (significant at 0.005 in all but one case); Vanguard rolling-window studies (US/UK/Australia, 1976–2022) — LSI beats DCA ~2/3 of the time (61.6%–73.7%) because markets finish positive in ~70% of years. BOUNDARY: LSI's edge is an average and is path-dependent — in a falling deployment window DCA wins (~1/3 of the time), and DCA is a legitimate risk-tolerance / regret-minimizing choice ("taking risk later"). This is a deployment-discipline guardrail against indefinite cash drag, NOT a market-timing or same-day buy signal.

- Mechanism: A positive ERP means equities have higher expected return than cash; every dollar held in cash instead of the target risky allocation forgoes that expected excess return, and since markets rise more often than they fall, un-deployed cash usually loses ground. DCA's schedule is deterministic and not state-contingent (Constantinides), keeping capital in cash longer and giving up ERP proportional to the averaging horizon (Rozeff). The ~1/3 of windows that fall are where DCA's later average entry wins; that path-dependence plus risk tolerance / regret aversion are the legitimate reasons to stage. Transaction costs are secondary (whole-share orders ~$0.02); the dominant cost is forgone ERP.

- Applicable environment: Small account carrying a high idle-cash balance (e.g., cash > 40–60% of equity) with no deployment plan — quantify the cash-drag cost and produce a time-bounded, risk-conditioned plan to deploy into a DIVERSIFIED core (grounds RULE-20260818-01 and its cash>60% first-action upgrade). Deciding how to deploy a cash lump toward a target: default bias to get invested sooner unless risk tolerance or a specific near-term risk argues for bounded staging. Reconciling de-risking with re-investment: cash freed by correct concentration trims (KG-20260812-CONC-001) should be redeployed into diversified ETFs (VOO/QQQM), not left idle or returned to single-name concentration. Postmarket audit of persistent under-investment as an operational cost, distinct from correct one-day "do not catch a falling knife" restraint.

- Non-applicable environment: Not a same-day market-timing or buy signal (buys remain risk-conditioned via VIX/dip-staging and approval-gated). When risk gates say wait (broad-base down day without stabilization), not deploying that day is correct (standing-voo-staging / standing-qqqm-staging). Investors whose risk tolerance genuinely favors DCA to minimize regret/sequence risk. Extreme-valuation or known imminent binary-event contexts. Very small residual cash where whole-share minimums make lump-sum impractical.

- Prohibited use: Do not use to justify deploying idle cash into a concentrated single name (redeploy into diversified core per CONC-001). Do not use to override VIX/dip-staging gates or to catch a falling knife. Do not present the ~2/3 LSI win rate as a guarantee (~1/3 of windows DCA wins; risk tolerance is a valid reason to stage). Not a market-timing signal or permission for unapproved buys.

- Contrary evidence: Path dependence (DCA wins in falling windows, ~1/3 of the time); DCA is rational under sufficient risk aversion / regret minimization; small-account whole-share lumpiness and event risk can justify staging. Contradiction note: research/contradictions/2026-08-19-dca-vs-lumpsum-boundary.md.

- Evidence strength: Strong — a mature theoretical principle (Constantinides 1979, JFQA) plus multiple independent empirical confirmations (Rozeff 1994 JPM; Williams-Bacon 1993; Vanguard 1976–2022 across markets) with a clear mechanism (forgone ERP; markets positive ~70% of years). Frequency figures are market/period/risk-tolerance dependent.

- Last review date: 2026-08-19.

- Revalidation trigger: Peer-reviewed evidence that the ERP has turned persistently non-positive (removing LSI's edge); OR a documented shift in the account mandate toward capital preservation making DCA/regret-minimization the stated objective; OR a structural change making whole-share lumpiness dominate deployment.

- Source: Constantinides, "A Note on the Suboptimality of Dollar-Cost Averaging as an Investment Policy", Journal of Financial and Quantitative Analysis 14(2):443–450 (1979); Rozeff, "Lump Sum Investing versus Dollar-Averaging", Journal of Portfolio Management 20(2):45–50 (1994); corroborated by Williams & Bacon (1993, S&P 500 1926–1991) and Vanguard rolling-window studies (1976–2022). Full daily note: research/daily/2026-08-19.md.

## KG-20260819-GZ-001 (admitted 2026-08-20): Excess Bond Premium (EBP) as Financial Sector Risk-Bearing Capacity Gauge — EBP Predicts GDP Decline, Investment Contraction, and Equity Drawdown via Intermediary Capital Channel

- Rule ID: KG-20260819-GZ-001

- Core conclusion: Credit spreads decompose into (1) a predicted-default component (Merton DD, bond characteristics) and (2) a residual Excess Bond Premium (EBP) capturing the pricing of credit risk above and beyond expected defaults. The EBP — not the expected-default component — accounts for virtually all predictive power of credit spreads for economic activity. Key quantitative findings from Gilchrist & Zakrajšek (GZ) 2012 AER: (a) 100 bps EBP increase → 1.5 pp GDP growth decline over subsequent 4 quarters (full sample 1973-2010); (b) in the 1985-2010 sub-sample, expected-default component is statistically insignificant for GDP prediction (β=−0.023), while EBP is highly significant (β=−0.501); paper explicitly states this implies 100 bps EBP → 2 pp GDP decline for this post-deregulation period (p.1710) — apply 2 pp when modeling post-1985 environments; (c) 1 SD EBP shock (~20 bps) in an 8-variable VAR → GDP -0.5 pp at 5 quarters + equity market -7 pp cumulative; (d) EBP explains >10% of output variation, >25% of business fixed investment variation at business cycle frequencies — larger than monetary policy shocks. Formal theoretical mechanism confirmed by He-Krishnamurthy (HK) 2013 AER: intermediaries face equity capital constraint H_t ≤ m·w_t; when specialist wealth falls below threshold, constraint binds → risk premium on intermediated assets (credit spreads) spikes nonlinearly → EBP widens. GZ EBP is directly measuring the HK model's constraint-binding state variable. Crisis recovery: 6-12 months half-life (LTCM 1998: 10 months; subprime 2007-09: ~6 months). EBP peaked at 275 bps in October 2008. [Primary paper re-verified 2026-08-25: all findings confirmed against source; 2 pp subsample figure added.]

- Mechanism: Intermediary capital impairment (equity losses, funding stress, CDS widening) → intermediaries' effective risk aversion rises → demand for higher compensation per unit of credit risk above expected loss (EBP rises) → reduced credit supply across bond and banking sector → lower asset prices + higher cost of external finance → GDP/investment contraction via financial accelerator. The EBP-intermediary capital linkage is confirmed empirically by three co-movement series in GZ: (1) SLOOS diffusion index of bank lending standards tightening; (2) inverse financial sector ROA; (3) average broker-dealer 1yr CDS spreads. The HK (2013) theoretical model provides formal derivation: risk premium = γ · Cov(dc_t/c_t, dR_t); in constrained region, specialist exposure to risky asset αI rises sharply → covariance rises → EBP widens. Capital rebuilds slowly (months), explaining recovery half-lives.

- Applicable environment: When monitoring macro financial conditions alongside equity market: rising FRED EBPUSA (or proxy: Baa-Aaa minus expected-default component rising faster than equity volatility justifies) signals credit supply tightening beyond fundamental risk — premarket reports should increase recession risk weight. When credit spreads widen broadly: distinguish EBP-driven widening (financial sector stress, SLOOS tightening, broker-dealer CDS rising) from fundamental-default-driven widening (unemployment, profit contraction) — EBP-type produces deeper macro contractions. KRE/regional bank sector: bank equity weakness + broker-dealer CDS widening together with rising EBP signals intermediary capital constraint potentially binding; further credit contraction expected. Supports COCH-002 cross-asset ERP coordination: when EBP widens alongside VIX spike and equity P/E compression, treat as macro ERP event requiring position review across all holdings.

- Non-applicable environment: Single-firm or single-sector credit events — EBP is an aggregate measure; idiosyncratic issuer spread widening does not constitute EBP. Short-term (<3 month) market timing — predictive power is at 3-month to 4-quarter horizons, not intraday. Equity ERP estimation — EBP does not directly measure equity ERP; use COCH-001 or FIE-002 for equity ERP context. Post-2010 quantitative magnitude — GZ sample ends September 2010; QE-era structural changes (standing repo facilities, Basel III) may have altered EBP-capital transmission; apply as directional indicator, not precise magnitude signal, for 2011-2026 data.

- Use in premarket reports: When FRED EBPUSA or proxy Baa-Aaa spread is at elevated levels (>100 bps above recent 6-month average): cite GZ-001 as supporting a risk-off bias for credit-sensitive and cyclical exposures; do not use as a same-day buy or sell signal. When Fed cuts rates in a financial crisis: cite HK-001 (candidate) to note that rate cuts are less effective than equity capital injection; watch for TARP-like measures as the more decisive policy intervention. Do not use the 100 bps → 1.5 pp GDP effect as a trading formula — it is a multi-quarter average from a specific historical sample.

- Prohibited use: Do not use as a precise mechanical order-entry trigger (EBP predicts multi-quarter GDP trends, not daily prices). Do not conflate EBP with the Baa-Aaa spread — Baa-Aaa contains large expected-default component that EBP explicitly strips. Do not extrapolate 100 bps → 1.5 pp GDP linearly beyond calibration range.

- Evidence strength: Strong — two independent AER peer-reviewed sources with complementary evidence: (1) GZ (2012): Tier-2 AER empirical, 37-year micro-level bond panel (1973-2010), 5,982 bonds, 1,112 firms, multiple robustness checks, VAR causal identification; (2) HK (2013): Tier-2 AER theoretical model, calibrated to match 1998 LTCM and 2007-09 subprime crises, providing formal mechanism for why EBP works. Admission criteria satisfied: two independent reliable studies (one empirical, one theoretical) from the same peer-reviewed journal with complementary evidence bases.

- Contrary evidence: Post-2012 QE and passive-investment era may have altered EBP-capital transmission (structured products market structure changed dramatically). Basel III regulatory capital requirements increased bank buffers, potentially muting the traditional equity-constraint channel. Standing repo facilities (BTFP 2023) provide direct liquidity support that the HK model's "rate cut" policy cannot fully capture. The HK model cannot explain stock market risk premia directly.

- Last review date: 2026-08-20.

- Revalidation trigger: Post-2012 empirical study extending GZ EBP sample (2010-2026) and confirming predictive power in QE era. FRED EBPUSA available for live monitoring. He-Kelly-Manela (2017 RFS) broker-dealer capital ratio as cross-sectional asset pricing factor would be a significant supporting study. OR evidence of structural break in EBP-GDP predictability after 2010.

- Sources: (1) Gilchrist, Simon and Egon Zakrajšek. "Credit Spreads and Business Cycle Fluctuations." American Economic Review 102(4):1692-1720, June 2012. DOI: 10.1257/aer.102.4.1692. (2) He, Zhiguo and Arvind Krishnamurthy. "Intermediary Asset Pricing." American Economic Review 103(2):732-770, April 2013. DOI: 10.1257/aer.103.2.732 (theoretical mechanism). Full daily notes: research/books/2026-08-19-gilchrist-zakrajsek-credit-spreads-2012.md; research/books/2026-08-20-he-krishnamurthy-intermediary-asset-pricing-2013.md. Cross-references: KG-20260820-HK-001 (theoretical mechanism); KG-20260818-COCH-002 (cross-asset ERP coordination); KG-20260818-COCH-001 (ERP time-variation); KG-20260812-CGFS63-002 (QE/APP toolkit).

## KG-20260820-HK-001 (admitted 2026-08-21): Intermediary Equity Capital Constraint Drives Nonlinear Crisis Risk Premia; Equity Capital Injection Is the Most Effective Crisis Policy

- Rule ID: KG-20260820-HK-001

- Core conclusion: When the marginal investor in intermediated asset markets faces an equity capital constraint (H_t ≤ m·w_t), risk premia exhibit nonlinear behavior: relatively flat in the unconstrained region (~3.14% average risk premium) but spiking sharply when the constraint binds (up to 12% in extreme crisis states). This mechanism is empirically confirmed across seven asset classes simultaneously (equities, US bonds, sovereign bonds, options, CDS, commodities, FX) with a consistent positive price of intermediary capital risk of 9% per quarter (annualized ~36%), statistically indistinguishable in magnitude across all markets. The constraint binding is not rare: 33.5% of the time in the calibrated theoretical model. Crisis recovery takes 6-12 months (LTCM 1998: 10 months; subprime 2007-09: ~6 months). Policy ranking in a pure capital-constraint crisis: (1) equity capital injection most effective (recovery 0.40yr) because it directly relaxes the binding constraint; (2) asset purchase/QE second (0.58yr); (3) rate cut/borrowing subsidy least effective (0.68yr) because it does not address equity scarcity. Scope: all seven major asset classes trade through primary dealer holding companies as marginal investors — the mechanism applies broadly, not just to credit markets.

- Mechanism: The core structural mechanism: households cannot invest directly in complex intermediated assets (MBS, structured credit, sophisticated derivatives) and must route through specialist financial intermediaries. The intermediary can raise external capital only up to m times its own equity stake (moral-hazard constraint). When specialist wealth w_t falls below threshold (constrained region), the specialist must bear more risk personally to clear markets → their marginal pricing of risk rises sharply and nonlinearly → risk premium spikes. The slow recovery reflects that specialist equity wealth rebuilds only gradually through trading profits. Equity injection directly increases the fund size relative to the constraint, most efficiently relaxing the bottleneck. Government asset purchases reduce risky asset supply facing intermediaries (second best); rate cuts reduce borrowing cost but do not address equity scarcity (third best). The empirical counterpart: NY Fed Primary Dealer holding company equity capital ratio η_t = Σ Market Equity / Σ(Market Equity + Book Debt) proxies specialist wealth. Innovations to η_t are AR(1) residuals scaled by lagged ratio (AR(1) ρ = 0.94, very persistent). When η_t falls (during recessions, crises), marginal value of wealth rises → ALL asset classes price the capital risk factor at the same positive price (9% per quarter in 1970-2012 empirical panel). Holding company level is the right unit (not broker-dealer subsidiary) because internal capital markets transmit shocks across divisions.

- Applicable environment: When primary dealer holding company equity is declining broadly (Goldman Sachs, JPMorgan Chase, Deutsche Bank, Citigroup equity prices falling significantly): interpret as possible intermediary capital constraint binding → expect elevated risk premia and wider credit spreads across ALL asset classes simultaneously, not just equities. Supports GZ-001 EBP monitoring: when EBP (FRED EBPUSA) is rising AND primary dealer equity is falling, both channels are consistent with constraint approaching binding state → higher recession risk weight in premarket reports. KRE / regional bank sector: KRE equity weakness signals potential intermediary capital impairment → further credit availability reduction expected via this channel. Fed policy interpretation: when Fed cuts rates but credit spreads remain elevated, HK mechanism predicts this is possible if binding constraint is equity capital, not borrowing cost → equity capital injection (TARP-type) more likely to resolve than additional rate cuts. COCH-002 cross-asset ERP coordination: when VIX, credit spreads, option premia, and commodity risk premia all spike together, the shared intermediary pricing kernel is the mechanism → single unified risk-off interpretation.

- Non-applicable environment: Intraday or same-week trading signals — factor is quarterly frequency only. Individual stock selection — factor explains cross-sectional differences in average returns across sorted groups. Post-2012 quantitative magnitudes — sample ends 2012Q4; Basel III full implementation and standing repo facilities may have changed the effective constraint parameter m and binding frequency. Direct equity market (S&P 500) pricing — HK 2013 theoretical model is explicitly for intermediated assets (MBS, corporate bonds, structured products); HKM 2017 empirical study shows it extends to all asset classes but is weakest for FF25 equities in single-factor tests. Crises driven by pure fundamental default risk — mechanism focuses on the non-default EBP component (equity capital, not credit losses per se).

- Use in premarket reports: When primary dealer equity is falling and EBP is rising simultaneously: apply HK-001 to raise risk weights on all credit-sensitive and volatility-sensitive positions (cite HK-001 and GZ-001 together). When evaluating central bank crisis response: note that rate cuts alone are the least effective tool in an equity-capital-constrained environment (HK-001); look for equity injection signals (TARP-type programs, direct equity injections) as the more decisive policy intervention. When KRE is weakening versus XLF/SPY: the intermediary capital constraint mechanism predicts further credit supply contraction → consistent with reducing KRE position per standing risk guardrail. Do not use the 9% per quarter risk price or the 6-12 month recovery half-life as precise mechanical inputs — they are model/sample averages.

- Prohibited use: Do not cite as evidence that Fed rate cuts are ineffective in recessions generally — mechanism applies specifically to financial crises where binding constraint is equity capital; liquidity crises require different analysis. Do not use to predict exact crisis onset or resolution timing — model gives probability distributions and historical averages. Do not argue against QE — asset purchases do help (second best in model); point is equity injection helps more. Do not use the 9% per quarter risk price as the actual expected risk premium — it is the price per unit of beta, and β_η averages near zero across most assets; only the dispersion in β_η drives cross-sectional expected return differences.

- Evidence strength: Strong — two independent peer-reviewed sources with complementary evidence: (1) He & Krishnamurthy (AER 2013): formal theoretical model, calibrated to LTCM 1998 (10-month recovery, matches) and subprime 2007-09 (~6-month recovery, matches), formal derivation of equity capital constraint, policy ranking, and nonlinear risk premium; (2) He, Kelly & Manela (JFE 2017): 43-year empirical panel (1970Q1-2012Q4), 7 asset classes, 125 portfolios, Fama-MacBeth and GMM cross-sectional tests, multiple robustness checks (pre-crisis, post-1990, monthly frequency, comparison with FF3/FF5/momentum/liquidity factors). Policy ranking (equity injection 0.40yr > asset purchase 0.58yr > rate cut 0.68yr) is still supported by one theoretical source only (HK 2013 calibration); independent empirical TARP causal study would complete two-source for this specific claim. Contrary evidence: AEM (JF 2014) supports debt constraint model for equities and bonds (HKM demonstrates this fails for sophisticated asset classes); Basel III/standing facilities may have changed constraint dynamics post-2012.

- Contrary evidence: AEM (Adrian-Etula-Muir, JF 2014) finds positive price of broker-dealer leverage risk in equities and bonds — contradicts HKM in those two classes specifically, where AEM is empirically stronger (higher R²). HKM resolves this by showing AEM measures a different entity (subsidiary book leverage vs. holding company market equity ratio, only 14% correlated in innovations). Basel III full implementation (2015-2019) increased bank capital buffers, potentially reducing constraint frequency; standing repo facilities (BTFP 2023) provide direct liquidity backstop. Post-2012 data needed to assess whether constraint binding frequency has changed.

- Last review date: 2026-08-21.

- Revalidation trigger: Post-2012 empirical extension of HKM cross-sectional tests (2013-2026 data) confirming 9% per quarter risk price remains stable after Basel III. OR independent empirical study on TARP causal effectiveness vs. rate cuts vs. QE in credit spread normalization speed (for policy ranking two-source). OR structural change in primary dealer composition, FDIC resolution regime, or TLAC requirements that reduces internal capital market relevance within holding companies.

- Sources: (1) He, Zhiguo and Arvind Krishnamurthy. "Intermediary Asset Pricing." American Economic Review 103(2):732-770, April 2013. DOI: 10.1257/aer.103.2.732. (2) He, Zhiguo, Bryan Kelly, and Asaf Manela. "Intermediary Asset Pricing: New Evidence from Many Asset Classes." Journal of Financial Economics 126(1):1-35, October 2017. DOI: 10.1016/j.jfineco.2017.08.002. Daily notes: research/books/2026-08-20-he-krishnamurthy-intermediary-asset-pricing-2013.md; research/books/2026-08-21-he-kelly-manela-intermediary-asset-pricing-new-evidence-2017.md. Cross-references: KG-20260821-HKM-001 (empirical detail candidate); KG-20260819-GZ-001 (EBP time-series channel); KG-20260818-COCH-002 (cross-asset ERP coordination); KG-20260812-CGFS63-001 (QE/UMP toolkit); KG-20260820-OSS-001 (Japan decade-scale case).

## KG-20260821-DIV-001 (admitted 2026-08-21): Cash Deployment Is Not Risk Repair When It Creates a 2-3 Name Concentrated Portfolio

- Rule ID: KG-20260821-DIV-001

- Core conclusion: In a small retail account, moving idle cash into a new concentrated single-name position does not solve the portfolio problem; it substitutes cash drag for under-diversified idiosyncratic risk. Statman (1987, JFQA) shows a randomly selected stock portfolio needs at least 30 stocks for a borrowing investor and 40 for a lending investor to be well diversified. Goetzmann and Kumar (NBER 2001; Review of Finance 2008) examine more than 40,000 U.S. discount-brokerage accounts from 1991-1996 and find a vast majority are under-diversified; in 1994-96, 2-stock portfolios had average Sharpe ratio about 0.34 vs about 0.56 for 15+ stock portfolios. A 2-3 name risky account, or any account with one name above the >20% red line, should therefore be treated as concentrated even when cash is low. Cash freed by de-risking should preferentially go to diversified core exposure such as VOO/QQQM/SPY, not to a new single-name or crypto-proxy concentration.

- Mechanism: Diversification reduces unsystematic/idiosyncratic risk by combining imperfectly correlated stocks. Retail investors often diversify naively by holding several stocks without controlling correlations or weights; overconfidence and active trading are associated with worse diversification. Broad index ETFs implement diversification more efficiently than a small account manually holding 15-40 individual stocks. The relevant control variables are concentration weight and effective risky-name count, not simply the number of tickers or the cash percentage.

- Applicable environment: Small retail account with any single name above the desk red line (>15% warning; >20% default de-risk / buy-0). Account appears invested because cash is low but risky exposure is concentrated in 2-3 names. Cash deployment after prior de-risking: use diversified core ETFs first unless a single-name buy remains below the cap and has documented edge/math. Premarket/postmarket classification of whether cash drag was actually solved or merely transformed into concentration risk.

- Non-applicable environment: Broad market ETFs or mutual funds such as VOO, QQQM, SPY, or total-market funds where one position already contains many underlying securities. Large sophisticated accounts with documented informational edge and explicit lower-Sharpe tolerance. Same-day tactical direction calls; this is a sizing and portfolio-construction rule only.

- Use in premarket reports: If cash is low but one name dominates or effective risky-name count is near 2-3, say the account is still under-diversified and make concentration the first portfolio-construction issue. If an off-plan fill creates >20% single-name exposure, calculate the notional/equity percentage and produce a concrete approval-gated reduce-to-cap draft when appropriate. When applying DCA/cash-drag logic, verify that the destination is diversified core exposure; do not call single-name concentration a successful cash-deployment fix.

- Prohibited use: Do not use this card as a directional sell signal on COIN, MSFT, BJ, or any other ticker. Do not place, modify, cancel, or automate orders from this rule; any action remains a user-approved draft. Do not mechanically require 30-40 individual stocks when a diversified ETF can provide broad exposure. Do not cite the informed-concentration exception to relax limits unless the account has documented edge, large-account risk capacity, and accepts lower Sharpe.

- Evidence strength: Strong empirical — two independent reliable studies plus consistency with existing `KG-20260812-CONC-001` and `KG-20260819-DCA-001`. Contrary evidence: Evans-Archer (1968) argued many diversification benefits are exhausted around 10 stocks, but even that lower threshold does not justify 2-3 names. Ivković-Sialm-Weisbenner (2008) show some concentrated households outperform in mean return, but with larger total risk and lower Sharpe, and the exception requires superior information not present in off-plan chase behavior. Idiosyncratic-risk pricing evidence is mixed and does not override sizing limits.

- Last review date: 2026-08-21.

- Revalidation trigger: Modern zero-commission/fractional-share retail-account replication showing that 2-3 name accounts no longer suffer materially worse risk-adjusted performance; OR strong evidence that idiosyncratic risk is reliably compensated after costs for small retail investors; OR documented change in account mandate accepting lower Sharpe and concentrated idiosyncratic drawdowns.

- Sources: (1) Statman, Meir. "How Many Stocks Make a Diversified Portfolio?" Journal of Financial and Quantitative Analysis 22(3):353-363, September 1987. (2) Goetzmann, William N. and Alok Kumar. "Equity Portfolio Diversification." NBER Working Paper 8686, December 2001; published Review of Finance 12(3):433-463, 2008. Daily note: research/daily/2026-08-21.md. Card: research/knowledge/cards/KG-20260821-DIV-001.json. Contradiction note: research/contradictions/2026-08-21-diversification-vs-concentration-boundaries.md.

## KG-20260821-RR-001 (admitted 2026-08-22): Banking Crises Repeatedly Follow High Capital Mobility; "This Time Is Different" Syndrome Always Precedes New Crisis Waves; Serial Default Is Universal; Center-Country Shocks Transmit Globally

- Rule ID: KG-20260821-RR-001

- Core conclusion: Two-source empirical evidence across 1300-2007 (Reinhart-Rogoff, 66 countries) and 1970-1995 (Kaminsky-Reinhart, 20 countries) establishes that: (1) BANKING CRISES CLUSTER WITH HIGH CAPITAL MOBILITY: periods of high international capital mobility have repeatedly produced international banking crises — the 1825, 1870s, 1890, 1907, 1929, 1930s, 1980-1990s, and 2007-08 episodes all correspond to high capital mobility eras (R-R 2008b Figure 3, Table A3). Independently confirmed by K-R 1999: banking crises per year quadrupled post-financial-liberalization vs. the regulated 1970s; financial liberalization predicts banking crises with p<0.01 in probit regressions; 72% of banking crises in the 1970-1995 sample preceded by liberalization within 5 years. The current era (post-1980) is classified as "high capital mobility" in R-R's framework — banking crisis risk is structurally elevated. (2) "THIS TIME IS DIFFERENT" SYNDROME: every quiet period of 1-3 decades in the historical data has been followed by a new crisis wave. The 2003-2007 calm was pre-GFC TIDS in action. TIDS applies equally to banking crises, sovereign defaults, and inflation episodes. (3) SERIAL DEFAULT: virtually all countries defaulted at least once during their emerging-market phase; Spain ≥13 defaults, France 8, Germany 8, Greece 50.6% of years since 1800 in default; median default duration 6 years (1800-1945) → 3 years (1946-2006). (4) CENTER-COUNTRY SHOCK TRANSMISSION: major global default waves (1820s, 1870s, 1930s, 1980s) traced to center-country shocks (London 1825, US Great Depression 1929, US Volcker disinflation 1980s) transmitted via commodity prices, capital flows, and investor confidence. (5) DOMESTIC DEBT IS NOT A SAFE HAVEN: countries have relied heavily on domestic debt throughout history; domestic defaults cause similar output losses as external defaults.

- Mechanism: Capital mobility mechanism: large capital inflows fund credit booms and asset price appreciation in periphery; when global conditions change (center-country crisis, commodity price reversal, interest rate shock), capital reverses → credit boom collapses → banking crisis. Independently confirmed by K-R 1999 financial liberalization → lending boom → capital inflow reversal → banking crisis chain. TIDS mechanism: long quiet periods reduce financial risk perception → leverage builds → constraint eventually binding → correction more severe. Serial default mechanism: countries in emerging-market development phase have limited institutional capacity to commit credibly to repayment.

- Applicable environment: Capital mobility monitoring — current post-1980 era is "High Capital Mobility" in R-R's framework; banking crisis risk remains structurally elevated. KRE/regional bank weakness is a symptom consistent with banking crisis onset. TIDS risk assessment: when market commentary asserts "we've learned from past mistakes" or "structural changes have permanently reduced crisis risk" — this is the precise TIDS signal, not evidence of safety; apply when credit spreads very tight for extended periods, leverage broadly elevated, EM inflows surging. Sovereign debt monitoring: serial default history shows currently-low-risk borrowers can return to crisis status after quiet periods. Center-country risk transmission: Fed rate hiking cycles are the modern Volcker-type center-country shock; EM crisis risk rises accordingly. Premarket macro risk framing: when banking sector equities (KRE, XLF) are falling alongside credit spread widening and broad risk-off: consistent with historical banking crisis onset pattern in high capital mobility era.

- Non-applicable environment: Short-term or intraday price prediction (all patterns are multi-year/multi-decade); individual company or sector default prediction (database covers sovereign and banking system defaults); post-2008 structural break assessment (central bank backstops — standing repo, emergency liquidity, asset purchases at scale — may have changed transmission); advanced economy sovereign debt default probability for near-term; predicting which asset class recovers first within a crisis (requires HKM-001/HK-001 framework).

- Use in premarket reports: When banking sector equities and EBP are deteriorating simultaneously, reference RR-001 and KR-001 together: banking crisis onset consistent with high-capital-mobility historical pattern; 56% historical base rate for a BOP/currency crisis follow-on within 3 years (K-R 1999). When evaluating EM sovereign exposure: check if financial liberalization within preceding 5 years → elevated banking crisis risk. When market commentary is universally confident ("this time is different"): TIDS signal — raise risk weight on crisis scenarios without predicting exact timing.

- Prohibited use: Do not apply capital mobility → banking crisis correlation as a mechanical timing tool (lag ranges from months to decades). Do not use serial default statistics to argue any specific country will inevitably default. Do not use TIDS to argue all current quiet periods will immediately reverse (quiet periods of 1-3 decades are normal; the framework provides a base rate, not a countdown). Do not extrapolate pre-1980 quantitative magnitudes to post-2023 environment without adjusting for central bank backstop changes.

- Evidence strength: Strong — two-source admission via methodologically independent studies: (1) Reinhart-Rogoff (NBER WP 13882, March 2008): 8-century historical database, 66 countries, 90% of world GDP, historical tabulation and chronology methodology; (2) Kaminsky-Reinhart (AER 1999 / FRB IFDP 544, March 1996): event-study probit regression, 20 countries, 1970-1995. Same capital-mobility-→-banking-crisis conclusion reached via different data and different methodology. Independence: different lead authors (Rogoff vs. Kaminsky), different datasets, different methods, published 12 years apart. Shared author (Reinhart) noted; methodological independence strong. Contrary evidence: post-GFC central bank backstops (standing repo, FDIC guarantees, Basel III buffers) may have structurally changed the crisis transmission mechanism compared to pre-2008 data.

- Last review date: 2026-08-22.

- Revalidation trigger: Post-2008 empirical extension confirming capital mobility → banking crisis correlation remains intact after post-GFC central bank backstop regime change (US 2008, Euro sovereign 2010-12, SVB/SBNY 2023). OR evidence that standing repo facilities, FDIC guarantees, and Basel III buffers have structurally broken the capital mobility transmission mechanism (would require a high-capital-mobility period with significantly fewer banking crises than the historical base rate predicts).

- Sources: (1) Reinhart, Carmen M. and Kenneth S. Rogoff. "This Time Is Different: A Panoramic View of Eight Centuries of Financial Crises." NBER Working Paper No. 13882, March 2008. Full daily note: research/books/2026-08-21-reinhart-rogoff-8-centuries-financial-crises-2008.md. (2) Kaminsky, Graciela L. and Carmen M. Reinhart. "The Twin Crises: The Causes of Banking and Balance-of-Payments Problems." American Economic Review 89(3):473-500, June 1999. FRB IFDP No. 544, March 1996. Full daily note: research/books/2026-08-22-kaminsky-reinhart-twin-crises-1999.md. Cross-references: KG-20260822-KR-001 (second source and twin-crisis sequencing extension); KG-20260820-HK-001 (intermediary capital constraint = micro mechanism of same pattern); KG-20260819-GZ-001 (EBP = early warning indicator); KG-20260818-COCH-001 (TIDS syndrome contributes to credit spread compression during quiet periods); KG-20260812-CGFS63-001 (QE/APP = center-country response to banking crises R-R documents).

## KG-20260820-OSS-001 (admitted 2026-08-23): Japan's 1987-1993 Bubble/Bust — Stable CPI Can Mask Building Financial Instability; Balance-Sheet Adjustment Is the Most Damaging Post-Bubble Mechanism; Monetary Easing Necessary But Not Sufficient

- Rule ID: KG-20260820-OSS-001

- Core conclusion: Two-source evidence (Japan-specific case study + cross-country empirical confirmation) establishes: (1) CPI STABILITY IS NOT SUFFICIENT FOR FINANCIAL STABILITY: financial imbalances can build up while measured consumer price inflation remains low or declining. Japan 1988: CPI was 0.2-0.7% annualized while equity yields implied 8% nominal GDP expectations. Confirmed cross-country by Borio-Lowe (2002): average inflation across 38 crisis episodes in 34 countries shows NO systematic pre-crisis pickup. (2) MULTI-FACTOR BUBBLE FORMATION: Japan's bubble required five amplifying factors interacting simultaneously — neither monetary easing alone nor financial deregulation alone was sufficient. The "chemical reaction" required aggressive bank behavior + protracted monetary easing + land-tax distortion + weak discipline mechanisms + self-confidence narrative operating together. (3) BALANCE-SHEET ADJUSTMENT IS THE MOST ASYMMETRIC POST-BUBBLE MECHANISM: of the three post-bust mechanisms (expectation reversal = symmetric and manageable; resource misallocation = permanent supply-side damage; balance-sheet adjustment = most asymmetric), balance-sheet adjustment is the dominant one. Bank equity erosion → capital constraint binding (HK model) → credit contraction → financial accelerator → prolonged GDP contraction. Damage during bust exceeds gains during boom. NPLs reached ¥44.6 trillion (9% of GDP); public funds for cleanup ¥70 trillion (14% of GDP). (4) TYPE I/TYPE II ASYMMETRY IN MONETARY POLICY: preemptive forward-looking tightening must accept Type I error risk (tightening a non-bubble) to avoid the catastrophic Type II error (missing a bubble). Policy delay of 27 months (discount rate held at 2.5% from February 1987 to May 1989) materially amplified the eventual bust. Key quantitative markers: Nikkei 225 fell 63%+ from peak (¥38,915 end-1989 → ¥14,309 August 1992); land prices fell 80% from peak; capital gains 452% of GDP in 1986-89 vs. capital losses 159% of GDP in 1990-93.

- Mechanism: Five amplifying factors (five-factor "chemical reaction"): (1) Aggressive bank behavior — financial deregulation eroded deposit-rate margins → banks pursued property-related loans; failed banks empirically showed worse ROA years before bubble burst; (2) Protracted monetary easing — market expectation (flat implied forward rate curve through 1988-89) that rates would remain low indefinitely → amplified speculator funding, equity-financed expansion, collateral inflation; (3) Tax/regulation bias toward land accumulation — capital gains tax and inheritance tax rules encouraged holding land; (4) Weak discipline mechanisms — no bank bankruptcies for decades, cross-shareholdings reduced takeover threat, weak accounting disclosure; (5) Self-confidence narrative — "world's largest creditor," Japanese management superiority, Tokyo as international financial center. Post-bust damage through three mechanisms: (a) bullish expectation reversal (symmetric, manageable); (b) resource misallocation / stranded capital (permanent supply-side damage); (c) balance-sheet adjustment — bank equity erosion → HK model capital constraint binding → reduced credit availability → Bernanke-Gertler-Gilchrist (1996) financial accelerator → prolonged recession persisting a full decade as banks worked through NPLs. BOJ-confirmed cross-country mechanism (Borio-Lowe): four pathways by which CPI stays stable during bubble buildup: supply-side improvements (productivity), stabilization program optimism, demand masked by supply gains, CB credibility paradox.

- Applicable environment: (a) CPI monitoring shortfall: when CPI is stable or low BUT credit growth is unusually rapid (credit-to-GDP gap running 4+pp above trend, per Borio-Lowe BL-001) AND asset prices are rising broadly — this combination may indicate building financial instability that CPI monitoring alone will not detect. Apply five risk-profile indicators simultaneously: output gap narrowing + credit acceleration + asset price rise + aggressive lender behavior + risk concentration; (b) KRE/regional bank equity erosion: if regional banks face equity erosion from real estate credit losses, Japan balance-sheet adjustment mechanism predicts prolonged credit contraction persisting until equity rebuilds; reduce KRE position if equity erosion is accelerating; consistent with GZ-001 (EBP widening) and HK-001 (capital constraint); (c) Monetary policy delay risk: if CB is constrained by international policy coordination, currency concerns, or political agendas from tightening when financial indicators are flashing, the Japan case shows delay amplifies the eventual bust; (d) Post-crisis recovery timing: balance-sheet adjustment creates a non-linear recovery path — no normal V-shape when banking system is the damaged institution; recovery requires sustained bank equity rebuild; (e) Broad premarket macro context for US bank/financial sector weakness: when KRE + EBP + credit conditions simultaneously deteriorate, apply OSS-001's Japan mechanism as an institutional parallel (with limitations noted).

- Non-applicable environment: Direct quantitative mapping of Japan's 1990s outcomes to US 2026 — different institutional context (Basel III capital buffers, standing repo, FDIC, QE tools, stronger Fed legal independence, no land-tax distortion equivalent). Single-sector equity bubbles without credit amplification — Japan required simultaneous overheating in stocks, land, AND credit; tech-stock-only bubble without banking system involvement is a different mechanism. Short-term (< 1 year) market timing — macro-structural insights at 3-10 year horizons only. Developed markets with flexible labor markets, low corporate cross-shareholdings, and strong disclosure standards — the specific Japanese institutional vulnerabilities (lifetime employment, cross-shareholdings, weak accounting, no bank failure precedent for decades) were material amplifiers of the five-factor mechanism.

- Use in premarket reports: When regional bank equities (KRE) or broader financials (XLF) are weakening alongside rising credit costs and real estate stress: (1) Reference OSS-001 balance-sheet adjustment mechanism as the persistent-recession risk scenario — do NOT assume V-shape recovery if banking system equity is impaired; (2) Apply BL-001's credit-gap + asset-price-gap joint threshold as quantitative confirmation check; (3) Reference HK-001 for the formal model and GZ-001 (EBP) for early-warning timing. When CPI is stable: cite OSS-001 explicitly to explain why low CPI does not rule out building financial instability; provide the five BOJ risk-profile indicators as the alternative monitoring framework.

- Prohibited use: Do not use Japan's 10-year stagnation outcome as a base case for any developed market without explicitly verifying the market has Japan's specific institutional vulnerabilities. Do not draw direct quantitative predictions from Japan's capital loss ratios (159% of GDP) to current US or other markets. Do not cite this as supporting permanent or secular bearishness without cross-reference to current financial stability indicators. Do not apply the three post-bust mechanisms as a mechanical playbook for post-crisis recovery timing — the balance-sheet adjustment duration was Japan-specific (decade) due to the no-bank-failure precedent and delayed NPL recognition.

- Evidence strength: Strong — two-source admission: (1) Okina-Shirakawa-Shiratsuka (2001) BOJ IMES — Japan-specific five-factor/three-mechanism case study with quantitative depth; (2) Borio-Lowe (2002) BIS WP 114 — cross-country confirmation (34 countries, 38 crisis episodes, 1970-1999) of CPI-stability-bubble-formation independence, the OR-clause in OSS-001's revalidation trigger. Independence: different lead authors (BOJ vs. BIS/RBA), different institutions, different dataset/methodology. Scope limitation noted: Borio-Lowe confirms the CPI-stability mechanism but does not independently quantify the three post-bust adverse mechanisms; the balance-sheet adjustment asymmetry claim remains primarily Japan-specific.

- Last review date: 2026-08-23.

- Revalidation trigger: Post-2008 or post-2023 (SVB/SBNY) empirical confirmation that balance-sheet adjustment asymmetry also operates in post-GFC backstop regime (FDIC, standing repo, QE tools may shorten the adjustment cycle). OR cross-country study specifically quantifying the three post-bust mechanisms across multiple episodes beyond Japan. Note: CPI-stability-bubble-formation independence is now two-source confirmed via Borio-Lowe (2002).

- Sources: (1) Okina, Kunio, Masaaki Shirakawa, and Shigenori Shiratsuka. "The Asset Price Bubble and Monetary Policy: Japan's Experience in the Late 1980s and the Lessons." Monetary and Economic Studies 19(S-1):395-450, February 2001 (Special Edition). Bank of Japan, Institute for Monetary and Economic Studies. Full daily note: research/books/2026-08-20-okina-shirakawa-shiratsuka-japan-bubble-2001.md. (2) Borio, Claudio and Philip Lowe. "Asset prices, financial and monetary stability: exploring the nexus." BIS Working Paper No. 114, July 2002. Bank for International Settlements, Monetary and Economic Department. Full daily note: research/books/2026-08-23-borio-lowe-bis-wp114-asset-prices-financial-stability-2002.md. Cross-references: KG-20260823-BL-001 (second source; Borio-Lowe's own credit-gap indicator); KG-20260820-HK-001 (intermediary equity capital constraint = formal model of balance-sheet adjustment mechanism); KG-20260819-GZ-001 (EBP = early warning gauge for balance-sheet adjustment activation); KG-20260805-FCIC-001 (loan-collateral correlation failure = mechanism by which real estate credit became unsecured as bubble burst); KG-20260812-CGFS63-001 (QE/ZIRP = Japan's policy response after ELB reached in 1999); KG-20260821-RR-001 (Japan 1992 fits the high-capital-mobility banking crisis cluster pattern).

---

## KG-20260823-LV-001: Banking Crises → Persistent Large Output Loss; High-Income Countries Face Larger, Longer Crises

- Core conclusion: Systemic banking crises produce large and persistent output level declines — not merely cyclical contractions. High-income advanced economy crises are associated with significantly larger and more prolonged output losses than low-income country crises. More than 50% of high-income country banking crises lasted 5+ years by end-date criterion (year before both GDP and credit growth positive for ≥2 consecutive years). Banking crises precede currency crises at a T+1 peak (independently confirmed). Key quantitative benchmarks from 151 episodes 1970–2017: direct fiscal costs median 6.7% GDP (high-income) vs. 10% GDP (low-middle); public debt increase median +21.1% GDP (high-income) vs. +16.4% (low-middle) over T-1 to T+3; peak NPL median 11% (high-income) vs. 30% (low-middle); peak liquidity support 12% (high-income) vs. 23% (low-middle).

- Mechanism: Bank solvency deterioration → capital constraint binding → credit supply contraction → real GDP decline (Bernanke-Gertler 1987; Van Den Heuvel 2006; Valencia 2014). Consistent with HK-001 (intermediary equity capital constraint as formal model of this channel) and GZ-001 (EBP as early warning). High-income countries have larger, more interconnected financial systems: deeper financial disruption → larger output effect. Fiscal and monetary policy space enables countercyclical stimulus (observed in reduced short-term rates and deteriorating primary balances in high-income), but may reduce urgency of bank restructuring, explaining longer duration (Claessens et al. 2011).

- Applicable environment: Premarket macro context when banking sector stress meets or approaches systemic crisis criteria. When KRE or XLF financials show sustained equity erosion: LV 2018 provides the historical reference for advanced economy banking crisis outcomes — fiscal cost scale (6.7% GDP median direct outlays), NPL ceiling (11% median but Japan 1997 reached 35%), public debt increase (~21% GDP over T+3), and very persistent output decline (level effect, not transitory). Duration: expect 5+ year disruption in credit and output recovery, not a V-shape. Banking crisis → currency pressure at T+1: monitor FX reserve/M2 dynamics when banking distress is identified.

- Non-applicable environment: Direct quantitative GDP or fiscal prediction for any single country without verifying that systemic banking crisis criteria are met (NPL >20% OR bank closures >20% of system OR fiscal costs >5% GDP, OR ≥3 of 6 policy triggers fired). US 2026 with modern backstop tools (FDIC, Fed standing facilities, QE) will likely have lower direct fiscal costs and shorter NPL accumulation than historical LV averages — the backstop regime narrows tail outcomes. Short-term (<1yr) intraday or swing-trade signals — all patterns operate at multi-year structural horizons.

- Use in premarket reports: When KRE reports sustained NPL increases or multiple regional bank failures: reference LV 2018 Japan 1997 (output loss 45% GDP, NPL 35%, public debt +41.7%) as a severe-episode scale reference for an advanced economy with strong institutions. Reference US 2007–2011 (output loss 30% GDP, NPL 5%, public debt +21.9%, net fiscal cost 0.6%) as the modern-backstop case. State that the LV historical baseline suggests large, prolonged output effects even with active policy response. Combined with OSS-001 (balance-sheet adjustment mechanism), HK-001 (intermediary capital model), and GZ-001 (EBP early warning), this gives a coherent macro stress toolkit. Do not present any LV benchmark as a forecast — use as "what history shows" framing.

- Prohibited use: Do not use median benchmarks to make precise US GDP or fiscal trajectory predictions. Do not equate any current banking stress episode to Japan 1997 output loss without explicit systemic crisis criteria being met. Do not use banking→currency T+1 sequencing to make directional FX trades without verifying reserve currency status differences.

- Evidence strength: Strong — two-source admission. (1) Laeven-Valencia (2018) IMF WP/18/206 — comprehensive cross-country database, 151 episodes, 1970–2017, standard reference in systemic banking crisis literature, Tier-1 source. (2) Reinhart-Rogoff (2009) NBER WP 14656 — 21 post-WWII systemic crises, independently confirms large and persistent output declines (GDP -9.3% peak-to-trough / 1.9yr average; government debt +86%/3yr primarily from revenue collapse). Independence: different lead authors (Laeven/Valencia at IMF/ECB vs. Reinhart/Rogoff at NBER/Harvard), different institutions, different sample compositions, different methodologies (cumulative trend deviation vs. peak-to-trough). Both confirm large and persistent banking crisis → output decline.

- Last review date: 2026-08-23.

- Revalidation trigger: Post-2023 study incorporating SVB/SBNY 2023 episodes and subsequent regional bank outcomes to verify whether modern backstop regime (FDIC bridge bank, Fed emergency facilities, rapid QE deployment) produces materially shorter or smaller output effects than LV 2018 historical averages. Also triggered if LV publish a post-2024 update covering 2017–2024.

- Sources: (1) Laeven, Luc and Fabian Valencia. "Systemic Banking Crises Revisited." IMF Working Paper WP/18/206, September 2018. International Monetary Fund, Strategy, Policy, and Review Department. Full daily note: research/books/2026-08-23-laeven-valencia-systemic-banking-crises-revisited-2018.md. (2) Reinhart, Carmen M. and Kenneth S. Rogoff. "The Aftermath of Financial Crises." NBER Working Paper No. 14656, January 2009. National Bureau of Economic Research. Daily note: research/books/2026-08-22-reinhart-rogoff-aftermath-financial-crises-2009.md. Cross-references: KG-20260822-KR-001 (banking→currency sequencing — independently confirmed by LV 2018 Fig 5); KG-20260820-OSS-001 (Japan bubble/bust — Japan 1997 LV data point consistent with OSS-001 balance-sheet adjustment mechanism); KG-20260820-HK-001 (intermediary capital — formal model of LV 2018's credit supply disruption mechanism); KG-20260819-GZ-001 (EBP — early warning gauge aligned with LV 2018 crisis onset); KG-20260821-RR-001 (banking crisis clustering — LV 2018 extends through 2017).

---

## KG-20260822-KR-001: Banking→Currency Crisis Sequencing; Financial Liberalization Predicts Banking Crises; Pre-Crisis Signature: Lending Boom + Capital Inflow Reversal

- Core conclusion: Banking crises predict currency/BOP crises (56% of banking crises followed by BOP crisis within 3yr; only 12% vice versa) but not vice versa. Currency crises peak at T+1 after banking crisis start (LV 2018 independently confirms for 151 episodes through 2017). Financial liberalization is the dominant banking crisis predictor: 72% of banking crises in K-R 1999 sample preceded by liberalization within 5yr; banking crises/yr quadrupled post-liberalization (probit β=0.44, p<0.01). Pre-crisis banking signature: output peak ~1yr before crisis; lending boom; money multiplier expansion; capital inflow reversal.

- Mechanism: Financial liberalization → money multiplier expansion → lending boom → capital inflows fund credit growth → real exchange rate appreciation → lending reversal → NPL surge → banking system fragility. Banking fragility "ties the hands" of the central bank (cannot raise rates to defend peg without further damaging banks) → reserves drain → BOP/currency crisis at T+1. Common macroeconomic background (lending boom + capital reversal) rather than direct unidirectional banking→BOP causality. Center-country rate shocks (US Volcker tightening in early 1980s) trigger crisis bunching via capital reversal mechanism (consistent with RR-001).

- Applicable environment: When KRE or XLF shows sustained equity erosion coinciding with rising EBP (GZ-001): K-R 1999 + LV 2018 two-source evidence says banking distress precedes currency stress at T+1 — monitor FX reserve adequacy, M2/reserve ratio, and EM capital flow dynamics. Financial liberalization risk: when evaluating EM banking sector exposures after recent financial deregulation (~5yr lag), banking crisis risk is historically elevated. Pre-crisis signature checklist (applies at 12-18 month horizon, not same-day): output peak, lending boom, money multiplier expansion, capital inflow reversal.

- Non-applicable environment: Japan-specific bubble/bust (Japan not in K-R 1999 sample). Advanced-economy floating-rate currency direction trading (K-R sample predominantly ERM peg/EM episodes). Individual equity signals — all patterns operate at country/system level over months to years. Post-1995 structural changes (Basel III, modern backstops) may have altered the 56%/3yr banking→BOP transmission rate.

- Use in premarket reports: When banking sector stress precedes any FX or sovereign spread widening, reference K-R 1999 + LV 2018 sequencing evidence to provide macro context: banking distress → currency stress at T+1 is the historical norm. Note that K-R-specific percentages (56%/3yr) predate modern backstop era and may overstate risk in current regime. When EM banking exposure is discussed: financial liberalization within 5yr is a risk flag. Combined with GZ-001 (EBP early warning) and OSS-001 (balance-sheet adjustment), these cards form the banking-to-macro transmission toolkit.

- Prohibited use: Do not use 56%/3yr base rate as a deterministic prediction for any specific banking crisis. Do not use K-R 1999 to validate Japan-specific bubble mechanisms (OSS-001) — Japan not in sample. Do not use pre-crisis signature as a same-day trading signal — patterns develop over 12-18 months.

- Evidence strength: Strong — two-source admission. (1) Kaminsky, Graciela L. and Carmen M. Reinhart. "The Twin Crises: The Causes of Banking and Balance-of-Payments Problems." American Economic Review Vol. 89, No. 3, June 1999 (FRB IFDP 544, March 1996). 20-country event study, 1970–mid-1995; probit econometrics; AER peer-reviewed. (2) Laeven, Luc and Fabian Valencia. "Systemic Banking Crises Revisited." IMF WP/18/206, September 2018. Figure 5 independently confirms banking→currency sequencing (T+1 currency crisis peak) across 151 episodes through 2017. Independence: different lead authors (Kaminsky/Reinhart vs. Laeven/Valencia), different institutions (Fed/NBER vs. IMF/ECB), different sample period (1970–1995 vs. 1970–2017), different methodology (probit event study vs. database/descriptive stats). Note: K-R 1999 specific quantitative thresholds (56%/3yr, probit β, financial liberalization p<0.01) remain single-source from K-R 1999.

- Last review date: 2026-08-23.

- Revalidation trigger: Post-2023 study covering SVB/SBNY 2023 + post-GFC episodes confirming whether banking→BOP sequencing holds under modern backstop regime (FDIC bridge bank, Fed emergency facilities). Also: Euro sovereign crisis (2010–12) — does banking distress → currency crisis sequencing hold in a monetary union context? K-R's 56%/3yr rate may need updating for post-Basel III banking systems.

- Sources: (1) Kaminsky, Graciela L. and Carmen M. Reinhart. "The Twin Crises: The Causes of Banking and Balance-of-Payments Problems." American Economic Review Vol. 89, No. 3, pp.473–500, June 1999. Federal Reserve Board IFDP No. 544, March 1996. Free public access at federalreserve.gov. Full daily note: research/books/2026-08-22-kaminsky-reinhart-twin-crises-1999.md. (2) Laeven, Luc and Fabian Valencia. "Systemic Banking Crises Revisited." IMF Working Paper WP/18/206, September 2018. Figure 5 — banking→currency crisis sequencing, T+1 peak, 151 episodes through 2017. Full daily note: research/books/2026-08-23-laeven-valencia-systemic-banking-crises-revisited-2018.md. Cross-references: KG-20260821-RR-001 (capital mobility → banking crisis clustering; K-R 1999 served as second source for RR-001 admission); KG-20260820-HK-001 (intermediary equity capital — formal mechanism of "tied hands" effect); KG-20260819-GZ-001 (EBP early warning precursor); KG-20260823-LV-001 (LV 2018 provides second source for sequencing direction; also extends sample through 2017).

---

## KG-20260824-DBT-001: Credit-to-GDP Gap as Best Single Early Warning Indicator for Banking Crises; CCyB Calibration 2pp–10pp, 0–2.5% Buffer Range; Release Phase Requires Judgment

- Rule ID: KG-20260824-DBT-001

- Core conclusion: Among all tested macro, banking sector, and market-based variables, the credit-to-GDP gap achieves the lowest noise-to-signal (NS) ratio of 16% while predicting ≥66% of systemic banking crises, across a 36-country, 49-crisis, 1960–2010 dataset. Second-best indicators (property growth, equity gap, credit growth, credit-minus-GDP growth) achieve NS of 20–30%. GDP growth and output gap are poor anchors (NS 40–60%). Banking sector profits and losses are near-useless for the build-up phase (NS 70–90%). Market indicators (CDS, Libor-OIS, credit spreads) are unreliable for build-up (sample too small, flat pre-crisis). Credit gap elevation typically begins 3–4 years before crisis onset, providing sufficient lead time for capital accumulation. CCyB calibration operationalized as: buffer = 0% when gap ≤2pp; rises linearly to 2.5% at gap ≥10pp (Basel Committee 2010 guidance). No single indicator reliably signals the release phase: the credit-to-GDP gap itself stays elevated 1–2 years post-crisis; market indicators (credit spreads most promising) signal release with high noise and very small sample. Release requires discretionary judgment combining aggregate loss measures with credit-condition tightening signals.

- Mechanism: Credit-to-GDP gap captures CUMULATIVE DEVIATION of credit from long-term trend (one-sided HP filter, λ=400,000 — financial cycles ~4x longer than business cycles), making it sensitive to sustained lending booms while robust to temporary swings. The gap grows for 3–4 years pre-crisis because credit expands faster than GDP while the backward-looking trend adjusts slowly. Credit continues growing post-crisis (existing lines drawn; banks reluctant to call loans), so the gap remains elevated and fails as a release signal. Asset prices fall BEFORE crisis onset — premature as mechanical release signals. Market indicators are coincident stress measures, not leading indicators. Procyclical bias in bank risk measurement (Basel II IRB weights reach minimum at boom peak) is the structural problem CCyB corrects.

- Applicable environment: (a) Credit-to-GDP gap monitoring: when BIS credit statistics show a country's credit-to-GDP gap running 2pp+ above trend, apply DBT-001 CCyB framework to assess 2–3yr systemic banking crisis risk; gap ≥4pp → elevated warning; gap ≥10pp → maximum historical risk zone. Use BIS quarterly statistics for US, EU, and EM credit-to-GDP ratios; apply HP filter with λ=400,000, one-sided, recursive. (b) Premarket banking sector context: when KRE or XLF financials weaken, check whether a large credit gap preceded the weakness by 2–3 years — if yes, system-wide stress is more likely than idiosyncratic failure; reference LV-001 for expected output loss scale. (c) Complementary to GZ-001: credit gap is the structural 2–3yr leading indicator; EBP (GZ-001) is the timelier market-price signal of financial sector distress — use together for a full banking stress diagnostic. (d) Globally active bank analysis: domestically focused credit gap alone misses exposures to foreign credit booms; an internationally weighted indicator (country credit gaps × exposure shares from BIS international banking statistics) better captures risks from cross-border lending books.

- Non-applicable environment: Short-term (intraday, weekly) market timing; release phase CCyB decisions (explicitly unreliable — use judgment instead); financial cycle analysis with standard λ=1600 (financial-cycle-specific λ=400,000 required); crises primarily caused by foreign credit booms without domestic gap signal; non-banking sector financial disruptions.

- Use in premarket reports: When discussing banking sector vulnerability or regional bank risk, reference DBT-001 for the structural macro backdrop: a credit-to-GDP gap that was elevated 2–3 years prior indicates the banking system was accumulating system-wide vulnerability during the boom. If the gap is now compressing post-crisis, reference DBT-001 to explain why output recovery may still be slow (credit gap compresses slowly; banking system balance-sheet adjustment ongoing — see OSS-001 and LV-001 for duration benchmarks). Do not use credit gap as a market timing signal. Combine with GZ-001 (EBP for concurrent market signal) and HK-001 (intermediary capital constraint for microeconomic mechanism) to build a coherent banking stress narrative.

- Prohibited use: Do not use credit-to-GDP gap as same-day or short-horizon trading trigger; do not use it to signal CCyB release; do not misinterpret NS=16% as "only 16% chance of false alarm" (it means 16% of on-signals are false, at the ≥66% crisis-capture threshold); do not apply 2pp–10pp calibration as a mechanical buy/sell threshold.

- Evidence strength: Strong — two-source admission. (1) Drehmann, Mathias, Claudio Borio, and Kostas Tsatsaronis. "Anchoring countercyclical capital buffers: the role of credit aggregates." BIS Working Paper No. 355, November 2011. Bank for International Settlements, Monetary and Economic Department. Published IJCB Vol. 7 No. 4, December 2011. 36 countries, 49 crises, 1960–2010, quarterly data. Full daily note: research/books/2026-08-24-drehmann-borio-tsatsaronis-bis-wp355-anchoring-ccyb-2011.md. (2) Borio, Claudio and Philip Lowe. "Asset prices, financial and monetary stability: exploring the nexus." BIS Working Paper No. 114, July 2002. 34 countries, 38 crisis episodes, 1970–1999. Established credit-gap concept; showed it outperformed other single indicators; foundation for Basel III CCyB approach. Full daily note: research/books/2026-08-23-borio-lowe-bis-wp114-asset-prices-financial-stability-2002.md. Independence: different lead authors (Drehmann leads DBT; Borio shared but second); different time period (extends through 2008 GFC); different primary research question (regulatory CCyB design vs. financial vulnerability monitoring); 11 additional crises; post-GFC validation. Note: the JOINT credit+asset price gap threshold — BL-001 candidate's distinctive finding — is NOT confirmed by DBT; DBT explicitly focuses on single indicators (fn.12). The joint indicator remains single-source from Borio-Lowe (2002).

- Last review date: 2026-08-24.

- Revalidation trigger: Post-2015 study confirming credit-to-GDP gap early warning performance on crisis episodes occurring after global CCyB adoption (UK 2015, EU 2016+). If active CCyB regimes structurally dampen credit booms, the gap may become a self-defeating indicator (Goodhart/Lucas critique materialization). Also: updated internationally weighted credit gap analysis covering 2010–2025 to confirm Germany/Switzerland-type cross-border exposure risk remains captured.

- Sources: (1) Drehmann, Mathias, Claudio Borio, and Kostas Tsatsaronis. "Anchoring countercyclical capital buffers: the role of credit aggregates." BIS Working Paper No. 355, November 2011. International Journal of Central Banking, Vol. 7 No. 4, pp. 189–240, December 2011. Free public access at bis.org. Full daily note: research/books/2026-08-24-drehmann-borio-tsatsaronis-bis-wp355-anchoring-ccyb-2011.md. (2) Borio, Claudio and Philip Lowe. "Asset prices, financial and monetary stability: exploring the nexus." BIS Working Paper No. 114, July 2002. Full daily note: research/books/2026-08-23-borio-lowe-bis-wp114-asset-prices-financial-stability-2002.md. Cross-references: KG-20260823-BL-001 (candidate — credit gap alone now two-source via DBT-001; joint indicator still single-source from BL 2002); KG-20260819-GZ-001 (EBP — timelier market signal complementing the 2–3yr structural credit gap indicator); KG-20260820-HK-001 (intermediary equity capital constraint — microeconomic mechanism of credit supply collapse after gap accumulation ignored); KG-20260820-OSS-001 (Japan 1992 in DBT-001 49-crisis sample; balance-sheet adjustment = post-bust outcome when credit gap unaddressed); KG-20260823-LV-001 (LV crisis dating used by DBT; output loss benchmarks for when gap goes unchecked); KG-20260821-RR-001 (capital mobility → banking crisis clustering provides structural context for why credit booms cluster).

## KG-20260824-SQINERT-001: Status-Quo Bias / Inertia in Real Financial Decisions — Investors Systematically Leave an Existing Allocation or Already-Decided Action Unchanged; Inaction Is a Costly Default and the Evidence-Based Remedy Is a Forced ACTIVE DECISION

- Rule ID: KG-20260824-SQINERT-001

- Core conclusion: In real financial decisions, decision-makers exhibit a robust, quantitatively large status-quo / inertia bias — they disproportionately leave a pre-existing allocation or a not-yet-executed decision unchanged even when transition costs are small and an updated (often already-approved) action is superior. (1) Samuelson & Zeckhauser (1988): controlled experiments, N=486, 8 scenarios (alternatives varied 2–4); an option's chosen share was significantly higher when it occupied the status-quo position than under neutral framing, and the bias GREW with the number of alternatives. Two field studies confirmed it in important repeated decisions: Harvard health plans (9,185 employees, 1986 — continuing enrollees stuck with old plans far more than the neutral-framed new-enrollee control) and nationwide TIAA/CREF faculty retirement allocations (~half at a naive 50/50 split; most never re-optimized). (2) Madrian & Shea (2001): a natural experiment switching new hires from opt-in to automatic 401(k) enrollment (default 3% into the money-market fund) lifted participation sharply (widely cited ~37% → ~86% for the <1yr-tenure cohort), and a substantial fraction stuck to BOTH the default rate AND the default fund even though almost no prior-cohort employee freely chose that combination; the inertia persisted over tenure. (3) Remedy — Carroll, Choi, Laibson, Madrian & Metrick (2009): present-biased procrastination drives default-stickiness, and forcing a compulsory ACTIVE DECISION (no do-nothing option) raised enrollment ~28 pp vs. opt-in. Account corollary: an already-USER-APPROVED de-risk draft left unexecuted is the status-quo-bias failure mode; re-surface it as a forced active decision (execute or explicitly withdraw), do not let it lapse silently.

- Mechanism: Three (non-exclusive) sources per Samuelson-Zeckhauser — (1) rational persistence under transition costs/uncertainty (a bounded justification); (2) cognitive misperception, i.e. loss aversion anchored on the current state makes switching-losses loom larger than equal gains (Kahneman-Tversky); (3) psychological commitment from misperceived sunk costs, regret avoidance, and a drive for consistency. Madrian-Shea add procrastination and reading the default as implicit endorsement/advice. Net: "doing nothing" is treated as a neutral non-choice when it is actually an active choice to retain current risk. The Carroll-et-al. remedy removes the do-nothing path. This is the OPPOSITE POLE of overtrading (KG-20260817-BEHAV-OT-001): there the error is too MUCH impulsive off-plan action; here it is too LITTLE action on an on-plan, already-decided risk reduction.

- Applicable environment: A user-approved de-risk/trim/invalidation-exit draft exists but shows no matching Webull open/filled order in a later session — grounds RULE-20260824-01 (escalate to the first-line action item every premarket/intraday/postmarket window and re-verify open/filled status until executed or explicitly withdrawn); a concentrated single-name (e.g., COIN ~54% of equity on 2026-08-24) left unchanged despite a standing reduction plan (pairs with KG-20260812-CONC-001 / KG-20260821-DIV-001 — inaction is not risk resolution); any allocation left at a naive/legacy default after the thesis/risk budget changed; report/UX design converting a lapsing approved draft into a forced active choice (execute vs. withdraw-with-reason).

- Non-applicable environment: Genuinely rational inertia where transition costs exceed the switching benefit (does NOT justify churn — e.g., a tiny fractional rebalance whose spread/fee exceeds the risk reduction); deliberate thesis-based HOLDs actively re-reasoned this session; cases where the user has explicitly withdrawn/paused the approved draft; use to override the >20% single-name concentration red line in the other direction or to force a trade against the approval gate.

- Prohibited use: Not a directional buy/sell or market-timing signal (it governs EXECUTION DISCIPLINE on already-decided actions). Does NOT authorize auto-execution — the account is approval-gated; the remedy is to re-surface the approved draft for the user, never to place/modify/cancel orders. Do not weaponize against rational inertia (state cost/benefit instead of mechanically forcing action). Do not pressure the user to trade against an explicit withdrawal.

- Contrary evidence: (1) Rational-inertia bound from Samuelson-Zeckhauser itself (transition costs can justify retention). (2) The 2021 replication of Samuelson-Zeckhauser reproduced the bias strongly in some scenarios (budget allocation, investment portfolio, jobs) but weaker/absent in others → scenario-dependence. (3) Choi-Laibson-Madrian-Metrick / Carroll et al. show defaults partly reflect endorsement + present-bias, not only passive inertia (refines mechanism, strengthens the active-decision remedy). Contradiction note: research/contradictions/2026-08-24-inertia-vs-rational-status-quo.md.

- Evidence strength: Strong — two independent Tier-1/Tier-2 peer-reviewed studies of real financial decisions (JRU 1988 lab + field; QJE 2001 field natural experiment), consistent effect, plausible mechanism, plus a Tier-1 QJE remedy study (Carroll et al. 2009).

- Last review date: 2026-08-24.

- Revalidation trigger: A credible failed replication showing status-quo bias / default effects do not appear in a well-powered financial-decision sample; OR evidence that this account's approved-draft execution gap is better explained by rational transaction-cost inertia than by procrastination (then the non-applicable boundary governs). Treat scenario-dependence (2021 partial replication) as a known boundary.

- Source: Samuelson, William and Richard Zeckhauser, "Status Quo Bias in Decision Making," Journal of Risk and Uncertainty 1:7–59 (1988); Madrian, Brigitte C. and Dennis F. Shea, "The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior," Quarterly Journal of Economics 116(4):1149–1187 (2001) (NBER WP 7682); remedy support: Carroll, Gabriel D., James J. Choi, David Laibson, Brigitte C. Madrian and Andrew Metrick, "Optimal Defaults and Active Decisions," Quarterly Journal of Economics 124(4):1639–1674 (2009). Full daily note: research/daily/2026-08-24.md.

## KG-20260823-BL-001: Credit-Gap + Asset-Price-Gap Joint Financial Vulnerability Indicator; CPI-Stability Paradox; Multi-Factor Bubble Formation; CB-Credibility Paradox

- Rule ID: KG-20260823-BL-001

- Core conclusion: Four durable empirical findings from 34 countries (1970–1999), 38 crisis episodes: (1) JOINT FINANCIAL VULNERABILITY INDICATOR: Credit-to-GDP gap >4-5 percentage points above trend COMBINED with asset price gap >40% above trend is the best-performing ex ante financial crisis predictor — noise-to-signal ratio drops from 0.24 (credit gap alone, 1yr) to 0.13 (credit+asset, 1yr) and from 0.20 to 0.06 at 3yr; false positive rate falls from ~18% to <5% at 1yr when joint threshold is used. NOTE: The specific threshold parameters (4-5pp credit gap, 40% asset price gap) are from Borio-Lowe (2002) alone; the general principle that joint credit+asset price excess substantially outperforms single indicators is independently confirmed by Jordà-Schularick-Taylor (2015) "Leveraged Bubbles" (LB-001 — different operationalization: credit growth above mean + bubble amplitude criterion; 17 countries 1870–2013; logit AUC 0.76→0.82 post-WW2 when asset price bubble interaction added). (2) CPI-STABILITY PARADOX CONFIRMED CROSS-COUNTRY: Average inflation across 38 crisis episodes shows NO systematic pre-crisis pickup; lending booms also show no CPI acceleration. Three historical case studies: Japan 1980s (CPI <4% during Nikkei/land boom), US 1920s (CPI fell 10% while credit/stocks boomed), Australia 1880s (GDP deflator fell before 1893 banking crisis). (3) MULTI-FACTOR BUBBLE FORMATION: Financial distress results from combinations of credit + asset price + investment booms — not any single indicator. (4) CB-CREDIBILITY PARADOX: A credible low-inflation central bank provides no tightening signal even as financial imbalances build — the endogenous response to credibility increases the probability that latent pressures manifest first in credit/asset markets.

- Mechanism: Four pathways for financial imbalances to build in low-CPI environments: (1) Successful stabilization program — credible disinflation → optimism + financial liberalization → credit boom + capital inflows → real estate inflation, CPI stays low; (2) Supply-side improvement — productivity gains compress unit labor costs while generating optimism → asset price boom with no CPI pressure; (3) Demand masked by supply — positive demand + supply-side gains offset → CPI stable while imbalances build; (4) CB credibility paradox — credible low-inflation regime → no tightening signal → imbalances accumulate in credit/asset markets. Credit gap (cumulative HP-filtered deviation from trend, rolling one-sided HP λ=400,000 per DBT-001) captures sustained nature of lending booms better than flow growth rates.

- Applicable environment: (a) cross-country macro monitoring: when credit-to-GDP gap runs 4+pp above trend AND asset prices run 40%+ above trend (both thresholds), signals elevated financial instability risk at 2–3 year horizon — same logic as Basel III CCyB activation rule; (b) interpreting periods of stable CPI + rising asset prices: do NOT assume CPI stability means financial stability; check credit/GDP deviation from trend as a separate signal; applies when CB or market commentary cites low inflation as evidence of financial health; (c) premarket macro context: when KRE, XLF, or EBP are deteriorating alongside reported history of rapid credit expansion in prior years, apply this framework — the buildup phase predicts the unwinding mechanism; (d) regional bank sector risk: credit booms in real estate combined with high property valuations satisfy the joint threshold — OSS-001 Japan balance-sheet adjustment mechanism is the downstream risk.

- Non-applicable environment: short-term (intraday, weekly) signals — credit-to-GDP gap is multi-year; countries with active macroprudential CCyB tools post-2010 may have altered crisis transmission; asset-price-only bubbles without credit amplification (equity alone, low credit; see LB-001 — these carry much lower crisis risk post-WW2).

- Prohibited use: not a mechanical same-day buy/sell trigger; the 4pp/40% thresholds are probabilistic improvements, not hard crisis-certain boundaries; CPI stability is not evidence of financial stability (the central lesson); do not cite as supporting blanket asset-price targeting by CBs.

- Contrary evidence: Borio-Lowe (2004) BIS WP 157 (same authors, 4-country subsample) confirms joint indicator and adds output/inflation prediction channel, but is not independent. DBT (2011) confirms credit gap alone (NS=16%) but explicitly excludes joint threshold test (fn.12). JST (2015) confirms general principle with different operationalization; AUC improvement (0.76→0.82) is consistent direction but smaller than the noise-to-signal improvement in BL (2002). Post-Basel III CCyB adoption may structurally alter credit boom dynamics.

- Evidence strength: Strong — two-source admission. (1) Borio-Lowe (2002): 34 countries, 1970–1999, noise-to-signal analysis; provides specific threshold parameters. (2) Jordà-Schularick-Taylor (2015) "Leveraged Bubbles": 17 countries, 1870–2013, logit AUC + local projections; confirms general principle with independent authors, data, and method. CAVEAT: specific threshold parameters (4-5pp, 40%) remain single-source from BL 2002; JST 2015 uses different operationalization.

- Last review date: 2026-08-26.

- Revalidation trigger: Post-2015 cross-country validation of specific threshold parameters (4-5pp credit gap + 40% asset price gap) on post-GFC crisis episodes. Specifically: SVB/SBNY 2023 US banking stress + Nordic housing correction 2022-2023. If CCyB-active regimes (UK, EU since ~2016) show reduced credit boom amplitude, assess whether threshold calibration should shift.

- Sources: (1) Borio, Claudio and Philip Lowe. "Asset prices, financial and monetary stability: exploring the nexus." BIS Working Paper No. 114, July 2002. Bank for International Settlements, Monetary and Economic Department. 34 countries, 38 crisis episodes, 1970–1999. Full daily note: research/books/2026-08-23-borio-lowe-bis-wp114-asset-prices-financial-stability-2002.md. (2) Jordà, Òscar, Moritz Schularick, and Alan M. Taylor. "Leveraged Bubbles." Journal of Monetary Economics, Vol. 76 (Supplement), pp. S1–S20, December 2015. NBER WP 21486. Full daily note: research/books/2026-08-26-jorda-schularick-taylor-nber-w21486-leveraged-bubbles-2015.md. Cross-references: KG-20260826-LB-001 (JST 2015 second source for general principle; separate admitted card with distinct output-cost findings); KG-20260824-DBT-001 (credit gap alone — timing/CCyB calibration signal); KG-20260820-OSS-001 (Japan bubble/bust — archetypal leveraged housing case); KG-20260819-GZ-001 (EBP — real-time risk-bearing capacity gauge, earlier signal than credit gap); KG-20260820-HK-001 (intermediary capital constraint — formal micro-model for the crisis mechanism); KG-20260825-BL04-001 (Borio-Lowe 2004, same authors — output/inflation prediction + CB asymmetric response, companion candidate).

## KG-20260826-LB-001: Leveraged (Credit-Financed) Asset Price Bubbles Dramatically Increase Crisis Probability and Output Costs; Leveraged Housing Bubbles Are the Most Dangerous Combination; Unleveraged Equity Bubbles Are Nearly Benign Post-WW2

- Rule ID: KG-20260826-LB-001

- Core conclusion: Credit-financed asset price bubbles substantially increase financial crisis probability and post-crisis output costs vs. unleveraged bubbles. Based on 17 advanced economies, 1870–2013 (JST 2014 credit data + Knoll 2014 house price data + equity indices): (1) CRISIS PROBABILITY (logit models, fixed effects): post-WW2 AUC from 0.763 (credit only) to 0.819 (credit + bubble interactions, Table 4 col.6); housing bubble × credit coefficient = 0.55* (post-WW2, significant); both bubbles × credit = 1.20** (highest); equity bubble alone × credit = −0.07 (NS post-WW2 — unleveraged equity bubbles not predictive). (2) OUTPUT COSTS (local projections with controls, full sample 1870–2013, Table 6 5yr sums): normal recession = +15.16%; equity+high credit = −14.50**; house+low credit = −14.74**; HOUSE+HIGH CREDIT = −28.95** (worst: still below start-level after 5 years). POST-WW2 ONLY (Table 7): equity+low credit = −4.32 (NS, nearly benign); equity+high credit = −8.46 (NS); house+low credit = −13.55; HOUSE+HIGH CREDIT = −19.63*** (most significant, p<0.01). (3) ROBUSTNESS: Three independent checks confirm housing+high-credit = worst combination: controlling for financial crisis indicator directly; excluding interwar period; excluding post-2006 GFC. (4) KEY FINDING: "It is not only credit growth, but the interaction of credit and asset prices that matters for financial stability risks and the economic costs of financial crises."

- Mechanism: Two-channel framework: (1) FINANCIAL ACCELERATOR (Bernanke-Gertler 1990) — credit-financed bubbles build leverage; asset price collapse → amplified collateral destruction → credit crunch → investment collapse (20%+ in financial crises). (2) DEBT OVERHANG (Fisher 1933; Mian-Sufi 2014) — high post-bust household/firm debt burdens suppress spending even as interest rates fall. Housing is worse than equity because (i) mortgage credit is procyclical and secured, (ii) housing is a larger fraction of household balance sheets, (iii) national average house price declines are more persistent than equity corrections, (iv) local concentration creates geographic transmission of debt overhang. Consistent with GZ-001 EBP widening (financial sector risk-bearing capacity impairment) and HK-001 intermediary capital constraint (formal model of leverage-driven crisis premium).

- Applicable environment: (a) macro risk backdrop when BOTH credit AND asset prices are elevated simultaneously — use LB-001 benchmarks (post-WW2 house+high-credit = −19.63pp 5yr, still negative at yr5) rather than normal recession path (+18.48pp) or even unleveraged asset price bust; (b) regional bank sector risk: US commercial real estate credit exposure + elevated property valuations qualifies as leveraged housing risk — apply OSS-001 balance-sheet adjustment + LB-001 output cost magnitude together; (c) evaluating dotcom/equity-type bubbles without credit expansion: post-WW2 evidence shows unleveraged equity bubbles are nearly benign (−4.32pp NS); do NOT equate equity bubble severity with leveraged housing bubble severity; (d) post-crisis recovery trajectory calibration: after a leveraged housing bust, historical benchmark is still below start-level at 5 years; do not expect V-shape; (e) macroprudential policy context: LB-001 provides outcome stakes for why CCyB and LTV restrictions specifically target credit-financed asset price booms.

- Non-applicable environment: short-term (intraday, weekly, monthly) timing — local projections are at 1–5yr annual horizons; unleveraged equity market corrections (dotcom analogy) — post-WW2 these are near-baseline risk; non-advanced economies (sample covers 17 advanced economies only); post-Basel III era with active CCyB (sample ends 2013, CCyB effectiveness post-2015 not captured).

- Prohibited use: not a same-session or short-term buy/sell trigger; do not equate unleveraged equity bubbles with leveraged housing bubbles in risk severity — post-WW2 evidence explicitly shows equity alone is near-baseline; do not ignore the credit dimension (house price elevated + low credit carries much lower cost than house+high credit); do not cite as precise crisis probability (AUC 0.819 means meaningful but imperfect classification).

- Contrary evidence: Extraordinary policy intervention (QE, FDIC guarantees, CARES Act) may reduce historical magnitude of output loss even in leveraged housing busts — US 2007–12 outperformed the JST 2013 sister paper (When Credit Bites Back) conditional path, likely due to policy support. Robustness check excludes post-2006 GFC and confirms results (Figure 8c), but the 2020-2022 US housing boom and 2022-2023 correction were not available in the sample. Post-Basel III CCyB may limit credit boom amplitude in future episodes.

- Evidence strength: Strong — Tier-2 JME peer-reviewed; 17-country advanced economy panel 1870–2013; well-established methods (logit models for crisis probability; Jordà 2005 local projections for output paths); three robustness checks confirm; consistent with prior independent work (Schularick-Taylor 2012 AER for credit side; Borio-Lowe 2002 for joint credit+asset price side). Single study — but this is a high-quality study with clear out-of-sample validation (pre-WW2 + post-WW2 subsamples) and a plausible mechanism; satisfies admission criterion (one high-quality study with clear OOS validation and plausible mechanism).

- Last review date: 2026-08-26.

- Revalidation trigger: Post-2013 extension of JST dataset to 2020+ covering the 2020-2022 US/EU housing boom and 2022-2023 correction — does leveraged housing bust output cost benchmark hold, or do extraordinary backstops systematically reduce the historical magnitude? Also: test whether Basel III CCyB/LTV regulations reduce the AUC gap between credit-only and credit+asset-price models in post-2015 episodes.

- Sources: Jordà, Òscar, Moritz Schularick, and Alan M. Taylor. "Leveraged Bubbles." Journal of Monetary Economics, Vol. 76 (Supplement), pp. S1–S20, December 2015. DOI: 10.1016/j.jmoneco.2015.08.005. NBER Working Paper No. 21486, August 2015. Federal Reserve Bank of San Francisco. Free public access at nber.org. Full daily note: research/books/2026-08-26-jorda-schularick-taylor-nber-w21486-leveraged-bubbles-2015.md. Cross-references: KG-20260823-BL-001 (admitted 2026-08-26 via this paper as second source: general principle confirmed; BL-001 provides threshold-based early warning, LB-001 provides output cost calibration); KG-20260824-DBT-001 (credit-to-GDP gap timing/CCyB calibration signal; DBT provides the build-up indicator, LB-001 provides the outcome stakes); KG-20260819-GZ-001 (EBP as financial sector risk-bearing capacity gauge; EBP is the real-time signal that the leveraged bubble is activating the crisis channel); KG-20260820-HK-001 (intermediary equity capital constraint — formal micro-model consistent with LB-001's empirical findings); KG-20260820-OSS-001 (Japan 1987-1993 = archetypal leveraged housing bubble in LB-001 sample); KG-20260826-JST-001 (candidate — JST 2013 sister paper on credit overhang and recession depth; complementary lens on same dataset).

## KG-20260826-EAVAR-001: Scheduled Earnings Announcements Sharply Raise Short-Horizon Return Variance, Volume and Implied Volatility (Post-Event Vol Crush) — a Concentrated Single Name Held Through Its Own Binary Catalyst Faces Quantifiable Elevated Gap/Tail Risk; De-Risk by Size, Not by Buying Expensive Event-Window Options

- Rule ID: KG-20260826-EAVAR-001

- Core conclusion: A scheduled earnings announcement is a known binary information event that sharply and predictably raises a stock's short-horizon return variance, trading volume, and option-implied volatility, followed by a post-event implied-volatility collapse ("vol crush"). (1) Beaver (1968): 143 NYSE firms, 506 annual-earnings announcements, 1961–1965 — in the announcement WEEK the squared unexpected return (return variability) and volume both spike far above non-announcement weeks (widely-cited magnitudes: variability ~1.67x / ~+67%, volume ~+33% in the report week vs. the non-report average); the reaction is concentrated in the announcement week itself. (2) Patell & Wolfson (1981): using option prices, implied volatility runs UP into the announcement, peaks just before it, and DROPS sharply immediately after — the run-up and crush are largest for short-dated options, i.e. the market prices the earnings-date variance as a transitory jump. (3) Landsman & Maydew (2002): the announcement-week return-variance and volume reaction did NOT decline (if anything strengthened) over three decades through the late 1990s — robust out-of-sample. Implication for a concentrated retail account: holding an oversized single name (>20% of equity) naked THROUGH its own scheduled earnings converts a documented variance/gap spike into account-level TAIL risk; the appropriate remedy is to reduce position SIZE before the event, because the vol crush makes buying event-window options an expensive hedge (you pay the bid-up pre-event IV).

- Mechanism: Earnings resolve a large chunk of firm-specific uncertainty at a known instant, so agents price a higher expected variance into the window (Patell-Wolfson ex-ante IV run-up) and the realized variance/volume spike when the news drops (Beaver). Because the extra variance is a one-time jump, short-dated options embed most of it and de-price immediately after (vol crush). Overnight/gap risk is elevated (report released after close / before open). For a diversified/appropriately-sized position this is a normal, small, roughly-compensated risk; for a CONCENTRATED single name it multiplies account tail exposure exactly when the variance is known in advance to be high — a timing-and-sizing risk distinct from the average-day volatility used in normal sizing. Read-through names (a peer/index/sector holding exposed to ANOTHER firm's report) inherit only the systematic/common component of that variance, scaled down (KG-20260807-ITSF-001).

- Applicable environment: A concentrated single name (>20% of equity) held into ITS OWN scheduled earnings/binary event — the documented variance/gap spike argues for reducing size before the event (pairs with KG-20260812-CONC-001 / KG-20260821-DIV-001 and standing-profit-taking-lines). Sizing event-window exposure by the options-implied (straddle) expected move rather than normal-day volatility. Read-through exposure (e.g., MSFT/QQQ into NVDA earnings): apply the attenuated systematic-component version (ITSF-001), not one-for-one. Postmarket audit: grade whether a concentrated name was carried naked through a known catalyst and whether the realized gap fell within the pre-event implied move. Premarket/intraday event-day planning and monthly prompt-eval canaries.

- Non-applicable environment: Diversified or appropriately-sized positions where one earnings gap cannot move the account materially — holding through earnings is a normal, roughly-compensated risk (announcement premium), NOT a mandate to sell. Using the variance spike as a directional/market-timing signal (it is symmetric — does not predict the sign). Routine event-window option hedging for over-concentration (pre-event IV run-up / vol crush makes it systematically expensive — reduce shares instead). Index/broad-ETF positions (idiosyncratic earnings variance diversifies away).

- Prohibited use: Do not convert into a mechanical "always sell before every earnings" rule — that is overtrading (KG-20260817-BEHAV-OT-001) and is contradicted by the small positive announcement premium; the rule targets OVERSIZED single-name tail risk. Do not use the variance/IV spike as a directional buy/sell signal (second-moment fact, not a first-moment forecast). Do not auto-execute any pre-event trim — approval-gated; produce a sized draft. Do not apply reporting-firm magnitude one-for-one to read-through names (scale by systematic exposure via ITSF-001).

- Contrary evidence: The announcement premium (Frazzini-Lamont 2007; Ball-Kothari) — a small POSITIVE average return to holding through earnings — means this is not a blanket sell rule; it is small, concentrated in illiquid/small names, and decayed in some samples. Vol crush makes option hedging expensive (buy shares-down, not puts). Read-through attenuation per ITSF-001. Contradiction note: research/contradictions/2026-08-26-earnings-variance-vs-announcement-premium.md.

- Evidence strength: Strong — two independent Tier-1/Tier-2 peer-reviewed studies (Beaver JAR 1968 stock; Patell-Wolfson JAR 1981 options), robust mechanism, and explicit out-of-sample confirmation (Landsman-Maydew JAR 2002, no decline over three decades). Exact Beaver peak ratios are widely-cited support; the load-bearing claim (sharp announcement-week variance/volume rise + IV run-up/crush) is directly documented in both primary sources.

- Last review date: 2026-08-26.

- Revalidation trigger: Post-2015 evidence that the earnings-announcement variance/IV run-up-and-crush has materially weakened (pre-announcement guidance, real-time information, or 0DTE/short-dated option flows altering the pattern), OR account-specific evidence that realized earnings gaps are reliably smaller than the implied move (then the sizing input changes). Landsman-Maydew (2002) found no decline through the 1990s; recheck 2015–2026.

- Source: Beaver, William H., "The Information Content of Annual Earnings Announcements," Journal of Accounting Research 6 (Supplement):67–92 (1968); Patell, James M. and Mark A. Wolfson, "The Ex Ante and Ex Post Price Effects of Quarterly Earnings Announcements Reflected in Options and Stock Prices," Journal of Accounting Research 19(2):434–458 (1981); OOS confirmation: Landsman, Wayne R. and Edward L. Maydew, "Beaver (1968) Revisited: Has the Information Content of Annual Earnings Announcements Declined in the Past Three Decades?," Journal of Accounting Research 40(3):797–808 (2002). Full daily note: research/daily/2026-08-26.md. Cross-references: KG-20260812-CONC-001 / KG-20260821-DIV-001 (concentration limits — EAVAR-001 adds the event-timing rationale for de-risking oversized names); KG-20260824-SQINERT-001 (inertia — the unexecuted COIN trim into NVDA night); KG-20260817-BEHAV-OT-001 (overtrading boundary — not a mechanical always-sell); KG-20260807-ITSF-001 (read-through attenuation for names exposed to another firm's report).

### KG-20260831-ACORR-001 — Asymmetric (Downside-Tail) Correlation Regime: an Aggregate Risk-Off / Breadth Signal Justifies a Bearish Read on an Individual High-Beta Holding Only in a Genuine Down-Tail Regime

- Title: Cross-stock/market correlation rises asymmetrically only in the genuine DOWNSIDE/bear-tail regime (not in a mild risk-off lean or merely volatile conditions). Admitted 2026-08-31 (research_a), domain market_microstructure.

- Core conclusion: Correlation between individual U.S. stocks / high-beta portfolios and the aggregate market is regime-asymmetric: it rises sharply in the genuine downside/bear-tail but not on the upside and not merely because a session is volatile or "risk-off." Ang & Chen (2002, JFE 63(3):443-494), using an H-statistic and exceedance correlations that correct for the Boyer-Gibson-Loretan conditioning bias, find U.S. stock–market correlations much greater for downside (especially extreme downside) moves; conditional on the downside the data correlation differs from the bivariate-normal-implied value by ~11.6%, significant, strongest for small/value/past-loser/higher-beta segments, with no mirror-image upside increase. Longin & Solnik (2001, JF 56(2):649-676), using extreme value theory on international indices, independently find correlation increases in BEAR markets but NOT bull markets, tied to the market TREND (down-tail) NOT to volatility per se. Implication: an aggregate risk-off / breadth-weak signal only justifies a DIRECTIONAL bearish read on an individual high-beta holding when a genuine down-tail/high-volatility regime is present; under a soft risk-off lean (VIX low, no index break, breadth soft but not collapsing) the asymmetry is not engaged, idiosyncratic variance dominates single-name daily returns (Roll 1988 low individual-stock R²), and high-beta decoupling from weak breadth is the expected base case.

- Mechanism: Correlation is a nonlinear function of returns, so conditioning on the level of returns/volatility mechanically distorts sample correlations (Boyer-Gibson-Loretan: under constant-correlation bivariate normal with true ρ=0.50, conditional correlation of small returns ~0.21 vs large returns ~0.62 is a pure artifact). Ang-Chen (H-statistic/exceedance) and Longin-Solnik (EVT tails) remove this bias with two different methods and a genuine downside asymmetry survives in both. In a real bear/down-tail the common systematic shock dominates, idiosyncratic components are swamped, correlations rise toward 1, decoupling vanishes — the regime where breadth-bearishness DOES transmit to single names. Outside that tail the systematic component is a minority of a single high-beta stock's daily variance (Roll 1988), so leaders routinely decouple from weak breadth.

- Supporting evidence: Two independent bias-corrected peer-reviewed studies (Ang-Chen 2002 JFE, U.S. stocks, H-statistic; Longin-Solnik 2001 JF, international indices, EVT) reaching the same asymmetry with different methods and samples. Consistent with the Roll (1988) low-R² caveat already recorded (research/daily/2026-08-07.md).

- Contrary evidence: Boyer, Gibson & Loretan (1999) show naive conditional-correlation comparisons are severely biased and can manufacture a spurious down-day asymmetry — this is a caveat, not a refutation, because the two admitted sources explicitly correct for it and the asymmetry survives. Debate is about magnitude/threshold, not existence. Contradiction note: research/contradictions/2026-08-31-asymmetric-correlation-vs-conditioning-bias.md.

- Applicable environment: Premarket direction calibration for individual high-beta holdings (crypto proxies, semis, high-beta single names) under an aggregate risk-off/breadth-weak read — require a genuine down-tail regime (align with standing-inverse-etf-conditions gates: VIX elevated & rising, SPY/QQQ<20DMA on 2+ closes, NYSE A/D<1.0 for 2+ days, explicit catalyst, RISK-OFF composite) before tilting a holding bearish; otherwise default to hold/assess. Intraday regime distinction (breadth weak vs down-tail engaged). Postmarket audit of whether a risk-off directional call was regime-justified. Monthly prompt-eval calibration canary (2026-08-31 breadth-vs-high-beta decoupling).

- Non-applicable environment: A genuine crash/down-tail (VIX spike + index break + A/D collapse) — there the asymmetry IS engaged and the aggregate signal DOES transmit; broad-index/diversified positions; and any use as a first-moment directional/timing signal.

- Time scale: Daily/weekly regime classification; the correlation asymmetry is a tail/regime property, not an intraday tick signal.

- Use in premarket reports: When holdings include high-beta single names and the macro read is risk-off, state explicitly whether a genuine down-tail regime is present; if not, do not extrapolate breadth-bearishness onto those names' direction — default the single-name action to hold/assess unless an independent single-name invalidation triggers.

- Prohibited use: Do not treat a mild/soft risk-off lean as sufficient to call a high-beta holding bearish or to justify a sell/trim draft (needs a genuine down-tail regime OR an independent single-name trigger). Do not invert into "ignore the macro tape" during a real down-tail. Do not use naive conditional-correlation eyeballing as evidence (conditioning bias). Never an auto-trade or Webull fee input.

- Evidence strength: Strong empirical (two independent Tier-1/Tier-2 bias-corrected studies + mechanism + consistency with Roll 1988).

- Last review date: 2026-08-31.

- Revalidation trigger: Post-2015 evidence that downside correlation asymmetry has materially changed (single-name/0DTE flows, passive dominance, crypto-equity coupling), OR account-specific evidence that this account's high-beta holdings reliably follow aggregate breadth on soft risk-off days.

- Source: Ang, Andrew and Joseph Chen, "Asymmetric Correlations of Equity Portfolios," Journal of Financial Economics 63(3):443–494 (2002); Longin, François and Bruno Solnik, "Extreme Correlation of International Equity Markets," Journal of Finance 56(2):649–676 (2001); conditioning-bias caveat: Boyer, Brian H., Michael S. Gibson and Mico Loretan, "Pitfalls in Tests for Changes in Correlations" (1999, FRB IFDP 597). Full daily note: research/daily/2026-08-31.md. Cross-references: Roll (1988) low individual-stock R² / idiosyncratic dominance (research/daily/2026-08-07.md); standing-inverse-etf-conditions (operationalizes the genuine risk-off regime gates); FAILED_IDEAS 2026-07-25 (VIX threshold is not a buy signal) and 2026-07-18 (do not infer direction from a single macro headline) — ACORR-001 is the bearish-side analogue: a risk-off state is not a bearish single-name direction.

### KG-20260830-GKX-001 — US Equity Predictor Hierarchy: Price Trend > Liquidity/Size > Volatility > Valuation (Two-Source Admitted)

- Title: For monthly US equity cross-section prediction, price-trend characteristics (short-term reversal, momentum) dominate; liquidity/size and volatility are secondary; most standalone fundamental accounting ratios lack independent incremental information when conditioning on the dominant predictors. Admitted 2026-09-01 (daily_book_learning_claude), domain methodology.

- Core conclusion: Two independent empirical studies from different research groups using different methods reach consistent conclusions about US equity cross-sectional return predictors. (1) GKX 2018/2020 (Gu-Kelly-Xiu, RFS): 11 ML methods (OLS through NN5) across 94 characteristics, CRSP 1957-2016, ~30,000 stocks — short-term reversal (mom1m) is #1 across ALL 11 methods; momentum (mom12m) is tier-1; liquidity/size tier-2; idio vol/beta tier-3; valuation tier-4; most accounting-ratio changes and event dummies near-zero. (2) FNW 2020 (Freyberger-Neuhierl-Weber, RFS): adaptive group LASSO nonparametric additive model, 36 characteristics, CRSP+Compustat 1963-2015 — selects only 15/36; most consistent predictors: r2-1 (short-term reversal), Rel to High (52-week high proximity), LME (size), SUV (volume); r12-2 (momentum) selected; BEME/book-to-market NOT selected after conditioning; most standalone accounting ratios excluded.

- Mechanism: Short-term reversal captures market microstructure effects and bid-ask bounce; momentum captures investor underreaction and trend-following. Liquidity and size proxy for expected illiquidity compensation or investor neglect. Fundamental ratios are slow-moving and persistent — at monthly frequency their incremental signal is absorbed by faster-moving trend and liquidity signals. FNW formalizes: portfolio sorts are a special case of nonparametric regression (Cochrane 2011), so the hierarchy is method-agnostic at the conceptual level.

- Supporting evidence: (1) GKX (Gu-Kelly-Xiu 2020, Review of Financial Studies, Tier-2 peer-reviewed, NBER WP 25398): 11 ML methods agree on hierarchy. (2) FNW (Freyberger-Neuhierl-Weber 2020, Review of Financial Studies, Tier-2 peer-reviewed, NBER WP 23227): nonparametric LASSO independently confirms same dominant predictors using different method and different characteristic universe. Both studies conducted independently, published in same journal in same year (2020) from different research groups.

- Contrary evidence: (a) McLean-Pontiff (2016): anomaly returns decay post-publication; GKX second-half hierarchy weaker; FNW finds more characteristics selected in 1991+ consistent with publication-period effects. (b) Transaction costs: GKX NN strategy requires ~120-130% monthly turnover; gross Sharpe ratios are NOT net-of-cost estimates. (c) Both studies end pre-2017 — post-2020 structural changes (passive ETF dominance, 0DTE flows, factor proliferation) may have altered the hierarchy. (d) Non-US markets: hierarchy is US-specific and not yet independently validated internationally in this program.

- Applicable environment: US equity signal priority ranking at monthly frequency — use as a "first-tier vs. second-tier" mental model when assessing whether a proposed factor/signal type is likely to provide independent information. Evaluating cross-sectional screening candidates. Justifying deprioritization of standalone P/B, P/E, ROA, ROE without trend/liquidity conditioning in multi-factor models.

- Non-applicable environment: Annual-frequency prediction (price trends less dominant; fundamentals more important at 1-year+ horizon). Non-US markets (not validated). Post-2016 data (revalidation needed). Direct trading strategy implementation without transaction cost modeling. Factor timing (cross-sectional hierarchy, not time-series).

- Time scale: Monthly cross-sectional return prediction. Not a market-timing or daily signal.

- Use in premarket reports: When evaluating a stock candidate, note its signal type tier. Price-trend signals (short-term reversal, 12-month momentum, 52-week high proximity) are in the dominant tier. Standalone valuation signals (P/B, P/E alone) are in the weaker tier without conditioning. Do not treat this as a buy/sell recommendation — it is a cross-sectional portfolio construction insight, not a single-stock predictor.

- Prohibited use: Do NOT use GKX or FNW gross Sharpe ratios as expected live-trading performance. Do NOT treat short-term reversal dominance as a single-stock buy/sell signal (it is a cross-sectional ranking result). Do NOT use this hierarchy for factor timing without verifying macro-regime conditioning. Do NOT dismiss fundamental analysis — prohibited use applies only to standalone signals without trend/liquidity conditioning. Never an auto-trade or Webull fee input.

- Evidence strength: Strong (two independent Tier-2 RFS peer-reviewed studies from different research groups using different methods — ML ensemble and nonparametric LASSO — reaching consistent conclusions for US equities 1957-2015/2016). Revalidation needed for post-2017 and non-US environments.

- Last review date: 2026-09-01.

- Revalidation trigger: Downgrade to candidate if post-2017 study with comparable methodology finds materially different hierarchy; or if non-US study finds price-trend dominance absent outside US; or if passive investing / 0DTE structural change produces evidence that short-term reversal or momentum have lost independent predictive power post-2020.

- Source: Gu, Shihao, Bryan Kelly, and Dacheng Xiu, "Empirical Asset Pricing via Machine Learning," Review of Financial Studies 33(5):2223-2273 (2020); original NBER Working Paper No. 25398 (December 2018, revised September 2019). Freyberger, Joachim, Andreas Neuhierl, and Michael Weber, "Dissecting Characteristics Nonparametrically," Review of Financial Studies 33(5):2279-2338 (2020); original NBER Working Paper No. 23227 (March 2017, revised August 2019). Full daily notes: research/books/2026-08-30-gu-kelly-xiu-nber-w25398-empirical-asset-pricing-ml-2018.md; research/books/2026-09-01-freyberger-neuhierl-weber-nber-w23227-dissecting-characteristics-2020.md. Cross-references: KG-20260901-FNW-001 (FNW-specific candidate card); KG-20260830-GKX-002 (shallow NN advantage); KG-20260803-HLZ-MP-001 (multiple-testing guardrail); FAILED_IDEAS.md (McLean-Pontiff decay).

### KG-20260902-CFO-001 — Options Strategies for Portfolio Risk Management: Covered Calls, Protective Puts, Straddles, and Greeks (Mature Methodology Admitted)

- Title: Standard option strategies (covered call, protective put, straddle) create asymmetric return distributions; Greeks (Delta, Gamma, Vega, Theta, Rho) measure position risk sensitivities with Delta as the dominant first-order risk. Admitted 2026-09-02 (daily_book_learning_claude), domain derivatives.

- Core conclusion: Covered call (long stock + short call): truncates right tail and adds call premium income, sacrificing upside above strike X; breakeven at S=X+C. Protective put (long stock + long put): floors downside at strike X at cost of put premium P; breakeven at S=X-P. Straddle (long call + long put at same X): profits when realized volatility exceeds implied (actual |move| > C+P). Bull call spread (buy X₁, sell X₂>X₁): limited gain and limited loss; net cost reduced vs. outright call. Key Greek risk hierarchy: Delta (∂C/∂S; 0-1 for calls; drives daily P&L most directly) > Gamma (∂²C/∂S²; highest ATM; rate of Delta change) > Vega (∂C/∂σ; same sign for calls and puts; highest ATM; critical in high-vol environments) > Theta (∂C/∂t; negative for holders; time decay) > Rho (∂C/∂r; smaller for short-dated options). Sharpe ratios are misleading for option strategies because standard deviation does not capture asymmetric tail truncation.

- Mechanism: Option payoffs are asymmetric (bounded on one side), so combining options with the underlying creates the desired asymmetric payoff profile. No-arbitrage put-call parity (c−p = S−X/(1+r)^T−D) ensures consistent relationships between calls, puts, and the underlying. Greeks are partial derivatives of the Black-Scholes formula; they are consistent across pricing models. Portfolio insurance (dynamic delta replication of a protective put) contributed to the 1987 crash by creating systematic selling pressure — practical replication requires continuous rebalancing and fails at price gaps.

- Supporting evidence: Clarke, de Silva, and Thorley (2013), CFA Institute Research Foundation monograph "Fundamentals of Futures and Options," 202 pages, full coverage. Admitted under "mature methodological principle" — Black-Scholes pricing (Nobel Prize 1997; peer-reviewed since 1973), standard option strategies (40+ years institutional practice), Greek risk measures (standard practitioner framework). CFA Research Foundation is an authoritative source for practitioner financial methodology.

- Contrary evidence: None to the mechanical relationships (no-arbitrage derived). Sharpe ratio limitation for option strategies is explicitly documented by the source itself. Dynamic replication has known practical limits (gap risk, transaction costs, continuous rebalancing requirement — 1987 crash cited). IV smile shows the BS lognormal assumption is violated in practice (addressed in CFO-002).

- Applicable environment: Understanding ETF/index option structure (QQQ, QQQM, SPY, VIX-based instruments) for premarket analysis context. Interpreting VIX and option-implied expected moves for event-day position sizing (see CFO-002). Evaluating covered call income potential or protective put cost for index ETF positions if options trading is user-approved. Postmarket assessment of whether option-strategy risk descriptions are mechanically correct.

- Non-applicable environment: Do not use 2012-era AAPL IV examples as current market benchmarks. Do not apply delta-neutral hedging formulas without current live option market quotes. Do not use dynamic replication / portfolio insurance without continuous automated hedging capability. Do not extend non-dividend-adjusted BS formula to dividend-paying stocks without the S* correction.

- Prohibited use: Do NOT use BS formula outputs as exact trading prices without current live market quotes. Do NOT treat Sharpe ratios of option strategies at face value — covered call truncates right tail, making SR appear higher than risk-adjusted reality. Do NOT treat covered call or protective put as "free" risk management — both have explicit costs. Do NOT auto-execute any option order. Do NOT assume options trading is available in the current account without user confirmation.

- Evidence strength: Strong (mature methodological principle — 40+ years of peer-reviewed and practitioner validation of no-arbitrage option pricing and Greek risk measures).

- Last review date: 2026-09-02.

- Revalidation trigger: No empirical revalidation required for the mechanical relationships (no-arbitrage derived). Update if: account confirms options trading access (changes applicable environment); new structural market change materially alters standard Greeks interpretations (e.g., 0DTE dominance).

- Source: Clarke, Roger G., Harindra de Silva, and Steven Thorley, "Fundamentals of Futures and Options," CFA Institute Research Foundation Monograph (2013). Research Foundation open-access PDF at rpc.cfainstitute.org; locally cached at research/books/cfa_rf_futures_options_2013.pdf; 3,249,438 bytes; SHA-256: 805583130215fe069b4d05edd1c110b9f6b584127b2cdadf8a2e29c8d7125c18; 202 pages, 193 substantive, 9 blank; PyMuPDF extraction; 193/193 substantive pages read. Daily note: research/books/2026-09-02-clarke-de-silva-thorley-cfa-rf-fundamentals-futures-options-2013.md. Cross-references: KG-20260902-CFO-002 (IV smile and VIX term structure); KG-20260826-EAVAR-001 (earnings-window variance spike — CFO-001 provides the option-cost context for hedging vs. share reduction); KG-20260821-DIV-001 (concentration limits — option strategies are one tool for managing concentrated single-name risk).

### KG-20260902-CFO-002 — Implied Volatility as Market Risk Indicator: IV Smile, VIX Term Structure, and Expected-Move Sizing (Mature Methodology Admitted)

- Title: Implied volatility (IV) is the market's forward-looking variance estimate extracted from option prices; IV smile shows downside tail risk is priced beyond lognormal; VIX term structure distinguishes current turbulence (inverted) from expected future volatility rise (upward-sloping); ATM straddle provides an options-implied expected-move sizing input. Admitted 2026-09-02 (daily_book_learning_claude), domain derivatives.

- Core conclusion: (1) IV SMILE/SKEW: For equity indices, OTM put IV > ATM IV > OTM call IV as strike increases — IV decreases monotonically with strike. AAPL August 2012: 560-strike IV=26.75%; 660-strike IV=20.83%. The skew indicates the market prices a fat left tail relative to the lognormal assumption — crash risk is more expensive than upside surprise of equal magnitude. (2) VIX TERM STRUCTURE: Upward-sloping (near-term VIX < longer-dated, e.g., Aug 2012 at 14/16/20 for near/3M/5M) = calm current environment, market expects volatility to rise over time. Inverted (near-term VIX > longer-dated, e.g., VIX>30 in Aug 2011) = current acute turbulence expected to resolve. (3) ATM IV APPROXIMATION (Brenner-Subrahmanyam): σ ≈ √(2π/T) × (C+P)/(2S) — allows rough IV estimation from ATM call + put market prices. Option-implied expected move: ≈ IV × S × √(T/252) for a T-day horizon; used for event-day position sizing (paired with KG-20260826-EAVAR-001 earnings variance context).

- Mechanism: Options are priced by no-arbitrage; the market's consensus expected future variance is embedded in current option prices. Extracting IV (by inverting BS or using the ATM approximation) provides a forward-looking volatility estimate. IV smile reflects excess demand for downside insurance (protective puts) beyond what the lognormal distribution implies — consistent with jump risk and fat left tails. VIX uses a model-free replication of the 30-day forward variance across all available S&P 500 option strikes and two nearest expirations, converting to an annualized standard deviation.

- Supporting evidence: Clarke, de Silva, and Thorley (2013), CFA Institute Research Foundation monograph, pp. 82-116. Admitted under "mature methodological principle" — IV extraction from BS has been standard practice since Black-Scholes (1973); VIX launched CBOE 1993; IV smile first documented systematically after the 1987 crash; Brenner-Subrahmanyam ATM approximation widely used. CFA Research Foundation is an authoritative practitioner methodology source.

- Contrary evidence: None to the IV extraction mechanics (no-arbitrage derived). Important caveats: IV is a risk-neutral measure, not a physical probability estimate — it includes variance risk premiums, so realized volatility is typically lower than IV on average (variance risk premium). IV is not a directional signal (see FAILED_IDEAS: VIX threshold is not a buy signal). 0DTE option proliferation post-2020 may have altered near-term VIX dynamics — worth noting in future research.

- Applicable environment: Premarket VIX level and term structure assessment — distinguish upward-sloping (calm/rising expected vol) from inverted (current turbulence). Event-day or earnings-day position sizing using option-implied expected move. Identifying vol regime for ACORR-001 (downside correlation asymmetry) regime gate: inverted high-VIX supports genuine down-tail regime; low upward-sloping VIX argues against. Monthly prompt-eval: verifying volatility references in reports correctly distinguish historical vol from IV.

- Non-applicable environment: Do not use 2012-era AAPL or specific historical IV numbers as current benchmarks. Do not use VIX level as a directional timing signal (see FAILED_IDEAS.md: VIX threshold is not a buy signal). Do not use IV alone as a sell trigger without confirming the underlying holding's price action. Annual or long-horizon prediction (IV is a 30-day or near-term risk measure).

- Time scale: Near-term (30-day for VIX; event-window for individual option straddles). Not a multi-month directional signal.

- Prohibited use: Do NOT treat IV as a first-moment (directional) trading signal — it is a second-moment (variance) measure. Do NOT auto-trade on VIX crossings or IV extremes without regime confirmation and approval-gated draft. Do NOT confuse IV with realized volatility — IV is ex-ante market expectation, realized vol is ex-post measurement. Do NOT treat VIX term structure inversion alone as a sell signal. Never an auto-trade or Webull fee input.

- Evidence strength: Strong (mature methodological principle — 40+ years of IV extraction practice, peer-reviewed since BS 1973, VIX standard since 1993, IV smile extensively documented post-1987).

- Last review date: 2026-09-02.

- Revalidation trigger: No empirical revalidation required for core mechanics. Monitor: 0DTE dominance post-2020 and its effect on near-term VIX dynamics (worth a future research note). Update if account enables options trading (changes applicable environment).

- Source: Clarke, Roger G., Harindra de Silva, and Steven Thorley, "Fundamentals of Futures and Options," CFA Institute Research Foundation Monograph (2013), pp. 82-96, 113-116. Research Foundation open-access PDF at rpc.cfainstitute.org; locally cached at research/books/cfa_rf_futures_options_2013.pdf; 3,249,438 bytes; SHA-256: 805583130215fe069b4d05edd1c110b9f6b584127b2cdadf8a2e29c8d7125c18. Daily note: research/books/2026-09-02-clarke-de-silva-thorley-cfa-rf-fundamentals-futures-options-2013.md. Cross-references: KG-20260902-CFO-001 (option strategies — CFO-002 is the volatility-risk lens for CFO-001 strategies); KG-20260826-EAVAR-001 (earnings-window IV run-up and vol crush — the post-event IV collapse makes buying event-window options systematically expensive); KG-20260831-ACORR-001 (downside correlation regime — CFO-002 provides the VIX term structure input for the regime gate); FAILED_IDEAS.md (VIX threshold is not a buy signal).

### KG-20260902-VMR-001 — Volatility Mean Reversion + Asymmetry: a Volatility-Driven Risk-Off STATE Is Transient; Downgrade a Stale Risk-Off Lean as VIX Rolls Over (Gated), Keep It in a Persistent Regime — NOT a Directional Buy Signal

- Title: Equity-index conditional volatility is persistent-but-mean-reverting and asymmetric (leverage/volatility-feedback); a volatility-driven risk-off STATE is transient once the shock stops renewing, so a directional risk-off lean must be actively belief-downgraded as VIX rolls over (gated on confirmation), kept only in a high-persistence / genuine regime shift. Admitted 2026-09-02 (research_a), domain risk_management, as mature methodological principle.

- Core conclusion: (1) MEAN REVERSION (Engle 1982 ARCH; Bollerslev 1986 GARCH): conditional variance clusters but, for a stationary process (persistence α+β<1), reverts toward long-run variance ω/(1−α−β); a k-step variance forecast decays to the long-run level at rate (α+β)^k once shocks stop renewing — a spike is not permanent. (2) ASYMMETRY (Black 1976; Christie 1982; Nelson 1991 EGARCH; Glosten-Jagannathan-Runkle 1993 GJR-GARCH): a negative return raises next-period conditional variance asymmetrically MORE than a positive one, so a selloff spikes VIX far more than a rally compresses it, and as prices stabilize the asymmetric term stops feeding variance and the spike relaxes. Implication: a risk-off STATE from a vol spike is TRANSIENT once down-shocks stop; as VIX rolls over, the term structure re-steepens from inverted, and breadth turns, the elevated-risk state decays and a directional risk-off LEAN must be belief-DOWNGRADED toward neutral/constructive, not anchored. Grounds RULE-20260902-01 (2026-09-02: held a 3-day risk-off lean while VIX −6.85% to 15.22, breadth positive, SPY +0.45%, IWM +1.19%, NVDA +3.21% — the shock had stopped renewing).

- Mechanism: GARCH(1,1) σ²_t=ω+α·ε²_{t-1}+β·σ²_{t-1}; unconditional variance ω/(1−α−β); persistence α+β sets decay speed. Clustering keeps the market jumpy for a few sessions after a shock; mean reversion fades that state once fresh negative shocks stop. GJR/EGARCH asymmetry (leverage: equity falls → leverage rises → vol rises; and/or volatility-feedback) means the spike is downside-driven and relaxes once prices stabilize/recover.

- Supporting evidence: Bollerslev (1986, J. Econometrics 31(3):307-327) on Engle (1982, Econometrica) — mean-reverting conditional variance; Glosten-Jagannathan-Runkle (1993, JF 48(5):1779-1801), Nelson (1991, Econometrica 59(2):347-370 EGARCH), Christie (1982, JFE) — downside volatility asymmetry. Admitted as mature methodology (ARCH/GARCH is Nobel-recognized, Engle 2003; the asymmetry is among the most replicated equity-volatility facts).

- Contrary evidence: High persistence / IGARCH (α+β≈1) → no finite unconditional variance, slow decay; long memory (Ding-Granger-Engle 1993 / FIGARCH) → hyperbolic (slow) decay, though apparent long memory may be spurious from structural breaks (Starica-Granger critique); mechanism-attribution debate ("Is the leverage effect a leverage effect?", Hasanhodzic-Lo) — asymmetry robust, cause debated. All bound the application: confirm the regime, do not assume fast decay. Contradiction note: research/contradictions/2026-09-02-volatility-mean-reversion-vs-persistence.md.

- Applicable environment: Premarket belief-update after a multi-day selloff (downgrade a risk-off lean once VIX rolls over + term structure re-steepens + breadth turns; reconsider conditional core-ETF dip-buys via approval-gated drafts and existing size gates). Setting the decaying RISK STATE / max-size input consumed by standing-vix-permission-not-order and staging rules. Intraday transient-vs-persistent spike distinction. Postmarket audit of regime-persistence / anchoring errors. Monthly prompt-eval missed-relief-rebound canary (paired with ACORR-001 down-tail canary).

- Non-applicable environment: High-persistence / IGARCH / long-memory / confirmed structural-break or crisis regime (keep the risk-off state; do not downgrade on one green day); any use as a directional return forecast or buy/sell trigger; single illiquid names.

- Time scale: Days-to-weeks risk-state decay (not intraday ticks, not multi-month direction).

- Use in premarket reports: After a selloff, state whether the vol shock is relaxing (VIX rolling over, term structure normalizing, breadth turning) or persistent; if relaxing, downgrade the risk-off lean to neutral/constructive rather than anchoring it; if persistent/regime-shift, keep it. Pair with CFO-002 (VIX term structure input) and ACORR-001 (down-tail entry).

- Prohibited use: A falling VIX is not a buy signal (it times risk-state decay, not price direction — FAILED_IDEAS 2026-07-25). Do not mechanically downgrade after one up day (regime-dependent decay; require confirmation). Do not over-literalize the leverage cause. Never an auto-trade or Webull fee input; any dip-buy is an approval-gated draft under the EV/W/confirmation math gate and concentration limits.

- Evidence strength: Strong (mature methodological principle; Nobel-lineage ARCH/GARCH mean reversion + extensively replicated downside asymmetry), scoped conservatively with explicit regime boundary conditions.

- Last review date: 2026-09-02.

- Revalidation trigger: Evidence that modern structure (0DTE flows, vol-control funds, passive dominance) materially changed VIX mean-reversion speed or the downside asymmetry, OR account-specific evidence of repeated too-early/too-late risk-off downgrades (recalibrate the confirmation gate).

- Source: Bollerslev, Tim, "Generalized Autoregressive Conditional Heteroskedasticity," Journal of Econometrics 31(3):307–327 (1986); Engle, Robert F., "Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation," Econometrica 50(4):987–1008 (1982); Glosten, Lawrence R., Ravi Jagannathan and David E. Runkle, "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks," Journal of Finance 48(5):1779–1801 (1993); Nelson, Daniel B., "Conditional Heteroskedasticity in Asset Returns: A New Approach," Econometrica 59(2):347–370 (1991); Christie, Andrew A., "The Stochastic Behavior of Common Stock Variances," Journal of Financial Economics 10(4):407–432 (1982). Full daily note: research/daily/2026-09-02.md. Cross-references: KG-20260831-ACORR-001 (down-tail ENTRY vs VMR-001 risk-relaxation EXIT — symmetric calibration pair); KG-20260902-CFO-002 (VIX term-structure snapshot input); KG-20260814-RERP-001 (short-term reversal as liquidity provision — reversal is a conditional risk frame, not a daily catalyst); FAILED_IDEAS 2026-07-25 (VIX drop is not a buy signal) and the admitted "VIX sets risk state and max size, not direction."

### KG-20260903-GKS-001 — Grinold-Kroner-Siegel Supply Model for Forward ERP Estimation (Mature Methodology Admitted)

- Title: The GKS supply model is a three-component identity for decomposing and forecasting equity total return: (1) Income Return = dividend yield + net repurchase yield + cash-financed M&A yield; (2) Nominal Earnings Growth = inflation + real growth − dilution; (3) Repricing = P/E change. ERP = total return − risk-free rate (10yr Treasury). Admitted 2026-09-03 (daily_book_learning_claude), domain portfolio_construction.

- Core conclusion: Equity return = Income Return + Nominal Earnings Growth + Repricing. This is an accounting identity, not an assumption — any ERP view must be expressible as component assumptions. KEY CONSTRAINTS: (a) Dilution (~1-2%/yr US): new share issuance from SEOs, employee options reduces per-share growth below aggregate GDP/earnings growth. (b) P/E expansion windfall: historical +0.58%/yr (P/E expanded 11.3→18.5, 1926-2010) is NOT expected to repeat; set repricing ≈ 0 for forward estimates. (c) Real dividend growth ≈ per-capita GDP growth − 2pp: cross-country evidence from 19 countries (DMS 1900-2010) shows real dividend growth averages 2-2.5pp BELOW real GDP growth consistently. (d) MULTI-AUTHOR CONVERGENCE (CFA RF 2011): Ibbotson (~4%), Asness (~3-4%), DMS (3-3.5%), Grinold-Kroner-Siegel (3.6%), Ilmanen (~3%), Chen (~3.6%) — all using supply-model variants — converge on 3.0-3.6% geometric ERP over 10yr Treasuries as of 2011. Forward estimate is not "current" — recompute with today's dividend yield, TIPS breakevens, and 10yr Treasury yield.

- Mechanism: No-arbitrage decomposition. Shareholders receive income (cash distributions) and capital gains (earnings growth). Capital gains can be further decomposed into fundamental growth (per-share earnings × economy) and multiple expansion (P/E change). Since multiple expansion cannot rise indefinitely, long-run forward ERP estimates should exclude it. Dilution corrects for the gap between aggregate corporate earnings growth and per-share growth: when companies issue new shares for options or capital raises, existing holders' proportional claims shrink.

- Supporting evidence: Grinold, Kroner, and Siegel (2011), "A Supply Model of the Equity Premium," pp. 53-70 in Hammond-Leibowitz-Siegel (eds.) "Rethinking the Equity Risk Premium," CFA RF 2011 (primary source). Corroborated within the same volume by chapters from Ibbotson (pp. 18-26), Asness (pp. 27-31), Dimson-Marsh-Staunton (pp. 32-52), Ilmanen (pp. 107-122), and Chen (pp. 123-135). All six authors use supply-model or build-up variants and converge on 3.0-3.6% forward geometric ERP. Admitted under "mature methodological principle" — GKS traces to Diermeier-Ibbotson-Siegel (1984) and Grinold-Kroner (FAJ 2002); 20+ years of practitioner application; included in CFA curriculum.

- Contrary evidence: P/E expansion could resume from macro/structural drivers (e.g., further decline in required returns from demographics or financial innovation — but Taylor 2026 argues opposite; Ilmanen 2011 shows CAPE elevated at 23 vs 16.5 historical mean). Dilution assumption (1-2%) may change in buyback-dominant era (Arnott argues buybacks historically offset by dilution; post-2010 aggregate is unclear). Key model risk: income return component changes daily with market price; real growth projections (GDP, population) carry high uncertainty.

- Applicable environment: Annual or multi-year strategic asset allocation: use supply model to generate forward-looking equity return rather than raw historical average. Cross-asset allocation: compare GKS equity expected return with current bond yield as the expected bond return. Research A macro analysis: when evaluating whether market is cheap/expensive, express the view as component assumptions (income return = current yield; growth = consensus; repricing = mean-reversion assumption). Monthly evaluation: update income return with current S&P 500 dividend + repurchase yield.

- Non-applicable environment: Do NOT use as a short-term or tactical trading signal — this is a 10-year expected-return framework, not a 1-3 month tool. Do NOT use 2011-vintage specific numbers (3.6%) as current ERP estimates — recompute with current market data. Do NOT extrapolate historical P/E expansion into forward estimates. Do NOT assume real dividend growth tracks real GDP growth (evidence shows 2pp below GDP growth consistently).

- Time scale: Multi-year (5-20yr investment horizon). Not applicable to quarterly or monthly return forecasting.

- Prohibited use: Do NOT treat GKS output as a precise forecast (wide uncertainty from repricing and growth assumptions). Do NOT auto-trade based on cross-asset ERP comparison without user approval. Never an auto-trade or Webull fee input.

- Evidence strength: Strong (mature methodological principle — 20+ years practitioner application, CFA curriculum, multi-author convergence in CFA RF 2011 authoritative volume).

- Last review date: 2026-09-03.

- Revalidation trigger: If corporate payout policy shifts materially (dividends vs. buybacks); if new empirical evidence changes the dividend-growth-vs-GDP relationship substantially; if supply model fails systematically vs. realized ERP over a 10-year OOS window.

- Source: Hammond, P. Brett Jr., Martin L. Leibowitz, and Laurence B. Siegel (eds.), "Rethinking the Equity Risk Premium," CFA Institute Research Foundation Monograph (2011). Primary chapter: Grinold, Kroner, and Siegel, "A Supply Model of the Equity Premium," pp. 53-70. CFA RF open-access monograph; rpc.cfainstitute.org; locally cached at research/books/rethinking_equity_risk_premium_cfa_rf_2011.pdf; 8,226,138 bytes; SHA-256: 3f6ec68ef136eee22b4150fbbb47e4537350ab5aeac0cc489eb1766505caa6ac; 164 pages (0 blank), 164/164 substantive pages read. Book note: research/books/2026-09-03-hammond-leibowitz-siegel-cfa-rf-rethinking-erp-2011.md. Cross-references: KG-20260818-COCH-001 (ERP time variation — all P/D variation = discount-rate variation; GKS-001 provides the decomposition framework); KG-20260813-FIE-002 (no fixed ERP; GKS-001 provides the component model for why ERP varies); KG-20260814-DMS-001 (cross-country global ERP evidence — confirms GKS-001's dividend-growth-below-GDP finding cross-country); KG-20260903-EPP-001 (candidate: equity premium puzzle — provides theoretical grounding for why ERP is structurally positive).

### KG-20260831-IMV-001 — Block Time-Series Cross-Validation Required for Autocorrelated Financial Data (Mature Methodology Admitted 2026-09-04)

- Title: Standard k-fold or LOO cross-validation on autocorrelated financial time series is invalid — it overfits due to look-ahead contamination via random fold assignment. Gap-block modified CV with temporal ordering is the required alternative. Admitted 2026-09-04 (daily_book_learning_claude), domain methodology, two independent peer-reviewed sources.

- Core conclusion: (1) INVALIDITY OF STANDARD CV: Hart and Wehrly (1986) proved that LOO CV systematically overfits when data are positively correlated, because the training and validation sets are not approximately independent — nearby time points share autocorrelation memory. Choosing folds randomly allows future observations to be included in training, leaking forward information. (2) REQUIRED SOLUTION: Modified CV with gap h — choose training set I(t) and validation set I(v) such that every training index and every validation index are separated by at least h time steps (min|i−j| > h for all i∈I(t), j∈I(v)). For LOO: I(v)={J}, I(t)={1,...,J-h-1, J+h+1,...,n}. Gap h ensures ξ_i (training) is approximately independent of ξ_J (validation) for short-range dependent processes. (3) BLOCK SIZE GUIDANCE: h should match the effective "memory length" of the series — the order of the autoregressive process or the regime-switching memory. (4) ASYMPTOTIC OPTIMALITY: Modified CV is proven asymptotically optimal for α-mixing processes (Hart-Vieu 1990) and long-range dependences (Hall et al. 1995) with appropriate h. (5) THREE APPROVED METHODS: Rolling window (constant training size), expanding window (cumulative training), time-series split (strict chronological ordering per fold).

- Mechanism: Autocorrelated time series have memory: the value at time t is correlated with values at t-1, t-2, ..., t-k. In standard k-fold CV, training folds contain observations from both before and after the validation point, making the model implicitly "aware" of future patterns. The gap block eliminates this by discarding the h observations immediately surrounding each validation point from training, ensuring the training sample cannot exploit autocorrelation memory of the validation period.

- Supporting evidence: (1) Simonian, Joseph, "Investment Model Validation: A Guide for Practitioners," CFA Institute Research Foundation Monograph (2024), Chapter 3, pp. 9-11, Figure 2 — block CV with gap blocks for financial time series. (2) Arlot, Sylvain and Alain Celisse, "A survey of cross-validation procedures for model selection," Statistics Surveys, Vol. 4 (2010), pp. 40-79, Section 8.1 — theoretical proof (Hart-Wehrly 1986), gap-block modified CV method, asymptotic optimality (Hart-Vieu 1990, Hall et al. 1995). Statistics Surveys is a peer-reviewed open-access journal by the Institute of Mathematical Statistics (IMS). Admitted under "mature methodological principle" — the issue of CV invalidity for dependent data has been known since at least Hart-Wehrly (1986) and is now standard in statistics education.

- Contrary evidence: Bergmeir-Hyndman-Koo (2018, CSDA) argue that for univariate forecasting with low autocorrelation in residuals, LOO CV can work if applied to residuals from a base model (because residuals are approximately iid). This is a narrow exception requiring explicit residual-iid verification — it does NOT apply to return or factor model validation where autocorrelation is structural.

- Applicable environment: Time-series return forecasting (monthly, weekly, daily frequencies) — all model validation must use block CV. Factor model validation on historical return panels. Volatility forecasting model evaluation. Macro signal model validation (GDP, credit spreads, yield curve). Trading model backtesting with autocorrelated signals. Research program evaluation of any model trained on financial time series.

- Non-applicable environment: Pure cross-sectional data without a temporal dimension. IID datasets where observations are truly independent (verify via Ljung-Box or Durbin-Watson before applying block CV). Very short time series (<20 observations) where CV has too few degrees of freedom in any form.

- Time scale: Applies whenever the evaluation set has autocorrelated structure. The gap h is typically 1-12 periods depending on the series memory length.

- Prohibited use: Do NOT use standard k-fold CV on autocorrelated financial time series without the gap-block modification — results will be optimistic due to look-ahead contamination. Do NOT omit gap blocks between folds when the time series exhibits even mild autocorrelation (test with Ljung-Box; if autocorrelation is detected, block CV is mandatory). Do NOT interpret random-fold CV performance as a valid OOS estimate for any model applied to autocorrelated financial data. Never an auto-trade or Webull fee input.

- Evidence strength: High (mature methodological principle — two independent peer-reviewed sources from different research groups: Simonian CFA RF 2024 practitioner synthesis + Arlot-Celisse Statistics Surveys 2010 theoretical proof; underlying Hart-Wehrly 1986 is foundational; asymptotic optimality of gap-block CV proven for standard dependence classes).

- Last review date: 2026-09-04.

- Revalidation trigger: If Bergmeir-Hyndman-Koo (2018) exception — LOO on residuals (not raw data) for low-autocorrelation forecasting — is read and found to apply to specific financial forecasting use cases, create a scoped exception note. No fundamental revalidation needed (theoretical proof is established).

- Source (primary): Simonian, Joseph. "Investment Model Validation: A Guide for Practitioners." CFA Institute Research Foundation Monograph (2024). Chapter 3, pp. 9-11. Book note: research/books/2026-08-31-investment-model-validation-simonian-cfa-rf-2024.md. Source (second): Arlot, Sylvain and Alain Celisse. "A survey of cross-validation procedures for model selection." Statistics Surveys, Vol. 4 (2010), pp. 40-79. DOI: 10.1214/09-SS054. Open-access at projecteuclid.org; locally cached at research/books/arlot_celisse_statistics_surveys_2010_cv_survey.pdf; 559,505 bytes; SHA-256: ac9095b16ba5f798496ded627e5f646988728a9dcb4da04fbc32896a7a4f242f; 40 pages. Book note: research/books/2026-09-04-arlot-celisse-statistics-surveys-2010-cv-survey.md. Cross-references: KG-20260801-ISL-OOS-002 (OOS validation discipline — IMV-001 extends with specific block structure requirement for time series); KG-20260803-HLZ-MP-001 (multiple-testing guardrail — block CV is one component of rigorous model validation); KG-20260831-IMV-002 (synthetic data hierarchy — companion methodology card from same Simonian source).

### KG-20260904-MNSD-001 — Macro-Data News Sign-Dependence: "Good News Is Bad News" in a Strong-Economy/Hawkish Regime (Discount-Rate Channel Dominates); Decompose, Condition on Regime, Expect Dispersion — NOT a Mechanical Fade Signal

- Title: The equity SIGN of scheduled macro-data news is state-dependent — good real-activity news (e.g., a strong jobs print) can PRESSURE broad/rate-sensitive equities in a strong-economy/hawkish regime because the discount-rate channel dominates the cash-flow channel. Admitted 2026-09-04 (research_a), domain macro.

- Core conclusion: A macro print bundles a DISCOUNT-RATE/interest-rate channel and a CASH-FLOW/earnings channel; the net equity sign depends on which dominates, which depends on the business-cycle state and policy regime. Boyd, Hu & Jagannathan (2005, JF 60(2):649-672): rising unemployment ("bad news") is GOOD for stocks in expansions (rate channel dominates → lower expected rates) and BAD in contractions (cash-flow channel dominates). McQueen & Roley (1993, RFS 6(3):683-707): conditioning on business-cycle state, the stock-macro-news link is much stronger, and WHEN THE ECONOMY IS STRONG the market responds NEGATIVELY to GOOD real-activity news because the discount-rate effect outweighs the cash-flow effect. Grounds RULE-20260904-03 (2026-09-04): strong economy + strong NFP +162k → 10Y +0.46% → broad pressure (SPY −0.39%, DIA −0.53%, COIN −4.18%, MSFT −2.04%), while SMH +2.61% decoupled up on the AI cycle. Do NOT extrapolate one strong print into whole-market risk-on.

- Mechanism: A release updates both discount-rate and cash-flow expectations. In a strong economy / hawkish regime a strong real-activity print mainly raises expected policy rates and yields (discount-rate channel = Cochrane discount-rate variation, KG-20260818-COCH-001), lowering equity present values ("good is bad"), hitting long-duration/rate-sensitive/broad exposure most. In a weak/contracting economy or a dovish "Fed put" regime the same print mainly lifts expected earnings or eases policy fear (good is good). Aggregate result; sectors can override with idiosyncratic drivers → dispersion (combine with ACORR-001).

- Supporting evidence: Boyd-Hu-Jagannathan (2005, JF; NBER WP 8092; ~788 citations) — unemployment-news state-dependent sign; McQueen-Roley (1993, RFS; NBER WP 3520) — business-condition state-dependence incl. nonfarm payroll. Two independent Tier-1/2 peer-reviewed studies + discount-rate/cash-flow decomposition mechanism.

- Contrary evidence: The sign is state-dependent, so any mechanical "fade good data" fails in weak/contracting or dovish-pivot regimes. The sign also depends on the monetary-policy reaction function (modern Fed FEDS 2025-007 "Decoding Equity Market Reactions to Macroeconomic News"; Nagel-Xu 2024; Davig-Gerlach 2006). Reactions are fast and hard to trade net of costs; simultaneous releases contaminate the signal. Aggregate result ≠ every sector (2026-09-04 semis decoupled). Contradiction note: research/contradictions/2026-09-04-good-news-bad-news-regime-dependence.md.

- Applicable environment: Premarket direction calibration on scheduled macro-data days (jobs/NFP, CPI/PPI, ISM, GDP, retail sales) — decompose into rate vs cash-flow channels, condition the sign on business-cycle state AND policy regime, expect cross-sectional dispersion. Intraday: read the equity move against the yield move. Postmarket audit of macro-news call sign/regime. Monthly prompt-eval good-news-bad-news canary.

- Non-applicable environment: As a mechanical fixed-sign fade signal; monetary-policy DECISION surprises (separate channel — Nagel-Xu 2024 / FAILED_IDEAS 2026-07-18); single-name/sector calls where an idiosyncratic driver dominates (use ACORR-001); a same-day high-frequency trade trigger.

- Time scale: Event-day / days-around-release direction calibration; not an intraday tick signal or a multi-month view.

- Use in premarket reports: On a macro-data day, state the expected print, decompose the likely rate-channel vs cash-flow-channel effect, name the regime (strong/weak economy; hawkish/dovish), and give a sign that reflects the dominant channel PLUS expected dispersion (rate-sensitive/broad vs idiosyncratically-led sectors) — do not sign the whole market from one print.

- Prohibited use: Not a fixed "good=sell/bad=buy" rule (state-dependent). Do not extrapolate one print into a uniform whole-market call. Not an auto-trade or same-day execution signal; any positioning is an approval-gated draft under the math gate and concentration limits. Never a Webull fee input.

- Evidence strength: Strong (two independent Tier-1/2 peer-reviewed studies + robust discount-rate/cash-flow mechanism), scoped as a direction-calibration frame with explicit regime boundary conditions.

- Last review date: 2026-09-04.

- Revalidation trigger: Evidence the modern regime changed the dominant channel (durable dovish/low-inflation regime restoring "good is good", or a structurally higher-rate regime making the discount-rate channel dominant across more releases), OR repeated one-directional mis-signing of premarket macro-data calls (recalibrate the regime classifier). Recheck vs the modern Fed FEDS (2025) re-examination.

- Source: Boyd, John H., Jian Hu and Ravi Jagannathan, "The Stock Market's Reaction to Unemployment News: Why Bad News Is Usually Good for Stocks," Journal of Finance 60(2):649–672 (2005) (NBER WP 8092); McQueen, Grant and V. Vance Roley, "Stock Prices, News, and Business Conditions," Review of Financial Studies 6(3):683–707 (1993) (NBER WP 3520). Full daily note: research/daily/2026-09-04.md. Cross-references: KG-20260818-COCH-001 (discount-rate variation drives returns — the rate channel here IS the discount-rate channel); KG-20260831-ACORR-001 (idiosyncratic sector decoupling — the cross-sectional dispersion layer); the monetary-surprise MARKET_KNOWLEDGE entry and FAILED_IDEAS 2026-07-18 (policy-decision channel, distinct from this macro-data channel).

### KG-20260907-ANCH-001 — Reference-Price Anchoring Keeps Cash Idle Through a Recovery: Don't Gate Deployment Solely on a "Pullback to $X" Anchor; Pre-Commit a Staged Plan — BOUNDARY: In a Confirmed Downtrend, Waiting Is Correct

- Title: A salient reference price (recent low, cost basis, 52-week high) anchors the price at which an investor will transact; gating deployment on a return to the anchor risks sitting in cash through a recovery the anchor never revisits. Admitted 2026-09-07 (research_a), domain behavioral.

- Core conclusion: George & Hwang (2004, JF 59(5):2145-2176): investors use the 52-week HIGH as an anchor, are reluctant to bid past it, and underreact to news; nearness-to-52wh predicts returns better than past returns — a reference price biases willingness to transact. Baker, Pan & Wurgler (2012, JFE 106(1):49-71): in real M&A, recent peak prices anchor offer prices and acceptance probability jumps discontinuously once an offer clears the peak — independent-domain confirmation. Read-across to entry timing: an investor anchored to a recent low / cost basis / desired "pullback to $X" is reluctant to BUY above it, so conditioning deployment purely on a return to the anchor risks missing an entire recovery. Grounds RULE-20260903-01 (2026-09-01→03: ~34% idle cash held through a full down-tail→strong-rebound cycle waiting for a pullback that never printed). Remedy: when deployment is event-locked / pullback-conditioned AND cash is elevated (>~30%), pre-commit a STAGED plan (first tranche + trigger + invalidation) tied to the current thesis/regime and diversified core.

- Mechanism: Anchor-and-adjust (Tversky-Kahneman) — agents latch onto a salient prior price and adjust insufficiently, biasing the price they will pay/accept toward the anchor and making them reluctant to transact on the "wrong" side of it. For a cash-holder the anchor is a recent low or a self-set "buy only on a pullback to $X"; if the market recovers without printing it, the anchor blocks deployment and the idle-cash opportunity cost (KG-20260819-DCA-001) compounds. Distinct from status-quo/inertia (SQINERT-001 = failing to EXECUTE a decided change) and the disposition effect (holding losers): ANCH is failing to ENTER because a reference price blocks paying up.

- Supporting evidence: George-Hwang (2004, JF; anchor-and-adjust explanation of momentum) + Baker-Pan-Wurgler (2012, JFE; NBER WP 15551; reference-point offer-price anchoring, acceptance discontinuity at the peak). Two independent Tier-1/2 peer-reviewed studies across two domains (cross-sectional returns; M&A) + robust anchoring mechanism.

- Contrary evidence: "Waiting for a pullback" is correct in a confirmed downtrend / persistent risk-off (VMR-001) or a genuine down-tail (ACORR-001) — the rule targets anchor-driven inaction during a confirmed/relaxing recovery, not disciplined patience. The "missing the best days" market-timing stat is misleading (best/worst-day clusters roughly symmetric; Estrada) — the case rests on anchoring + DCA-001 idle-cash cost, not that stat. 52wh momentum/anchoring magnitude varies internationally, decays, and has transaction costs; the core cross-domain claim survives. Contradiction note: research/contradictions/2026-09-07-anchoring-waiting-vs-justified-patience.md.

- Applicable environment: Premarket deployment decisions that are event-locked or pullback-conditioned while cash is elevated (>~30%) — name the anchor risk and pre-commit a staged plan into diversified core (QQQM/VOO). Postmarket audit of idle-cash-through-recovery (anchor-driven inaction vs justified patience). Monthly prompt-eval idle-cash-through-recovery canary (ties to monthly-c-20260906 lockup-deployment gate). Any decision using a cost basis or 52-week high/low as an implicit threshold.

- Non-applicable environment: A confirmed downtrend / persistent risk-off / genuine down-tail (waiting is correct); legitimate event-lock caution for the catalyst's duration; as a market-timing/directional signal; as justification for a rushed off-plan single-name chase (FAILED_IDEAS 2026-08-22).

- Time scale: Days-to-weeks deployment-decision framing (not intraday ticks, not a multi-month view).

- Use in premarket reports: When cash is elevated and deployment is being deferred to a pullback/anchor, state the anchor risk explicitly and give a staged pre-committed deployment plan (first tranche + trigger + invalidation) conditioned on the current regime — rather than an open-ended "wait for a pullback to $X." Pair with the regime read (VMR-001/ACORR-001) that decides whether waiting is justified.

- Prohibited use: Do not force deployment in a confirmed downtrend/risk-off (gate on regime). Do not rest the case on the misleading best-days stat. Not an auto-trade or mechanical buy trigger — deployment is an approval-gated staged draft into diversified core under concentration + EV/W/confirmation math gates. Never a Webull fee input.

- Evidence strength: Strong (two independent Tier-1/2 peer-reviewed studies across two domains + robust anchor-and-adjust mechanism), scoped as a behavioral guardrail with an explicit regime boundary.

- Last review date: 2026-09-07.

- Revalidation trigger: Evidence reference-price anchoring in entry decisions has weakened, OR account/postmarket evidence the staged-deployment remedy either deployed into falling knives (tighten the regime gate) or still left cash idle through recoveries (strengthen the pre-commit).

- Source: George, Thomas J. and Chuan-Yang Hwang, "The 52-Week High and Momentum Investing," Journal of Finance 59(5):2145–2176 (2004); Baker, Malcolm, Xin Pan and Jeffrey Wurgler, "The Effect of Reference Point Prices on Mergers and Acquisitions," Journal of Financial Economics 106(1):49–71 (2012) (NBER WP 15551). Full daily note: research/daily/2026-09-07.md. Cross-references: KG-20260819-DCA-001 (idle-cash opportunity cost — the economic leg ANCH explains behaviorally); KG-20260821-DIV-001 (diversified-core deployment target); KG-20260902-VMR-001 / KG-20260831-ACORR-001 (regime boundary where waiting IS correct); KG-20260824-SQINERT-001 (inertia — failing to execute a decided change, vs ANCH failing to enter); FAILED_IDEAS 2026-08-22 (direction-agnostic deployment — the remedy must stay disciplined).

### KG-20260908-KNS-001 — PC-Sparse SDF Feasibility: Characteristics-Dense SDF Required for 50 Anomalies; PC-Sparse SDF (2-5 PCs) Captures Most Pricing; Eigenvalue-Proportional L2 Shrinkage Critical — CAUTION: Post-2005 Anomaly Decay Documented

- Title: Characteristics-sparse SDFs (FF5-type) fail to explain the cross-section of US equity anomaly portfolios; a PC-sparse SDF (2-5 high-variance PCs) captures most pricing; eigenvalue-proportional L2 shrinkage is critical. Admitted 2026-09-09 (daily_book_learning_claude), domain methodology.

- Core conclusion: Kozak, Nagel & Santosh (JFE 2020 / NBER WP 24070): for 50 well-known US equity anomaly portfolios (CRSP daily, 1974-2016), a characteristics-sparse SDF (e.g., FF5-type with 3-5 factors) cannot adequately summarize the cross-section. OOS R² (cross-validated) only rises to ~30% when all ~50 anomalies are included. Level shrinkage (Pástor-Stambaugh) achieves <5% OOS R²; eigenvalue-proportional L2 shrinkage (KNS method) achieves ~30%. In PC space: 2 PCs → ~65% of max OOS R²; 5 PCs → ~90%+. Pure OOS holdout (SDF estimated pre-2004; evaluated 2005-2016): 50-anomaly MVE portfolio earns 14.34%/yr alpha vs. CAPM (t=2.53) and 10.58% vs. FF5 (t=1.99), but only 3.21%/yr vs. 5-PC-sparse model (t=1.49). Top SDF factors (Table 1): Industry Rel. Rev. (LV) t=3.67, Ind. Mom-Reversals t=1.98, Earnings Surprises t=1.39; pure Momentum 12m only t=0.91 (11th) — industry reversals dominate the SDF, not price-trend. POST-2005 ANOMALY DECAY (Table 5): Momentum 12m 12.7%→-0.0%; Seasonality 18.7%→-4.6%; Industry Rel. Rev. (LV) -47.6%→-4.5%; Ind. Mom-Reversals 29.3%→-1.2% — systematic publication-decay pattern consistent with McLean-Pontiff (2016).

- Mechanism: (1) Absence of near-arbitrage implies factors earning substantial risk premia must concentrate in high-variance PCs; low-eigenvalue PCs that earn high SDF loadings would represent near-arbitrage, so they must be shrunk aggressively. This motivates eigenvalue-proportional L2 shrinkage. (2) The 50 documented anomalies are not redundant with each other in SDF space — each contributes a distinct pricing facet. (3) SDF risk prices (b = Σ⁻¹μ) are distinct from expected-return risk premia (μ): price-trend may dominate expected returns (GKX-001/FNW-001) while industry reversals dominate the SDF because the SDF depends on risk-price weights relative to covariances. (4) Post-2005 decay is consistent with McLean-Pontiff: publication causes arbitrageurs to trade anomalies, reducing return differentials.

- Supporting evidence: Primary: KNS (JFE 2020, Tier 1, 58 pages fully read, 10 spot-checks confirmed). Second source: KPS (KG-20260909-KPS-001; Kelly-Pruitt-Su JFE 2019; IPCA on individual stocks and managed portfolios; confirms PCA on managed portfolios achieves 95-98% total R² consistent with KNS PC-sparse finding; independently shows 4 latent factors span the cross-section; different data, different method). KPS explicitly cited in KNS-001's revalidation trigger.

- Contrary evidence: KPS extends KNS at the individual stock level: static PCA (without dynamic loadings/IPCA) has NEGATIVE predictive R² at the stock level → PC-sparse works for managed portfolios but requires dynamic loadings (IPCA) for individual stocks. Post-2005 momentum decay does not necessarily mean momentum is permanently dead — may be cyclical crowding effect. Post-publication decay most severe in momentum and seasonality; some anomalies (earnings surprises, value-profitability) show more modest decay.

- Applicable environment: Factor model construction using anomaly portfolios: include ALL available anomaly characteristics (50+); compress into PCs using eigenvalue-proportional L2 shrinkage; a 3-5 factor sparse model (FF5-type) should be assumed inadequate. Evaluating factor model adequacy: an FF5-type model leaves 10-25% annual alpha unexplained in OOS tests. Post-2005 anomaly performance: most documented anomalies experienced severe decay; momentum (12m), seasonality, and industry reversals especially affected.

- Non-applicable environment: Individual stock return prediction (risk premia estimation): KNS addresses SDF/risk prices for managed portfolios; for individual stocks, use KPS-001/GKX-001. Non-equity asset classes (US equities only). Short-horizon intraday or high-frequency strategies (all characteristics are monthly).

- Time scale: Monthly cross-sectional factor model construction; long-run evaluation of anomaly portfolio pricing.

- Use in premarket reports: When evaluating factor model adequacy or multi-factor signal construction, note that FF5-type sparse models are inadequate and leave substantial unexplained alpha. Post-2005 anomaly returns should not be extrapolated from pre-2005 backtests without post-publication-decay discount. Do not use this card to generate a buy/sell signal directly.

- Prohibited use: Do NOT treat post-2005 momentum decay as permanent death of momentum (may be cyclical crowding). Do NOT add characteristics without eigenvalue-proportional regularization (KNS method requires it; without it, more characteristics hurt OOS R²). Never an auto-trade or Webull fee input.

- Evidence strength: High (two independent Tier-1 peer-reviewed studies using different methods and different test assets: KNS JFE 2020 + KPS JFE 2019).

- Last review date: 2026-09-09.

- Revalidation trigger: Evidence that a post-2016 or non-US replication fails to confirm PC-sparse SDF feasibility or finds eigenvalue-proportional shrinkage is NOT critical vs. equal shrinkage. Post-2005 anomaly decay section should be rechecked against 2017-2026 data when available.

- Source: Kozak, Serhiy, Stefan Nagel, and Shrihari Santosh, "Shrinking the Cross Section," NBER Working Paper No. 24070 (November 2017); published Journal of Financial Economics 135(2):271-292 (February 2020). Full book note: research/books/2026-09-08-kozak-nagel-santosh-nber-w24070-2017.md. Cross-references: KG-20260909-KPS-001 (IPCA — second source for admission; confirms PC-sparse latent factor structure); KG-20260830-GKX-001 (return prediction ML — different objective but post-2005 momentum decay relevant as caution); KG-20260901-FNW-001 (candidate — risk premia, NOT the same objective); KG-20260803-HLZ-MP-001 (multiple testing and publication decay — corroborated by Table 5).

### KG-20260909-KPS-001 — IPCA (Instrumented PCA): 4 Latent Factors Explain US Equity Cross-Section; Only 8 of 36 Characteristics Significant; Zero-Alpha Restriction Not Rejected (K≥2) — Characteristics Are Risk Exposures, Not Anomaly Alphas

- Title: IPCA bridges latent factor models and observable factor models: characteristics instrument time-varying factor loadings; 4 IPCA factors dominate FF5 on predictive R²; characteristics align with expected returns through risk exposures, not unexplained alphas. Admitted 2026-09-09 (daily_book_learning_claude), domain methodology.

- Core conclusion: Kelly, Pruitt & Su (JFE 2019 / NBER WP 24540; Yale/ASU/Chicago; 36 characteristics, 12,813 stocks, CRSP July 1962–May 2014): four IPCA factors explain the cross-section of US stock returns significantly more accurately than existing models. Predictive R² (in-sample): 1.77% for K=4 (vs. FF5: 0.29%); OOS predictive R² (recursive estimation): 0.7% for K=4, still more than double FF5's in-sample 0.3%. Zero-alpha restriction (Γ_α=0) fails to reject for K≥2 (p=15.4% for K=2), implying characteristics explain expected returns through risk exposures, not anomaly alphas. STANDARD PCA FAILS AT STOCK LEVEL: static PCA achieves 29.0% total R² but NEGATIVE predictive R² for individual stocks → cannot explain expected returns. PCA succeeds for managed portfolios (95.3% total R², 2.59% predictive R² for K=4) — consistent with KNS-001. ONLY 8 OF 36 SIGNIFICANT: size (2.18%), mom_12_2 (1.71%), mom_1_0/reversal (0.83%), beta (0.65%), rel_high/52wk-high (0.61%), mom_12_7 (0.69%), total assets/at (0.44%), operating leverage/ol (0.49%). Book-to-market (beme), ROA, ROE: NOT significant. 8-characteristic model achieves same fit as 36-characteristic model. OOS tangency Sharpe ratio: IPCA K=4 → 2.55 (vs. FFC6: 1.37).

- Mechanism: IPCA defines loadings β_i,t = z_i,t' Γ_β (where z_i,t is the characteristics vector and Γ_β is a global loading-mapping matrix), making loadings time-varying functions of observable characteristics. Factor estimation is equivalent to applying PCA to "managed portfolios" x_t = Z_t'r_t (characteristic-weighted returns). Static PCA fails at the individual stock level because it imposes constant loadings — if loadings change with characteristics, static PCA captures covariance structure but misspecifies conditional expected returns (predictive R² turns negative). IPCA's dynamic loadings align risk exposures with observable conditions, enabling both high total R² (systematic risk description) and high predictive R² (expected return description). No-arbitrage and market equilibrium imply that characteristics driving expected returns should do so via risk loadings — the zero-alpha test verifies this empirically.

- Supporting evidence: Primary: KPS (JFE 2019, Tier 1, 60 pages fully read). Second source: KG-20260830-GKX-001 (admitted; Gu-Kelly-Xiu JFE 2020; 94 characteristics, CRSP 1957-2016; 11 ML methods; independently confirms momentum, short-term reversal, and size as dominant characteristics — overlapping with KPS's top-8). Methodological corroboration (same dataset, independent method): KG-20260901-FNW-001 (candidate; FNW 2020 RFS; adaptive group LASSO finds 15 of 36 significant including overlapping top characteristics: reversal, momentum, size, 52-week high proximity).

- Contrary evidence: KPS's OOS tangency Sharpe of 2.55 is gross of transaction costs; IPCA factors driven by momentum and short-term reversal imply high turnover (net-of-cost returns unvalidated in the paper). Cross-validated parameters show 40% correlation between large/small stock subsamples (not perfect stability). Post-2005 anomaly decay documented in KNS-001 may reduce forward applicability of momentum-driven IPCA factors. The predictive R² of 0.7% OOS is economically small in absolute terms (though material relative to FF5's 0.3% in-sample).

- Applicable environment: Factor model construction for cross-sectional equity pricing: use IPCA with K=4 and 8 significant characteristics (size, momentum family, beta, 52-week high) rather than FF5; expect predictive R² ~1.8× higher than FF5. Characteristic selection: screen with IPCA significance tests (not just t-stats from single-characteristic regressions) to control for multicollinearity. Testing whether a characteristic is a risk factor vs. anomaly alpha: use IPCA zero-alpha test (more general than GRS). Cost-of-capital estimation: IPCA provides a formula (z_i,t' Γ_β λ̂) that works even for stocks with short histories.

- Non-applicable environment: Individual stock alpha tests without panel data (IPCA requires N and T both large). Gross-of-cost performance benchmarking (high-turnover factors; net performance unvalidated). Non-equity asset classes (US stock-level calibration). Intraday/high-frequency (monthly cross-sectional model).

- Time scale: Monthly cross-sectional factor model construction and conditional expected return estimation.

- Use in premarket reports: When assessing factor model adequacy or evaluating which characteristics matter for risk pricing, note that (1) FF5 is substantially inferior to IPCA on predictive R²; (2) book-to-market and standalone accounting ratios are NOT significant when conditioning on momentum, size, and reversal; (3) characteristics are best interpreted as risk exposures, not anomaly alphas, for K≥2. Do not generate a buy/sell signal from IPCA factors directly.

- Prohibited use: Do NOT use the 2.55 OOS Sharpe ratio as an expected return target — gross of transaction costs; IPCA factor strategies have high turnover. Do NOT use the 8-characteristics list as if it were fixed for all time periods and markets (see KNS-001 for post-2005 momentum decay). Never an auto-trade or Webull fee input.

- Evidence strength: High (JFE Tier 1 primary source with clear OOS validation; GKX-001 as independent second source from different dataset and method; FNW-001 as methodological corroboration on same dataset).

- Last review date: 2026-09-09.

- Revalidation trigger: Evidence OOS predictive R² advantage over FF5 reverses on a fresh post-2014 sample OR that IPCA is severely distorted by microstructure noise in the short-term reversal characteristic.

- Source: Kelly, Bryan, Seth Pruitt, and Yinan Su, "Characteristics Are Covariances: A Unified Model of Risk and Return," NBER Working Paper No. 24540 (April 2018); published Journal of Financial Economics 134(3):501-524 (December 2019). Full book note: research/books/2026-09-09-kelly-pruitt-su-nber-w24540-2018.md. Cross-references: KG-20260908-KNS-001 (admitted — KNS PC-sparse SDF using L2 shrinkage on anomaly portfolios; KPS confirms PCA works for managed portfolios; KPS IPCA extends to individual stocks with dynamic loadings; KPS served as second source for KNS-001 admission); KG-20260830-GKX-001 (admitted — independent second source for KPS-001 admission via dominant characteristics overlap); KG-20260901-FNW-001 (candidate — same dataset as KPS; same top characteristics via independent LASSO method; method-independent corroboration on same data, not data-independent second source); KG-20260802-ESL-HDP-001 (admitted — high-dimensional regularization; KPS's Γ_β dimension reduction is exactly the type of parameter parsimony required in p>>N settings).

### KG-20260909-ESCAL-001 — Averaging Down Into a Loser Near Its Stop Is Loss-Domain Risk-Seeking + Escalation of Commitment: a Near-Stop Holding Is HOLD or SELL-Staged Only, NEVER an Add Candidate — BOUNDARY: Not a Ban on Diversified-Core Accumulation

- Title: Adding to a losing position near its stop/invalidation (averaging down) is driven by loss-domain risk-seeking (KT-1979 reflection effect) + escalation of commitment / self-justification (Staw 1976); a holding within ~5% of its stop must be HOLD or SELL-staged only, never an add/averaging candidate. Admitted 2026-09-09 (research_a), domain behavioral.

- Core conclusion: Kahneman & Tversky (1979, Econometrica 47(2):263-291): the reflection effect — value function concave in gains, convex (and steeper) in losses → risk-averse for gains but RISK-SEEKING for losses; people prefer to gamble on a probable larger loss rather than accept a smaller certain one. Facing a certain loss (sell at the stop), the investor prefers the gamble: add more to try to break even. Staw (1976, OBHP 16(1):27-44; 240 subjects): escalation of commitment — people commit the MOST additional resources to a failing course AFTER negative outcomes, strongest when personally responsible (self-justification; "throwing good money after bad"). Together they explain averaging down into a loser. Grounds RULE-20260909-01 (2026-09-09: premarket listed BJ "+1 share conditional buy ~$89" while BJ was already ≤5% from its $86 stop with a pre-staged SELL — a disguised averaging-down; lineage MU 08-17, COIN 08-20). A holding within ~5% of its stop must be HOLD or SELL-staged ONLY; a new entry needs a fresh independent thesis-confirming trigger + the math gate, which a near-stop name on a weak tape lacks.

- Mechanism: KT-1979 gives the decision-theoretic engine (in the convex loss region a sure loss is maximally aversive, so a break-even gamble is preferred even at worse EV → average down). Staw-1976 gives an independent motivational driver (self-justification of the original buy → escalate). They compound. Market manifestation independently documented (disposition effect / Odean 1998 — the passive sibling: not selling losers; averaging-down is the active one). Distinct from the carded disposition effect (NOT SELLING losers) and SQINERT-001 (inertia): ESCAL = actively BUYING MORE of a loser near its stop.

- Supporting evidence: Kahneman-Tversky (1979, Econometrica; Nobel-recognized foundational) + Staw (1976, OBHP; ~2,095 citations). Two independent mechanisms (decision-theoretic risk-seeking; self-justification escalation) + independent market manifestation (disposition effect).

- Contrary evidence: Averaging down is NOT always wrong — disciplined diversified-core accumulation (VOO/QQQM) on a broad pullback with an intact thesis is legitimate (DCA-001 / staging). The reflection effect is robust but framing/probability-weighting dependent (some critical examinations); Staw evidence is partly lab/organizational — but the market analog is documented. A profitable averaging-down is outcome bias, not validation (FAILED_IDEAS 2026-08-20). Contradiction note: research/contradictions/2026-09-09-averaging-down-vs-disciplined-accumulation.md.

- Applicable environment: Premarket candidate construction (never list a holding within ~5% of its stop as an add/averaging/"+1 share" candidate; near-stop = HOLD or SELL-staged). Postmarket audit (flag add-to-near-stop as an escalation violation regardless of outcome). Monthly prompt-eval add-near-stop canary. Any size increase in a down name near its invalidation (require fresh independent trigger + math gate to treat as a NEW entry).

- Non-applicable environment: Disciplined diversified-core accumulation on a broad pullback with intact thesis (DCA/staging domain); a genuinely new independently-triggered entry passing the math gate and not motivated by the existing loss/breakeven; market-timing/directional use; selling/trimming decisions (disposition/SLCOMMIT domain).

- Time scale: Position-management decision framing (days-to-weeks); not an intraday tick signal.

- Use in premarket reports: When a holding is within ~5% of its stop, present it only as HOLD or SELL-staged; do not generate an add/averaging draft for it. If proposing any new size in a down name, state the fresh independent trigger and the EV/W/confirmation math block; otherwise default to no-add.

- Prohibited use: Do not average down into a single losing name near its stop (hold or SELL-stage). Do not treat a profitable averaging-down as validation (outcome bias). Do not use to block disciplined diversified-core accumulation. Not an auto-trade or directional signal; new entries are approval-gated under the math gate and concentration limits. Never a Webull fee input.

- Evidence strength: Strong (two independent foundational behavioral studies + documented market manifestation), scoped as a position-management guardrail with an explicit accumulation boundary.

- Last review date: 2026-09-09.

- Revalidation trigger: Evidence the reflection effect / escalation does not manifest in this account's add decisions, OR that the ~5%-to-stop no-add threshold is too tight (blocks legitimate re-entries) or too loose (still permits averaging-down) — recalibrate.

- Source: Kahneman, Daniel and Amos Tversky, "Prospect Theory: An Analysis of Decision under Risk," Econometrica 47(2):263–291 (1979); Staw, Barry M., "Knee-Deep in the Big Muddy: A Study of Escalating Commitment to a Chosen Course of Action," Organizational Behavior and Human Performance 16(1):27–44 (1976). Full daily note: research/daily/2026-09-09.md. Cross-references: the disposition-effect card (holding losers — ESCAL is the active-adding sibling); KG-20260824-SQINERT-001 (inertia / sunk cost); KG-20260819-DCA-001 & KG-20260821-DIV-001 (the legitimate diversified-core accumulation boundary); KG-20260828-SLCOMMIT-001 candidate (stop-loss commitment — ESCAL explains why pre-committed stop devices are needed); FAILED_IDEAS 2026-08-22 (direction-agnostic deployment) and 2026-08-20 (outcome-bias on a profitable violation); standing-quant-math-gate.

### KG-20260904-ACV-001 — AIC-BIC Dilemma: No Model Selection Procedure Can Be Simultaneously Efficient (Prediction-Optimal) and Model-Consistent (True-Model-Recovering) — Yang (2005) Impossibility

- Title: No model selection procedure can simultaneously minimize prediction error (AIC-like efficiency) AND recover the true sparse model with probability → 1 (BIC-like consistency). Admitted 2026-09-10 (daily_book_learning_claude), domain methodology. Full reading: Arlot & Celisse (2010) Statistics Surveys 4:40–79. Primary theorem: Yang (2005, Biometrika 92(4):937–950).

- Core conclusion: Yang (2005) proved in the regression framework: **no single model selection procedure can be simultaneously (a) efficient (minimizes expected prediction error, asymptotically optimal relative to oracle best model) AND (b) model-consistent (selects the true sparse model with probability → 1 when it exists)**. AIC/LOO optimize for prediction (efficiency); BIC optimizes for true-model recovery (consistency). The penalty required for efficiency (AIC: ~2 per parameter) is too light to eliminate false-positive variables; the penalty required for consistency (BIC: ~log(n) per parameter) is too heavy for prediction-optimal bias-variance balance. These goals are mathematically incompatible. Practical rule: (1) PREDICTION GOAL → use AIC, LOO, VFCV (V=5–10); (2) VARIABLE SELECTION / CAUSAL INFERENCE GOAL → use BIC, BIC-penalized Lasso, or LPO with p/n → 1.

- Mechanism: AIC/efficiency achieves κ_n ≈ 1 (per-observation penalty ≈ 2): sufficient to beat the oracle's prediction risk asymptotically, but leaves false-positive variable inclusion rate non-zero → cannot identify the true model. BIC/consistency achieves κ_n → ∞ (penalty grows as log(n)): eliminates false positives with probability → 1, but over-penalizes the prediction criterion → estimated risk above minimax optimum → inefficient. The geometry of penalized selection guarantees this trade-off is fundamental, not an artifact of specific implementation.

- Supporting evidence: Yang (2005, Biometrika 92(4):937–950) — mathematical proof in regression framework; van Erven, Grünwald & de Rooij (2008) — shows some partial sharing of properties is possible in restricted frameworks, confirming the general impossibility cannot be fully escaped. Arlot-Celisse (2010, Statistics Surveys, §2.4) explicitly confirms and contextualizes the result. Mature methodological principle (50+ years: Akaike 1970/1973, Schwarz 1978, Yang 2005).

- Contrary evidence: In specific simple frameworks (small model count, very large n), AIC and BIC converge and the practical difference is negligible. Van Erven et al. (2008) show some properties can be shared in restricted settings. In practice, the distinction matters most when comparing a large set of candidate models with a moderate sample size.

- Applicable environment: Research program design (explicitly choose AIC or BIC based on goal before model evaluation). Monthly prompt evaluation (when assessing whether a standing rule correctly distinguishes prediction minimization from regime-identification). Factor/signal research evaluation (when selecting trading characteristics: use AIC/CV for prediction; BIC/Lasso with BIC-tuning for identifying the "true" factor set). Interpreting KPS-001 "8 of 36 significant": that count reflects estimation-optimal (AIC-like IPCA) selection; a BIC-consistent selection might find fewer, which is equally valid for that goal.

- Non-applicable environment: Simple descriptive statistics without model selection. Limiting regime where AIC ≈ BIC (small M_n, large n). Trading signal screening under multiple-testing (use HLZ-MP-001 framework).

- Time scale: Research-level decision (model design phase); not a trading-session signal.

- Use in premarket reports: Not directly actionable intraday. Applied in research program when assessing which selection criterion was used to identify a factor or rule, and whether the finding is prediction-optimal or identification-optimal. A factor selected via AIC/LOO cannot be claimed as the "true" sparse signal; a factor surviving BIC selection cannot be claimed to yield minimum prediction error.

- Prohibited use: Do NOT claim AIC/LOO selects the true sparse model. Do NOT claim BIC minimizes prediction error. Never an auto-trade or Webull fee input.

- Evidence strength: High (mathematical impossibility theorem, mature methodology, confirmed by comprehensive peer-reviewed survey).

- Last review date: 2026-09-10.

- Revalidation trigger: Evidence that Yang (2005) impossibility is shown incorrect in a published major statistics journal proof, or that a new procedure simultaneously achieves both efficiency and consistency formally.

- Source: Arlot, Sylvain and Alain Celisse, "A survey of cross-validation procedures for model selection," Statistics Surveys 4 (2010) 40–79. DOI: 10.1214/09-SS054. Full book note: research/books/2026-09-10-arlot-celisse-statistics-surveys-2010.md. Primary theorem source (not read directly): Yang, Yuhong, "Can the Strengths of AIC and BIC Be Shared?" Biometrika 92(4):937–950 (2005). Cross-references: KG-20260910-ACV-ID-001 (candidate — LOO/VFCV inconsistency for identification via Shao 1993); KG-20260831-IMV-001 (admitted — h-block CV for time series, from same Arlot-Celisse paper §8.2); KG-20260803-HLZ-MP-001 (admitted — multiple-testing guardrail; distinct framework for factor discovery); KG-20260909-KPS-001 (admitted — IPCA uses estimation-optimal selection; ACV-001 adds nuance to characteristic count interpretation).

---

## KG-20260911-LTA-001: Limits to Arbitrage — Three Risks Prevent Rational Traders from Correcting Behavioral Mispricings

- Core conclusion: When noise traders cause asset mispricings, rational arbitrageurs ("smart money") often cannot correct them fully or quickly. Three barriers: (1) FUNDAMENTAL RISK — no perfect substitute security; the arbitrageur cannot fully hedge idiosyncratic risk. (2) NOISE TRADER RISK (De Long, Shleifer, Summers, Waldmann 1990a, JF) — the mispricing can worsen before correcting; arbitrageur with a short horizon faces potential forced liquidation at a loss before the position pays off. (3) IMPLEMENTATION COSTS — transaction costs, short-selling fees/constraints, research costs. Shleifer-Vishny (1997, JF) add agency: professional arbitrageurs manage other people's money; investors withdraw capital when mark-to-market losses mount, forcing premature liquidation at exactly the wrong time ("separation of brains and capital"). Critical distinction: "prices are right" ≠ "no free lunch." Arbitrage inefficiency can persist even without an easily exploitable excess return.

- Evidence: De Long et al. (1990a, JF) — theoretical foundation for noise trader risk; Shleifer-Vishny (1997, JF) — agency/capital constraint model; Froot-Dabora (1999) — Royal Dutch/Shell twin share deviation ±35% over 94 years; Harris-Gurel (1986) and Shleifer (1986) — S&P 500 inclusion +3.5% permanent price jump with no fundamental change; Lamont-Thaler (2003) — Palm/3Com Internet carve-out arbitrage impossibility.

- Applicable environment: (1) Evaluating why a fundamentally sound analysis is not immediately reflected in prices — the answer is often LTA, not a flaw in the analysis. (2) Position sizing discipline: even a correct fundamental position can lose money if sizing forces early exit before the mispricing corrects. (3) Understanding persistent market anomalies (value premium, closed-end fund discounts) — they persist precisely because correcting them carries LTA risks. (4) Assessing risk of crowded trades: coordinated forced exits by multiple arbitrageurs amplify losses when redemptions occur simultaneously. (5) Premarket risk assessment: when a held position is moving against the fundamental thesis, distinguish "noise trader momentum worsening temporarily" from "fundamental thesis invalidated."

- Non-applicable environment: When the arbitrage is simple, cheap, and low-risk (near-expiry index futures mispricing with perfect hedges); as a justification for holding a losing position indefinitely (LTA does not guarantee return nor guarantee correction timing); crypto or speculative assets where noise trader risk dominates so completely that fundamental arbitrage is not even attempted.

- Prohibited use: Do NOT use LTA as a reason to hold a losing position without a specific thesis on why the mispricing will correct within the account's time horizon. Do NOT cite LTA to delay or avoid a stop-loss exit when the fundamental thesis has been invalidated. Never an auto-trade or Webull fee input.

- Evidence strength: High (two independent Tier-1 JF empirical/theoretical papers; three independent empirical examples confirming persistent mispricings).

- Last review date: 2026-09-11.

- Revalidation trigger: Evidence that real-world arbitrage costs have declined to near zero (fully liquid perpetual perfect substitutes), eliminating noise trader risk as a practical constraint; or evidence that short-selling constraints have been fully lifted market-wide.

- Source: Barberis, Nicholas and Richard Thaler, "A Survey of Behavioral Finance," Handbook of the Economics of Finance, Vol. 1B, Ch. 18, pp. 1053-1128 (Elsevier, 2003). DOI: 10.1016/S1574-0102(03)01027-6. Author-posted PDF at nicholasbarberis.github.io/ch18_6.pdf. Full book note: research/books/2026-09-11-barberis-thaler-handbook-economics-finance-2003.md. Primary studies (not read directly): De Long, Shleifer, Summers, Waldmann (1990a, Journal of Finance); Shleifer-Vishny (1997, Journal of Finance). Cross-references: KG-20260911-MENTA-001 (admitted — mental accounting break-even effect; same loss-domain risk-seeking that makes noise traders persist also prevents rational correction); KG-20260909-ESCAL-001 (admitted — escalation/averaging down); KG-20260907-ANCH-001 (admitted — reference-price anchoring); KG-20260902-VMR-001 (admitted — volatility mean reversion; noise trader risk explains why VIX can spike while a fundamentally cheap market stays cheap).

---

## KG-20260911-MENTA-001: Mental Accounting with Reference-Point — Break-Even Effect Drives Risk-Seeking Near Losses; House Money Effect Drives Overconfidence After Wins

- Core conclusion: Investors evaluate gains and losses in separate mental "accounts" using their COST BASIS as the reference point (not total portfolio value). Two critical consequences: (1) BREAK-EVEN EFFECT: when a position is at a loss, prospect theory's convex loss-domain value function makes the investor RISK-SEEKING — they prefer gambling (holding hoping to get back to zero) over accepting the certain loss. This is the primary mechanism behind holding losers too long and behind the "approved draft not executed" failure pattern (COIN/NVDA/BJ cases). A losing position within ~5% of its stop line is in maximum break-even-effect territory. (2) HOUSE MONEY EFFECT: prior gains expand the perceived "risk budget" because subsequent risk is framed as gambling with "found money." Drives overconfident risk-taking after profitable periods. Both effects are predictable, persistent, and documented across retail investors AND professional traders. Neither is rational: the cost basis is sunk; only future expected value and risk should determine portfolio decisions.

- Mechanism: Prospect theory v(x): concave for gains (risk-averse in gain domain), CONVEX for losses (risk-seeking in loss domain), with kink at origin (loss aversion λ≈2.25, TK 1992). Mental accounting assigns cost basis as reference point x=0 for each position. When a position is underwater by $X: v(-X) [sell and realize loss] vs. expected-utility of holding [convex loss domain → holding preferred]. NARROW FRAMING amplifies both effects: positions evaluated individually, not portfolio-wide.

- Evidence: Thaler (1985, JMBE) and Thaler (1999, JBD) — foundational papers with 6,673 Google Scholar citations; mature behavioral economics principle grounded in Kahneman-Tversky (1979) prospect theory (best-validated description of decision-making under risk from 40+ years of experimental evidence). Coval-Shumway (2000, JF) — professional CBOT treasury bond futures traders exhibit break-even effect and house money effect (morning losers take more risk in afternoon; morning winners take less). Genesove-Mayer (2001) — housing market data confirms cost-basis anchoring behavior.

- Applicable environment: (1) Position review for any holding showing an unrealized loss: actively counteract the break-even effect with pre-committed stop rules and explicit thesis re-evaluation. (2) COIN/NVDA/BJ scenario: a position within ~5% of its stop line is in maximum break-even-effect territory — this exact pattern drives the SQINERT-001 "approved draft not executed" failure; the stop was set when rational, the break-even effect prevents execution. (3) Post-profitable-period risk assessment: house money effect predicts the investor will take excess risk after recent wins — require same EV/W gate regardless of recent P/L. (4) Daily P/L framing: professional traders up in the morning take less risk in the afternoon; those down take more — affects intraday decision quality systematically.

- Non-applicable environment: When the cost basis is irrelevant to the forward decision (genuinely new entry with no legacy basis); when stop-loss rules are pre-committed and automatically executed (pre-commitment removes the real-time break-even effect from the exit decision); when the remaining thesis is intact and the loss reflects systematic broad market decline, not idiosyncratic deterioration (in that case, a continued hold may be rational under DCA-001/DIV-001 logic, not break-even effect).

- Prohibited use: Do NOT leave an approved stop-loss exit unexecuted because it would "realize a loss" — the break-even effect describes a bias to counteract, not a permission to delay (see SQINERT-001). Do NOT average down into a loser citing house-money-effect reasoning (prior wins do not justify adding to a losing position — see ESCAL-001). Never an auto-trade or Webull fee input.

- Evidence strength: High (mature behavioral economics principle; two foundational papers by Thaler; prospect theory mechanism confirmed in professional traders by Coval-Shumway 2000 JF; mechanism derives from best-validated decision theory framework).

- Last review date: 2026-09-11.

- Revalidation trigger: Evidence that pre-committed stop-loss rules fully eliminate the break-even effect in live trading data (would require only a methodology update, not disconfirmation of the core mechanism). The core Kahneman-Tversky prospect theory mechanism has no published disconfirmation since 1979.

- Source: Barberis, Nicholas and Richard Thaler, "A Survey of Behavioral Finance," Handbook of the Economics of Finance, Vol. 1B, Ch. 18, pp. 1053-1128 (Elsevier, 2003). DOI: 10.1016/S1574-0102(03)01027-6. Author-posted PDF at nicholasbarberis.github.io/ch18_6.pdf. §§3.2.1 and 7.4 (PDF pp. 17–22, 52–54; Handbook pp. 1067–1072, 1102–1104). Full book note: research/books/2026-09-11-barberis-thaler-handbook-economics-finance-2003.md. Primary studies: Thaler (1985, JMBE; 1999, JBD); Kahneman-Tversky (1979, Econometrica); Coval-Shumway (2000, JF). Cross-references: KG-20260909-ESCAL-001 (admitted — escalation/averaging down: ESCAL is the active adding-to-losers version; MENTA-001 explains the mechanism via break-even effect); KG-20260824-SQINERT-001 (admitted — inertia/status quo: SQINERT is the process failure; MENTA-001 provides the psychological driver); KG-20260828-SLCOMMIT-001 (candidate — pre-committed stop devices: MENTA-001 is the primary reason pre-commitment is needed); KG-20260810-BFSG-001 (admitted — disposition effect: BFSG-001 describes the pattern; MENTA-001 explains the mechanism); KG-20260907-ANCH-001 (admitted — reference-price anchoring: cost basis as reference point is the mental accounting anchor).


### KG-20260911-RESMOM-001 — Sector-Relative (Residual) Strength Is Horizon-Dependent: a Few Sessions of Underperformance Is MONITOR-Not-Trim; Escalate a Laggard Only on Sustained Multi-Week Residual Weakness AND/OR an Invalidation Break

- Title: A held stock's return relative to its sector/factors (residual return) carries horizon-dependent information — short horizon (days to ~1 month) is reversal-noisy, medium horizon (~3-12 months) persists; escalate a chronic laggard to a trim-review on sustained multi-week residual underperformance and/or a break of its own invalidation, not raw session count. Admitted 2026-09-11 (research_a), domain portfolio_construction.

- Core conclusion: Jegadeesh & Titman (1993, JF 48(1):65-91): 3-12 month winners minus losers earn ~1%/month (not systematic-risk-explained), but they compute momentum from month -12 to -2, SKIPPING month -1 to avoid short-term reversal — the most recent ~1 month is reversal-prone/noisy, not momentum. Blitz, Huij & Martens (2011, JEF 18(3):506-521): ranking on RESIDUAL (factor/sector-adjusted) returns ~doubles the risk-adjusted momentum profit, is more consistent, less concentrated in extremes, and greatly reduces crash risk (~double Sharpe) — the sector-relative component (what "NVDA vs SMH" measures) carries robust MEDIUM-horizon continuation. Grounds RULE-20260911-01 (NVDA lagging SMH a 3rd session on 2026-09-11, deepest unrealized loss): a few sessions of underperformance vs the sector is short-reversal territory = MONITOR, not a trim signal; escalate to a discretionary trim-review only on sustained multi-week residual/sector-relative underperformance AND/OR a break of the position's own invalidation — not a session count. Overreacting to a 3-day lag risks selling into a reversal.

- Mechanism: Relative returns decompose by horizon — short-horizon (days to ~1 month) relative moves are dominated by liquidity-provision reversal/noise (Jegadeesh 1990; RERP-001; J-T skip month -1), so a brief sector-relative lag mean-reverts; medium-horizon (~3-12 months) relative strength/weakness persists (under/overreaction continuation). Ranking on RESIDUAL returns strips time-varying common-factor exposure that makes raw momentum crash-prone, so residual momentum is more robust. A held name's persistence of residual underperformance over a medium window is informative about thesis deterioration; a few days is not. Distinct from ACORR-001 (idiosyncratic-vs-common on a single day) — RESMOM-001 is about the HORIZON over which the residual signal is real.

- Supporting evidence: Jegadeesh-Titman (1993, JF; foundational momentum + explicit short-term-reversal horizon caveat) + Blitz-Huij-Martens (2011, JEF; residual momentum robustness, reduced crash risk). Two independent Tier-1/2 peer-reviewed studies.

- Contrary evidence: Short-term reversal (Jegadeesh 1990/Lehmann 1990; carded RERP-001) directly contradicts acting on a few days of relative weakness. Momentum crashes (Daniel-Moskowitz 2016) and transaction costs (Lesmond-Schill-Zhou 2004, carded) bound trading use; residual momentum reduces crash risk not costs; post-2005 momentum-as-SDF-factor decay (KNS-001). So this is a risk-frame/escalation gate, not a mechanical signal (consistent with the admitted "momentum/reversal not a daily catalyst" entry). Contradiction note: research/contradictions/2026-09-11-relative-weakness-horizon-momentum-vs-reversal.md.

- Applicable environment: Premarket position management (a holding lagging its sector for only a few sessions = MONITOR, not trim; escalate only on sustained multi-week residual underperformance and/or an own-invalidation break). Distinguishing relative-strength signal from noise (use a weeks-months residual window, not the reversal-contaminated recent month or a few days). Postmarket audit of relative-weakness escalation horizon. Monthly prompt-eval NVDA-vs-SMH relative-weakness canary.

- Non-applicable environment: A break of the position's own stop/invalidation (that is a risk-management exit per ESCAL-001/stop discipline, regardless of horizon); mechanical same-day/short-horizon trading (reversal-noisy); cost-insensitive application; broad-index/diversified positions without a single-name residual.

- Time scale: Weeks-to-months for the continuation signal; the short (days-to-~1-month) window is reversal-noisy and non-signaling.

- Use in premarket reports: When a holding lags its sector, state the horizon — a few sessions is MONITOR; only sustained multi-week residual/sector-relative underperformance (or an invalidation break) justifies a trim-review with a conditional draft. Combine with ACORR-001 (is the lag idiosyncratic or common-factor?).

- Prohibited use: Do not trim/add on a few sessions of sector-relative underperformance alone (short-reversal noise). Do not treat relative strength as a mechanical buy/sell signal. Do not use the recent ~1 month as a continuation signal (reversal-contaminated). Not an auto-trade; trims are approval-gated. Never a Webull fee input.

- Evidence strength: Strong (two independent Tier-1/2 peer-reviewed studies; horizon structure + residual robustness), scoped as a position-management escalation gate with an explicit horizon boundary.

- Last review date: 2026-09-11.

- Revalidation trigger: Evidence the short-reversal / medium-continuation horizon structure changed (e.g., faster information diffusion compressing the horizon), OR account/postmarket evidence that relative-weakness escalations are systematically early (selling into reversals) or late (holding chronic laggards too long) — recalibrate the window. Recheck residual-momentum robustness on post-2015 samples after realistic costs.

- Source: Jegadeesh, Narasimhan and Sheridan Titman, "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency," Journal of Finance 48(1):65-91 (1993); Blitz, David, Joop Huij and Martin Martens, "Residual Momentum," Journal of Empirical Finance 18(3):506-521 (2011). Full daily note: research/daily/2026-09-11.md. Cross-references: KG-20260831-ACORR-001 (idiosyncratic-vs-common decoupling — the single-day complement to RESMOM-001's horizon view); KG-20260814-RERP-001 (short-term reversal as liquidity provision — why days are noise); KG-20260909-ESCAL-001 (stop discipline / no-add near invalidation — an own-invalidation break overrides the horizon nuance); the admitted "Momentum And Reversal Evidence Are Conditional Risk Frames, Not Daily Catalysts" entry; Lesmond-Schill-Zhou (2004) momentum costs; KG-20260830-GKX-001 / KG-20260909-KPS-001 (momentum as a dominant characteristic).

---

## KG-20260911-REP-001: Representativeness Heuristic — Overextrapolation of Recent Performance Creates Value Premium and Momentum/Reversal Sequence

- Core conclusion: Representativeness heuristic (Kahneman-Tversky 1974): people judge the probability of an event by its superficial resemblance to a mental model, ignoring base rates and sample size. Griffin-Tversky (1992) strength/weight framework: LOW strength, HIGH weight events (single earnings announcement — high predictive value, but only 1 data point) → CONSERVATISM → underreaction; HIGH strength, LOW weight events (5 consecutive good quarters — strong visual pattern, but small sample with high base rate of mean reversion) → REPRESENTATIVENESS → overreaction. Financial manifestations: (1) SAMPLE SIZE NEGLECT: a few good quarters makes investors believe the company is a permanent growth star; aggressive extrapolation → growth stocks overvalued, value stocks undervalued → value premium (DeBondt-Thaler 1985: worst past 3-5yr performers outperform best past performers by ~25pp over next 3-5yr). (2) CONSERVATISM→REPRESENTATIVENESS SEQUENCE: investors initially UNDERREACT to a single earnings announcement (insufficient Bayesian update), then OVERREACT as earnings stream continues (pattern "looks like" a trend) → 6-12 month momentum followed by 3-5 year reversal. (3) BASE RATE NEGLECT: systematically overestimates future growth rates for glamour stocks, underestimates for value stocks.

- Mechanism: Representativeness = probability judged by resemblance, ignoring base rates. In stock markets: (a) Three consecutive quarters of 20% earnings growth LOOKS LIKE a growing company → investors extrapolate indefinitely, ignoring mean reversion base rates. (b) Conservatism (Edwards 1968) dominates when data is "not representative of a model" (single data points → underreaction); representativeness dominates when data "looks like a trend" (long series → overreaction). (c) Formally proved by BSV (1998) two-regime model: the conservatism/underreaction and representativeness/overreaction emerge naturally from the same parameter space — NOT a knife-edge result.

- Evidence: BSV (1998, JFE 49:307-343) — formal proof (primary; see also BSV-001 for formal model detail). DeBondt-Thaler (1985, JF 40:793-808) — empirical reversal evidence (confirmatory; cited throughout BSV). Barberis-Thaler (2003, Handbook of Economics of Finance, Ch. 18) — comprehensive survey synthesis. Two independent sources: BSV formal model + DeBondt-Thaler empirical evidence.

- Applicable environment: (1) Earnings catalyst analysis: isolated positive surprise → underreaction drift expected (buy/hold bias); 4+ consecutive strong quarters → Model 2 / representativeness territory → overreaction risk rising (expect mean reversion, reduce sizing). (2) Value premium: high B/M stocks often unloved due to representativeness overextrapolation of bad recent earnings; 3-5yr horizon fundamentals reassert. (3) Momentum as a 6-12 month signal: consistent with GKX-001 and KPS-001 empirical evidence; representativeness-based behavioral mechanism provides theoretical grounding. (4) Risk of buying "hot" stocks after multiple strong quarters: representativeness premium likely already embedded.

- Non-applicable environment: Short-term intraday or same-week trading (representativeness effects operate on weeks-to-years timescales). Isolated non-recurring events (dividend cut, stock split, regulatory decision) — per BSV §5.3, these do NOT constitute part of the same-type earnings trend that generates overreaction; they generate underreaction drift instead. Macro factor exposure orthogonal to company-level earnings history.

- Time scale: Underreaction phase: 6–12 months (momentum). Overreaction phase: 3–5 years (reversal). Single-event underreaction: weeks to months of drift.

- Use in premarket reports: When a candidate has posted 4+ consecutive earnings beats, flag Model 2 / representativeness regime as active — momentum still valid near-term but reversal risk elevated at the 3-5yr horizon; do not over-extrapolate the streak. When evaluating a value stock with a history of earnings misses, note that representativeness may have driven the selloff beyond fundamentals — 3-5yr recovery possible.

- Prohibited use: Do NOT treat as a standalone BUY signal for value stocks — value premium has multiple competing explanations; need current fundamental view. Do NOT use to justify buying a momentum stock on the basis of good past performance alone — representativeness predicts eventual reversal. Do NOT apply overreaction logic to isolated non-recurring events. Never an auto-trade or Webull fee input.

- Evidence strength: Strong (two-source: BSV 1998 JFE formal model + DeBondt-Thaler 1985 JF empirical evidence; Griffin-Tversky 1992 psychological foundation).

- Last review date: 2026-09-12.

- Revalidation trigger: Evidence that the momentum/reversal sequence has disappeared in a comprehensive post-2010 international sample under realistic transaction costs. Or DeBondt-Thaler (1985) direct read revealing contradictions not captured by BSV simulation.

- Source: Barberis, Nicholas, Andrei Shleifer and Robert Vishny, "A Model of Investor Sentiment," Journal of Financial Economics 49(2):307-343 (1998). DOI: 10.1016/S0304-405X(98)00027-0. Author-posted at nicholasbarberis.github.io/bsv_jnl.pdf. Full book note: research/books/2026-09-12-barberis-shleifer-vishny-jfe-1998.md. Secondary source: Barberis-Thaler (2003). Cross-references: KG-20260912-BSV-001 (formal model); KG-20260830-GKX-001 (empirical price-trend dominance); KG-20260909-KPS-001 (IPCA momentum significance); KG-20260811-RESMOM-001 (residual momentum horizon); KG-20260810-BFSG-001 (disposition effect); KG-20260907-ANCH-001 (reference-price anchoring); KG-20260911-LTA-001 (limits to arbitrage).

---

## KG-20260912-BSV-001: BSV Two-Regime Investor Sentiment Model — Formal Proof That Conservatism + Representativeness Generate Underreaction (1–12mo) and Overreaction (3–5yr) From the Same Parameter Space

- Core conclusion: BSV (1998) formally proves that a representative investor using a wrong two-state Markov regime model on true random-walk earnings generates both underreaction (positive return serial correlation at 1–12 months) and overreaction (negative return serial correlation at 3–5 years) simultaneously, for a wide non-knife-edge parameter range. Model 1 = mean-reverting (nL < 0.5; investor expects recent shock to reverse → underreaction); Model 2 = trending (nH > 0.5; investor expects streak to continue → overreaction). State variable qt = investor's probability weight on Model 1. PRICE FORMULA (Proposition 1): Pt = Nt/d + yt(p1 − p2qt). Proposition 2 (sufficient conditions for both effects): k₁p2 < p1 < k̄p2, p2 ≥ 0. Simulation confirmation: r1W−r1L = +0.028 (momentum, matching JT 1993); r4W−r4L = −0.018 (reversal, matching DeBondt-Thaler 1985); E/P value premium +0.043. KEY QUANTITATIVE IMPLICATIONS: (1) Short-horizon earnings surprise → drift trade backed (underreaction domain); (2) String of 4+ same-sign consecutive earnings → overreaction risk rising; reversal trade backed at 3-5yr horizon.

- Mechanism: TRUE EARNINGS: random walk (no predictability). INVESTOR'S WRONG MODEL: two-state Markov with regime-switching transition parameters j1, j2. MODEL 1 (conservatism, nL < 0.5): positive shock expected to be reversed next period. MODEL 2 (representativeness, nH > 0.5): positive shock expected to be followed by another positive shock. qt UPDATING: same-sign shocks → qt falls (trending belief rises); alternating shocks → qt rises (mean-reversion belief rises). UNDERREACTION: on average investor in Model 1 (j1 < j2 → j2/(j1+j2) > 0.5); after +shock, expects reversal; price set below fundamental → positive future return (underreaction). OVERREACTION: after long string of +shocks, qt near lower bound q₁ (firmly in Model 2); when earnings regress, large negative surprise → negative average return following a long trend (overreaction). ISOLATED EVENTS (per §5.3): dividend cuts, stock splits are not part of a same-type earnings series → conservatism/underreaction domain only; overreaction requires a sustained series of same-type signals.

- Evidence: BSV (1998, JFE 49:307-343) — formal mathematical proof of Propositions 1 and 2; simulation replicates three independent empirical patterns (JT 1993 momentum, DeBondt-Thaler 1985 reversal, E/P value premium) simultaneously and without invoking any risk premium. Two-source criterion: BSV (1998) formal model as primary + DeBondt-Thaler (1985, JF 40:793-808) empirical overreaction evidence as confirmatory (cited throughout BSV §2 and §5.2). Wide parameter range satisfies conditions (Figs. 1 and 2) — non-knife-edge result.

- Applicable environment: (1) Post-earnings positioning: underreaction drift backed at 6-12 months for single surprise; use alongside GKX-001 empirical momentum evidence. (2) Value/contrarian strategy horizon calibration: reversal takes 3-5yr to materialize; do NOT expect immediate reversion after buying past losers. (3) Stocks posting 4+ consecutive strong earnings quarters: Model 2/representativeness regime likely active → overpriced vs. true fundamental; momentum still valid short-term but reversal risk elevated. (4) Premarket earnings: modest disappointment after long streak can cause outsized negative reaction (investor in Model 2 was expecting continuation).

- Non-applicable environment: Intraday or 1-3 day trading (model operates at quarterly-to-annual earnings cycles). Individual one-time events (merger, IPO, regulatory decision). Macro/sector-level factors not anchored to firm-specific earnings history. Markets where earnings are not the primary information channel.

- Time scale: Underreaction phase: 6–12 months. Overreaction phase: 3–5 years. Regime transition: continuous as qt updates with each earnings report.

- Use in premarket reports: Count consecutive same-sign earnings beats for each holding/candidate. ≤2 beats → Model 1/conservatism regime likely → underreaction drift; support hold or momentum entry. ≥4 beats → Model 2/representativeness regime likely → overreaction risk rising; flag for closer monitoring, reduce willingness to add. A stock beating for 5+ consecutive quarters at high premium is in maximum BSV Model 2 territory — modest disappointment can cause outsized negative reaction.

- Prohibited use: Do NOT use as a mechanical buy/sell signal — directional model of average tendencies, not a per-stock timing formula. Do NOT claim to observe qt directly (it's a latent state). Do NOT apply to isolated non-recurring events (those are underreaction territory per BSV §5.3). Never an auto-trade or Webull fee input.

- Evidence strength: Strong (formal mathematical proof; simulation replicates three well-documented empirical patterns simultaneously; wide non-knife-edge parameter range; same paper provides the psychological foundation via Griffin-Tversky 1992 strength/weight framework).

- Last review date: 2026-09-12.

- Revalidation trigger: Evidence that the momentum/reversal pattern has been eliminated in a comprehensive post-2010 US/international sample under realistic transaction costs. Or alternative models (DHS 1998, HS 1999) shown to empirically dominate BSV's specific two-regime formulation.

- Source: Barberis, Nicholas, Andrei Shleifer and Robert Vishny, "A Model of Investor Sentiment," Journal of Financial Economics 49(2):307-343 (1998). DOI: 10.1016/S0304-405X(98)00027-0. Author-posted at nicholasbarberis.github.io/bsv_jnl.pdf. Full book note: research/books/2026-09-12-barberis-shleifer-vishny-jfe-1998.md. Cross-references: KG-20260911-REP-001 (behavioral mechanism); KG-20260830-GKX-001 (empirical price-trend dominance; momentum characteristic); KG-20260909-KPS-001 (IPCA momentum significance); KG-20260911-RESMOM-001 (residual momentum at 3-12mo horizon); KG-20260811-RERP-001 (short-term reversal, consistent with BSV's "skip recent month" implication); KG-20260911-LTA-001 (limits to arbitrage; explains why BSV mispricings persist).

## KG-20260913-ST2012-001: Credit Boom as Primary Leading Indicator of Financial Crises

**Status:** ADMITTED (2026-09-13)
**Domain:** macro
**Source:** Schularick & Taylor (2012), "Credit Booms Gone Bust: Monetary Policy, Leverage Cycles and Financial Crises, 1870–2008," *American Economic Review* 102(2):1029-1061. NBER WP 15512.

**Core rule:** Five-year real bank loan growth is the dominant predictor of financial crises in 14 advanced economies (1870–2008). Logit AUROC = 0.717; out-of-sample AUROC = 0.646. One standard deviation increase in 5-year credit growth raises crisis probability by ~2.8 pp relative to a 4% base rate (~70% relative increase). Credit aggregates clearly outperform money aggregates as predictors, especially post-WW2. Financial system size (loans/GDP) independently amplifies crisis risk.

**Key quantitative facts:**
- AUROC (in-sample, full panel): **0.717**
- AUROC (out-of-sample, post-1983 rolling): **0.646** (significant at 5%)
- L2 logit coefficient (2-year lagged credit growth): **7.14** (p<0.001)
- +1 SD credit growth over 5 years → **+2.8 pp** crisis probability (vs. 4% base)
- Post-WW2 credit AUROC 0.720 vs. money AUROC 0.657; narrow money p=0.256 (fails)
- Loans/GDP level as additional predictor: AUROC rises to **0.764**
- Post-WW2 cumulative output loss: **−7.9%** vs. trend; investment: **−25.7%**

**Two Eras structural finding:**
- Pre-WW2: loan growth 4.16%/yr ≈ money growth 3.65%/yr; loan/money growth 0.17%/yr
- Post-WW2: loan growth 10.94%/yr >> money growth 8.57%/yr; loan/money growth 2.22%/yr (20× higher)
- By ~2000: loan/money ratio ~2× prewar average (log +0.75)

**Applicable to:**
- Banking sector holdings (KRE): credit boom phases appear profitable for banks but plant seeds of future stress; do not extrapolate credit-driven earnings indefinitely
- Macro scenario risk: BIS credit-to-GDP gap is the operational real-time implementation of this concept
- Distinguishing monetary signals from credit signals: M2 growth ≠ financial stability signal post-WW2; bank credit aggregates are the relevant variable
- Post-crisis policy interpretation: aggressive monetary response maintains money supply but does NOT eliminate real output losses (~8% GDP, ~26% investment cumulative decline)

**Not applicable to:** individual stock picking, EM/developing-country analysis, intraday trading, commodity/FX markets directly

**Prohibited use:** Do not use as a timing signal (model identifies elevated risk over 1-5 yr horizon, not a short-term sell trigger). Never auto-trade. Never a Webull fee input.

**Cross-references:** JST-001 (candidate — Jorda-Schularick-Taylor 2013 post-crisis recession depth, different but related); LB-001 (admitted — JST 2015, leveraged bubbles); DBT-001 (admitted — credit-to-GDP gap early warning); BL-001 (admitted — joint credit+asset price imbalance indicator)

---

## KG-20260914-HXZ-001: Anomaly Replication Methodology — NYSE-BP + VW Eliminate 64-85% of Equity Anomalies as Microcap Artifacts

**Status:** ADMITTED (2026-09-14) | **Domain:** methodology | **Evidence:** strong

**Source:** Hou-Xue-Zhang (2020) "Replicating Anomalies," *Review of Financial Studies* 33(5):2019–2133. NBER WP 23394.

**Core rule:** When testing any equity return anomaly, use NYSE breakpoints + value-weighted portfolio returns. Studies using all-stock (NYSE-Amex-NASDAQ) breakpoints and/or equal-weighted returns systematically overweight microcaps, which inflate apparent anomaly profits by 50-300%.

**Quantitative facts:**
- 447 anomaly variables tested (CRSP/Compustat, Jan 1967–Dec 2014, 576 months)
- **64% of anomalies (286/447) insignificant at 5% under NYSE-BP + VW**
- **85% of anomalies (380/447) insignificant at t≥3**
- Liquidity/trading frictions: 95/102 (93%) fail — virtually the entire category is microcap artifact
- Distress anomaly (failure prob, Z-score, O-score): virtually nonexistent under proper controls
- **161/447 survive** at t≥1.96 — the true anomaly space is sparse
- q-factor model (size + investment/I/A + Roe) accounts for 115/161 significant anomalies
- **46 residual q-anomalies** survive (11 at t≥3); combined return: 1.66%/m (t=10.28)
- Microcaps = 61% of stock count, 3.3% of market cap; EW microcap return 1.32%/m vs. VW market 0.93%/m

**Surviving anomaly categories (significant at t≥1.96):**
- Momentum: 37/57 survive (price momentum R66: 0.82%/m, t=3.49; Abr1: 0.74%/m, t=5.85)
- Value-growth: 31/68 survive (cash-flow-to-price Cp: 0.49%/m, t=2.47)
- Investment: 27/38 survive
- Profitability: 33/79 survive (Roe1: 0.69%/m, t=3.07; dRoe1: 0.76%/m, t=5.43)
- Intangibles: 26/103 survive (R&D-to-market Rdm: 1.19%/m at 1m, t=2.93)
- Trading frictions: **only 7/102 survive**

**q-factor premiums (1967-2014, t-stats):** Investment factor 0.43%/m (t=5.08); Roe factor 0.56%/m (t=5.24)

**Applicable to:**
- Due diligence on any claimed equity return anomaly or factor: first check whether original study used all-stock breakpoints + EW; if yes, prior probability of microcap artifact is >60%
- Factor ETF evaluation: most "smart beta" factors citing academic literature have not been properly replicated; expect substantial premium decay when properly controlled
- Backtest credibility checks: EW returns over any cross-section of stocks will overstate tradable alpha

**Not applicable to:** macro/credit analysis, international EM markets (different cap structure), intraday/options, individual security analysis

**Prohibited use:** Do not use to dismiss ALL return predictability (161 anomalies are real; q-anomaly composite 1.66%/m is real). Do not auto-trade. Not a Webull fee input.

**Cross-references:** GKX-001 (admitted — dominant predictors align with HXZ's surviving categories: price trend/momentum, profitability); KPS-001 (admitted — IPCA finds 8/36 significant, consistent with HXZ sparsity); HLZ-MP-001 (admitted — multiple-testing: HXZ is the empirical proof of HLZ's prediction); FNW-001 (candidate — HXZ supports sparsity premise but does not directly confirm FNW's specific LASSO selection)


---

## KG-20260826-JST-001: Credit Overhang Hypothesis — Pre-Crisis Bank Credit Boom Intensity Predicts Post-Crisis Recession Depth (Jordà-Schularick-Taylor JMCB 2013)

**Title:** Credit Overhang Hypothesis: Pre-Crisis Bank Credit Boom Intensity Predicts Post-Crisis Recession Depth

**Status:** Admitted 2026-09-15 (promoted from candidate after direct read; single-source OOS criterion)

**Core conclusion:** Two empirical facts confirmed across 14 advanced economies, 1870-2008, 223 recession episodes (50 financial, 173 normal), using local projection methods conditioned on a 7-variable macro system:

1. **Financial-crisis recessions are substantially worse than normal recessions.** Conditional path (Table 7): normal recession reaches +4.0% at year 5; financial recession is −2.0% at year 5. The gap widens through year 2 (normal 0%, financial −4.6%) and remains significant throughout. Robust to excluding the Great Depression (Table 7b).

2. **For both recession types, more credit-intensive prior expansions → deeper recessions.** Excess credit ξ (pp/yr change in bank loans/GDP in prior expansion, demeaned) predicts worse post-peak trajectories. Marginal effects (Table 8): N×ξ: −0.7* yr2, −0.9† yr4; F×ξ: −0.4† yr1, −1.0* yr2, −1.3† yr4. Equality across bins cannot be rejected at any horizon. Joint F-test: F(10,585)=3.026, p=0.001. A 1 SD excess credit (≈+2 pp/yr above mean) adds ~100-200 bps of GDP drag at peak divergence year 2.

**Investment and lending channels (Figure 4):**
- Investment collapses **~20%** in financial recessions; remains 3-4 pp below counterfactual in highly-levered scenarios at year 5. Normal: −5%, recovers.
- Real lending **flat for the entire 5-year window** in highly-levered financial crises. Highly-levered financial crises presage prolonged credit crunches.
- Interest rates fall further and stay lower for longer in highly-levered financial crises.

**Out-of-sample validation (§5, Figure 5):** Model estimated on 1870-2006 data (2007-08 recessions explicitly excluded). Applied to US 2007-12:
- Bank-loan ξ: +1.74 pp/yr (2001-07), 60th percentile of F-bin
- Shadow-banking-adjusted ξ: +5.0 pp/yr (+2.75 pp above F-bin mean), top tercile
- US actual GDP path tracked within/above model's predicted financial-crisis band; 2008-09 policy support (QE1, ARRA) plausibly explains outperformance in years 1-2

**Mechanism:** Three non-exclusive channels: (1) Financial accelerator (Bernanke-Gertler 1990) — more leveraged balance sheets amplify collateral damage; (2) Debt overhang (Fisher 1933; Mian-Sufi) — high prior debt delays spending even as rates decline; (3) Expectational coordination — extreme credit booms create larger Minsky moments.

**Evidence strength:** Strong — JMCB (Tier-2 specialized macro/banking journal); NBER WP 17621; 14 countries, 140 years; local projections; explicit OOS holdout (§5); robust to Great Depression exclusion; three independent mechanism channels. Admitted on same criterion as ST2012-001 (single-source OOS) at same journal tier as LB-001 (JME).

**Supporting evidence:**
- JST 2013 (primary source) — 42 pages, Tables 4-8, Figures 2-5; full read completed 2026-09-15
- ST2012-001 (admitted) — independent evidence that credit booms predict CRISIS ONSET (AUROC 0.717); JST 2013 addresses what happens AFTER onset
- LB-001 (admitted) — JST 2015 adds asset price interaction; house+high credit = −19.63pp (worst)

**Contrary evidence:**
- Results rely on 1870-2008 pre-Basel III/QE sample; US 2007-12 outperformed model, suggesting unprecedented policy interventions can offset credit overhang
- Shadow banking is not fully captured by bank-loan-only ξ; broader credit measures show even worse predicted paths for the US
- Credit overhang effect within normal recessions is negative but only weakly significant in some specifications

**Applicable environment:**
- Macro risk assessment at 1-5 year horizon: when bank credit/GDP ratio has grown substantially above historical mean in the prior expansion, weight post-peak recession severity upward
- KRE / regional bank monitoring in credit-stressed environments: prior credit-intensive expansion signals prolonged loan book damage and low-rate-for-longer environment
- Post-recession investment/capex outlook: financial crises with prior credit booms → 20%+ investment collapse sustained 5+ years; do not expect quick capex recovery from highly-levered downturns
- US GFC historical reference: +1.74 pp/yr bank ξ (2001-07); shadow-adjusted top tercile; policy support (QE1/ARRA) explains years 1-2 outperformance; model correctly predicted sustained sluggishness

**Not applicable to:**
- Normal recessions without financial sector stress: credit overhang effect still present but smaller (−0.7%/yr vs −1.0%/yr for financial); do not apply financial-crisis depth benchmarks to non-crisis cycles
- Short-term intraday or weekly market timing: results operate at 1-5 year annual horizons
- Post-QE/Basel III era extension: sample ends 2008; post-2009 applicability requires revalidation with extended data

**Prohibited use:**
- Do not use as a precise market-timing trigger or order entry signal — operates at 1-5yr horizons
- Do not conflate with ST2012-001 (credit booms predict CRISIS ONSET) — JST studies RECESSION DEPTH conditional on crisis occurrence; complementary, not substitutes
- Do not use as sole basis for position change; macro-structural backdrop requiring corroboration with current session data and GZ-001 EBP monitoring
- Never auto-trade or use as Webull order input

**Time scale:** 1-5 year post-recession-peak outcomes. Not a short-term signal.

**Use in premarket reports:** When assessing multi-year macro backdrop for financial-sector holdings (KRE, XLF), or evaluating the depth/duration of any declared recession: apply JST-001 to assess whether the current recession is credit-overhang-amplified. Condition the assessment on the pre-recession credit intensity vs. historical mean.

**Last review date:** 2026-09-15

**Revalidation trigger:** Post-2008 study extending the JST dataset through 2010-2023 using similar local projection methods on advanced economies — confirming or updating the excess credit → recession depth relationship in the QE/Basel III era. OR evidence that CB balance sheet expansion (QE/forward guidance) systematically offsets the credit overhang channel, which would weaken applicability for post-2009 episodes.

**Cross-references:** ST2012-001 (onset), LB-001 (sister JST 2015; house+high credit worst), BL-001 (joint credit+asset price gap), DBT-001 (CCyB anchor), GZ-001 (EBP channel mechanism), HK-001 (intermediary capital constraint), RR2-001 (aftermath benchmarks)

---

## KG-20260916-AMP-001: Cross-Asset Value and Momentum Premium

**Status:** ADMITTED 2026-09-16 | **Domain:** portfolio_construction | **Source:** Asness, Moskowitz & Pedersen (2013), *Journal of Finance* 68(3):929–985

**Core Conclusion (2 facts):**

**Fact 1 — Universal premia:** Both value and momentum earn positive excess returns in every major asset class: US/UK/Europe/Japan individual stocks, country equity index futures (18 markets), currencies (10), sovereign bonds (10), and commodity futures (27), over 1972–2011 (up to 40 years). Key numbers (annualized factor returns):
- Global stocks: value +5.8%/yr (t=3.18), momentum +7.1%/yr (t=3.73)
- Country indices: value +5.7%/yr (t=3.40), momentum +7.4%/yr (t=3.57)
- Commodities: value +7.3%/yr (t=1.92), momentum +11.5%/yr (t=3.14)
- Global all assets: value +4.6%/yr (t=4.47), momentum +5.4%/yr (t=4.59), COMBO Sharpe = **1.59**
- Bond value (single measure): NOT significant (t~0.4); with composite 3-measure value: Sharpe=1.10 (t=5.48)

**Fact 2 — Strong negative correlation generates powerful COMBO strategy:**
- Within-class val–mom correlation: US stocks −0.65, global stocks −0.60, country indices −0.37, commodities −0.46, global other −0.49
- Across-class: stock value with nonstock momentum = −0.26; stock momentum with nonstock value = −0.16
- COMBO (50/50) consistently outperforms either strategy alone in every asset class
- COMBO Sharpe stable over time: ~1.40 in 1972–91 AND ~1.43 in 1992–2011, despite declining individual strategy Sharpes
- First PC of all-asset val/mom strategies explains 23% of total covariance; 54% among equity strategies alone

**Funding Liquidity Channel:**
- Global funding PC: value β = −0.0094 (t=−4.74); momentum β = +0.0112 (t=+3.58)
- Market liquidity: weak, mostly t<1.5
- COMBO immune to funding risk (β≈0, t=0.58) → combination is a more stable source of alpha
- Economic mechanism: momentum = crowded positions, crushed in funding-stress; value = contrarian, also underperforms when funding easy (prices stay stretched)
- Funding liquidity only partially explains premia — COMBO earns Sharpe ~1.5 with zero liquidity exposure

**AMP 3-Factor Model (MKT + VALeverywhere + MOMeverywhere):**
- 48 cross-asset test assets: R²=0.71 (vs. −0.316 for CAPM, 0.55 for 2-factor market+liquidity)
- FF 25 size-BM + 25 size-momentum (US): R²=0.68 (vs. 0.17 CAPM, 0.30 FF3, 0.77 FF4)
- 13 Hedge fund indices: best explained by AMP 3-factor (R²=0.47; avg |α|=18 bps vs. 22 bps FF4)

**Applicable in premarket:**
1. Cross-asset momentum confirmation: when global equities, commodities, and currencies all in momentum-aligned trend, cross-class confirmation increases signal confidence for US equity momentum signals (RESMOM-001)
2. Portfolio stress interpretation: in funding stress episodes (TED spread widening, EBP spike per GZ-001), both momentum drawdown AND temporary value underperformance are expected — not divergent signals
3. Hedging insight: combining a value tilt with a momentum tilt produces COMBO immune to funding liquidity risk — more stable than either alone; applicable to multi-asset thinking

**NOT applicable:**
- Intraday/daily momentum: AMP uses 12-month lookback, monthly rebalancing
- Japan equity momentum standalone: t-stat not significant; Japan value is strong
- Bond momentum/value with single-measure: needs composite 3-measure approach

**Evidence strength:** Journal of Finance top-tier; 8 asset classes; 1972–2011; conservative liquid large-cap universe; genuine cross-asset OOS validation. Post-2011 Sharpe decline observed but premia persist directionally.

**Last review date:** 2026-09-16

**Revalidation trigger:** Consistent post-2015 evidence of dissipated premia across the same 8 asset classes (exploited away), or AMP 3-factor systematic mispricing of a new international cross-asset dataset.

**Cross-references:** RESMOM-001 (US equity momentum, complementary), GKX-001 (ML characteristic hierarchy — confirms r12-2 at cross-asset level), JST-001 (funding stress timing risk to momentum), GZ-001 (EBP/funding stress channel), BIS-SBC-003 (stock-bond correlation regime context for bond signals)

---

## KG-20260916-SLEFF-001: Stop-Loss / Invalidation-Exit Efficacy Is Conditional on the Return Process

**Status:** ADMITTED 2026-09-16 | **Domain:** risk_management | **Source:** Kaminski & Lo (2014), *Journal of Financial Markets* 18:234–254 (theory + daily-futures empirics); boundary: Lei & Li (2013), *Financial Services Review* (SSRN 1214737); serial-correlation/regime/transaction-cost extension (2017, ScienceDirect S1386418117300472)

**Core Conclusion:** Whether a stop-loss (invalidation-exit) rule improves **expected return** is fully governed by the underlying return process, captured by the **stopping premium** `Δμ = p_o·(rf − E[r | stopped])`:
- **Random walk / i.i.d. (Prop 1):** `Δμ = −p_o·π` is **always negative** (π = risk premium over safe asset rf). Stopping only forgoes the higher-yielding asset → *"stop-loss rules never stop losses."*
- **Momentum / AR(1), ρ>0 (Prop 2):** `Δμ/p_o ≥ −π + ρσ`, **positive and ∝ return persistence** → stops add value.
- **Mean reversion (ρ<0):** stop **misses the reversal** → hurts expected return.
- **Regime-switching (Prop 3):** positive premium if the low-return/high-vol regime is identified accurately enough.

**Empirical validation:** Daily U.S. futures, **Jan 1993 – Nov 2011**, IMM S&P equity leg vs. **10-yr CBT Treasury-note futures as the safe asset** (equity/bond corr −17.29%). Serial correlation is time-varying (momentum vs. mean-reverting regimes alternate). **Short-horizon stops → negative premia; longer-horizon (> ~1 month) stops → positive premia, higher Sharpe, and substantially lower volatility** via flight-to-safety rotation into bonds. The **exit threshold dominates the re-entry threshold.** Earlier working-paper version (monthly CRSP 1950–2004): certain stops added **~50–100 bps/month during stop-out periods** (corroborating direction).

**Boundary / contradiction (verified):** Lei & Li (2013) — on **individual U.S. stocks 1964–2014**, stops **neither reliably reduce nor increase losses** vs. buy-and-hold once returns are extended to possible future paths; **raw returns poor after transaction costs**, but **certainty-equivalent improves via volatility reduction**. So on i.i.d./mean-reverting single names the honest benefit is **risk/tail reduction, not return** — and only if not eaten by costs.

**Mechanism:** Under persistence (momentum) or a persistent low-return regime, cumulative losses *forecast* further low/negative returns, so the conditional gap `(rf − E[r|stopped])` turns positive while a negatively-correlated safe asset rallies (flight-to-safety). Under mean reversion cumulative losses forecast a rebound, so stopping sells right before it. Transaction costs subtract from the premium and scale with frequency.

**Applicable in premarket/postmarket:**
1. When a holding's **pre-set invalidation breaks during a momentum/regime-persistent drawdown** (e.g., COIN < $173 in a trending crypto/risk-off sell-off, BTC toward $76K), the stopping premium is expected **positive** → an approval-gated de-risk/exit draft is evidence-supported; **converting a broken invalidation to "keep observing" (转观望) is the value-destroying error** the theory warns against (ties to RULE-20260915-01 / RULE-20260916-01).
2. Postmarket audit: grade "held past a broken invalidation in a trending regime" as a process failure with named evidence; require stop-benefit claims on a single mean-reverting name to be framed as risk reduction, not return.

**NOT applicable / prohibited:**
- Do not treat stops as universally good (random walk → provably negative premium).
- Do not tighten stops on a mean-reverting / diversified-core (VOO/QQQM) pullback — a mechanical stop would sell the reversal.
- Not an auto-trade or same-day mechanical sell signal; execution stays approval-gated. Not a Webull fee input.

**Evidence strength:** *Journal of Financial Markets* (top field), theory + OOS empirical validation, two independent boundary sources. **Last review date:** 2026-09-16.

**Revalidation trigger:** Evidence that this account's holdings' return process is predominantly mean-reverting at the relevant horizon (flips the premium sign); OR a post-2011 replication showing the momentum/regime stopping premium arbitraged away net of realistic retail costs; OR repeated cases where executing a broken invalidation in a trending regime materially underperformed holding.

**Cross-references:** SLCOMMIT-001 / ESCAL-001 / MENTA-001 (behavioral drivers of failing to execute a stop), VMR-001 (regime persistence vs. mean reversion), CONC-001 (single-name concentration sizing).

---

## KG-20260917-LWZ-001 — ML in Chinese A-Shares: Liquidity Dominates, Predictor Hierarchy is Market-Structure Dependent

**Source:** Leippold, Wang & Zhou (2022). "Machine Learning in the Chinese Stock Market." *Journal of Financial Economics*, Vol. 145, No. 2, pp. 64–82. DOI: 10.1016/j.jfineco.2021.08.017. CC BY 4.0 open access. **Admitted 2026-09-17.**

**Core finding:** Applying the GKX (2020) empirical design to 3,900+ Chinese A-shares (Jan 2000–Jun 2020; 1,160 covariates), ML methods dramatically outperform OLS cross-market: GBRT monthly R²_oos = 2.71% (full sample) vs. GKX US best 0.40% — 6.8× higher; LASSO selects ~20/90 predictors (sparsity confirmed); long-short NN3 SR = 3.45 before costs, 2.79 after 80 bps; long-only NN3 SR = 1.76 (1.53 after 80 bps). The predictor hierarchy is market-structure dependent: **China: liquidity #1** (std_dolvol, std_turn, zerotrade, ill) >> fundamentals >> China-specific (atr, er_trend) >> risk/momentum. US GKX top-3 average rank 41st in China. LASSO time-varying: structural break pre/post 2015 crash.

**Applicable:** When analyzing Chinese A-share stocks or interpreting signals for mainland-listed companies — liquidity signals (turnover volatility, zero-trade days) are primary predictors, NOT momentum. When confirming that ML/nonparametric sparsity works cross-market (methodology generalization). When sizing transaction cost assumptions for Chinese equities (80 bps round-trip reasonable; stamp tax 0.1% on sell). SOE positions: neural network treatment required (nonlinear state signaling).

**Not applicable / Caution:** US equity signals — FNW/GKX US predictor ranking does not transfer to China. Long-short strategies — only ~800 of 4,000+ Chinese stocks shortable. Post-2020 changes (regulatory, institutional ownership shift) not captured. Hong Kong H-shares (different investor base).

**Evidence strength:** *Journal of Financial Economics* top-tier; strict OOS structure (testing 2012-2020, never used in estimation); CC BY 4.0 published 2022. **Last review date:** 2026-09-17.

**Revalidation trigger:** Chinese A-share regulatory changes post-2020 shifting retail/institutional composition materially (>30% institutional ownership); OR independent post-2020 replication showing momentum dominant in China.

**Cross-references:** KG-20260830-GKX-001 (US predictor hierarchy; different from China), KG-20260901-FNW-001 (FNW sparsity — LWZ provides second-source confirmation), KG-20260916-AMP-001 (cross-asset momentum — country-level vs. individual stock distinction).

---

## KG-20260901-FNW-001 — Nonparametric Characteristic Selection: US Equities Sparse (15/36); Price-Trend and Size Dominate

**Source:** Freyberger, Neuhierl & Weber (2020). "Dissecting Characteristics Nonparametrically." *Review of Financial Studies*, Vol. 33, No. 5, pp. 2326–2377. DOI: 10.1093/rfs/hhz123. **Promoted to admitted 2026-09-17** via LWZ-001 (KG-20260917-LWZ-001) as non-US second source.

**Core finding:** Adaptive group LASSO on nonparametric additive model with 36 US equity characteristics (CRSP + Compustat, July 1963–June 2015) selects only 15/36 with independent return information. Most consistent predictors: r2-1 (short-term reversal), Rel to High (52-week high proximity), LME (market cap/size), SUV (standardized unexplained volume); r12-2 (momentum) also selected. **BEME (book-to-market) NOT selected** after conditioning on dominant predictors — most standalone accounting ratios lack independent information. Linear model overfits (selects 21 in-sample but lower OOS Sharpe vs. 8-variable nonparametric). Nonlinear relationships in size and reversal are important. OOS EW Sharpe ≈ 2.73 (nonparametric) vs. 2.26 (linear).

**Admission note:** LWZ (2022, JFE) provides the independent non-US confirmation: LASSO selects ~20/90 predictors in Chinese A-shares (same sparsity principle); ML >> linear cross-market. Specific predictor hierarchy differs — China finds liquidity dominant (not momentum/trend) — reflecting market-structure dependence, consistent with FNW's framework that the economic forces driving the cross-section vary by market.

**Applicable:** Cross-sectional screening priority for US equities — prefer price-trend (r2-1, 52-week high, momentum) and size signals over standalone accounting ratios (BEME, ROA, ROE). Justifying LASSO/group LASSO-style signal selection (penalizes redundant characteristics). Evaluating whether proposed US equity factors have independent information.

**Not applicable:** Non-US equity markets — use market-specific sparsity findings (LWZ-001 for China: liquidity dominant). Post-2015 US data (McLean-Pontiff decay applies). Annual-frequency or macro-timing predictions. Direct trading (no transaction cost model).

**Evidence strength:** *Review of Financial Studies* Tier-2 (below JF/JFE/RFS Tier-1 but top field journal); single study but corroborated by KPS-001 (method-independent, same US dataset) and LWZ-001 (independent non-US dataset). **Last review date:** 2026-09-17.

**Revalidation trigger:** Post-2016/non-US replication with same methodology finding DIFFERENT dominant US predictors (contradicting r2-1/LME primacy); OR strong evidence that McLean-Pontiff decay has eliminated the sparse US characteristic set's signal.

**Cross-references:** KG-20260917-LWZ-001 (second source; non-US confirmation), KG-20260830-GKX-001 (US predictor hierarchy; consistent), KG-20260909-KPS-001 (IPCA; method-independent; same dataset), KG-20260908-KNS-001 (momentum decay post-2005 caution), KG-20260803-HLZ-MP-001 (multiple testing; FNW's group LASSO addresses directly).
