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

执行《美股闭环健康巡检》。这是只读巡检任务，不做市场预测，不交易，不下单，不改prompt，除非明确写入健康日志文件。工作区：/home/openclaw/.openclaw/workspace-us-market。

时间：每个美股工作日 17:05 ET。先确认当前美东日期和最近交易日。

巡检目标：检查整套美股系统是否“一环扣一环”：
1. 盘前归档：检查 /home/openclaw/.openclaw/workspace-us-market/reports/premarket-predictions/YYYY-MM-DD.md 是否存在且非空。
2. 盘中归档：检查 /home/openclaw/.openclaw/workspace-us-market/reports/intraday-predictions/YYYY-MM-DD.md 是否存在且包含 run_time_et/job_label/full_report；统计条数，列出缺失窗口。
3. 盘后归档：检查 /home/openclaw/.openclaw/workspace-us-market/reports/postmarket-reviews/YYYY-MM-DD.md 是否存在且非空；如果17:05时盘后任务仍未完成，说明“等待盘后任务完成”，不要误报为永久失败。
4. 账户/订单快照：检查 PORTFOLIO_STATE.md、WEBULL_ORDER_STATUS.md、webull_portfolio_snapshot.json、webull_order_status_snapshot.json 是否存在，并报告最新更新时间；不要输出凭据或token。
5. 长期知识接线：用可用的cron工具检查 09:00盘前、16:20盘后、17:05健康、研究A、周度B、月度C、每日Claude开放书籍学习任务 仍启用；:03盘中、:33盘中按用户2026-07-30要求应为关闭但未删除。检查相关prompt包含 MARKET_KNOWLEDGE.md、BOOK_LEARNING_LATEST.md、KNOWLEDGE_GOVERNANCE.md、FAILED_IDEAS.md、DATA_SOURCE_POLICY.md、webull_portfolio_sync.py、webull_order_status.py、预测正文、VIX分层。
6. 研究闭环：检查 research/queue/postmarket-failures.md、research/EVAL_CASES.md、research/RESEARCH_QUEUE.md、MARKET_KNOWLEDGE.md、research/BOOK_LEARNING_LATEST.md、research/KNOWLEDGE_GOVERNANCE.md、research/knowledge/cards/、research/knowledge/domains/、research/FAILED_IDEAS.md 是否存在且非空。
7. 输出“闭环状态”：绿色=全部通过；黄色=非关键缺失或等待盘后完成；红色=归档缺失、任务停用、prompt接线缺失、Webull快照长期缺失、或错误未沉淀。
8. 若黄色或红色，给出明确修复建议；不要自行修改cron或系统设置。
9. 把巡检结果追加到 /home/openclaw/.openclaw/workspace-us-market/reports/closed-loop-health/YYYY-MM-DD.md。末尾写健康日志归档状态。
10. Telegram输出控制在1200中文字符以内。

新增"冗余验证项"硬性要求（每日17:05必须执行）：
1. **订单批准链审计**：读取 webull_order_status.json，对当天每笔已成交订单检查 approval_audit 字段是否在当天盘后JSONL中存在；若缺失，状态至少黄色并列出缺失ticker。
2. **fee最终化追踪**：读取 webull_order_status.json，统计 fees=[] 的订单；若发生超过24小时仍未返回费用，标注 fee_status: unresolved_24h，并确认盘后JSONL的 fee_audit 字段已记录；若未记录，追加到 postmarket-failures.md。
3. **特殊事件+盘中禁用交叉检查**：若当天为特殊事件日且 cron_03/cron_33 disabled，检查盘前JSONL是否包含 intraday_cron_disabled=true 和警告提示；若缺失，状态至少黄色。
4. **approval-audit目录**：确认 reports/approval-audit/YYYY-MM-DD.jsonl 存在且非空；若当天有成交订单但文件缺失或为空，状态黄色。若只有 `gap`/`unverifiable_intraday_disabled`，写成“批准链已留痕但未核验”，不得写成完整通过。
5. **特殊事件artifact质量**：若 `reports/special-event-monitoring/YYYY-MM-DD.jsonl` 只有
   `documented_skip_outside_window`，不得把它写成真实盘中覆盖；状态最多只能从“无痕迹”改善为
   “documented failure/yellow”，并要求下一次盘前修复提醒命令。

独立验证脚本硬性要求：巡检时必须运行 `cd /home/openclaw/.openclaw/workspace-us-market && python3 scripts/market_closed_loop_validate.py --date YYYY-MM-DD --require-all-archives --write-health`，其中YYYY-MM-DD为最近应完成复盘的美东交易日。如果脚本返回红色或非零退出，仍要读取输出并向Telegram报告红/黄原因；不要因为脚本非零就停止解释。该脚本是文件/schema验证层，cron接线验证仍需用可用cron工具检查。

