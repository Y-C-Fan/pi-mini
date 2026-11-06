# SSE fixtures 说明与抓取方法

一句话：`sse/` 下两个文件是从真实 OpenAI 兼容网关抓下来的原始 `text/event-stream` 响应，未经改写，供 P0 的 SSE 解析测试回放。
什么时候读：写 `ai/client.py` 之前读一遍；要重新抓 fixture 时按第 2 节的命令照做。
层级：三级，上级入口 `docs/002-实现方案-每个模块的接口数据结构和验收点.md`（§4.1）。

## 1 文件清单

`sse/text-deltas.raw.sse`
- 内容：纯文本回复流。共 72 个带 `choices[0].delta.content` 的帧，每帧 1–3 个字符。
- 尾帧：`finish_reason: "stop"`，随后是一帧只带 `usage` 的响应，最后 `data: [DONE]`。
- 验证点：增量文本要按到达顺序拼接，不能按帧边界猜句子。

`sse/tool-call-stream.raw.sse`
- 内容：一次工具调用的流。无文本帧。
- 一个 `tool_calls` 条目，`index: 0`，`id: call_...`，`function.name` 只在部分片里出现。
- `function.arguments` 被拆成 10 片，拼接后是 `{"limit":20,"path":"README.md"}`。
- 尾帧：`finish_reason: "tool_calls"`，加一帧 `usage`，最后 `data: [DONE]`。
- 验证点：按 `index` 归并分片；`name`/`id` 只取首次出现；参数拼完才 `json.loads`。

原始需求的写法是「三段文本 + 一个两片 tool_call」。真实服务端的分片粒度由网关决定，抓到的是 72 片文本和 10 片参数，比要求更严。这里保留真实数据，不为了凑数字去改写帧，测试断言以文件实际帧数为准。

## 2 抓法（可复现）

网关：本机 magpie，`http://127.0.0.1:3425/v1`，OpenAI 兼容。模型 `glm-5.3-flash`。
抓取时间：2026-11-07。请求体先写成 UTF-8 文件，再用 `--data-binary` 发，避免 shell 编码把非 ASCII 打乱。

文本流请求体：
```json
{"model":"glm-5.3-flash","stream":true,"max_tokens":120,"messages":[{"role":"user","content":"Explain what an agent harness is in three short sentences. Plain text only, no lists, no headings."}]}
```

工具流请求体：
```json
{"model":"glm-5.3-flash","stream":true,"max_tokens":120,"messages":[{"role":"user","content":"Call the read tool to read README.md, limit 20 lines. Call the tool only, do not explain."}],"tools":[{"type":"function","function":{"name":"read","description":"Read a text file from disk","parameters":{"type":"object","properties":{"path":{"type":"string","description":"file path"},"offset":{"type":"number","description":"1-based start line"},"limit":{"type":"number","description":"max lines"}},"required":["path"]}}}],"tool_choice":"auto"}
```

命令（把 `<payload>.json` 换成上面的请求体文件）：
```bash
curl -N -s http://127.0.0.1:3425/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <key>' \
  --data-binary @<payload>.json \
  -o tests/fixtures/sse/<name>.raw.sse
```

`-N` 关掉缓冲，否则 curl 会把整段响应一次性写盘，分片边界就丢了。

## 3 格式

标准 SSE：每条 `data: <json>`，帧之间空行分隔，末尾 `data: [DONE]`。
JSON 形状照 OpenAI Chat Completions 流式响应。回放时按行读、跳过空行与非 `data:` 行，即可得到帧序列。