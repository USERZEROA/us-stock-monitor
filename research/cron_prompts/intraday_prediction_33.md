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

现在是美股常规交易日每小时33分的盘中判断提醒。请先确认当前美东日期时间、NYSE/Nasdaq是否处于常规开市状态；若是假日、非交易日、盘前、熔断、或提前休市后，则只简短说明跳过本次交易提醒。若市场开市，请为Telegram用户the user做盘中高流动性美股候选池扫描和当前持仓买/卖/持有判断。

硬性要求：不得声称完成全美股穷尽扫描；只能称为“高流动性美股候选池扫描”，并说明覆盖限制。不得执行交易。必须重新获取最新行情与时间戳，至少检查SPY/QQQ/IWM/DIA、VIX、2Y/10Y美债收益率、美元、原油、黄金、主要行业ETF（XLK/SMH/XLF/XLE/XLV/XLI/XLY/XLC/XLU/XLRE）和高流动性个股/事件股。

Webull API持仓同步要求：在账户基线判断前，必须先尝试执行只读同步命令：`cd /home/openclaw/.openclaw/workspace-us-market && timeout 45s python3 scripts/webull_portfolio_sync.py`。该脚本只允许读取账户、余额、持仓并更新`/home/openclaw/.openclaw/workspace-us-market/webull_portfolio_snapshot.json`和`/home/openclaw/.openclaw/workspace-us-market/PORTFOLIO_STATE.md`，不得下单、改单、撤单。若同步成功，账户基线必须优先使用Webull API快照。若同步失败、超时、token为PENDING/EXPIRED或2FA未完成，必须在报告中说明“Webull API同步失败/未验证”，然后回退使用`PORTFOLIO_STATE.md`里的最新用户确认截图/成交基线；不得把旧现金或旧持仓伪装成实时API数据。

账户基线要求：必须先读取`/home/openclaw/.openclaw/workspace-us-market/PORTFOLIO_STATE.md`和（若存在）`/home/openclaw/.openclaw/workspace-us-market/webull_portfolio_snapshot.json`。同时检索记忆里的最新账户基线，搜索关键词包含“Latest account baseline 最新账户截图 最新持仓 VOO QQQM PYPL MSFT XLC cash Buying Power settled cash Webull API”。必须使用Webull API成功快照或用户最新已知账户截图、成交回传、现金/settled cash、VOO/QQQM股数和其他持仓作为账户基线；用户说每次账户变动都会发截图，所以若本次任务能看到最新截图、成交文字或成功API快照，必须覆盖旧基线。不要使用旧示例仓位作为事实；若API失败但记忆/文件里有最新账户基线，必须使用该基线，不能写未知。若既无API快照、截图也无记忆基线，才标注“账户状态沿用最新已知，需用户确认”。

交易执行权限边界：Webull API接入不是全自动交易许可。任何买入/卖出都只能先生成订单草稿，等待用户对该具体订单明确批准后，才可在后续单独步骤提交。当前盘中扫描任务不得直接提交订单。

目标口径：用户希望评估30天内翻倍路径，因此每次都必须判断现有仓位卖/持/买，而不是只补仓。必须先用Webull最新持仓表划分“当前持仓”和“已卖出/0股候选”：只有当前持仓才进入卖出/减仓/全卖审计；已经卖出且数量为0的ticker（例如PYPL卖出后）不得再判断“需不需要卖出”，只能和其他待买股票一样判断是否重建、等待触发或回避。VOO/QQQM不能因为已有盈利或核心属性就默认不卖，也不能机械加仓；但不得建议融资、期权、杠杆ETF、反向ETF或极端赌博。

