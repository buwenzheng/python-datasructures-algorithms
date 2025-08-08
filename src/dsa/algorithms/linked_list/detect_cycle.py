from __future__ import annotations

from typing import Optional

from dsa.structures.list_node import ListNode


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    fast = slow = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next  # type: ignore[assignment]
        if fast is slow:
            break
    if not fast or not fast.next:
        return None
    slow = head
    while slow is not fast:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next
    return slow


__all__ = ["detect_cycle"]

