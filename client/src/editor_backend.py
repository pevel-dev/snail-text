import difflib
import random

from PyQt6.QtWidgets import QFileDialog

from crdt.heap import HeapCRDT


class EditorBackend:
    def __init__(self, file_path=None):
        self.differ = difflib.SequenceMatcher()
        init_str = ""
        if file_path is not None:
            with open(file_path, "r") as f:
                init_str = f.read()
                print(init_str)

        self.file = file_path
        self.crdt = HeapCRDT(random.randint(10, 1000000), init_str)  # TODO: нормально получать id

    def handle_change_text(self, current_text, last_text):
        s1 = current_text
        #  s2 = last_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    self.crdt.new_chr_sub_idx(None, i1)
                # print(f'Удалить {s1[i1:i2]} из позиции [{i1}:{i2}]')
            elif tag == "insert":
                for j in range(j1, j2):
                    self.crdt.new_chr_at_idx(s1[j], j)
                print(i1, end=" ")
        print(str(self.crdt))
