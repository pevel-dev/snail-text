import argparse
import random
import curses
from crdt.Sequence import Sequence
import tkinter as tk


class Editor:
    def __init__(self, id, file_path=None):
        self.id = id
        if file_path is None:
            initial_string = ""
        else:
            with open(file_path, 'r') as f:
                initial_string = f.read()
        self.sequence = Sequence(id, initial_string)
        self.selected_index = 0

    def insert(self, char):
        self.sequence.insert(char, self.selected_index)
        self.selected_index += 1

    def remove(self):
        if self.selected_index <= 0:
            return

        self.sequence.remove_at(self.selected_index - 1)
        self.selected_index -= 1

    def set_selection(self, index):
        self.selected_index = index

    def clear_selection(self):
        self.selected_index = None


class TextEditor:
    def __init__(self, master, editor):
        self.master = master
        self.editor = editor
        self.text = tk.Text(master)
        self.text.pack()
        self.text.insert(tk.END, self.editor.sequence.get_seq())
        self.text.bind("<Button-1>", self.on_click)
        self.text.bind("<Key>", self.on_key)

    def on_click(self, event):
        index = self.text.index(tk.CURRENT)
        self.editor.set_selection(int(index.split('.')[1]) - 1)
        self.refresh_text()

    def on_key(self, event):
        if event.char == '\b':
            self.editor.remove()
        elif event.char.isprintable():
            self.editor.insert(event.char)

        self.refresh_text()

    def refresh_text(self):
        self.text.delete(0.0, tk.END)
        self.text.insert(tk.END, self.editor.sequence.get_seq())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Snail Text Editor",
                                     description="Edits text at very low speeds",
                                     epilog="Licensed under the BEERWARE license.")
    parser.add_argument('-f', '--file', default="")
    args = parser.parse_args()

    file = args.file if args.file != "" else None
    editor = Editor(1, file)

    root = tk.Tk()
    text_editor = TextEditor(root, editor)
    root.mainloop()
