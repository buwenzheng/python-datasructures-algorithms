"""LeetCode 142 - 环形链表 II

链接: https://leetcode.cn/problems/linked-list-cycle-ii/
对应 labuladong: https://labuladong.online/algo/data-structure-basic/linked-list-basic/

题目:
    给定链表 head，若链表中有环，返回入环的第一个节点；否则返回 None。

思路:
    快慢指针（Floyd 判圈算法）：
    1. fast 每次走 2 步，slow 每次走 1 步
    2. 若有环，fast 和 slow 必定在环内相遇
    3. 相遇后，让 slow 回到 head，两者同时走 1 步，再次相遇即为入环点

    为什么第 3 步有效？
    - 设 head 到入环点距离为 a，入环点到相遇点距离为 b，环长为 c
    - 相遇时 fast 走了 a + b + n*c，slow 走了 a + b
    - 因为 fast = 2 * slow，所以 a + b = n*c，即 a = n*c - b
    - 所以从 head 走 a 步 = 从相遇点走 n*c - b 步 = 到达入环点
"""

from typing import Optional
from dsa import ListNode, build_cycle_list


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """检测链表环，返回入环节点。"""
    # TODO: 请自行实现
    raise NotImplementedError


# ============================================================
# 调试区域 —— F5 运行当前文件即可看到输出
# ============================================================
if __name__ == "__main__":
    # 测试 1: 有环 [3, 2, 0, -4]，pos=1（入环点值为 2）
    head1 = build_cycle_list([3, 2, 0, -4], pos=1)
    print("输入:", head1)
    result1 = detect_cycle(head1)
    print("入环节点:", result1.val if result1 else None)
    print("期望: 2")

    print()

    # 测试 2: 无环 [1, 2, 3]
    head2 = build_cycle_list([1, 2, 3], pos=-1)
    print("输入:", head2)
    result2 = detect_cycle(head2)
    print("入环节点:", result2.val if result2 else None)
    print("期望: None")

