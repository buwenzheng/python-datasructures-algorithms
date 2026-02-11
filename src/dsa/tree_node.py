"""二叉树节点与构造工具。

提供 TreeNode 数据结构、二叉树构造器、可视化打印。
print() 即可看到直观的树形结构。
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class TreeNode:
    """二叉树节点。

    属性:
        val: 节点值
        left: 左子节点
        right: 右子节点
    """

    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None

    def __str__(self) -> str:
        """可视化打印二叉树。

        示例输出:
            1
           / \\
          2   3
           \\
            4
        """
        lines = _build_tree_lines(self)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()


def _build_tree_lines(node: Optional[TreeNode]) -> list[str]:
    """递归生成树的可视化行。"""
    if node is None:
        return []

    val_str = str(node.val)

    if node.left is None and node.right is None:
        return [val_str]

    left_lines = _build_tree_lines(node.left)
    right_lines = _build_tree_lines(node.right)

    if not left_lines:
        connector = " \\"
        shifted = ["  " + line for line in right_lines]
        return [val_str, connector] + shifted

    if not right_lines:
        connector = " /"
        shifted = ["  " + line for line in left_lines]
        return [val_str, connector] + shifted

    left_width = max(len(line) for line in left_lines)
    gap = 3

    padded_left = [line.ljust(left_width) for line in left_lines]

    connector = " " * (left_width - 1) + "/ \\"
    merged: list[str] = []
    max_len = max(len(padded_left), len(right_lines))
    for i in range(max_len):
        l_part = padded_left[i] if i < len(padded_left) else " " * left_width
        r_part = right_lines[i] if i < len(right_lines) else ""
        merged.append(l_part + " " * gap + r_part)

    root_pos = left_width - 1
    root_line = " " * root_pos + val_str
    return [root_line, connector] + merged


def build_tree(values: Iterable[Optional[int]]) -> Optional[TreeNode]:
    """根据层序数组构造二叉树。

    None 表示空节点，与 LeetCode 输入格式一致。

    示例:
        >>> root = build_tree([1, 2, 3, None, 4])
        >>> print(root)
          1
          / \\
        2     3
         \\
          4
    """
    values_list: List[Optional[int]] = list(values)
    if not values_list:
        return None
    iter_vals = iter(values_list)
    root_val = next(iter_vals)
    if root_val is None:
        return None
    root = TreeNode(root_val)
    queue: deque[TreeNode] = deque([root])
    for left_val, right_val in zip(iter_vals, iter_vals):
        node = queue.popleft()
        if left_val is not None:
            node.left = TreeNode(left_val)
            queue.append(node.left)
        if right_val is not None:
            node.right = TreeNode(right_val)
            queue.append(node.right)
    return root


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """将二叉树序列化为层序数组。"""
    if root is None:
        return []
    result: List[Optional[int]] = []
    queue: deque[Optional[TreeNode]] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
            continue
        result.append(node.val)
        if node.left is not None or node.right is not None:
            queue.append(node.left)
            queue.append(node.right)
    while result and result[-1] is None:
        result.pop()
    return result


__all__ = ["TreeNode", "build_tree", "tree_to_list"]

