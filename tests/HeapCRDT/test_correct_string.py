import pytest
from crdt.heap import HeapCRDT, Char

test_str = "The quick brown fox jumps over the lazy dog."


def test_init():
    crdt = HeapCRDT(1, test_str)
    assert str(crdt) == test_str


def test_nonempty():
    from random import shuffle
    crdt = HeapCRDT(1)
    chars = []
    idx = 0
    for c in test_str:
        pos_id = crdt.new_pos_id_from_idx(idx := idx + 1)
        crdt.set_char(Char(c, pos_id, 2))

    shuffle(chars)
    for c in chars:
        crdt.set_char(c)

    assert str(crdt) == test_str


def test_empty():
    crdt = HeapCRDT(1)
    assert str(crdt) == ""
