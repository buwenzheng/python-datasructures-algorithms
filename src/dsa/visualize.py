"""算法可视化工具。

提供以下可视化函数，帮助理解算法执行过程：

- :func:`show_linked_list` — 链表可视化（支持高亮节点）
- :func:`show_tree` — 二叉树可视化
- :func:`show_array` — 数组可视化（支持指针标记）
- :func:`show_dp` — DP 表格可视化
- :func:`show_window` — 滑动窗口可视化

使用方式：在算法代码的关键步骤调用这些函数，即可看到当前状态。
配合 labuladong 网站的可视化面板对照参考效果更佳。
"""

from __future__ import annotations

from typing import Any

from rich.console import Console

from dsa.list_node import ListNode
from dsa.tree_node import TreeNode

_console = Console(legacy_windows=False)


def show_linked_list(
    head: ListNode | None,
    highlights: list[ListNode | None] | None = None,
    label: str | None = None,
) -> None:
    """可视化链表，高亮指定节点。

    参数:
        head: 链表头节点
        highlights: 需要高亮的节点列表（按对象身份匹配）
        label: 标题文字

    示例::

        slow = fast = head
        show_linked_list(head, highlights=[slow, fast], label="初始: slow=fast=head")

        slow = slow.next
        fast = fast.next.next
        show_linked_list(head, highlights=[slow, fast], label="移动后")
    """
    if label:
        _console.print(f"[bold cyan]{label}[/]")

    if head is None:
        _console.print("[dim]None[/]")
        _console.print()
        return

    highlight_ids: set[int] = set()
    if highlights:
        for n in highlights:
            if n is not None:
                highlight_ids.add(id(n))

    parts: list[str] = []
    seen: set[int] = set()
    node: ListNode | None = head
    while node is not None:
        if id(node) in seen:
            parts.append(f"[dim][回到 {node.val}][/]")
            break
        seen.add(id(node))
        if id(node) in highlight_ids:
            parts.append(f"[bold yellow on blue] {node.val} [/]")
        else:
            parts.append(str(node.val))
        node = node.next
    else:
        parts.append("[dim]None[/]")

    _console.print(" -> ".join(parts))
    _console.print()


def show_tree(
    root: TreeNode | None,
    label: str | None = None,
) -> None:
    """可视化二叉树。

    参数:
        root: 树的根节点
        label: 标题文字

    示例::

        root = build_tree([4, 2, 7, 1, 3, 6, 9])
        show_tree(root, label="翻转前")

        root = invert_tree(root)
        show_tree(root, label="翻转后")
    """
    if label:
        _console.print(f"[bold cyan]{label}[/]")

    if root is None:
        _console.print("[dim]None[/]")
        _console.print()
        return

    _console.print(str(root))
    _console.print()


def show_array(
    arr: list[Any],
    pointers: dict[int, str] | None = None,
    label: str | None = None,
) -> None:
    """可视化数组，标记指针位置。

    参数:
        arr: 数组
        pointers: 指针位置 ``{index: 名称}``，如 ``{0: "left", 3: "right"}``
        label: 标题文字

    示例::

        left, right = 0, 3
        show_array([1, 3, 5, 7, 9], {left: "L", right: "R"}, label="双指针")

    输出示例::

        双指针
         1    3    5    7    9
         ↑              ↑
         L              R
    """
    if label:
        _console.print(f"[bold cyan]{label}[/]")

    if not arr:
        _console.print("[dim][][/]")
        _console.print()
        return

    str_vals = [str(v) for v in arr]
    cell_w = max(len(s) for s in str_vals) + 3

    # 值行
    value_line = "".join(s.center(cell_w) for s in str_vals)
    _console.print(value_line)

    # 指针行
    if pointers:
        ptr_line = list(" " * len(value_line))
        name_line = list(" " * len(value_line))

        for idx, name in pointers.items():
            if 0 <= idx < len(arr):
                center = idx * cell_w + cell_w // 2
                if center < len(ptr_line):
                    ptr_line[center] = "↑"
                start = center - len(name) // 2
                for j, c in enumerate(name):
                    pos = start + j
                    if 0 <= pos < len(name_line):
                        name_line[pos] = c

        _console.print("".join(ptr_line).rstrip())
        _console.print("".join(name_line).rstrip())

    _console.print()


