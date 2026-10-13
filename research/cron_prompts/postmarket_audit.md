OPENCLAW_CRON_LOCAL_WORKSPACE_DELEGATION_HARD_REQUIREMENT（置顶，必须执行）：
- 若本任务需要读取/写入 /home/openclaw/.openclaw/workspace-us-market、本地 Markdown/JSONL/研究文件，或运行 Webull 只读同步脚本，而当前隔离 cron 会话没有本地 shell/exec/文件写入能力，必须立即使用 sessions_spawn(runtime="subagent", mode="run", cwd="/home/openclaw/.openclaw/workspace-us-market", agentId="us-market") 委托本地工作区子任务完成对应命令、归档和验证；等待并复核子任务结果后，才允许把归档/更新写成成功。
- 委托子任务只允许执行本任务要求的只读同步、文件读取、文件追加/归档、schema/闭环验证；不得登录券商网页或App，不得下单、改单、撤单，不得输出token/凭据。
- 若 delivery.mode=announce 或本任务本应用户可见，最终用户正文必须主动调用 message(action="send", message=完整用户可见正文) 投递到 Telegram；不得只依赖 cron final/announce 自动投递。正文末尾必须写明触发成功/投递成功/messageId/归档或更新路径/下游读取路径。
- 若 delivery.mode=none 或本任务明确为静默研究维护任务，不要发 Telegram；但必须完成文件更新或写明跳过原因，并在普通 final 中给出可被 run history 捕捉的文件摘要。
- 如果委托、投递、归档或验证失败，必须把该环节标为失败/未完成并说明原因；不得把 status=ok 当成业务闭环成功。

OPENCLAW_CRON_DELIVERY_HARD_REQUIREMENT（置顶，必须执行）：
- 本任务若 delivery.mode=announce，最终给用户看的报告/摘要不能只放在普通 final；必须调用 message(action="send", message=完整用户可见正文) 发送到默认 Telegram 会话。发送后再结束。
- 若本任务需要归档或更新研究/结构化文件，必须在发送前完成写入；如果因休市或资料不足跳过，也必须发送简短跳过说明，并在适用的健康/结构化日志中记录 skip/failed_backfilled_audit，不得空跑。
- 最后一段必须说明：触发成功/投递成功/归档或更新路径/下游读取路径。
- 不得交易、下单、改单、撤单；所有交易只能给草稿并等待 the user 批准。

现在是美股开市日盘后复盘任务。请为Telegram用户the user输出当天美股盘后总结与预测/操作审计。不要执行交易，不要下单、改单、撤单；任何后续交易只能在未来给具体订单草稿并等待用户明确批准。

首先确认当前美东日期时间、NYSE/Nasdaq是否已收盘；若今天是假日、非交易日或提前休市，请按实际日期/收盘时间说明并仍尝试做最近交易日复盘。不得声称完成全美股穷尽扫描；只能称为“高流动性美股候选池/账户相关复盘”。

盘后账户与订单同步硬性要求：在账户和操作审计前，必须先尝试执行只读同步命令：
1) `cd /home/openclaw/.openclaw/workspace-us-market && timeout 45s python3 scripts/webull_order_status.py`
2) `cd /home/openclaw/.openclaw/workspace-us-market && timeout 45s python3 scripts/webull_portfolio_sync.py`
这些脚本只允许读取订单、余额、持仓并更新本地快照，不得下单、改单、撤单。若同步成功，账户基线必须优先使用Webull API快照。若同步失败、超时、token为PENDING/EXPIRED或2FA未完成，必须清楚说明并回退到`PORTFOLIO_STATE.md`和`WEBULL_ORDER_STATUS.md`最新本地基线，不得把旧数据伪装成实时数据。

必须读取/使用：`/home/openclaw/.openclaw/workspace-us-market/PORTFOLIO_STATE.md`、`/home/openclaw/.openclaw/workspace-us-market/WEBULL_ORDER_STATUS.md`、若存在则读取`webull_portfolio_snapshot.json`和`webull_order_status_snapshot.json`。尽量检索当天记忆/会话里的盘前、开盘后:03/:33报告和用户批准的实际操作，关键词包括：当天日期、盘前、开盘、09:00、09:33、10:03、10:33、11:03、11:33、12:03、12:33、13:03、13:33、14:03、14:33、15:03、15:33、QQQM、VOO、PYPL、MSFT、KRE、抄底、订单、成交、预测正确性、操作正确性。