新增巡检项：止盈审计线与买后判断接线
- 用可用cron工具检查 09:00盘前、16:20盘后任务仍启用，:03盘中、:33盘中任务按预期关闭但未删除；上述任务prompt均应包含“止盈审计线”、“全卖线”、“买后判断”、“position_reviews”、“standing-profit-taking-lines”。
- 检查 `/home/openclaw/.openclaw/workspace-us-market/AGENTS.md`、`MARKET_KNOWLEDGE.md`、`research/STRUCTURED_LOG_SCHEMA.md`、`research/rules/RULE_PERFORMANCE.md` 是否包含止盈审计和买后判断规则。
- 若当天结构化日志存在但缺少 `position_reviews` 字段，状态至少为黄色；若当天有BUY成交但没有后续买后判断，状态为红色并给出修复建议。

新增巡检项：决策纪律接线
- 用可用cron工具检查 09:00盘前、16:20盘后任务仍启用，:03盘中、:33盘中任务按预期关闭但未删除；上述任务prompt均应包含“DECISION DISCIPLINE”、“决策纪律检查”、“该买未买/该卖未卖”或等价硬性审计要求。
- 检查 /home/openclaw/.openclaw/workspace-us-market/AGENTS.md 是否包含 DECISION DISCIPLINE。
- 若交易报告缺少明确买/卖/持有/回避/等待触发动作，或“仅观察”没有触发条件、失效条件、金额/股数和复核窗口，状态至少为黄色；若因此错过明确买卖或违反止盈/止损，状态为红色。

新增巡检项：最终操作总结接线
- 用可用cron工具检查 09:00盘前、16:20盘后任务仍启用，:03盘中、:33盘中任务按预期关闭但未删除；上述任务prompt均应包含“最终操作总结”和“final_action_summary”。
- 检查当天盘前/盘中/盘后Markdown报告是否以“最终操作总结：”作为用户可见正文最后行动句，明确写买入0/卖出0或具体买卖ticker、金额/股数、持有和回避。
- 检查结构化JSONL是否包含 final_action_summary 字段；若缺失，状态至少为黄色。

新增巡检项：KRE持仓风控/候选降级接线
- 检查盘前、盘中、盘后任务prompt是否包含“KRE持仓风控/候选降级”或等价要求。
- 只有Webull最新持仓显示KRE数量>0时，才检查报告是否单独审计KRE，并在KRE弱于XLF/SPY或跌破失效位时给出SELL KRE全仓草稿。
- 若KRE数量=0，检查报告是否把KRE降级为0股候选/默认回避；不得要求每轮作为重点持仓风控单独展开。
- 若报告在KRE无持仓时仍反复写待卖、止损或全仓SELL草稿，状态至少为黄色。

Cron接线CLI只读兜底：
- 如果在 isolated cron 运行中，可用 cron 工具只能列出/读取当前17:05任务，或返回“Cron tool is restricted to the current cron job”，不要直接判定cron接线黄色。
- 先用本机只读CLI兜底复核：`openclaw cron list --all`，以及 `openclaw cron get JOB_ID` 读取 09:00盘前、:03盘中、:33盘中、16:20盘后、17:05健康巡检任务。
- CLI兜底只允许 read/list/get/status/runs 类检查，禁止 edit/update/enable/disable/remove/run 等会修改或触发任务的操作。
- 若CLI兜底能确认09:00盘前、16:20盘后、17:05健康、研究A、周度B、月度C、每日Claude开放书籍学习任务 enabled，且确认:03盘中、:33盘中 expected_enabled=false/disabled但未删除；同时prompt包含 MARKET_KNOWLEDGE.md、BOOK_LEARNING_LATEST.md、FAILED_IDEAS.md、DATA_SOURCE_POLICY.md、webull_portfolio_sync.py、webull_order_status.py、止盈审计线、全卖线、买后判断、position_reviews、最终操作总结、final_action_summary、KRE持仓风控/候选降级，则cron接线视为通过。
- 只有当可用cron工具和CLI只读兜底都无法确认，或发现任务停用/marker缺失时，才把cron接线列为黄色或红色。

