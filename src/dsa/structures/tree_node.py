from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def build_tree(values: Iterable[Optional[int]]) -> Optional[TreeNode]:
    """
    根据层序数组（None 表示空）构造二叉树。
    例如：[1, 2, 3, None, 4]
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
    # 去掉末尾多余的 None
    while result and result[-1] is None:
        result.pop()
    return result


__all__ = ["TreeNode", "build_tree", "tree_to_list"]