报告必须包含以下结构：
1) 盘后账户快照：总权益、现金/Buying Power/settled cash、持仓、未成交/挂单、当天P/L；数据时间和同步状态必须写清楚。
2) 收盘市场快照：SPY/QQQ/IWM/DIA、VIX、2Y/10Y收益率、美元、原油、黄金、主要行业ETF（XLK/SMH/XLF/XLE/XLV/XLI/XLY/XLC/XLU/XLRE）。说明覆盖限制。
3) 开盘总结：复盘当天盘前/开盘主线、开盘风险开关、最重要观察点，以及开盘后的真实演变。
4) 预测正确性审计：按时间窗口列出盘前、开盘后每次:03/:33任务和重要手动判断的核心预测/触发条件/实际结果/评级（正确、部分正确、错误、无法验证）/原因。重点检查：风险开关是否准确、QQQ/SMH/VIX判断是否及时、是否正确识别宽基ETF低吸机会、是否误判单股或行业强弱。
5) 操作正确性审计：列出当天所有实际执行/建议但未执行的操作。必须包含：订单代码、方向、数量、限价/成交价、成交时间、收盘或最新价格、当前盈亏、是否遵守用户批准和风控条件、操作评级（正确、可接受、偏早、偏晚、错误）。如果有卖单，必须根据成本和API费用计算已实现P/L；如果费用未返回，按用户默认小单费用$0.02暂估并标注最终以Webull为准。

新增"订单批准链审计"硬性要求：
- 每份盘后复盘必须核对当天所有已成交订单的审计链：①Telegram消息中用户批准时间戳（可引用消息id或时间）→②Webull成交时间→③时差是否合理（通常<5分钟）。若找不到批准消息（盘中cron关闭、无本地预测归档等），必须明确标注"批准链路无法从本地文件核验，以Telegram原始对话和Webull券商记录为最终审计源"。不得把批准链路缺失当作无需解释的正常状态。
- 结构化JSONL必须包含 approval_audit 字段，格式为：[{ticker, side, quantity, filled_price, filled_time_et, approval_message_id_or_time, chain_status: "verified"|"unverifiable_intraday_disabled"|"gap"}]。
- 同时必须把当天 approval_audit 逐行写入
  `/home/openclaw/.openclaw/workspace-us-market/reports/approval-audit/YYYY-MM-DD.jsonl`。
  若找不到本地批准证据，也要写入 `chain_status="gap"` 或
  `chain_status="unverifiable_intraday_disabled"` 的只读审计记录；不得留下空目录让健康巡检无法判断。

新增"fee最终化追踪"硬性要求：
- 每份盘后复盘必须检查 webull_order_status.json 中的 fees 字段。若某笔成交的 fees 仍为空数组，必须标注 fee_status: "provisional_$0.02"。
- 若该成交发生已超过24小时，标注 fee_status: "unresolved_24h"，并在 postmarket-failures.md 追加一条 fee_finalization_overdue 记录（去重，同笔订单只写一条）。
- 结构化JSONL必须包含 fee_audit 字段：[{ticker, side, filled_time_et, fees_raw, fee_status, net_pnl_provisional}]。
- weekly_distillation_b 每周必须汇总当周所有 unresolved_24h 条目并在报告中输出。
6) 当前持仓复盘：逐项判断 QQQM、VOO、PYPL、MSFT、KRE 和其他持仓是否继续持有、是否需要次日关注止盈/止损/加仓条件。不要自动下单。
7) 抄底复盘：单独评价当天宽基ETF抄底判断是否正确。说明如果买了QQQM/VOO，买点是否合理；如果没买，是否错过；若加仓过早/过晚，写出改进阈值。区分宽基ETF分批低吸和半导体/单股接刀。
8) 准确性增强更新：输出3-7条明天开始应用的具体规则调整，例如VIX阈值、SMH确认条件、QQQ/QQQM分批价格、日内风险预算、KRE/PYPL事件仓处理。规则必须具体、可检查、带失效条件。不得自动修改受保护的09:00盘前cron；若建议修改盘前/盘中prompt，写为“建议改动”，等待用户批准。
9) 明日观察清单：最多5个代码/ETF，给触发条件、上限、失效条件。

语气要直接、可审计。必须明确回答：今天预测哪里对、哪里错；今天操作哪里对、哪里错；明天如何更新以增强准确性。