新增巡检项：结构化风险规则和BUY后复盘对账
- 在独立验证脚本之后，额外运行只读对账：`cd /home/openclaw/.openclaw/workspace-us-market && python3 scripts/post_buy_review_audit.py --date YYYY-MM-DD --lookback-days 7`。
- 在独立验证脚本之后，额外运行只读实际订单审计：`cd /home/openclaw/.openclaw/workspace-us-market && python3 scripts/actual_trade_watcher.py --date YYYY-MM-DD --write`。the user 经常自行在券商操作，券商出现FILLED但缺本地提交引用时，默认写为“用户手动/未链接成交，需复盘”，健康状态至少黄色但不因这一点单独判红；若是超20%权益BUY、明显脱离风控红线、或本地系统声称执行却缺审批链，健康状态必须红色。若只有CANCELLED/REJECTED订单，必须记录但不当作成交。
- 在独立验证脚本之后，额外运行费用最终化审计：`cd /home/openclaw/.openclaw/workspace-us-market && python3 scripts/fee_finalization_audit.py --date YYYY-MM-DD --write`。若24小时以上已成交卖单仍无broker fee，健康状态至少黄色并报告 unresolved_fee_count；不得把暂估费用写成最终券商费用。
- 在独立验证脚本之后，额外运行知识治理审计：`cd /home/openclaw/.openclaw/workspace-us-market && python3 scripts/book_learning_audit.py --json && python3 scripts/knowledge_audit.py --json`。若 knowledge_audit 返回 red 或非零，健康状态必须红色；若 yellow，健康状态至少黄色。
- 检查当天每条包含 position_reviews 的JSONL记录，其 risk_rules_applied 必须包含 standing-profit-taking-lines；若缺失，状态至少为黄色，若导致止盈/全卖审计不可追溯，状态为红色。
- 检查近期FILLED BUY成交后第一份可用结构化报告是否在 position_reviews 中复核该ticker；若未复核，状态为红色；若买单发生在所有报告之后，标记pending而非红色。
- 检查交易报告prompt是否包含“结构化JSONL风险规则硬性要求”、“standing-profit-taking-lines”和“standing-post-buy-review”；检查17:05健康巡检prompt和CLOSED_LOOP_MANIFEST.json是否包含“post_buy_review_audit.py”、“actual_trade_watcher.py”和“fee_finalization_audit.py”。

新增巡检项：盘中时间窗失败补档审计
- 仅当盘中 cron_03/cron_33 启用或该交易日启用过时，才按预期时间窗逐个核对：cron_33=09:33、10:33、11:33、12:33、13:33、14:33、15:33；cron_03=10:03、11:03、12:03、13:03、14:03、15:03，允许实际报告时间比调度时间晚最多10分钟。若任务按用户要求在该日开盘前已关闭，不得因缺少盘中窗口判红。
- 巡检脚本 `market_closed_loop_validate.py --require-all-archives` 已包含窗口级覆盖检查；必须读取其结果，不要只凭总条数判断。
- 如果 run history 显示某个窗口 error/not delivered，但当天 Markdown 和 JSONL 已有对应 `archive_status.status: "failed_backfilled_audit"` 或等价 documented failure，且 `final_action_summary` 明确说明原始报告失败、未投递、无订单执行、不是事后预测，则该窗口视为“已审计历史失败”，不再判红灯。
- 如果窗口既无成功报告，也无 `failed_backfilled_audit`/documented failure 补档，状态必须为红色，并建议复查失败会话、只做原始缓存补档，禁止事后编造预测。

Manifest路径硬性要求：
- CLOSED_LOOP_MANIFEST 的唯一有效路径是 `/home/openclaw/.openclaw/workspace-us-market/research/CLOSED_LOOP_MANIFEST.json`。
- 不要检查或要求 `/home/openclaw/.openclaw/workspace-us-market/CLOSED_LOOP_MANIFEST.json`；根目录没有该文件不算缺失。
- 验证 `post_buy_review_audit.py`、`failed_backfilled_audit`、结构化风险规则、最终操作总结、KRE风控等 manifest 标记时，必须读取 research/CLOSED_LOOP_MANIFEST.json。

8任务cron接线审计脚本硬性要求：
- 除手动读取cron外，必须运行只读脚本：`cd /home/openclaw/.openclaw/workspace-us-market && python3 scripts/cron_prompt_audit.py`。
- 该脚本读取 `research/CLOSED_LOOP_MANIFEST.json` 的全部 required_jobs，覆盖 09:00盘前、:33盘中、:03盘中、16:20盘后、17:05健康巡检、研究A、周度B、月度C、每日Claude读书任务；其中:33盘中、:03盘中当前预期为关闭但未删除。
- 如果 `cron_prompt_audit.py` 返回 red 或非零退出且输出状态为 red，健康状态必须红色；若输出状态为 yellow（例如每日Claude读书任务因外部模型限额被记录为非致命跳过），健康状态至少黄色但不得写成市场cron接线红灯；若 green，说明8个任务均 enabled/disabled符合预期、调度匹配、sessionTarget/agent可见、required markers完整，且真实cron `lastRunStatus=ok`、`consecutiveErrors=0`。
- Telegram摘要必须写明“8个cron任务接线审计：green/yellow/red”。
