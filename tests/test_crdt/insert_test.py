import os

import pytest

from crdt.Sequence import Sequence


def test_insert():
    text = "Code is stolen"
    s = Sequence(0)
    actions = []

    actions += s.insert(text, 0)

    actions += s.insert("not ", 7)
    assert s.get_seq() == "Code is not stolen"

    actions += s.insert('!', -1)
    assert s.get_seq() == "Code is not stolen!"

    from random import shuffle
    s2 = Sequence(1)
    shuffle(actions)
    for oper in actions:
        s2.insert_tuple(oper)

    assert s.get_seq() == s2.get_seq()


@pytest.mark.parametrize("file_name", ["test_crdt/sample_files/simple.txt"])
# "test_crdt/sample_files/40KB.txt"])
def test_append_real_files(file_name):
    print(os.getcwd())
    with open(file_name, "r") as file:
        lines = file.readlines()

    s = Sequence(0)
    c = 0
    for line in lines:
        for sign in line:
            s.append_subseq(sign)
            c += 1

    assert s.get_seq() == ''.join(lines)
