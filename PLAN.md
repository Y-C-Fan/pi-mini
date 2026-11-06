# pi-mini 学习计划

一句话：六个阶段，每阶段一个能跑的产物，按 Pi 的真实骨架分层实现。
什么时候读：每次开工前读当前阶段段落；阶段验收通过再进下一段。
层级：002，上级入口 README.md。

## 基准事实（先读，别猜）

上游 Pi v1.5.0（github.com/earendil-works/pi），架构总纲 `docs/how-pi-works.md`。
它的 agent loop 是这样一句话：消息进入 active branch → 用 system prompt + 分支历史 + 工具定义组请求 → provider 流式返回 text 与 tool_calls → 记录响应 → 执行每个 tool call → 记录结果 = 一个 turn → 还有待办就再来一个 turn。
会话是树，不是数组。JSONL 每行一个 entry，带 id 和 parent。压缩是往树里插一条 summary entry，旧 entry 不删。

## P0 最小可跑（约半天）

产物：`uv run pi-mini -p "hi"` 能流式打印模型回复。
做：uv 项目骨架；config 三级来源（CLI 参数 > .env > ~/.pi-mini/config.json）；OpenAI 兼容 /chat/completions 的 SSE 客户端；delta 文本与 tool_calls 分片累加器。
学到：provider 抽象放在哪一层；流式解析的增量拼接为什么必须按 index 累加。
验收：逐字输出；中途断流不抛未捕获异常。

## P1 agent loop + 工具（1~2 天）

产物：`uv run pi-mini -p "读 README 并总结"` 自主调工具完成任务。
做：消息模型；tool registry（从函数签名生成 JSON schema）；read_file、write_file、edit_file（str replace）、bash；turn 循环；max_turns 上限；工具异常转成 tool 结果回喂模型。
学到：harness 本质是 while + dispatch；错误信息本身是上下文的一部分；工具结果必须截断。
验收：串行多轮工具调用跑通；单个工具失败后模型能自我纠正；无限循环被 max_turns 拦住。

## P2 session 树（约 1 天）

产物：`--continue`、`--resume <id>`、`--list`。
做：JSONL 追加写入；entry 类型（message / tool_result / model_change / compaction）；active leaf 指针；从 leaf 沿 parent 回溯重建上下文；fork 与 clone。
学到：为什么用树而不是数组——分支、回退、压缩全靠 parent 指针；压缩不破坏历史。
验收：同一文件里两条分支，切换后模型看到的上下文不同；`--list` 显示树。

## P3 上下文工程 + 压缩（1~2 天）

产物：长任务超过预算时自动摘要并继续。
做：system prompt 组装（base 指令 + AGENTS.md 发现 + 工具说明 + skill 摘要）；token 估算；compaction 插入 summary entry 并在后续请求替换旧消息；保留最近 N 轮。
学到：模型看到什么完全由 harness 决定；压缩是「插入」而非「删除」。
验收：20 轮以上长任务不断线；用 `--debug-context` 打印每次请求的消息条数与 token。

## P4 交互模式（1~2 天）

产物：REPL，流式渲染、Ctrl-C 中断、消息排队。
做：prompt_toolkit 输入；流式渲染；运行状态机 idle/running/aborting；steering 消息插在 assistant turn 之后；follow-up 消息等任务结束再进；中断后把未发消息还给编辑器。
学到：agent 的状态机与 UI 事件流怎么解耦。
验收：跑到一半 Ctrl-C，历史完整、能继续输入；运行中打字不被丢弃。

## P5 扩展面（选做，2 天+）

产物：skills 按需加载 + 斜杠命令 + JSON/RPC 模式。
做：扫描 skills 目录，只把 name 和 description 放进 system prompt，模型要求时才读 SKILL.md 全文；prompt template 展开；stdin/stdout JSONL RPC 驱动一次完整 run。
学到：为什么 Pi 把 sub-agent 和 plan mode 推给扩展——核心保持小。
验收：脚本通过 RPC 跑完一次带工具的 run；skill 全文只在被需要时进上下文。

## 不做

TUI 差分渲染、多家 provider、扩展沙箱、sub-agent、plan mode。Pi 自己也不带后两个。

## 每阶段固定动作

1. 先读 Pi 对应实现或文档，写三条对照笔记。
2. 自己实现，不复制源码；卡住再看。
3. 跑验收用例，通过后勾 README 进度。
4. 写 `notes/` 一条：Pi 怎么做 / 我怎么做 / 差在哪。
