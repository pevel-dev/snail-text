from dataclasses import dataclass, field


@dataclass(order=True)
class Insert:
    value: str = field(compare=False)
    pos_id: int = field(compare=True)
    author_id: int = field(compare=False)


@dataclass
class SyncState:
    state_hash: str


class HeapCRDT:
    def __init__(self):
        pass

    def process_op(self, op: Insert | SyncState):
        """
        Applies provided operation.

        :param op:
        - Insert(value, pos_id, author_id) - sets the value at the given pos_id to value.
        If already assigned and Insertion author_id is higher than the id in the heap, rewrites.
        Otherwise, does nothing. If the value is already None, does nothing.
        - SyncState(state_hash) - will wait for a state with the given state_hash, and then rebuild
        """
        pass

    def __repr__(self):
        """Construct a string from every non-removed element"""
        pass

    def try_rebuild(self, state_hash) -> bool:
        """Rebuilds the inner data structure,
         while assigning each not-removed element a new index.
         If current state matches the state_hash, rebuilds and returns True.
         Otherwise, returns False and does nothing."""
        pass

    def get_state_hash(self):  # нужен будет для синхронизации состояний перед ребилдом
        pass
