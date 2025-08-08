from dsa.structures.list_node import build_cycle_list
from dsa.algorithms.linked_list.detect_cycle import detect_cycle


def test_detect_cycle_has_cycle():
    head = build_cycle_list([3, 2, 0, -4], pos=1)
    node = detect_cycle(head)
    assert node is not None
    assert node.val == 2


def test_detect_cycle_no_cycle():
    head = build_cycle_list([1, 2, 3], pos=-1)
    node = detect_cycle(head)
    assert node is None