抄底判断要求：每次报告必须单独加入“是否抄底”判断，不能因为QQQ/QQQM/VOO等宽基ETF下跌就机械写不买。必须区分宽基ETF回撤低吸机会、单股/半导体加速下跌接刀风险、以及账户当日风险预算压力。对QQQM、VOO、SPY/QQQ相关宽基ETF，若出现明显回撤，必须明确判断是否适合分批抄底：可以买则给第一笔代码、金额/股数、限价、触发条件、第二笔观察价位和失效条件；不买则说明是因为趋势仍在加速、VIX/SMH/QQQ条件恶化、账户风险超限，还是价格没有到位。不得只写“本窗口不操作”而不回答是否应该抄底。

输出必须明确到当前时间能执行的金额/股数，不要只给方向。必须包含：1) 当前市场风险开关；2) API同步状态和账户基线：最新已知现金、settled cash、VOO/QQQM和其他持仓；3) 【当前可执行指令】逐项写清：买入哪些=代码/美元金额/约股数，卖出哪些=代码/美元金额/约股数，持有哪些=代码/股数；如果不操作，买入金额和卖出金额必须写0；4) 当前持仓逐项判断：卖多少/买多少/继续持有多少，以及理由；5) 新候选最多3个，每个给触发条件、买入金额上限、失效条件；6) 明确不买/不卖条件；7) 若没有合格机会，明确“本窗口不操作，继续现金”，并写清最接近可买的1-2个ticker差哪一条硬门槛、下一次何时复核、若门槛满足应买多少；8) 提醒用户下单前确认券商实时报价、股数、settled cash、订单类型和滑点；9) 如果涉及API下单，只能给订单草稿并等待用户批准。风险输出必须使用小账户口径：正常单笔计划亏损约账户净值0.25%-0.50%，正常单日风险约0.50%-0.75%，100美元只是绝对上限不是正常预算。

订单复盘/成交盈亏要求：在账户基线判断前，必须同时尝试执行只读订单状态命令：`cd /home/openclaw/.openclaw/workspace-us-market && timeout 45s python3 scripts/webull_order_status.py`。该脚本只读取订单历史和未成交挂单，不得下单、改单、撤单。报告必须包含“订单复盘/成交盈亏”部分，说明上次尝试买卖了什么、哪些订单已成交、哪些订单仍未成交/挂单/被拒绝；对已成交卖单必须写明成交价、成本、API返回的手续费/监管费，以及扣除成本和已知费用后的已实现盈亏。如果API尚未返回费用，默认先按用户确认的小额订单费用 `$0.02` 估算，必须标注“费用未返回，净盈亏暂按 $0.02 费用估算，最终以券商记录为准”。

预测正文归档要求：本任务必须把“本次完整预测正文”保存下来，供16:20 ET盘后复盘逐条审计，不得只依赖Telegram聊天上下文。生成最终报告后，先创建目录 `/home/openclaw/.openclaw/workspace-us-market/reports/intraday-predictions`，再按美东日期追加保存到 `/home/openclaw/.openclaw/workspace-us-market/reports/intraday-predictions/YYYY-MM-DD.md`。每次追加必须包含：
- 分隔线 `---`
- `run_time_et`：本次报告美东时间
- `job_label`：cron_33
- `job_id`：ed297920-efc6-4001-9674-a5235b10c726
- `market_status`：开市/跳过/异常
- `webull_portfolio_sync_status` 和 `webull_order_sync_status`
- `prediction_summary`：本次核心预测、触发条件、买/卖/持有、是否抄底
- `full_report`：和发给Telegram用户的完整正文
如果文件写入失败，必须在报告中明确写“预测正文归档失败”，并说明失败原因。

