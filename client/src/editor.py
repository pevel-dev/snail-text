import argparse
import tkinter as tk

from crdt.heap import HeapCRDT


class Editor:
    def __init__(self, id, file_path=None):
        self.id = id
        if file_path is None:
            initial_string = ""
        else:
            with open(file_path, "r") as f:
                initial_string = f.read()

        self.crdt = HeapCRDT(id, initial_string)
        self.cursor_index = 0

    def insert(self, char):
        self.crdt.new_chr_at_idx(char, self.cursor_index)
        self.cursor_index += 1

    def erase(self):
        if self.cursor_index <= -1:
            return

        self.crdt.new_chr_sub_idx(None, self.cursor_index)
        self.cursor_index -= 1

    def set_cursor(self, index):
        self.cursor_index = index
        print(index)

    def clear_oper_queue(self):
        pass

    def get_oper_queue(self):
        pass


class TextEditor:
    def __init__(self, master, editor):
        self.master = master
        self.editor = editor
        self.text = tk.Text(master)
        self.text.pack()
        self.text.insert(tk.END, str(self.editor.crdt))
        self.text.bind("<Button-1>", self.on_click)
        self.text.bind("<Key>", self.on_key)

    def on_click(self, event):
        index = self.text.index(tk.CURRENT)
        self.editor.set_cursor(int(index.split(".")[1]) - 1)
        self.refresh_text()

    def on_key(self, event):
        c: str = event.char
        if c == "\b":
            self.editor.erase()
        elif c.isalnum() or c == "\n" or c == " " or c == "\t":
            self.editor.insert(c)
            print(self.editor.cursor_index)
        else:
            self.refresh_text()

    def refresh_text(self):
        self.text.delete(0.0, tk.END)
        self.text.insert(tk.END, str(self.editor.crdt))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Snail Text Editor",
        description="Edits text at very low speeds",
        epilog="Licensed under the BEERWARE license.",
    )
    parser.add_argument("-f", "--file", default="")
    args = parser.parse_args()

    file = args.file if args.file != "" else None
    editor = Editor(1, file)

    root = tk.Tk()
    text_editor = TextEditor(root, editor)
    root.mainloop()
