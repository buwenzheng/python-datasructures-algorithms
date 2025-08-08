"""回溯模板（参考 labuladong 框架）。

链接：`https://labuladong.online/`
"""

from typing import List


def permutations(nums: List[int]) -> List[List[int]]:
    res: List[List[int]] = []
    used = [False] * len(nums)

    def dfs(path: List[int]) -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, v in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(v)
            dfs(path)
            path.pop()
            used[i] = False

    dfs([])
    return res


__all__ = ["permutations"]

