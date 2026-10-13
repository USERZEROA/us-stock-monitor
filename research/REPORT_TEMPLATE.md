# Report Template

Use this file for output shape. Accuracy and evidence are more important than
length; if a section has no verified material, say so briefly rather than
inventing content.

## Premarket Report

1. 盘前执行摘要
2. 市场仪表盘
3. 昨夜至今核心催化剂
4. 大型企业动态
5. 行业与市场内部结构
6. 今日宏观与政策日历
7. 今日财报日历
8. 今日事件股说明
9. 盘前异常波动
10. 三种市场情景
11. 今日最重要的风险
12. 开盘后继续跟踪
13. 来源账本
14. 今日行动清单
15. 现有持仓处理
16. 今日具体操作摘要
17. 今日提醒计划
18. 请确认
19. 最终多空结论
20. 归档状态和自洽检查
21. 最终操作总结

Premarket action list requirements:
- Top 1-5 tickers by opportunity quality.
- Classify each as conditional long candidate, conditional short candidate,
  wait-for-trigger, avoid, or hold.
	- Include catalyst, official event time or observation window, expected
	  volatility window, likely interpretation, whether priced in, entry trigger,
	  no-entry conditions, invalidation, risk, confidence and source id.
	- For every held ticker and any manual portfolio position discussed by the
	  user, include an individualized loss-limit line. The line must consider
	  instrument type, liquidity/lot constraints, current concentration, the next
	  six months of material events, and peer/sector/country confirmation. Do not
	  apply one default loss percentage across U.S. stocks, ETFs, Hong Kong stocks,
	  event trades, and low-liquidity names.
	- For every event stock named in the user-visible report or Telegram summary,
	  add a plain-language company explanation: what the company does, its main
	  products or revenue engines, why the event can affect related ETFs/sectors or
  current holdings/candidates, and familiar reference events or risks that help
  a non-specialist judge relevance. Keep it factual and source-grounded; do not
  use generic labels like "AI stock" or ticker-only shorthand as the only
  explanation.
- On weekends or holidays, do not write “today buy”; write next trading day
  watchlist and Sunday 18:00 ET futures validation conditions when relevant.

## Postmarket Report

1. 盘后账户快照
2. 收盘市场快照
3. 开盘总结
4. 预测正确性审计
5. 操作正确性审计
6. 订单批准链审计
7. fee最终化追踪
8. 当前持仓复盘
9. 抄底复盘
10. 准确性增强更新
11. 明日观察清单
12. 闭环健康检查
13. 来源与归档
14. 最终操作总结

Postmarket audit requirements:
- Rate predictions as correct, partially correct, wrong, or unverifiable.
- If intraday archives are missing, list missing windows and treat as a system
  issue, not as evidence that no review was needed.
- For filled sells, compute gross and net P/L with broker fees when available;
  otherwise mark provisional using $0.02 and say final broker record controls.
- For filled orders, show execution facts and approval-chain status separately:
  order draft reference, user approval evidence/time when available, Webull
  order id or fill facts, and whether the chain is complete or unverified.
- Add material failures to `research/queue/postmarket-failures.md` and suitable
  cases to `research/EVAL_CASES.md` without duplicates.

## Special Event Monitoring

When active, include the replacement-monitor status: one-time monitor artifact,
manual-review-required warning, or not-applicable reason. Do not cite disabled
:03/:33 crons as future coverage.

## Tables And Labels

Use the standard labels:
- confirmation status: 已确认 / 多源确认 / 单源报道 / 尚未确认
- expected impact: 偏正面 / 偏负面 / 混合 / 不明确
- horizon: 盘前/日内 / 1至5个交易日 / 中期
- confidence: 高 / 中 / 低

Every important fact needs a source id from the source ledger.
