import pytest

from crdt.Treedoc import Treedoc


def test_parent_or_grandparent():
    assert Treedoc.parent_or_grandparent("00", "0001")
    assert Treedoc.parent_or_grandparent("1", "10101")
    assert not Treedoc.parent_or_grandparent("000", "00100")