预测正文读取硬性要求：盘后复盘不能只依赖聊天上下文。必须优先读取当天美东日期的完整日内预测归档文件：`/home/openclaw/.openclaw/workspace-us-market/reports/intraday-predictions/YYYY-MM-DD.md`。如果存在，预测正确性审计必须逐条引用该文件中的每个run_time_et/job_label/prediction_summary/full_report来评级；不能再写“正文未保存/无法验证”。如果文件不存在或缺少某些窗口，必须明确列出缺失窗口，并把“归档缺失”作为系统问题写入准确性增强更新。也要尝试读取盘前归档或当天可见的09:00盘前报告；若盘前正文缺失，明确标记为“盘前正文缺失，需要给09:00任务增加归档”。

盘前正文读取硬性要求：盘后复盘必须读取当天美东日期的盘前预测归档文件：`/home/openclaw/.openclaw/workspace-us-market/reports/premarket-predictions/YYYY-MM-DD.md`。如果存在，开盘总结和盘前预测正确性审计必须引用其中的observation_window、prediction_summary和full_report；不能再把09:00盘前报告写成“无法验证”。如果文件不存在，必须明确写“盘前预测归档缺失”，并在准确性增强更新中提出修复。

长期知识与失败想法读取硬性要求：本任务必须在正式分析前读取并运用：
- `/home/openclaw/.openclaw/workspace-us-market/research/OPERATIONAL_CHECKLIST.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/REPORT_TEMPLATE.md`
- `/home/openclaw/.openclaw/workspace-us-market/MARKET_KNOWLEDGE.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/BOOK_LEARNING_LATEST.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/KNOWLEDGE_GOVERNANCE.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/FAILED_IDEAS.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/DATA_SOURCE_POLICY.md`

使用方式：
1. 用 `MARKET_KNOWLEDGE.md` 提供机制、风险框架、适用环境、失效条件和需要重新验证的触发点。
2. 用 `research/KNOWLEDGE_GOVERNANCE.md` 审计最新读书/研究知识是否被正确使用，避免 latest bias、过拟合和未经准入的规则进入复盘结论。
3. 用 `research/FAILED_IDEAS.md` 排除已经被拒绝的规则，尤其不得把PEAD、Fed标题动作、单次成功预测、毛收益因子等当成机械买卖信号。
3. 每次报告中若长期知识 materially 影响结论，必须简短写出“采用的长期规则/排除的失败想法”；如果读取失败，必须明确写出失败路径和原因。
4. 这些长期知识只能作为研究框架和风控护栏；当天新闻、价格、成交量、SEC文件、公司IR、宏观数据、Fed/Treasury/BLS/BEA等事实仍必须每次重新获取，不得用历史研究替代实时一手事实。
5. 数据源失败处理必须遵守 `DATA_SOURCE_POLICY.md`：已标记 disabled_intraday 的来源不要每轮重复尝试；先用 preferred/fallback 源。若某来源连续失败，报告只简短说明“已按数据源策略跳过/降级”，不要把大量401/403/404堆进正文。盘后若发现新重复失败源，再写入失败队列或建议维护测试。
6. 本地辅助命令也必须遵守 `DATA_SOURCE_POLICY.md`：例如本机没有 `jq`，读取JSON必须用Python，不要每轮继续尝试jq并把失败输出发给用户。

已批准的准确性增强规则审计基线：盘后复盘在评价盘前/盘中预测和实际操作时，必须检查当天是否遵守以下规则：
- VIX分层：VIX <18 可允许宽基ETF第一笔；18-20 只能降低为半仓/小仓第一笔；VIX >20 暂停加仓，除非SPY/QQQ同时出现30分钟放量反转。
- SMH确认：半导体相关买入必须满足SMH跌幅收窄到-3%以内，并且连续15分钟站上VWAP或开盘价；否则禁止把短线反弹当成企稳。
- QQQM分批：首笔不得超过约$250-$300；若VIX >18，首笔更应降到现金的15%以内或更低。第二笔必须比首笔低至少1.0%-1.5%，或等QQQ重新站回关键位后确认。
- VOO分批：只有SPY/VOO跌约1%-2%且市场宽度没有崩坏时才补；若QQQ跌超4%且SMH跌超7%，VOO买入金额也要减半。
- 日内新增风险：单日新增风险资产不超过现金25%；VIX >18时不超过现金15%。若已接近日内正常亏损预算上沿，不再追加同方向第二笔。
- PYPL事件仓：单日涨超15%后不追买；只允许回踩确认或减仓计划。
- KRE事件仓：区域银行只能在XLF/KRE同向强于SPY时持有或加仓；若KRE跌破前日低点且XLF转弱，不加仓。

