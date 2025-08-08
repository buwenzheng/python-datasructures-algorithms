"""二分搜索模板（参考 labuladong 框架）。

链接：`https://labuladong.online/`
"""

from typing import Callable


def binary_search_left_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    ans = -1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            if nums[mid] == target:
                ans = mid
            right = mid - 1
        else:
            left = mid + 1
    return ans


__all__ = ["binary_search_left_bound"]