已批准的准确性增强规则：后续盘中判断必须应用以下规则，而不是只作为建议：
- VIX分层：VIX <18 可允许宽基ETF第一笔；18-20 只能降低为半仓/小仓第一笔；VIX >20 暂停加仓，除非SPY/QQQ同时出现30分钟放量反转。
- SMH确认：半导体相关买入必须满足SMH跌幅收窄到-3%以内，并且连续15分钟站上VWAP或开盘价；否则禁止把短线反弹当成企稳。
- QQQM分批：首笔不得超过约$250-$300；若VIX >18，首笔更应降到现金的15%以内或更低。第二笔必须比首笔低至少1.0%-1.5%，或等QQQ重新站回关键位后确认。失效条件：QQQ跌破日低且VIX创日高。
- VOO分批：只有SPY/VOO跌约1%-2%且市场宽度没有崩坏时才补；若QQQ跌超4%且SMH跌超7%，VOO买入金额也要减半。
- 日内新增风险：单日新增风险资产不超过现金25%；VIX >18时不超过现金15%。若已接近日内正常亏损预算上沿，不再追加同方向第二笔。
- PYPL事件仓：单日涨超15%后不追买；只允许回踩确认或减仓计划。失效条件是跌回事件启动价/缺口下沿且放量。
- KRE事件仓：区域银行只能在XLF/KRE同向强于SPY时持有或加仓；若KRE跌破前日低点且XLF转弱，不加仓。

长期知识与失败想法读取硬性要求：本任务必须在正式分析前读取并运用：
- `/home/openclaw/.openclaw/workspace-us-market/research/OPERATIONAL_CHECKLIST.md`
- `/home/openclaw/.openclaw/workspace-us-market/MARKET_KNOWLEDGE.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/BOOK_LEARNING_LATEST.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/KNOWLEDGE_GOVERNANCE.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/FAILED_IDEAS.md`
- `/home/openclaw/.openclaw/workspace-us-market/research/DATA_SOURCE_POLICY.md`

使用方式：
1. 用 `MARKET_KNOWLEDGE.md` 提供机制、风险框架、适用环境、失效条件和需要重新验证的触发点。
2. 用 `research/KNOWLEDGE_GOVERNANCE.md` 防止最新读书摘要覆盖实时行情、账户约束和长期风控规则。
3. 用 `research/FAILED_IDEAS.md` 排除已经被拒绝的规则，尤其不得把PEAD、Fed标题动作、单次成功预测、毛收益因子等当成机械买卖信号。
3. 每次报告中若长期知识 materially 影响结论，必须简短写出“采用的长期规则/排除的失败想法”；如果读取失败，必须明确写出失败路径和原因。
4. 这些长期知识只能作为研究框架和风控护栏；当天新闻、价格、成交量、SEC文件、公司IR、宏观数据、Fed/Treasury/BLS/BEA等事实仍必须每次重新获取，不得用历史研究替代实时一手事实。
5. 数据源失败处理必须遵守 `DATA_SOURCE_POLICY.md`：已标记 disabled_intraday 的来源不要每轮重复尝试；先用 preferred/fallback 源。若某来源连续失败，报告只简短说明“已按数据源策略跳过/降级”，不要把大量401/403/404堆进正文。
6. 本地辅助命令也必须遵守 `DATA_SOURCE_POLICY.md`：例如本机没有 `jq`，读取JSON必须用Python，不要每轮继续尝试jq并把失败输出发给用户。

归档状态输出硬性要求：报告末尾必须追加一行“归档状态”。格式为：
- 归档状态：成功，路径：/home/openclaw/.openclaw/workspace-us-market/reports/intraday-predictions/YYYY-MM-DD.md，本次标签：cron_33
或：
- 归档状态：失败，路径：...，原因：...
如果主行情源或任一工具失败但使用了备用源，也必须在报告中写清“数据冗余状态：主源失败/备用源成功/哪些数据缺失”。
若失败源已列入 DATA_SOURCE_POLICY.md 的 disabled_intraday，不再每轮尝试；数据冗余状态只需写“按策略跳过已禁用源”，并说明使用了哪个可用源。

