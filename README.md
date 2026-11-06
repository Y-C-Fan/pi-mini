# pi-mini

用 Python 手写一个 mini 版 Pi，把 Agent Harness 的每个零件自己造一遍。

一句话：不是用 Pi，而是把 Pi 拆开重写，学到 harness 到底管什么。
什么时候读：动手前先看 PLAN.md 的阶段表；改代码前看对应阶段的「学到」一行。
层级：仓库根入口（000）。下一步读 PLAN.md（001 阶段计划），动笔前读 `docs/002-实现方案-每个模块的接口数据结构和验收点.md`（002 接口与验收）。

## 参考基准

本机已装 Pi v1.4.0，源码与文档在：
`D:\DevEnv\node_global\node_modules\@earendil-works\pi-coding-agent`
重点读 `docs/how-pi-works.md`（agent loop、context、session、interfaces 四段）。
不要凭印象设计，拿它的行为对照自己的实现。

Pi 的骨架只有五件事：
1. agent loop —— 请求、流式响应、执行工具、再请求。
2. context assembly —— 决定这次请求带哪些消息。
3. session —— JSONL 树，每行一个 entry，靠 parent 串成分支。
4. tools —— read/write/edit/bash 四个够用。
5. interfaces —— interactive / print / json / rpc，共用上面四件。

## 快速开始

```bash
cd D:\AgentWS\HermesWS\pi-mini
uv run pi-mini --version
uv run pi-mini --roadmap
```

## 目录

```
src/pi_mini/
  cli.py        命令行入口（当前只有 --version / --roadmap）
  config.py     配置读取（.env + .pi-mini/config.json）  [P0]
  ai/           provider 客户端与流式解析               [P0]
  agent/        agent loop、状态机、消息模型            [P1]
  tools/        工具注册表与四个内置工具                [P1]
  session/      JSONL 会话树、分支、压缩               [P2 P3]
  modes/        interactive / print / json / rpc       [P4 P5]
```

## 进度

- [ ] P0 最小可跑：流式对话
- [ ] P1 agent loop + 工具
- [ ] P2 session 树
- [ ] P3 上下文工程 + 压缩
- [ ] P4 交互模式
- [ ] P5 扩展面

## 笔记

踩坑写 `notes/`，按阶段编号。每阶段结束后补一条「Pi 怎么做 / 我怎么做 / 差在哪」。
