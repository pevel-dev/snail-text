import pytest

from crdt.heap import HeapCRDT


@pytest.mark.parametrize("file", ("unit/scenarios/1",))
def test_from_files(file):
    crdt = []
    with open(file, "r", encoding="utf-8") as file:
        n = int(file.readline())
        for i in range(n):
            crdt.append(HeapCRDT(i, file.readline().rstrip()))

        for command in file.readlines():
            mode = command.split()[0]
            if mode == "assert":
                parse = command.split()
                mode, index_crdt, expected = (
                    parse[0],
                    parse[1],
                    " ".join(parse[2:]),
                )
                index_crdt = int(index_crdt)
                assert str(crdt[index_crdt]) == expected
            elif mode == "insert":
                mode, index_crdt, index, char = command.split()
                index_crdt, index = int(index_crdt), int(index)
                crdt[index_crdt].new_chr_at_idx(char, index)
            elif mode == "delete":
                mode, index_crdt, index = command.split()
                index_crdt, index = int(index_crdt), int(index)
                crdt[index_crdt].new_chr_sub_idx(None, index)
