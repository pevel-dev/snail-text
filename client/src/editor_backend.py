import difflib
import random
from collections import deque

from client.src.editor_pyqt6 import MainWindow
from crdt.heap import HeapCRDT, Char


class EditorBackend:
    def __init__(self, file_path=None, debug_mode=False):
        self.differ = difflib.SequenceMatcher()
        init_str = ""
        if file_path is not None:
            with open(file_path, "r") as f:
                init_str = f.read()
                print(init_str)

        self.file = file_path
        self.crdt = HeapCRDT(
            random.randint(10, 1000000), init_str
        )  # TODO: нормально получать id и пофиксить вставку

        if debug_mode:
            self.handle_change_text = self.__debug_handle_change_text
        else:
            self.handle_change_text = self.__handle_change_text

        self.oper_queue = deque()

        self.frontend = MainWindow(self)

    async def __handle_change_text(self, current_text, last_text):
        s1 = current_text
        #  s2 = last_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    c = self.crdt.new_chr_sub_idx(None, i1)
                    self.oper_queue.append(c)
            elif tag == "insert":
                for j in range(j1, j2):
                    c = self.crdt.new_chr_at_idx(s1[j], j)
                    self.oper_queue.append(c)

    async def __debug_handle_change_text(self, current_text, last_text):
        s1 = current_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    c = self.crdt.new_chr_sub_idx(None, i1)
                    await self.__debug_print_oper(c, i1)
                    self.oper_queue.append(c)
            elif tag == "insert":
                for j in range(j1, j2):
                    c = self.crdt.new_chr_at_idx(s1[j], j)
                    await self.__debug_print_oper(c, j)
                    self.oper_queue.append(c)

        await self.__debug_text_matches(current_text)

    async def __debug_text_matches(self, current_text: str):
        if str(self.crdt) != current_text:
            print()
            print("-----")
            print("CRDT and GUI text mismatch:")
            print(f"CRDT: {str(self.crdt)}")
            print()
            print(f"GUI: {current_text}")
            print("-----")
            print()

    async def __debug_print_oper(self, char: Char, index: int):
        if char.value is None:
            print("delete", end=" ")
        else:
            print("insert", end=" ")
        print(char.value, index, char.pos_id)

    async def apply_queue(self, oper_queue: deque):
        has_changes = len(oper_queue) > 0

        while oper_queue:
            c = oper_queue.pop()
            self.crdt.set_char(c)

        if has_changes:
            self.frontend.refresh_text()
