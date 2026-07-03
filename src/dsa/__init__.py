"""dsa —— 数据结构与算法学习工具包。

提供常用数据结构的构造器、可视化打印、题解验证和算法可视化。

使用方式::

    from dsa import ListNode, build_linked_list, build_cycle_list
    from dsa import TreeNode, build_tree, tree_to_list
    from dsa import verify
    from dsa import show_linked_list, show_tree, show_array, show_dp, show_window
"""

import sys as _sys

# Windows 终端默认使用 GBK 编码，无法输出 emoji 等字符
# 尝试切换到 UTF-8，失败则忽略（不影响核心功能）
if _sys.platform == "win32":
    try:
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

from dsa.list_node import ListNode, build_cycle_list, build_linked_list
from dsa.tree_node import TreeNode, build_tree, tree_to_list
from dsa.verify import verify
from dsa.visualize import (
    show_array,
    show_dp,
    show_linked_list,
    show_tree,
    show_window,
)

__all__ = [
    # 链表
    "ListNode",
    "build_linked_list",
    "build_cycle_list",
    # 二叉树
    "TreeNode",
    "build_tree",
    "tree_to_list",
    # 验证
    "verify",
    # 可视化
    "show_linked_list",
    "show_tree",
    "show_array",
    "show_dp",
    "show_window",
]