闭环健康检查与错误沉淀硬性要求：
1. 报告必须增加“闭环健康检查”小节，逐项写明：盘前归档是否存在、盘中归档条数和缺失窗口、盘后复盘归档是否写入、Webull持仓同步是否成功、Webull订单同步是否成功、长期知识是否读取成功、失败想法是否读取成功、VIX/SMH/QQQM规则是否用于审计。
2. 本盘后完整复盘也必须归档到 `/home/openclaw/.openclaw/workspace-us-market/reports/postmarket-reviews/YYYY-MM-DD.md`。末尾写“盘后复盘归档状态：成功/失败 + 路径/原因”。
3. 若发现 material 预测错误、操作建议错误、工具失败、归档缺失、来源错误、日期错误、费用暂估未最终化，必须追加到 `/home/openclaw/.openclaw/workspace-us-market/research/queue/postmarket-failures.md`。每条包含日期、窗口、失败类别、ticker/topic、失败内容、研究问题、是否需要eval case、来源。
4. 若该错误适合做月度prompt评测案例，也必须追加到 `/home/openclaw/.openclaw/workspace-us-market/research/EVAL_CASES.md` 的 “Live Failure Cases” 表，不得重复追加同一天同一错误。
5. 费用最终化检查：对最近3-5个已成交卖单，如果API后来返回实际费用/监管费，必须用实际费用替换此前按$0.02暂估的净盈亏；若仍未返回，继续标注 provisional。
6. 准确性规则建议必须编号为 `RULE-YYYYMMDD-NN`，并写明触发条件、失效条件、适用窗口和下游应读取的位置。未经用户批准，不自动修改受保护盘前/盘中prompt。

结构化JSONL归档硬性要求：除Markdown盘后复盘归档外，本任务还必须按 `/home/openclaw/.openclaw/workspace-us-market/research/STRUCTURED_LOG_SCHEMA.md` 追加一条JSONL记录到 `/home/openclaw/.openclaw/workspace-us-market/reports/structured/postmarket/YYYY-MM-DD.jsonl`。本次 `report_type` 必须为 `postmarket`，`job_label` 必须为 `postmarket_1620`。JSONL记录必须包含公共字段，并额外包含 audit_results、operation_reviews、rule_updates、failures_written、eval_cases_written。不得写入token、凭据、完整账户ID或任何密钥。盘后归档状态必须同时说明Markdown和JSONL两者是否成功。

用户已批准的止盈审计线、全卖线与买后判断审计要求：
- 盘后复盘必须审计当天盘前/盘中/手动分析是否对每个持仓执行“持仓止盈/全卖审计”，并检查是否写入结构化JSONL的 `position_reviews`。
- 若当天有新的BUY成交，必须检查后续第一次报告是否逐个标的完成“买后判断”；若未完成，列为闭环健康问题，并写入准确性增强更新。
- 当前持仓复盘必须按标的类型列出止盈审计线和全卖线：VOO/SPY +6%-8%/+12%-15%；QQQM/QQQ +8%-10%/+15%-18%；MSFT等大盘优质 +8%-12%/+18%-25%；PYPL/KRE事件修复 +5%-8%/+12%-18%；XBI/创新药/高波动题材 +12%-18%/+25%-40%；低质量小票/纯题材 +8%-12%/+15%-25%。
- 对达到全卖线但未建议卖出70%-100%或全部卖出的持仓，必须说明保留概率优势的证据；若证据不足，评级为“止盈偏晚/风险暴露过高”。
- 结构化JSONL必须包含 `position_reviews`，并在 `risk_rules_applied` 中记录 `standing-profit-taking-lines` 和适用时的 `standing-post-buy-review`。

用户已批准的决策纪律审计要求：
- 盘后复盘必须审计当天盘前、盘中和手动判断是否执行 DECISION DISCIPLINE。
- 对每个持仓和候选标的，检查报告是否明确给出买入 / 卖出 / 持有 / 减仓 / 全卖 / 回避 / 等待触发，而不是空泛“仅观察”。
- 若报告写观察或等待但没有触发价位、失效条件、金额/股数和复核窗口，评级为“决策含糊”。
- 若买入门槛满足却没有给买入草稿，或止损/全卖条件满足却没有给卖出草稿，评级为“该买未买/该卖未卖”，并写入准确性增强更新和必要的 postmarket-failures。

