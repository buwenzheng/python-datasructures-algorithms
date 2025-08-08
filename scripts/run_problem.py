from __future__ import annotations

import argparse
from typing import Optional

from dsa.algorithms.linked_list.detect_cycle import detect_cycle
from dsa.structures.list_node import ListNode, build_cycle_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a demo problem.")
    parser.add_argument("--cycle-pos", type=int, default=1, help="cycle entry position (-1 for none)")
    args = parser.parse_args()

    head: Optional[ListNode] = build_cycle_list([3, 2, 0, -4], pos=args.cycle_pos)
    node = detect_cycle(head)
    print("Has cycle:", node is not None, "/ Entry value:", getattr(node, "val", None))


if __name__ == "__main__":
    main()

