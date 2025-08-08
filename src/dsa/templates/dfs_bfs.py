"""DFS/BFS 模板（参考 labuladong 框架）。

链接：`https://labuladong.online/`
"""

from collections import deque
from typing import Callable, Iterable, List, Tuple


def bfs(start: int, get_neighbors: Callable[[int], Iterable[int]]) -> List[int]:
    visited = set([start])
    queue: deque[int] = deque([start])
    order: List[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in get_neighbors(node):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order


__all__ = ["bfs"]

