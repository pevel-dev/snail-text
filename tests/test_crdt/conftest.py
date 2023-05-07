import pytest

from crdt.Sequence import Sequence


@pytest.fixture
def sequence():
    s = Sequence(0)
    text = "I am CRDT!"

    for i in text:
        s.append_subseq(i)

    return s
