"""SSE fixture 回放测试（占位，未实现）。

fixture 位置：tests/fixtures/sse/，抓取方法与文件内容见 tests/fixtures/README.md。

格式：原始 SSE，一行一条 `data: <json>`，帧之间空行，末尾 `data: [DONE]`。
每一帧是 OpenAI Chat Completions 的流式响应片段，关键字段：
- `choices[0].delta.content` —— 文本增量
- `choices[0].delta.tool_calls[i]` —— 工具调用分片，带 `index`；`function.name` 与 `function.arguments` 都会分片
- `choices[0].finish_reason` —— `stop` 或 `tool_calls`
- 末尾可能有一帧只带 `usage`

这些用例在 P0 实现前全部 skip。断言口径写在每个用例的 docstring 里。
"""

from __future__ import annotations

import pathlib

import pytest

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "sse"
TEXT_STREAM = FIXTURES / "text-deltas.raw.sse"
TOOL_STREAM = FIXTURES / "tool-call-stream.raw.sse"


def _fixture_exists(path: pathlib.Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


@pytest.mark.skip(reason="P0 未实现：等 ai/client.py 落地后打开")
def test_text_stream_yields_text_deltas_then_stop() -> None:
    """回放 text-deltas.raw.sse。

    断言：72 个 text_delta 事件，拼接后与文件里 content 的顺序拼接一致；
    出现 1 次 usage；最后 done.reason == "stop"。
    文件不存在时同样失败，防止 fixture 被误删。
    """
    assert _fixture_exists(TEXT_STREAM), f"fixture 缺失: {TEXT_STREAM}"


@pytest.mark.skip(reason="P0 未实现：等 ai/client.py 落地后打开")
def test_tool_call_fragments_merge_by_index() -> None:
    """回放 tool-call-stream.raw.sse。

    断言：只产出 1 个 tool_call，id 与文件首片一致，name == "read"，
    arguments 拼接后 == {"limit": 20, "path": "README.md"}；
    分片顺序错乱时该用例必须失败（这是按 index 归并的唯一理由）。
    """
    assert _fixture_exists(TOOL_STREAM), f"fixture 缺失: {TOOL_STREAM}"


@pytest.mark.skip(reason="P0 未实现：等 ai/client.py 落地后打开")
def test_stream_survives_split_network_chunks() -> None:
    """把 fixture 按随机字节边界切块喂给解析器。

    断言：切块位置不影响结果——文本帧数与工具参数都与整段回放相同。
    这条覆盖「SSE 一行可能跨两个 recv」的坑。
    """
    assert _fixture_exists(TEXT_STREAM) and _fixture_exists(TOOL_STREAM)