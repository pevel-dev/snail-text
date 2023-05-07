from typing import Any


class SeqFunctions:
    """
    A class to provide static methods to Sequence Class
    """

    @staticmethod
    def add(payload, elem, id):
        """
        The function to add an element with its ID to Sequence object's payload.

        Args:
            payload (list): Payload in which element has to be added.
            elem (any_type): The element to be added.
            id (any_type): ID of the element.

        Returns:
            payload (list): Payload in which element is added.
        """

        # Add the element to the payload
        payload.append((elem, id))

        # Sort the payload
        payload.sort(key=lambda i: i[1])

        return payload

    @staticmethod
    def remove(payload, id):
        """
        The function to remove an element from Sequence object's payload.

        Args:
            payload (list): Payload in which elements to be removed are added.
            id (any_type): ID of the element to be removed.

        Returns:
            payload (list): Payload in which elements to be removed are added.
        """

        # Add the ID to the payload
        payload.append(id)

        # Sort the payload
        payload.sort()

        return payload

    @staticmethod
    def merge(payload1, payload2):
        """
        The function to merge the payload2 to payload1.

        Args:
            payload1 (list): Payload to be merged to.
            payload2 (list): Payload to be merged from.

        Returns:
            payload1 (list): Payload merged to.
        """

        for item in payload2:
            if item not in payload1:
                payload1.append(item)

        return payload1

    @staticmethod
    def display(name, payload):
        """
        The function to print the object.

        Args:
            name (string): Payload type.
            payload (list): Payload to display.
        """

        print("{}: ".format(name), payload)

    @staticmethod
    def get_seq(payload):
        """
        The function to return a string of elements in the payload.

        Args:
            payload (list): Payload to display.

        Returns:
            seq (string): String of elements in the payload
        """

        seq = ""
        for elem in payload:
            seq += elem
        return seq


class Sequence:
    """
    Sequence CRDT Implementation.

    Notes:
        An ordered set, list or a sequence of elements.
        This CRDT can be build on top of other Set based CRDTs by sorting them on some basis.
        We have used this CRDT to build a Collaborative Code/Text Editor.

    Attributes:
        elem_list (list): List of elements added.
        id_remv_list (list): List of IDs removed.
        id_seq (list): List of IDs in sequence.
        id_elem_seq (list): List of elements in sequence.
        id (any_type): ID of the class object.
        seqf (SeqFunctions): SeqFunctions object to access the static methods.
    """

    def __init__(self, id, initial_sequence=None):
        self.elem_list = []
        self.id_remv_list = []
        self.id_seq = []
        self.elem_seq = []
        self.id = id
        self.seqf = SeqFunctions()

        if initial_sequence is not None:
            self.append_subseq(initial_sequence)

    def update_seq(self):
        for item in self.elem_list:
            if item[1] not in self.id_remv_list and item[1] not in self.id_seq:
                self.id_seq.append(item[1])
        for id in self.id_remv_list:
            if id in self.id_seq:
                del self.elem_seq[self.id_seq.index(id)]
                self.id_seq.remove(id)
        self.id_seq.sort()
        for id in self.id_seq:
            for item in self.elem_list:
                if item[1] == id:
                    if len(self.elem_seq) > self.id_seq.index(id):
                        if item[0] != self.elem_seq[self.id_seq.index(id)]:
                            self.elem_seq.insert(self.id_seq.index(id), item[0])
                    else:
                        self.elem_seq.append(item[0])

    def get_id_for_index(self, index=-1):
        """
        Returns the id necessary to place the element after the given index in the represented string.
        TODO!!!!!! Examples
        """

        if (index == 0 or index == -1) and len(self.id_seq) == 0:
            return 1
        elif index > len(self.id_seq) or (index < 0 and index != -1):
            raise IndexError(f"Incorrect index: {index}")
        elif index == len(self.id_seq) or index == len(self.id_seq) - 1 or index == -1:
            import math
            return math.ceil(self.id_seq[-1]) + 1
        else:
            left = self.id_seq[index]
            right = self.id_seq[index + 1]
            return (left + right) / 2

    def insert(self, subseq, index=-1) -> list[tuple[Any, int | float | Any]]:
        """
        Inserts the substring after the given index in the string.
        Returns the list tuples of (elem, id)
        """

        if index == -1:
            return self.append_subseq(subseq)

        insertions = []
        for i, elem in enumerate(subseq, index):
            elem_id = self.get_id_for_index(i)
            self._add(elem, elem_id)
            insertions.append((elem, elem_id))

        return insertions

    def append_subseq(self, subseq) -> list[tuple[Any, int]]:
        import math
        start_index = 0
        if len(self.id_seq) > 0:
            start_index = math.ceil(self.id_seq[-1]) + 1

        insertions = []
        for elem_id, elem in enumerate(subseq, start_index):
            self._add(elem, elem_id)
            insertions.append((elem, elem_id))

        return insertions

    def insert_tuple(self, insertion_tuple: tuple[Any, int | float | Any]):
        self._add(*insertion_tuple)

    def _add(self, elem, id):
        """
        You probably should use insert() or insert_tuple()
        The function to add the element.

        Args:
            elem (any_type): The element to be added.
            id (any_type): ID of the element.

        Note:
            'elem' is added to elem_list
        """

        self.elem_list = self.seqf.add(self.elem_list, elem, id)

        # Call update_seq function
        self.update_seq()

    def remove(self, id):
        """
        The function to remove the element.

        Args:
            id (any_type): The ID of the element to be removed.

        Note:
            'elem' is added to id_remv_list
        """

        self.id_remv_list = self.seqf.remove(self.id_remv_list, id)

        # Call update_seq function
        self.update_seq()

    def remove_at(self, index):
        removable = self.id_seq[index]
        self.remove(removable)

    def query(self, id):
        """
        The function to return True if ID of the element is present in the list.

        Args:
            elem (any_type): The element to be searched for.

        Returns:
            bool: True if element's ID present in the elem_list but not in id_remv_list , False otherwise.
        """

        for item in self.elem_list:
            if item[1] == id:
                if id not in self.id_remv_list:
                    return True
                else:
                    return False
        return False

    def merge(self, list, func="na"):
        """
        The function to merge the lists with the argument's list.

        Args:
            list (
                list: List to be merged from,
                Sequence: Object to be merged from.
            )
            func (
                'na': Merge both elem_list and id_remv_list,
                'elem': Merge elem_list,
                'id': Merge id_remv_list,
            )
        """

        if func == "na":
            self.elem_list = self.seqf.merge(self.elem_list, list.elem_list)
            self.id_remv_list = self.seqf.merge(self.id_remv_list, list.id_remv_list)
        elif func == "elem":
            self.elem_list = self.seqf.merge(self.elem_list, list)
        elif func == "id":
            self.id_remv_list = self.seqf.merge(self.id_remv_list, list)
        self.update_seq()

    def display(self):
        """
        The function to print the object's payloads.
        """

        self.seqf.display("Elem List", self.elem_list)
        self.seqf.display("ID Removed List", self.id_remv_list)
        self.seqf.display("ID Seq", self.id_seq)
        self.seqf.display("Elem Seq", self.elem_seq)

    def get_seq(self):
        """
        The function to get the sequence as string.
        """
        self.update_seq()
        return self.seqf.get_seq(self.elem_seq)