def show_dp(
    dp: list[list[Any]],
    highlight: tuple[int, int] | None = None,
    label: str | None = None,
) -> None:
    """可视化 DP 表格，高亮当前计算的格子。

    参数:
        dp: 二维数组
        highlight: ``(row, col)`` 高亮位置
        label: 标题文字

    示例::

        dp = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                dp[i][j] = compute(i, j)
                show_dp(dp, highlight=(i, j), label=f"dp[{i}][{j}] = {dp[i][j]}")

    输出示例::

        dp[1][1] = 1
             j:  0   1   2
          ┌─────────────┐
        0 │  0   0   0  │
        1 │  0  [1]  1  │ ←
        2 │  0   1   2  │
          └─────────────┘
    """
    if label:
        _console.print(f"[bold cyan]{label}[/]")

    if not dp or not dp[0]:
        _console.print("[dim]空表格[/]")
        _console.print()
        return

    rows = len(dp)
    cols = len(dp[0])

    # 格式化值，None 显示为 ·
    str_dp = [
        [str(dp[i][j]) if dp[i][j] is not None else "·" for j in range(cols)] for i in range(rows)
    ]

    # 计算每列宽度
    col_widths = []
    for j in range(cols):
        w = max(len(str_dp[i][j]) for i in range(rows))
        col_widths.append(w + 2)

    # 行号宽度
    row_label_w = max(len(str(i)) for i in range(rows)) + 2

    # 列头
    header = " " * row_label_w + "[dim]j:[/]"
    for j in range(cols):
        header += str(j).center(col_widths[j])
    _console.print(header)

    # 上边框
    top = " " * (row_label_w - 1) + "┌"
    for w in col_widths:
        top += "─" * w
    top += "┐"
    _console.print(top)

    # 数据行
    for i in range(rows):
        row_prefix = str(i).rjust(row_label_w - 1) + "│"
        row_str = row_prefix
        for j in range(cols):
            val = str_dp[i][j]
            pad_total = col_widths[j] - len(val)
            left_pad = pad_total // 2
            right_pad = pad_total - left_pad
            if highlight and highlight == (i, j):
                row_str += " " * left_pad + f"[bold yellow][{val}][/]" + " " * right_pad
            else:
                row_str += " " * left_pad + val + " " * right_pad
        row_str += "│"
        if highlight and highlight[0] == i:
            row_str += " [dim]←[/]"
        _console.print(row_str)

    # 下边框
    bottom = " " * (row_label_w - 1) + "└"
    for w in col_widths:
        bottom += "─" * w
    bottom += "┘"
    _console.print(bottom)

    _console.print()


def show_window(
    s: str | list[Any],
    left: int,
    right: int,
    label: str | None = None,
) -> None:
    """可视化滑动窗口，窗口范围为 ``[left, right)``。

    参数:
        s: 字符串或列表
        left: 窗口左边界（含）
        right: 窗口右边界（不含）
        label: 标题文字

    示例::

        left, right = 0, 0
        while right < len(s):
            right += 1
            show_window(s, left, right, label=f"窗口 [{left}, {right})")
            # ... 收缩窗口
            show_window(s, left, right, label=f"收缩后 [{left}, {right})")

    输出示例::

        窗口 [1, 5)
         a   b   c   a   b   c   b   b
             ↑           ↑
            left       right
         window: bcab
    """
    if label:
        _console.print(f"[bold cyan]{label}[/]")

    if isinstance(s, str):
        chars = list(s)
    else:
        chars = [str(c) for c in s]

    n = len(chars)
    if n == 0:
        _console.print("[dim]空[/]")
        _console.print()
        return

    cell_w = 4
    value_line = "".join(c.center(cell_w) for c in chars)
    _console.print(value_line)

    # 指针行
    ptr_line = list(" " * len(value_line))
    name_line = list(" " * len(value_line))

    if 0 <= left < n:
        pos = left * cell_w + cell_w // 2
        if pos < len(ptr_line):
            ptr_line[pos] = "↑"
        name = "left"
        start = pos - len(name) // 2
        for j, c in enumerate(name):
            p = start + j
            if 0 <= p < len(name_line):
                name_line[p] = c

    # right 指向窗口右边界（不含），即下一个要加入的位置
    right_display = right if right < n else n - 1
    if right_display >= 0 and right_display != left:
        pos = right_display * cell_w + cell_w // 2
        if pos < len(ptr_line):
            ptr_line[pos] = "↑"
        name = "right"
        start = pos - len(name) // 2
        for j, c in enumerate(name):
            p = start + j
            if 0 <= p < len(name_line):
                name_line[p] = c
    elif right_display == left:
        # left 和 right 重合
        pos = left * cell_w + cell_w // 2
        if pos + 2 < len(name_line):
            name_line[pos] = "L"
            name_line[pos + 1] = "/"
            name_line[pos + 2] = "R"

    _console.print("".join(ptr_line).rstrip())
    _console.print("".join(name_line).rstrip())

    # 窗口内容
    if isinstance(s, str):
        window_content = s[left:right]
        _console.print(f'[dim]window:[/] "{window_content}"')
    else:
        window_content = s[left:right]
        _console.print(f"[dim]window:[/] {window_content}")

    _console.print()


__all__ = [
    "show_linked_list",
    "show_tree",
    "show_array",
    "show_dp",
    "show_window",
]
