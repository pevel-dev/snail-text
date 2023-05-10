import pytest

from crdt.Treedoc import Treedoc


@pytest.fixture
def treedoc():
    s = Treedoc(0, 0)
    return s
