"""草稿本 —— 随手写代码，F5 立即运行。

使用方式:
  1. 在 main() 里写你要调试的代码
  2. 按 F5（选择「▶ 运行草稿本」）即可运行
  3. 可以打断点、单步执行、查看变量

可视化工具：
  - Debug Visualizer: F5 调试时输入 head.getVisualizationData() 或 root.getVisualizationData()
  - 终端可视化: show_linked_list / show_array / show_dp / show_window
  - PythonTutor: https://pythontutor.com/python-compiler.html#mode=edit
"""

from dsa import (
    build_cycle_list,
    build_linked_list,
    build_tree,
    show_array,
    show_dp,
    show_linked_list,
    show_tree,
    show_window,
    verify,
)


def demo_linked_list() -> None:
    """链表工具演示。"""
    # 构造链表
    head = build_linked_list([1, 2, 3, 4, 5])
    print("链表:", head)

    # 构造带环链表
    cycle = build_cycle_list([3, 2, 0, -4], pos=1)
    print("环链表:", cycle)

    # 可视化高亮节点
    slow = fast = head
    show_linked_list(head, highlights=[slow, fast], label="初始: slow=fast=head")

    slow = slow.next
    fast = fast.next.next
    show_linked_list(head, highlights=[slow, fast], label="移动一步后")


def demo_tree() -> None:
    """二叉树工具演示。"""
    root = build_tree([4, 2, 7, 1, 3, 6, 9])
    show_tree(root, label="二叉树")


def demo_verify() -> None:
    """题解验证演示。"""

    def two_sum(nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, num in enumerate(nums):
            if target - num in seen:
                return [seen[target - num], i]
            seen[num] = i
        return []

    verify(
        two_sum,
        [
            (([2, 7, 11, 15], 9), [0, 1], "基本用例"),
            (([3, 2, 4], 6), [1, 2], "中间匹配"),
            (([3, 3], 6), [0, 1], "重复元素"),
        ],
    )


def demo_visualize() -> None:
    """可视化工具演示。"""
    # 数组双指针
    show_array([1, 3, 5, 7, 9, 11], {0: "L", 4: "R"}, label="数组双指针")

    # DP 表格
    dp = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 1, 2, 2, 2],
        [0, 1, 2, 3, 3],
    ]
    show_dp(dp, highlight=(2, 2), label="dp[2][2] = 2")

    # 滑动窗口
    show_window("abcabcbb", 1, 5, label="窗口 [1, 5)")


def main() -> None:
    print("=" * 50)
    print("  dsa 工具包演示")
    print("=" * 50)

    print("\n--- 链表 ---")
    demo_linked_list()

    print("\n--- 二叉树 ---")
    demo_tree()

    print("\n--- 题解验证 ---")
    demo_verify()

    print("\n--- 可视化工具 ---")
    demo_visualize()

    # ===== 在下面写你的代码 =====


if __name__ == "__main__":
    main()
