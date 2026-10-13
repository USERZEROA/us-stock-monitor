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

执行今天的《美股盘前机构级情报报告》。

首先确认当前 America/New_York 日期、时间、美股交易状态，以及本次观察窗口。默认观察窗口为上一个美股交易日 16:00 ET 至当前执行时间。

盘前深度事件扫描硬性要求：

由于用户已关闭每天每小时03分和33分的高频盘中扫描，09:00 ET盘前报告必须承担更完整的当日事件发现职责。正式形成结论前，必须建立并逐项核对“今日事件总清单”，至少覆盖以下来源和事件类型：

1. 官方宏观日历：BLS、BEA、Federal Reserve、U.S. Treasury、CFTC、EIA、ISM、Conference Board、University of Michigan等，列出当天和下一个交易日美东时间内的已确认数据、讲话、纪要、拍卖、库存、政策公告；如果没有一级事件，也要写明“未发现CPI/PCE/NFP/FOMC级别事件”。
2. 公司IR和财报电话会：检查当天盘前、盘中、盘后以及次日盘前的S&P 100、市值前50、Magnificent Seven、主要半导体、云、银行、能源、医疗、消费、工业龙头的财报发布日期、电话会时间、8-K/新闻稿链接和管理层指引窗口。必须特别标注当前持仓和候选标的相关事件。
3. SEC/交易所/监管：检查当前持仓、S&P 100和异常波动标的的8-K、10-Q、10-K、6-K、Form 4、S-3/424B、并购、回购、增发、分红、拆股、诉讼、监管、召回等一手披露；无重大新披露时写“未发现影响当前持仓的重大新SEC/IR披露”。
4. 盘前异常波动：扫描盘前涨跌幅、成交量和可靠原因。只有价格、时间戳和一手/高质量来源同时可得，才进入行动清单；无法确认原因时写“异动存在，原因尚未确认”，不得当作买入理由。
5. 事件影响映射：每个重要事件必须映射到相关股票、ETF、持仓和候选名单，例如AMZN/AAPL影响QQQ/QQQM/VOO/NVDA，XOM/CVX影响XLE/油价链，银行事件影响KRE/XLF。
6. 明日预告：列出下一个交易日前24小时内会影响今天收盘持仓决策的已确认事件，尤其是盘后财报电话会、次日08:30 ET宏观数据、次日开盘前财报和重大监管截止时间。
7. 提醒口径：由于03/33盘中高频任务已按用户要求关闭，不得在报告中写“交由cron_03/cron_33每30分钟复核”。若存在重大事件，需要创建更少但更精准的一次性提醒；若无法创建，明确写入失败原因。

事件股说明硬性要求：
- 每个进入“今日事件总清单”“今日财报日历”“盘前异常波动”“行动清单”“最终多空结论”或 Telegram 摘要的公司事件股，后面都必须补充可读的公司背景，不得只写代码和涨跌幅。
- 背景至少包括：公司主要做什么、核心产品/服务或收入驱动、为什么这个事件会影响相关ETF/行业/当前持仓或候选、一个用户容易联想到的典型事件或风险点。
- 示例格式：`亚马逊（AMZN）：电商、AWS云服务和广告平台公司；AWS增速/资本开支会读穿云和AI链，电商利润率会影响消费与大盘权重；类似事件是财报后因AWS指引或利润率变化带动QQQ/VOO。今日事件：...`
- 对用户不一定熟悉的公司（例如PLTR、ON、VRTX、WMB、FANG、OKE等）必须更详细；对Mag 7等耳熟公司也要说明其影响机制，不要只写“权重股”。
- Telegram摘要若篇幅有限，也必须至少有一行“今日事件股：代码 + 一句话公司说明 + 今日事件/操作结论”；完整报告中再展开。

严格按照工作区 AGENTS.md 中的长期规则完成任务，包括：

1. 检索市场整体、股指期货、利率、美元、原油、黄金、比特币及波动率信息；
2. 检索美国大型上市公司、S&P 100、美国市值前50公司及当日重大异动公司的最新动态；
3. 检查 SEC 申报、公司投资者关系官网、政府机构、交易所和其他第一方原始来源；
4. 汇总今日宏观经济数据、美联储活动、政策事件和国债拍卖；
5. 汇总今日盘前与盘后财报；
6. 识别有可靠新闻原因的盘前异常波动；
7. 对高影响事件进行独立核验，去除重复新闻和没有新增事实的旧闻；
8. 自动判断今天是否属于 CPI、非农、FOMC、重大财报等高事件风险日；如属于，自动启用重大事件增强分析；
9. 明确区分已确认事实、市场反应、分析判断和未确认消息；
10. 每个核心事实、数字和事件必须附来源、发布时间及原始链接；
11. 实时数据无法获得时明确说明，不得根据模型记忆猜测或编造；
12. 使用中文，按照 AGENTS.md 规定的机构级报告结构输出。

