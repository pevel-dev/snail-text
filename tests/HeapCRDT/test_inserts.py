from random import shuffle

from crdt.heap import HeapCRDT

test_p1 = "Якутия - "
test_p2 = "крупнейший "
test_p3 = "субъект "
test_p4 = "России."
test_p5 = "Российской Федерации."


def test_insert_beginning():
    pass


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


#    assert str(crdt) == test_p1 + test_p2 + test_p3 + test_p4
#    assert str(crdt2) == test_p1 + test_p2 + test_p3 + test_p4


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