结构化JSONL归档硬性要求：除Markdown盘中预测正文归档外，本任务还必须按 `/home/openclaw/.openclaw/workspace-us-market/research/STRUCTURED_LOG_SCHEMA.md` 追加一条JSONL记录到 `/home/openclaw/.openclaw/workspace-us-market/reports/structured/intraday/YYYY-MM-DD.jsonl`。本次 `report_type` 必须为 `intraday`，`job_label` 必须为 `cron_33`。JSONL记录必须包含：run_time_et、trading_date、job_id、job_label、report_type、market_status、archive_status、inputs、predictions、action_drafts、risk_rules_applied、failure_flags、source_refs。不得写入token、凭据、完整账户ID或任何密钥。报告末尾的“归档状态”必须同时说明Markdown和JSONL两者是否成功。

用户已批准的止盈审计线、全卖线与买后判断硬性要求：
- 每次涉及账户或持仓的报告，必须按 `/home/openclaw/.openclaw/workspace-us-market/AGENTS.md` 的 PROFIT TAKING AND PER-POSITION REVIEW 和 `MARKET_KNOWLEDGE.md` 的 Profit Taking Uses Type-Specific Audit And Exit Lines 执行。
- 每个当前持仓必须单独输出“持仓止盈/全卖审计”：ticker、标的类型、数量、成本、当前价、浮盈/浮亏百分比、止盈审计线、全卖线、是否触发、概率优势是否仍存在、移动止盈/失效条件、当前动作（买入0/卖出0/持有/减仓/卖出70%-100%/全部卖出）。
- 已卖出、当前数量为0的ticker不能写在“当前持仓止盈/全卖审计”里作为待卖仓位；可以在候选池或特殊事件监控里写为“0股，候选重建/回避”，并且action_drafts里approx_shares必须为0，side只能是BUY条件候选、HOLD/AVOID或WAIT_TRIGGER，不能出现SELL已卖出仓位。
- 类型阈值必须分开：VOO/SPY宽基核心ETF审计+6%-8%、全卖线+12%-15%；QQQM/QQQ成长宽基ETF审计+8%-10%、全卖线+15%-18%；MSFT等大盘优质股审计+8%-12%、全卖线+18%-25%；PYPL/KRE等事件修复仓审计+5%-8%、全卖线+12%-18%；XBI/创新药/高波动题材审计+12%-18%、全卖线+25%-40%；低质量小票/纯题材审计+8%-12%、全卖线+15%-25%。
- 达到全卖线后，若没有新的强催化、趋势确认或更高胜率理由，且出现放量跌破5日/10日线、日内高点回撤超过正常日波动1.5倍、VIX>20且QQQ/SPY转弱、催化兑现无新上修、持仓盈利成为账户主要风险或有更高胜率替代机会，默认给出卖出70%-100%或全部卖出的订单草稿；不得直接下单，必须等待用户批准。
- 每当Webull订单同步、用户回报或上下文显示有新的BUY成交，后续第一次报告必须对每一只新买入股票/ETF单独运行一次“买后判断”：买入原因是否仍成立、成本/现价/浮盈亏、标的类型、止损或失效位、止盈审计线、全卖线、是否允许加仓、是否禁止补仓、当前动作草稿。一次买入多个标的时必须逐个判断，不能合并成一句。
- 结构化JSONL必须包含 `position_reviews` 数组，并为每个持仓或新买入标的写入一条记录；`risk_rules_applied` 必须包含 `standing-profit-taking-lines` 和适用时的 `standing-post-buy-review`。