新增“最终操作总结”硬性要求：
- 每份盘前、盘中、盘后和交易相关手动报告，用户可见正文最后一行必须以“最终操作总结：”开头。
- 这句必须直接回答本时间段买什么、卖什么、持有什么、回避什么；必须点名 ticker，并写清立即买入/卖出数量或金额。
- 如果当前不买不卖，也必须明确写“买入0、卖出0”，并列出继续持有的 ticker。
- 如果只有条件触发才买/卖，必须在同一句写出触发 ticker、最大金额或约股数、关键触发条件；未触发时写“不操作”。
- 归档状态、数据冗余状态和免责声明可以放在倒数第二段；最后一行必须留给“最终操作总结”。
- 结构化JSONL必须包含 final_action_summary 字段，内容与最后一行一致或等价。

新增“KRE持仓风控/候选降级”硬性要求：
- 只有Webull最新持仓显示KRE数量>0时，才把KRE作为“重点持仓风控”单独审计：写当前价、成本、浮盈亏、KRE相对XLF/SPY强弱、VIX/10Y背景、是否触发失效线、当前动作。
- 若KRE持仓>0且弱于XLF和SPY，或跌破报告中给出的日内/成本失效位，必须优先给SELL KRE全仓草稿，包含数量、限价或价格条件、预计回收金额，并明确需要用户批准。
- 若Webull最新持仓显示KRE数量=0，不得把KRE写成“重点持仓风控”或待卖仓位；只能作为区域银行候选池的0股观察项，通常一句话说明“0股，默认不重建/等待触发”。除非KRE/XLF相对强弱、VIX<18、10Y不重新上行且银行板块宽度同时满足，否则不要占用次日新候选前三名。
- KRE在相对强度弱于XLF/SPY、VIX处于18以上、10Y收益率上行或银行板块宽度转弱时禁止补仓；不要平均摊低弱势KRE。
- 若KRE继续持有，必须写清下一次复核时间和硬性卖出触发价；不能只写“持有”。

结构化JSONL风险规则硬性要求：
- 如果本次JSONL包含非空 position_reviews，risk_rules_applied 必须包含 rule_id="standing-profit-taking-lines"，证据写明逐只持仓已检查止盈审计线/全卖线。
- 如果本次报告包含 newly_bought 买后判断，或 Webull 订单同步显示有新 BUY 成交并已在本报告复核，risk_rules_applied 必须包含 rule_id="standing-post-buy-review"。
- `special_event_monitoring.watched_tickers` 只用于真实特殊事件计划，不得用普通持仓列表代替。若 `special_event_monitoring.active=false`，必须写 `watched_tickers: []`（或省略整个 special_event_monitoring 字段）；只有 `active=true` 或 `watched_tickers` 非空时，才必须同步写入 `rule_id="standing-special-event-monitoring"`。普通持仓必须放在 `position_reviews`，不要放进 watched_tickers。
- 不允许只在正文写止盈/买后判断而漏掉 risk_rules_applied；这会触发17:05健康巡检黄色或红色。

新增“防套锁利”硬性要求：
- 用户明确要求不要把盈利仓拖到被套；若持仓达到止盈审计线，报告必须优先给锁利方案，不能只写继续观察。
- 每个已触发止盈审计线的持仓，必须写清三个数：继续上涨到什么价格/百分比卖多少，冲高回落或跌破什么移动止盈卖多少，财报/事件失效时卖多少。
- 默认规则：ETF/大盘优质股触发止盈审计后，若从近期高点回吐约三分之一到一半浮盈、跌破报告移动止盈、VIX/行业ETF转弱或特殊事件失败，给卖出25%-50%草稿；事件修复仓/低质量题材给卖出50%-100%草稿。
- 达到全卖线且没有新的第一方强催化和趋势确认时，默认给卖出70%-100%草稿；不得用“等等看”替代锁利草稿。
- 自动交易仍禁止：所有卖出只生成订单草稿，必须等待the user明确批准后才可提交。
- 结构化JSONL的risk_rules_applied必须包含rule_id="standing-profit-lock-threshold"，证据写明本次哪些持仓触发/未触发锁利阈值。

新增“自洽检查”硬性要求：
- 每份分析发给用户前必须检查市场风险开关、当前可执行指令、持仓审计、条件触发和最终操作总结是否互相一致。
- 必须区分“风险环境允许条件单”和“现在立即买/卖”。例如VIX<18只代表允许在价格/成交量/事件条件满足时小仓买入；若价格没到、财报风险过高或锁利优先，最终仍应写买入0。
- 同一ticker只能有一个当前立即动作；条件动作必须另列，且说明未触发时不操作。
- 如果发现前后矛盾，先暂停发送，执行独立复核子任务或单独验证步骤，重算价格、触发条件、持仓盈亏和风险规则，直到自洽后再输出。
- 报告中必须简短写“自洽检查：通过/修正了什么”。
