"""动态规划模板（参考 labuladong 框架）。

链接：`https://labuladong.online/`
"""

from typing import List


def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    dp: List[int] = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


__all__ = ["fibonacci"]

