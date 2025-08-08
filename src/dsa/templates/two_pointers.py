"""快慢指针 / 双指针常用模板（参考 labuladong 框架）。

链接：`https://labuladong.online/`
"""

from typing import List


def remove_duplicates_sorted(nums: List[int]) -> int:
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


__all__ = ["remove_duplicates_sorted"]

