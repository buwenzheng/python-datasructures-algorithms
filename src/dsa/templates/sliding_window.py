"""滑动窗口模板（参考 labuladong 框架）。

链接：`https://labuladong.online/`
"""

from typing import Callable, Dict


def min_window_substring(s: str, t: str) -> str:
    need: Dict[str, int] = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1
    window: Dict[str, int] = {}
    have, required = 0, len(need)
    left = 0
    best = (float("inf"), 0, 0)
    for right, ch in enumerate(s):
        if ch in need:
            window[ch] = window.get(ch, 0) + 1
            if window[ch] == need[ch]:
                have += 1
        while have == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            left_char = s[left]
            if left_char in need:
                window[left_char] -= 1
                if window[left_char] < need[left_char]:
                    have -= 1
            left += 1
    if best[0] == float("inf"):
        return ""
    _, i, j = best
    return s[i : j + 1]


__all__ = ["min_window_substring"]