最后必须生成“第13部分：今日行动清单”。明确回答：

1. 今天最值得关注的1至5只股票；
2. 哪些股票属于条件性候选买入、仅观察或回避；
3. 每只股票最可能因何种已确认事件发生波动；
4. 事件的官方时间或合理观察窗口；
5. 只有满足哪些价格、成交量或事件确认条件后才值得考虑；
6. 哪些条件出现时必须放弃该判断；
7. 如果今天休市，不得建议今天买入，改为输出下一个交易日的行动计划。

不得预测某只股票在无官方事件支持的具体分钟一定上涨或下跌。

新增“持仓复核与卖出确认”要求：

在正式分析前，必须优先读取 `/home/openclaw/.openclaw/workspace-us-market/PORTFOLIO_STATE.md`。该文件是用户最新确认的持仓、现金和账户基线；如果用户在本次任务上下文中又提供更新的截图、文字账户更新或成交记录，则以后者为准并明确标注。若文件无法读取，必须在报告中说明“PORTFOLIO_STATE.md 读取失败”，不得无提示回退到更早旧快照。

不得使用旧硬编码账户基线作为精确下单依据。正常情况下必须以 Webull API 成功快照、PORTFOLIO_STATE.md 或用户最新截图/成交文字为准；如果这些全部读取失败，只能透明说明“账户精确状态不可验证，不能给精确买入/卖出金额”，不得把历史仓位伪装成当前可执行基线。

用户已明确确认：助手看见的所有现金、Cash Balance、Buying Power 都视为 Settled Cash。以后不得再询问这些可见现金是否为 Settled Cash，也不得因截图未单列 Settled Cash / Unsettled Cash 就把短期可部署资金按 0 处理。只有当最新截图或更新根本没有显示现金 / Buying Power 金额时，才说明“现金金额未知，无法精确给出新买入金额”。

本任务只读取用户确认的快照和公开市场信息，不登录券商、不提交订单、不替用户交易；如果用户确认执行或提供执行后的账户数据，后续报告才可根据用户确认的信息更新“当前持仓”和“现金剩余”。

每天报告必须单独加入“现有持仓处理”小节，逐项判断：

1. 标普500ETF（VOO）：今天是否继续持有、止盈卖出、止损、减仓、停止加仓或用新资金再平衡；
2. 纳斯达克100ETF（QQQM）：今天是否继续持有、止盈卖出、止损、减仓、停止加仓或用新资金再平衡；
3. 判断依据必须包括：最新价格与趋势、宏观/利率环境、当日事件、ETF或行业风险、持仓集中度、普通应税账户的潜在税务影响、现金账户结算规则；
4. 盈利本身不得自动构成卖出理由；只有当风险收益、集中度、趋势破坏、资金需求或税务/账户规则支持时，才建议卖出或减仓；
5. 如果建议卖出盈利、止损、减仓或调整持仓，必须明确写“需要用户确认后才执行”，不得把建议表述成已执行；
6. 不登录券商、不提交订单、不替用户交易；
7. 如果用户确认执行或提供执行后的账户数据，后续报告才可根据用户确认的信息更新“当前持仓”和“现金剩余”；未收到确认前，不得自行更新账户状态。

新增“今日具体操作摘要”要求：

每天盘前报告必须在行动清单后追加一个短小、可直接执行的“今日具体操作摘要”，回答用户真正需要的四件事：

