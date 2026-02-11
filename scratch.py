"""草稿本 —— 随手写代码，F5 立即运行。

使用方式:
  1. 在 main() 里写你要调试的代码
  2. 按 F5（选择「▶ 运行草稿本」）即可运行
  3. 可以打断点、单步执行、查看变量
"""

from dsa import ListNode, build_linked_list, build_cycle_list
from dsa import TreeNode, build_tree


def main() -> None:
    # ===== 链表 =====
    head = build_linked_list([1, 2, 3, 4, 5])
    print("链表:", head)

    cycle = build_cycle_list([3, 2, 0, -4], pos=1)
    print("环链表:", cycle)

    # ===== 二叉树 =====
    root = build_tree([1, 2, 3, None, 4])
    print("\n二叉树:")
    print(root)

    # ===== 在下面写你的代码 =====


if __name__ == "__main__":
    main()