用户已批准的决策纪律硬性要求：
- 每次涉及账户、持仓或候选标的的报告，必须按 /home/openclaw/.openclaw/workspace-us-market/AGENTS.md 的 DECISION DISCIPLINE 执行。
- 每个当前持仓和每个候选标的必须给出明确动作：买入 / 卖出 / 持有 / 减仓 / 全卖 / 回避 / 等待触发。
- “仅观察”不得单独作为结论；若写观察或等待，必须同时给出触发价位或事件、失效条件、最大金额、约股数、有效时间窗口和下一次复核条件。
- 若所有买入门槛满足，必须给出买入订单草稿；若止损、失效或全卖条件满足，必须给出卖出订单草稿。不得用“市场复杂”“继续观察”等空泛理由替代买/卖/持有判断。
- 报告必须增加“决策纪律检查”：逐项说明哪些标的满足买/卖条件、哪些未满足、未满足的是哪条硬门槛。
- 决策纪律检查不得只给“全部未满足所以不操作”。如果买入0，必须点名最接近可执行买入的ticker和缺失门槛；如果卖出0，必须点名当前持仓未触发哪条止损/止盈/失效门槛；若现金超过账户50%，必须说明现金部署计划是“立即买0”还是“条件触发买入”，以及金额上限。
- 果断给草稿不等于自动交易；任何买入或卖出仍必须等待用户批准后才能提交。

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
- 若Webull最新持仓显示KRE数量=0，不得把KRE写成“重点持仓风控”或待卖仓位；只能作为区域银行候选池的0股观察项，通常一句话说明“0股，默认不重建/等待触发”。除非KRE/XLF相对强弱、VIX<18、10Y不重新上行且银行板块宽度同时满足，否则不要占用新候选前三名。
- KRE在相对强度弱于XLF/SPY、VIX处于18以上、10Y收益率上行或银行板块宽度转弱时禁止补仓；不要平均摊低弱势KRE。
- 若KRE继续持有，必须写清下一次复核时间和硬性卖出触发价；不能只写“持有”。

结构化JSONL风险规则硬性要求：
- 如果本次JSONL包含非空 position_reviews，risk_rules_applied 必须包含 rule_id="standing-profit-taking-lines"，证据写明逐只持仓已检查止盈审计线/全卖线。
- 如果本次报告包含 newly_bought 买后判断，或 Webull 订单同步显示有新 BUY 成交并已在本报告复核，risk_rules_applied 必须包含 rule_id="standing-post-buy-review"。
- 不允许只在正文写止盈/买后判断而漏掉 risk_rules_applied；这会触发17:05健康巡检黄色或红色。

新增“特殊事件监控”硬性要求：
- 每次盘前/盘中必须按 /home/openclaw/.openclaw/workspace-us-market/AGENTS.md 的 SPECIAL EVENT MONITORING 执行“特殊事件监控”。若当天有大型公司财报/电话会、FOMC/CPI/非农、国债拍卖、重大SEC/IR披露、监管裁决或确认原因的盘前异常波动，必须把该日标记为特殊事件日。
- 盘前任务若识别出特殊事件日，必须输出“特殊事件监控计划”：watched tickers、事件类型、官方时间、监控开始/结束、关联ETF/持仓、分钟级指标、30分钟复核时间、买入/卖出草稿触发条件、失效条件、最大金额或约股数。
- 本盘中任务若被用户重新启用，必须优先读取当天最新结构化JSONL或盘前报告中的special_event_monitoring计划；若仍有效，先复核这些ticker，再扫描普通候选。复核必须比较事件前后价格、成交量、VWAP/开盘区间、同业/ETF相对强弱、VIX、QQQ/SPY/SMH或相关行业ETF，以及最新IR/SEC/可靠新闻。
- 若本任务未启用，不得把特殊事件复核责任写成“交由cron_03/cron_33”；应由盘前创建的deleteAfterRun一次性提醒或用户手动触发复核承担。
- 财报事件不得只看EPS/营收；必须同时看指引、利润率、现金流、分部指标、capex/AI/云读穿、电话会和ETF/同业确认。
- 特殊事件监控只生成买入/卖出订单草稿，不得自动下单、改单或撤单；所有交易仍必须等待用户批准。
- 如果special_event_monitoring.active=true或watched_tickers非空，结构化JSONL必须包含special_event_monitoring字段，risk_rules_applied必须包含rule_id="standing-special-event-monitoring"。

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