1. 在保持原有 VOO 和 QQQM 持仓的情况下，今天是否卖出：分别写 VOO 卖多少、QQQM 卖多少；若不卖，写“卖0”。
2. 今天用现金买什么：列出候选代码、策略类型、最大金额、第一笔金额、加仓金额、前置条件和失效条件。
3. 今天在哪些时间点决策：时间点不得机械固定。必须根据当天分析出来的实际宏观数据、Fed事件、公司财报、财报电话会、产品发布、监管/法院决定、国债拍卖、盘前已发生事件和盘后待发生事件来确定。固定市场结构窗口只作为默认框架：09:30-09:45 开盘价格发现、09:45-10:15 第一交易复核、10:15-11:30 第二交易复核、15:30-15:50 尾盘复核。事件型提醒必须跟随当天真实事件时间，例如公司12:00 ET财报就设在12:00后或电话会后，明天1:00 ET事件就设在1:00后，不得每天固定写14:05，除非当天确有14:00 ET重要事件。
4. 今天不该做什么：例如不追第一根K线、不把长期核心仓用于日内、不把100美元当正常亏损预算、不用未确认资金快进快出。

如果 PORTFOLIO_STATE.md、用户最新截图或用户文字更新中显示现金 / Cash Balance / Buying Power，则按用户规则视为 Settled Cash，并可以据此给出“可部署金额”；不要再询问是否为 Settled Cash。若最新信息根本没有显示现金 / Buying Power 金额，必须写“现金金额未知，无法精确给出新买入金额”。每个金额必须与账户规模匹配，避免过度集中。默认规则：单笔正常风险约账户净值0.25%-0.50%，单日正常风险约0.50%-0.75%，单日绝对停止线为100美元和账户净值1.5%两者取较低者。不得把100美元当正常亏损预算。

新增“自动创建当天一次性提醒”要求：

如果当天是美股正常交易日，且报告中给出了可观察的买卖/加减仓时间窗口，必须在报告完成后为当天创建一次性提醒 Cron，提醒执行后自动删除（deleteAfterRun=true）。这些提醒负责重新拉取并多源交叉核对最新行情、复核事件结果与失效位，然后提醒用户；全程只读、不得交易（交叉检验的具体硬性要求见下文“一次性提醒资源预算与交叉检验”）。

一次性提醒的 payload.model 硬性要求（否则 cron preflight 会拒绝，任务空转并触发失败告警）：
- payload.model 必须使用当前 agents allowlist 内的模型；唯一非 Claude 选项是 `openai/gpt-5.5`。禁止填写 `gpt-5`、`gpt-5-mini` 或任何不在 allowlist 的模型名。
- 若无特殊需要，直接省略 payload.model 让其继承 agent 默认路由；需要显式指定时只能用 `openai/gpt-5.5` 或某个 `anthropic/claude-*` allowlist 成员。
- 创建后应确认返回无 preflight 报错；当天若出现 `payload.model ... rejected by ... allowlist`，必须立即改用 `openai/gpt-5.5` 重建，并在报告中标注已修复。

一次性提醒资源预算与交叉检验（硬性要求，2026-09-03 用户指令）：
- 用户明确要求：不给这类一次性事件复核设紧超时——宁可跑久，也要把数据抓全、交叉验证完再收尾，不得因超时在工具执行阶段（tool-execution-started）被截断。核心价值是"交叉检验"，不是省时间。此前 `timeoutSeconds=240` + 抓取被砍导致 ISM 一次性复核连挂即为反面教训。
- payload.timeoutSeconds 设足够大以容纳完整多源抓取：≥`1200`，宏观数据/多源交叉检验建议 `1500`-`1800`。scheduler 需要一个数值上限，故用大值来表达"想抓多久就跑多久"，绝不再用 240/480 这类会截断抓取的低值。
- payload.thinking 保持 `"high"`，不得为省时降档。
- 交叉检验为硬性要求：每个关键结论所依赖的数字（宏观实际值 vs 预期/前值、持仓与基准的价格/涨跌幅/成交量、失效位是否触发）必须从 ≥2 个相互独立来源确认，并按 SOURCE HIERARCHY 分级（官方 Tier1 优先，专业财经 Tier2 交叉印证）。来源冲突时必须写明分歧、取更高层级来源、标注不确定性，不得只凭单一来源或单次抓取下结论。
- 抓取范围保持完整、不得为省时间缩减：事件相关标的 + 全部当前持仓 + 大盘/波动率/利率基准（SPY/QQQ/SMH/VIX/10Y/2Y 及事件相关行业ETF）。
- 创建后确认返回的 timeoutSeconds/thinking 与上述一致；若仍超时，说明超时值还不够，下一份报告须记入 postmarket-failures 并进一步上调超时（继续加大 timeoutSeconds，不得转而削减抓取或降低 thinking/交叉检验强度）。

