"""二叉树节点与构造工具。

提供 TreeNode 数据结构、二叉树构造器、可视化打印。
print() 即可看到直观的树形结构。
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable


class TreeNode:
    """二叉树节点。

    属性:
        val: 节点值
        left: 左子节点
        right: 右子节点
    """

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __str__(self) -> str:
        """可视化打印二叉树。

        示例输出::

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

    def __eq__(self, other: object) -> bool:
        """按结构和值比较两棵二叉树是否相同。"""
        if not isinstance(other, TreeNode):
            return NotImplemented
        return _tree_equal(self, other)

    def to_list(self) -> list[int | None]:
        """将二叉树序列化为层序数组（与 LeetCode 格式一致）。"""
        return tree_to_list(self)

    def getVisualizationData(self) -> str:
        """返回 JSON 字符串，供 VSCode Debug Visualizer 扩展渲染。

        使用方式：
            1. 安装 Debug Visualizer 扩展（hediet.debug-visualizer）
            2. F5 调试时，打开 Debug Visualizer 视图
               （命令面板 → Debug Visualizer: New View）
            3. 在表达式输入框中输入：root.getVisualizationData()
            4. 单步调试时实时看到二叉树结构变化
        """
        import json

        def build(node: TreeNode | None) -> dict | None:
            if node is None:
                return None
            return {
                "value": str(node.val),
                "left": build(node.left),
                "right": build(node.right),
            }

        return json.dumps({"kind": {"tree": True}, "root": build(self)})


def _tree_equal(a: TreeNode | None, b: TreeNode | None) -> bool:
    """递归比较两棵树是否结构和值都相同。"""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return a.val == b.val and _tree_equal(a.left, b.left) and _tree_equal(a.right, b.right)


def _build_tree_lines(node: TreeNode | None) -> list[str]:
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


def build_tree(values: Iterable[int | None]) -> TreeNode | None:
    """根据层序数组构造二叉树。

    None 表示空节点，与 LeetCode 输入格式一致。

    示例:
        >>> root = build_tree([1, 2, 3, None, 4])
        >>> print(root)
          1
         / \\
        2   3
         \\
          4
    """
    values_list: list[int | None] = list(values)
    if not values_list or values_list[0] is None:
        return None
    root = TreeNode(values_list[0])
    queue: deque[TreeNode] = deque([root])
    i = 1
    n = len(values_list)
    while queue and i < n:
        node = queue.popleft()
        # 左子节点
        if i < n:
            left_val = values_list[i]
            i += 1
            if left_val is not None:
                node.left = TreeNode(left_val)
                queue.append(node.left)
        # 右子节点
        if i < n:
            right_val = values_list[i]
            i += 1
            if right_val is not None:
                node.right = TreeNode(right_val)
                queue.append(node.right)
    return root


def tree_to_list(root: TreeNode | None) -> list[int | None]:
    """将二叉树序列化为层序数组。"""
    if root is None:
        return []
    result: list[int | None] = []
    queue: deque[TreeNode | None] = deque([root])
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
