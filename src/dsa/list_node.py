"""链表节点与构造工具。

提供 ListNode 数据结构、链表构造器、可视化打印。
print() 即可看到直观的链表结构，支持环链表检测。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class ListNode:
    """链表节点。

    属性:
        val: 节点值
        next: 指向下一个节点的指针
    """

    val: int
    next: Optional["ListNode"] = None

    def __str__(self) -> str:
        """可视化打印链表，自动检测环。

        普通链表: 1 -> 2 -> 3 -> None
        环链表:   1 -> 2 -> 3 -> 4 -> [回到 2]
        """
        parts: list[str] = []
        seen: set[int] = set()
        node: Optional[ListNode] = self
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


def build_linked_list(values: Iterable[int]) -> Optional[ListNode]:
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


def build_cycle_list(values: Iterable[int], pos: int) -> Optional[ListNode]:
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
    join: Optional[ListNode] = None
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