一次性提醒必须配置失败告警（failureAlert），确保失败时有痕迹可查：
- failureAlert.mode = "announce"，failureAlert.channel = "telegram"，failureAlert.to = "YOUR_TELEGRAM_CHAT_ID"，failureAlert.accountId = "us-market"，failureAlert.after = 1（首次失败即告警）。
- 若创建时无法设置 failureAlert（工具限制），必须在结构化JSONL的 intraday_reminders 字段写入每个 jobId，由17:05健康检查验证其是否成功运行（通过run history）；若健康检查无法获取已删除任务的history，在 closed_loop_health 报告中注明"一次性任务结果无法追溯，依赖 failureAlert 兜底"。

提醒时间必须动态生成，不得把固定时间当作每天模板。创建提醒前先列出“今日提醒计划”，每个提醒必须说明触发原因：

1. 市场结构提醒：若存在日内或2-3日候选，通常创建 09:45 ET 或 10:15 ET 的开盘后复核；如果盘前报告完成时间已晚于这些窗口，则跳过过期窗口，改为下一个合理复核时间。
2. 事件型提醒：根据当天真实事件时间创建，例如宏观数据公布后5-15分钟、Fed讲话/Beige Book/FOMC后5-15分钟、公司财报发布后或电话会开始后10-20分钟、国债拍卖结果后、监管/法院/产品发布的可靠时间窗口后。若事件时间尚未可靠确认，不创建伪精确提醒，只在报告中列为“等待确认”。
3. 持仓/尾盘提醒：如果当天建议过短线仓、需要决定是否隔夜，或有重大盘后财报影响现有/候选持仓，创建 15:45 ET 尾盘复核；否则可跳过。
4. 每天提醒数量以必要为准，通常2-5个；宁可少而准，不要固定生成无事件意义的提醒。

一次性提醒的输出必须简洁：只写“买/不买、卖/不卖、金额、触发条件、止损或失效条件、需要用户确认后自行操作”。注意：输出简洁不等于抓取或核对从简——结论仍须建立在上文要求的完整抓取与多源交叉检验之上，简洁只针对最终呈现文本。提醒不得修改长期研究文件、不得修改本盘前Cron、不得登录券商、不得下单。若提醒工具不可用、时间已经过期或创建失败，必须在报告中明确说明失败原因。

每天报告末尾必须追加“请确认”小节，列出需要用户确认的事项：

1. 是否继续持有标普500ETF（VOO）；
2. 是否继续持有纳斯达克100ETF（QQQM）；
3. 是否卖出盈利、止损、减仓或暂停加仓；
4. 当天是否有新资金到账、成交、撤单或账户截图更新；如果最新信息显示现金 / Cash Balance / Buying Power，按用户规则直接视为 Settled Cash，不再追问是否为 Settled Cash；
5. 若用户已执行交易，要求用户回传更新后的持仓、现金、Buying Power、Settled Cash 和 Unsettled Cash，以便下一次报告更新。

在报告最后追加一个极简结论，标题固定为“最终多空结论”。该结论必须直接写明：

1. 今日条件性做多：列出股票中文名（股票代码）及一句触发条件；如没有明确机会，写“无明确做多，等待确认”。
2. 今日条件性做空/回避：列出股票中文名（股票代码）及一句触发条件或回避理由；如没有明确做空，写“无明确做空，以下仅为回避/观察名单”。
3. 所有股票、ETF、指数、公司和机构名称尽量使用“中文名（英文代码或英文简称）”格式，例如“高盛集团（GS）”“摩根大通（JPM）”“纳斯达克100ETF（QQQ）”。不要只用英文缩写或股票代码指代。
4. 这一部分要短、直接、可扫读，让用户能快速判断做多什么、做空什么、对应股票代码是什么。

本任务只读取公开信息，不登录券商，不交易，不下载未知文件，不修改系统设置。

盘前预测正文归档要求：本09:00盘前任务必须保存“完整盘前预测正文”，供16:20 ET盘后复盘审计“开盘总结”和“盘前预测正确性”。生成最终报告后，先创建目录 `/home/openclaw/.openclaw/workspace-us-market/reports/premarket-predictions`，再按美东日期写入或追加到 `/home/openclaw/.openclaw/workspace-us-market/reports/premarket-predictions/YYYY-MM-DD.md`。每次记录必须包含：
- 分隔线 `---`
- `run_time_et`：本次盘前报告美东时间
- `job_label`：premarket_09
- `job_id`：9b80bc8f-c054-4503-8d71-924b2861ed04
- `observation_window`：本次观察窗口
- `prediction_summary`：盘前核心主线、风险开关、候选买/卖/持有、重要触发条件、失效条件、今日具体操作摘要
- `full_report`：和发给Telegram用户的完整正文
如果文件写入失败，必须在报告中明确写“盘前预测正文归档失败”，并说明失败原因。

