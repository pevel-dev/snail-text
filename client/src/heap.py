import math
from bisect import bisect_left, insort_left
from dataclasses import dataclass, field
from decimal import Decimal

from dataclasses_json import dataclass_json
from sortedcontainers import SortedSet


@dataclass_json
@dataclass(order=True)
class Char:
    value: str | None = field(compare=False)
    pos_id: Decimal = field(compare=True)
    author_id: int = field(compare=False)

    def __iter__(self):
        yield self.value
        yield self.pos_id
        yield self.author_id


class HeapCRDT:
    def __init__(self, author_id: int, init_str: str = ""):
        """
        Creates a new heap CRDT.

        :param author_id:
        Used for disambiguation for conflict solution:
        if two users create the same character in the same place,
        Char from the user with lower id is going to overwrite the others.
        Value -1 is used for UNKNOWN.
        """

        self.author_id = author_id

        self.heap = list()
        self.positions = set()
        self.present_positions = SortedSet()
        self.reset_from(init_str)

    def set_char(self, chr: Char):
        """
        Applies provided operation.

        :param chr:
        Sets the value at the given pos_id to value. If already assigned and
        Char author_id is higher than the id in the heap, rewrites.
        Otherwise, does nothing. If the value is already None, does nothing.
        """

        self.__handle_insert(chr)
        # print(str(self), chr)

    def __get_next_id_from_spread(self, id):
        id = math.ceil(id)
        return id - id % self.INDEX_DEFAULT_SPREAD + self.INDEX_DEFAULT_SPREAD

    def __get_existing_heap_idx(self, chr):
        idx = bisect_left(self.heap, chr)
        if idx != len(self.heap) and self.heap[idx] == chr:
            return idx

        return None

    def __handle_insert(self, i: Char):
        if i.pos_id in self.positions:
            idx = self.__get_existing_heap_idx(i)
            if i.value is None:
                self.present_positions.remove(i.pos_id)
                self.heap[idx] = i
            elif self.heap[idx].author_id < i.author_id:
                self.heap[idx] = i
        else:
            self.positions.add(i.pos_id)
            self.present_positions.add(i.pos_id)
            insort_left(self.heap, i)

    def __repr__(self):
        """Construct a string from every non-removed element"""
        prev_id = self.heap[0].pos_id if len(self.heap) > 0 else -1
        result = []

        for c, pos_id, _ in self.heap:
            if pos_id < prev_id:
                self.heap.sort()
                return self.__repr__()

            prev_id = pos_id
            if c is not None:
                result.append(c)

        return "".join(result)

    def reset_from(self, init_str: str):
        """Rebuilds the inner data structure from the given string"""
        curr_idx = Decimal(1)
        self.heap = list()
        self.positions = set()

        for c in init_str:
            self.heap.append(Char(c, curr_idx, -1))
            self.positions.add(curr_idx)
            self.present_positions.add(curr_idx)
            curr_idx += 1

    def new_pos_id_from_idx(self, idx):
        if len(self.heap) == 0:
            return Decimal(1)
        elif idx <= 0:
            return Decimal(math.floor(self.heap[0].pos_id) - 2)
        elif idx >= len(self.present_positions):
            return Decimal(math.ceil(self.heap[-1].pos_id) + 2)

        left = self.present_positions[idx - 1]
        right = self.present_positions[idx]

        c = (left + right) / 2
        while c in self.positions:  # TODO очень неэффективно
            c = (c + right) / 2

        return c

    def find_pos_id_from_idx(self, idx):
        if idx >= len(self.present_positions) or idx < 0:
            raise ValueError(f"No position matches given index [{idx}].")

        return self.present_positions[idx]

    def new_chr_at_idx(self, value: str | None, index: int) -> Char:
        """
        Returns a new Char which after processing will be INSERTED
        BEFORE the given index
        """

        c = Char(value, self.new_pos_id_from_idx(index), self.author_id)
        self.set_char(c)
        return c

    def new_chr_sub_idx(self, value: str | None, index: int) -> Char:
        """
        Returns a new Char which after processing will REPLACE the existing
        char at the given index
        """

        c = Char(value, self.find_pos_id_from_idx(index), self.author_id)
        self.set_char(c)
        return c

    def get_idx_from_pos_id(self, pos_id: Decimal):
        return bisect_left(self.present_positions, pos_id)

    def __iter__(self):
        return self.heap.__iter__()

