"""一键验证题解正确性。

在题解文件的 ``__main__`` 区域调用 :func:`verify` 即可快速验证，
无需手动写 assert 或 pytest。

示例::

    from dsa import verify

    def two_sum(nums: list[int], target: int) -> list[int]:
        ...

    if __name__ == "__main__":
        verify(two_sum, [
            # (输入参数, 期望输出)  —— 单参数直接写值，多参数用 tuple
            (([2, 7, 11, 15], 9), [0, 1]),
            (([3, 2, 4], 6), [1, 2]),
            (([3, 3], 6), [0, 1], "重复元素"),  # 第三项可选，作为描述
        ])

输出::

    ✅ Case 1
    ✅ Case 2: 重复元素

    3/3 passed 🎉
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from rich.console import Console

_console = Console(legacy_windows=False)


def verify(
    func: Callable[..., Any],
    cases: list[tuple],
) -> None:
    """快速验证题解正确性，打印彩色 ✅/❌ 结果。

    参数:
        func: 你的解法函数
        cases: 测试用例列表，每个元素格式为:

            - ``(args, expected)`` —— 基本格式
            - ``(args, expected, description)`` —— 带描述

            ``args`` 可以是:

            - 单个值 —— 自动包装为单参数调用 ``func(args)``
            - tuple —— 解包为多参数调用 ``func(*args)``

    示例::

        # 单参数
        verify(reverse_string, [
            ("hello", "olleh"),
            ("world", "dlrow"),
        ])

        # 多参数
        verify(two_sum, [
            (([2, 7, 11, 15], 9), [0, 1]),
            (([3, 2, 4], 6), [1, 2]),
        ])

        # 带描述
        verify(two_sum, [
            (([2, 7, 11, 15], 9), [0, 1], "基本用例"),
            (([3, 2, 4], 6), [1, 2], "中间匹配"),
        ])
    """
    passed = 0
    total = len(cases)

    _console.print()

    for i, case in enumerate(cases):
        # 解析用例
        if len(case) == 2:
            args, expected = case
            desc = ""
        elif len(case) == 3:
            args, expected, desc = case
        else:
            _console.print(f"  [red]⚠️  Case {i + 1}: 格式错误，跳过[/]")
            continue

        # 统一 args 为 tuple
        if not isinstance(args, tuple):
            args = (args,)

        # 运行
        try:
            actual = func(*args)
        except Exception as e:
            label = f": {desc}" if desc else ""
            _console.print(f"  [red]💥 Case {i + 1}{label}[/]")
            _console.print(f"     [dim]异常: {e!r}[/]")
            continue

        # 比较（自动处理 ListNode / TreeNode）
        if _deep_equal(actual, expected):
            label = f": {desc}" if desc else ""
            _console.print(f"  [green]✅ Case {i + 1}{label}[/]")
            passed += 1
        else:
            label = f": {desc}" if desc else ""
            _console.print(f"  [red]❌ Case {i + 1}{label}[/]")
            _console.print(f"     [dim]期望: {_format_value(expected)}[/]")
            _console.print(f"     [dim]实际: {_format_value(actual)}[/]")

    # 汇总
    _console.print()
    if passed == total:
        _console.print(f"[bold green]{passed}/{total} passed 🎉[/]")
    else:
        _console.print(f"[bold yellow]{passed}/{total} passed[/]")

    _console.print()


def _deep_equal(a: Any, b: Any) -> bool:
    """深度比较，自动处理 ListNode / TreeNode。

    - 如果两边都是 ListNode，按链表值序列比较
    - 如果两边都是 TreeNode，按树结构和值比较
    - 否则用 ==
    """
    # 延迟导入避免循环依赖
    from dsa.list_node import ListNode
    from dsa.tree_node import TreeNode

    if isinstance(a, ListNode) and isinstance(b, ListNode):
        return a.to_list() == b.to_list()
    if isinstance(a, TreeNode) and isinstance(b, TreeNode):
        return a == b
    # 一边是 ListNode 另一边是 list
    if isinstance(a, ListNode) and isinstance(b, list):
        return a.to_list() == b
    if isinstance(a, list) and isinstance(b, ListNode):
        return a == b.to_list()
    # 一边是 TreeNode 另一边是 list
    if isinstance(a, TreeNode) and isinstance(b, list):
        return a.to_list() == b
    if isinstance(a, list) and isinstance(b, TreeNode):
        return a == b.to_list()
    # 默认
    return a == b


def _format_value(val: Any) -> str:
    """格式化值用于显示。"""
    from dsa.list_node import ListNode
    from dsa.tree_node import TreeNode

    if isinstance(val, ListNode):
        return f"ListNode({val.to_list()})"
    if isinstance(val, TreeNode):
        return f"TreeNode({val.to_list()})"
    return repr(val)


__all__ = ["verify"]