已批准的准确性增强规则：今日行动清单和具体操作摘要必须应用以下规则：
- VIX分层：VIX <18 可允许宽基ETF第一笔；18-20 只能降低为半仓/小仓第一笔；VIX >20 暂停加仓，除非SPY/QQQ同时出现30分钟放量反转。
- SMH确认：半导体相关买入必须满足SMH跌幅收窄到-3%以内，并且连续15分钟站上VWAP或开盘价；否则禁止把短线反弹当成企稳。
- QQQM分批：首笔不得超过约$250-$300；若VIX >18，首笔更应降到现金的15%以内或更低。第二笔必须比首笔低至少1.0%-1.5%，或等QQQ重新站回关键位后确认。失效条件：QQQ跌破日低且VIX创日高。
- VOO分批：只有SPY/VOO跌约1%-2%且市场宽度没有崩坏时才补；若QQQ跌超4%且SMH跌超7%，VOO买入金额也要减半。
- 日内新增风险：单日新增风险资产不超过现金25%；VIX >18时不超过现金15%。若已接近日内正常亏损预算上沿，不再追加同方向第二笔。
- PYPL事件仓：单日涨超15%后不追买；只允许回踩确认或减仓计划。失效条件是跌回事件启动价/缺口下沿且放量。
- KRE事件仓：区域银行只能在XLF/KRE同向强于SPY时持有或加仓；若KRE跌破前日低点且XLF转弱，不加仓。

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
2. 用 `research/KNOWLEDGE_GOVERNANCE.md` 防止最新读书摘要覆盖长期规则；只有适用、已准入、未触发禁用条件的知识才能影响判断。
3. 用 `research/FAILED_IDEAS.md` 排除已经被拒绝的规则，尤其不得把PEAD、Fed标题动作、单次成功预测、毛收益因子等当成机械买卖信号。
3. 每次报告中若长期知识 materially 影响结论，必须简短写出“采用的长期规则/排除的失败想法”；如果读取失败，必须明确写出失败路径和原因。
4. 这些长期知识只能作为研究框架和风控护栏；当天新闻、价格、成交量、SEC文件、公司IR、宏观数据、Fed/Treasury/BLS/BEA等事实仍必须每次重新获取，不得用历史研究替代实时一手事实。
5. 数据源失败处理必须遵守 `DATA_SOURCE_POLICY.md`：已标记 disabled_intraday 的来源不要每轮重复尝试；先用 preferred/fallback 源。若某来源连续失败，报告只简短说明“已按数据源策略跳过/降级”，不要把大量401/403/404堆进正文。
6. 本地辅助命令也必须遵守 `DATA_SOURCE_POLICY.md`：例如本机没有 `jq`，读取JSON必须用Python，不要每轮继续尝试jq并把失败输出发给用户。

Webull API持仓与订单同步硬性要求：在账户基线判断前，必须先尝试执行只读同步命令：
1) `cd /home/openclaw/.openclaw/workspace-us-market && timeout 45s python3 scripts/webull_portfolio_sync.py`
2) `cd /home/openclaw/.openclaw/workspace-us-market && timeout 45s python3 scripts/webull_order_status.py`
这些脚本只允许读取账户、余额、持仓、订单历史和未成交挂单，不得下单、改单、撤单。若同步成功，账户基线必须优先使用Webull API快照。若同步失败、超时、token为PENDING/EXPIRED或2FA未完成，必须清楚说明并回退到`PORTFOLIO_STATE.md`和`WEBULL_ORDER_STATUS.md`最新本地基线，不得把旧数据伪装成实时数据。

归档状态输出硬性要求：报告末尾必须追加一行“归档状态”。格式为：
- 归档状态：成功，路径：/home/openclaw/.openclaw/workspace-us-market/reports/premarket-predictions/YYYY-MM-DD.md
或：
- 归档状态：失败，路径：...，原因：...
如果归档失败，仍要投递报告，但必须把失败列入“闭环健康问题”。

