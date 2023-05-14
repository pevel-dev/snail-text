from random import shuffle

import pytest

from crdt.heap import Char, HeapCRDT

test_p1 = "Якутия - "
test_p2 = "крупнейший "
test_p3 = "субъект "
test_p4 = "России."
test_p5 = "Российской Федерации."


def test_insert_beginning():
    crdt = HeapCRDT(0, test_p1 + test_p2)
    for i in reversed(test_p3):
        crdt.new_chr_at_idx(i, 0)
    assert str(crdt) == test_p3 + test_p1 + test_p2


def test_insert_middle():
    crdt = HeapCRDT(1, test_p1)
    crdt2 = HeapCRDT(2, test_p1)
    oper = []
    for c in test_p3 + test_p4:
        oper.append(crdt.new_chr_at_idx(c, 1000000))

    shuffle(oper)

    for o in oper:
        crdt2.set_char(o)

    assert str(crdt) == test_p1 + test_p3 + test_p4
    assert str(crdt2) == test_p1 + test_p3 + test_p4

    oper = []
    insertion_start = len(test_p1)
    for i, c in enumerate(test_p2, insertion_start):
        oper.append(crdt.new_chr_at_idx(c, i))

    shuffle(oper)

    for o in oper:
        crdt2.set_char(o)

    assert str(crdt) == test_p1 + test_p2 + test_p3 + test_p4
    assert str(crdt2) == test_p1 + test_p2 + test_p3 + test_p4


def test_remove():
    crdt = HeapCRDT(1, test_p1 + test_p2 + test_p3 + test_p4)
    crdt2 = HeapCRDT(2, test_p1 + test_p2 + test_p3 + test_p4)

    remove_index = len(test_p1) + len(test_p2) + len(test_p3)

    oper = []
    for _ in range(len(test_p4)):
        oper.append(crdt.new_chr_sub_idx(None, remove_index))

    for c in test_p5:
        oper.append(crdt.new_chr_at_idx(c, len(crdt.heap)))

    for o in oper:
        crdt2.set_char(o)

    assert str(crdt) == test_p1 + test_p2 + test_p3 + test_p5
    assert str(crdt2) == test_p1 + test_p2 + test_p3 + test_p5


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


@pytest.mark.parametrize(
    "file", ("../sample_files/simple.txt", "../sample_files/40KB.txt")
)
def test_insert_from_files(crdt, file):
    lines = []
    with open(file, "r") as f:
        lines = f.readlines()

    c = 0
    for line in lines:
        for char in line:
            crdt.new_chr_at_idx(char, c)
            c += 1

    assert str(crdt) == "".join(lines)


def test_insert_new_line():
    crdt = HeapCRDT(0, test_p1 + test_p2)
    crdt.new_chr_at_idx("\n", 0)
    crdt.new_chr_at_idx("\n", 10)
    crdt.new_chr_at_idx("\n", 22)
    assert str(crdt) == "\n" + test_p1 + "\n" + test_p2 + "\n"
