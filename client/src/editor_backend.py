import difflib

from crdt.heap import HeapCRDT


class EditorBackend:
    def __init__(self):
        self.differ = difflib.SequenceMatcher()
        self.crdt = HeapCRDT(0, " ")  # TODO: получать id

    def handle_change_text(self, current_text, last_text):
        s1 = current_text
        #  s2 = last_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    self.crdt.new_chr_sub_idx(None, i2)
                # print(f'Удалить {s1[i1:i2]} из позиции [{i1}:{i2}]')
            elif tag == "insert":
                self.crdt.new_chr_at_idx(s1[j1], i1)
                print(i1, end=" ")
                # print(
                #     f'Вставить {s2[j1:j2]} из s2[{j1}:{j2}] в s1 перед {s1[i1]}')
        print(str(self.crdt))
