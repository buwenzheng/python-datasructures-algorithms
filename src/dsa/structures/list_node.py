from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def build_linked_list(values: Iterable[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cursor = dummy
    for value in values:
        cursor.next = ListNode(value)
        cursor = cursor.next
    return dummy.next


def build_cycle_list(values: Iterable[int], pos: int) -> Optional[ListNode]:
    """
    构造带环链表：pos 为入环位置（-1 表示无环）。
    行为与 LeetCode 环形链表题目描述一致。
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
    # 若 pos 指向最后一个节点
    if index == pos:
        join = tail
    if join is None:
        join = head
    tail.next = join
    return head


__all__ = ["ListNode", "build_linked_list", "build_cycle_list"]

