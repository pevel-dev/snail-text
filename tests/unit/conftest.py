import pytest

from crdt.heap import HeapCRDT


@pytest.fixture(scope="function")
def crdt() -> HeapCRDT:
    return HeapCRDT(0, "")