结构化JSONL归档硬性要求：除Markdown盘前预测正文归档外，本任务还必须按 `/home/openclaw/.openclaw/workspace-us-market/research/STRUCTURED_LOG_SCHEMA.md` 追加一条JSONL记录到 `/home/openclaw/.openclaw/workspace-us-market/reports/structured/premarket/YYYY-MM-DD.jsonl`。本次 `report_type` 必须为 `premarket`，`job_label` 必须为 `premarket_09`。JSONL记录必须包含：run_time_et、trading_date、job_id、job_label、report_type、market_status、archive_status、inputs、predictions、action_drafts、risk_rules_applied、failure_flags、source_refs。不得写入token、凭据、完整账户ID或任何密钥。报告末尾的“归档状态”必须同时说明Markdown和JSONL两者是否成功。

用户已批准的止盈审计线、全卖线与买后判断硬性要求：
- 每次涉及账户或持仓的报告，必须按 `/home/openclaw/.openclaw/workspace-us-market/AGENTS.md` 的 PROFIT TAKING AND PER-POSITION REVIEW 和 `MARKET_KNOWLEDGE.md` 的 Profit Taking Uses Type-Specific Audit And Exit Lines 执行。
- 每个当前持仓必须单独输出“持仓止盈/全卖审计”：ticker、标的类型、数量、成本、当前价、浮盈/浮亏百分比、止盈审计线、全卖线、是否触发、概率优势是否仍存在、移动止盈/失效条件、当前动作（买入0/卖出0/持有/减仓/卖出70%-100%/全部卖出）。
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

新增”盘中cron关闭+特殊事件日冗余警告”硬性要求：
- 盘前报告必须检查 cron_03（f00b7b64）和 cron_33（ed297920）是否 enabled。若两者均 disabled（用户有意关闭）且当天识别为特殊事件日，必须在报告末尾 ⚠️ 单独输出：”盘中cron已关闭，特殊事件监控需人工执行。建议在以下时间窗口手动触发复核：[列出事件官方时间前后30分钟]。”此警告不可合并入其他段落，必须独立可见。
- 结构化JSONL的 special_event_monitoring 必须包含 intraday_cron_disabled 字段（true/false）；若为 true 且 active=true，failure_flags 必须包含 “intraday_cron_disabled_on_special_event_day”。
- 盘后任务必须检查当天是否同时满足：特殊事件日 + 盘中cron disabled。若是，在 EVAL_CASES.md 写入 intraday_disabled_on_special_event_day 案例（去重，同日只写一条）。

新增”特殊事件监控”硬性要求：
- 每次盘前/盘中必须按 /home/openclaw/.openclaw/workspace-us-market/AGENTS.md 的 SPECIAL EVENT MONITORING 执行”特殊事件监控”。若当天有大型公司财报/电话会、FOMC/CPI/非农、国债拍卖、重大SEC/IR披露、监管裁决或确认原因的盘前异常波动，必须把该日标记为特殊事件日。
- 盘前任务若识别出特殊事件日，必须输出”特殊事件监控计划”：watched tickers、事件类型、官方时间、监控开始/结束、关联ETF/持仓、分钟级指标、30分钟复核时间、买入/卖出草稿触发条件、失效条件、最大金额或约股数。
- 若Cron工具允许，为当天创建少量只读一次性事件提醒Cron（deleteAfterRun=true）；若Cron受限、时间已过或创建失败，必须在正文、failure_flags和special_event_monitoring.minute_monitor_status中写明原因，并要求用户盘中手动触发复核。不得把复核责任交给已关闭的cron_03/cron_33。
- 每个一次性特殊事件提醒在给用户输出前，必须先运行或委托本地运行：
  `python3 scripts/special_event_minute_collect.py --date YYYY-MM-DD --event-window "HH:MM ET reason" --tickers "SPY,QQQ,VOO,QQQM,SMH,XLF,KRE,..."`
  并确认写入 `reports/special-event-monitoring/YYYY-MM-DD.jsonl`。若提醒已经过期或采集失败，必须用
  `--allow-outside-window` 写入 documented skip/failure artifact；不得只发Telegram文字而不留本地artifact。
- 一次性事件提醒必须优先读取当天最新结构化JSONL或盘前报告中的special_event_monitoring计划；若仍有效，先复核这些ticker，再扫描普通候选。复核必须比较事件前后价格、成交量、VWAP/开盘区间、同业/ETF相对强弱、VIX、QQQ/SPY/SMH或相关行业ETF，以及最新IR/SEC/可靠新闻。
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
