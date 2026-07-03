"""链表节点与构造工具。

提供 ListNode 数据结构、链表构造器、可视化打印。
print() 即可看到直观的链表结构，支持环链表检测。
"""

from __future__ import annotations

from collections.abc import Iterable


class ListNode:
    """链表节点。

    属性:
        val: 节点值
        next: 指向下一个节点的指针
    """

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next

    def __str__(self) -> str:
        """可视化打印链表，自动检测环。

        普通链表: 1 -> 2 -> 3 -> None
        环链表:   1 -> 2 -> 3 -> 4 -> [回到 2]
        """
        parts: list[str] = []
        seen: set[int] = set()
        node: ListNode | None = self
        while node is not None:
            if id(node) in seen:
                parts.append(f"[回到 {node.val}]")
                return " -> ".join(parts)
            seen.add(id(node))
            parts.append(str(node.val))
            node = node.next
        parts.append("None")
        return " -> ".join(parts)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """按值比较两个链表是否相同（忽略环）。"""
        if not isinstance(other, ListNode):
            return NotImplemented
        seen: set[int] = set()
        a: ListNode | None = self
        b: ListNode | None = other
        while a is not None and b is not None:
            if id(a) in seen:
                break
            seen.add(id(a))
            if a.val != b.val:
                return False
            a = a.next
            b = b.next
        return a is None and b is None

    def to_list(self) -> list[int]:
        """将链表转为值列表（遇到环时停止）。"""
        result: list[int] = []
        seen: set[int] = set()
        node: ListNode | None = self
        while node is not None:
            if id(node) in seen:
                break
            seen.add(id(node))
            result.append(node.val)
            node = node.next
        return result

    def getVisualizationData(self) -> str:
        """返回 JSON 字符串，供 VSCode Debug Visualizer 扩展渲染。

        使用方式：
            1. 安装 Debug Visualizer 扩展（hediet.debug-visualizer）
            2. F5 调试时，打开 Debug Visualizer 视图
               （命令面板 → Debug Visualizer: New View）
            3. 在表达式输入框中输入：head.getVisualizationData()
            4. 单步调试时实时看到链表结构变化
        """
        import json

        nodes: list[dict] = []
        edges: list[dict] = []
        seen: dict[int, str] = {}
        node: ListNode | None = self
        idx = 0

        while node is not None:
            if id(node) in seen:
                # 检测到环，添加回边
                edges.append({"from": seen[id(node)], "to": str(idx - 1), "label": "cycle"})
                break
            seen[id(node)] = str(idx)
            nodes.append({"id": str(idx), "label": str(node.val)})
            if node.next is not None and id(node.next) not in seen:
                edges.append({"from": str(idx), "to": str(idx + 1), "label": "next"})
            elif node.next is not None and id(node.next) in seen:
                edges.append({"from": str(idx), "to": seen[id(node.next)], "label": "next"})
                break
            node = node.next
            idx += 1

        return json.dumps({"kind": {"graph": True}, "nodes": nodes, "edges": edges})


def build_linked_list(values: Iterable[int]) -> ListNode | None:
    """从值列表构造链表。

    示例:
        >>> head = build_linked_list([1, 2, 3])
        >>> print(head)
        1 -> 2 -> 3 -> None
    """
    dummy = ListNode(0)
    cursor = dummy
    for value in values:
        cursor.next = ListNode(value)
        cursor = cursor.next
    return dummy.next


def build_cycle_list(values: Iterable[int], pos: int) -> ListNode | None:
    """构造带环链表。

    参数:
        values: 节点值列表
        pos: 入环位置索引（-1 表示无环），与 LeetCode 题目描述一致

    示例:
        >>> head = build_cycle_list([3, 2, 0, -4], pos=1)
        >>> print(head)
        3 -> 2 -> 0 -> -4 -> [回到 2]
    """
    head = build_linked_list(values)
    if pos < 0 or head is None:
        return head
    tail = head
    join: ListNode | None = None
    index = 0
    while tail.next is not None:
        if index == pos:
            join = tail
        tail = tail.next
        index += 1
    if index == pos:
        join = tail
    if join is None:
        join = head
    tail.next = join
    return head


__all__ = ["ListNode", "build_linked_list", "build_cycle_list"]
