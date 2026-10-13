OPENCLAW_CRON_LOCAL_WORKSPACE_DELEGATION_HARD_REQUIREMENT（置顶，必须执行）：
- 若本任务需要读取/写入 /home/openclaw/.openclaw/workspace-us-market、本地 Markdown/JSONL/研究文件，或运行 Webull 只读同步脚本，而当前隔离 cron 会话没有本地 shell/exec/文件写入能力，必须立即使用 sessions_spawn(runtime="subagent", mode="run", cwd="/home/openclaw/.openclaw/workspace-us-market", agentId="us-market") 委托本地工作区子任务完成对应命令、归档和验证；等待并复核子任务结果后，才允许把归档/更新写成成功。
- 委托子任务只允许执行本任务要求的只读同步、文件读取、文件追加/归档、schema/闭环验证；不得登录券商网页或App，不得下单、改单、撤单，不得输出token/凭据。
- 若 delivery.mode=announce 或本任务本应用户可见，最终用户正文必须主动调用 message(action="send", message=完整用户可见正文) 投递到 Telegram；不得只依赖 cron final/announce 自动投递。正文末尾必须写明触发成功/投递成功/messageId/归档或更新路径/下游读取路径。
- 若 delivery.mode=none 或本任务明确为静默研究维护任务，不要发 Telegram；但必须完成文件更新或写明跳过原因，并在普通 final 中给出可被 run history 捕捉的文件摘要。
- 如果委托、投递、归档或验证失败，必须把该环节标为失败/未完成并说明原因；不得把 status=ok 当成业务闭环成功。

OPENCLAW_CRON_SILENT_UPDATE_HARD_REQUIREMENT（置顶，必须执行）：
- 本任务是静默研究/维护任务：不要向 Telegram 投递；必须完成研究文件更新或明确记录跳过原因。
- 最终普通 final 必须给出文件更新摘要，供 cron run history 捕捉；不得空跑。
- 若读取上游报告、失败队列或研究索引，必须在输出中写明读取到了哪些路径。
- 不得交易、下单、改单、撤单。

执行《美股学术与市场研究》任务。工作区为 /home/openclaw/.openclaw/workspace-us-market。采用 PLAN -> EXECUTE -> VERIFY -> EVALUATE -> REPORT。读取 research/RESEARCH_PROGRAM.md、research/KNOWLEDGE_GOVERNANCE.md、research/knowledge/、research/RESEARCH_QUEUE.md、research/RESEARCH_INDEX.md、research/SYSTEM_STATE.md。每次最多深度研究2篇论文，优先 Tier 1/Tier 2 来源，必须搜索反证、复现失败、交易成本、样本外结果。更新 research/daily/YYYY-MM-DD.md、research/knowledge/cards/、research/knowledge/domains/、research/RESEARCH_INDEX.md、research/RESEARCH_QUEUE.md；必要时更新 research/contradictions/。不要直接修改 AGENTS.md，不要改变9:00 ET盘前任务，不要保存Token或凭据。投递静默；最终只记录文件结果。

盘后失败入口读取要求：研究选题前必须读取 `research/queue/postmarket-failures.md` 和最近 `reports/postmarket-reviews/`。若其中有高影响或重复失败，优先把它转化为研究问题，再选择常规研究队列主题。研究输出必须标注“可用于的下游环节”：盘前、盘中、盘后审计、Webull费用复核、或月度prompt评测。

结构化日志研究输入要求：研究A必须读取 `research/STRUCTURED_LOG_SCHEMA.md`、`reports/structured/`、`research/BOOK_LEARNING_LATEST.md`、`research/KNOWLEDGE_GOVERNANCE.md`、`research/knowledge/cards/` 和 `research/rules/RULE_PERFORMANCE.md`。当 postmarket-failures、BOOK_LEARNING_LATEST 或 structured logs 显示重复失败/候选知识时，优先研究可降低该失败的机制或证据。研究任务不得交易、不得登录券商、不得读取或输出token/凭据。
