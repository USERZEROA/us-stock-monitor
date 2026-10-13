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

执行《周度知识蒸馏与反证审计》。工作区为 /home/openclaw/.openclaw/workspace-us-market。采用 PLAN -> EXECUTE -> VERIFY -> EVALUATE -> REPORT。读取过去7天 research/daily/、research/books/、research/BOOK_LEARNING_LATEST.md、research/KNOWLEDGE_GOVERNANCE.md、research/knowledge/cards/、research/knowledge/domains/、research/contradictions/、research/RESEARCH_INDEX.md、research/RESEARCH_PROGRAM.md。只把满足长期知识准入规则且有合格 knowledge card 的结论写入 MARKET_KNOWLEDGE.md；未通过、失效或有负面效果的规则写入 research/FAILED_IDEAS.md。不得修改 AGENTS.md，不得改变9:00 ET盘前任务，不得保存Token或凭据。最终输出不超过1800个中文字符的周度摘要，说明新增知识、读书候选、反证、失败想法和待办。

下游接线验证要求：周度总结末尾必须增加“下游接线验证”。用cron get/list或可用工具确认：09:00盘前和16:20盘后仍启用且prompt仍包含 `MARKET_KNOWLEDGE.md`、`BOOK_LEARNING_LATEST.md`、`KNOWLEDGE_GOVERNANCE.md` 和 `FAILED_IDEAS.md`；每日Claude开放书籍学习任务仍启用且只允许Claude；:03盘中和:33盘中任务应保持存在但 `enabled=false`，这是用户确认的低频模式，不能报警为“应启用”。若盘中任务被误启用、被删除，或盘前prompt缺少禁用后的一次性特殊事件提醒/替代监控要求，必须在Telegram总结中明确报警，不得只写研究摘要。

规则表现蒸馏要求：周度B必须读取 `research/rules/RULE_PERFORMANCE.md`、`reports/structured/` 和 `reports/postmarket-reviews/`。蒸馏时不仅判断研究证据，也要检查已批准规则是否在实盘审计中减少错误；不能因为单次成功就提高证据等级。任务不得交易、不得登录券商、不得读取或输出token/凭据。
