import asyncio
import difflib
import json
import sys
from collections import deque
from random import randint

import websockets
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QMenuBar, QFileDialog, \
    QMessageBox
from qasync import QEventLoop, asyncSlot
from crdt.heap import HeapCRDT, Char


class EditorBackend(QtCore.QObject):
    dataChanged = QtCore.pyqtSignal(dict)

    def __init__(self, file_path=None, debug_mode=False):
        super().__init__()
        self._websocket = None

        self.differ = difflib.SequenceMatcher()
        init_str = ""
        if file_path is not None:
            with open(file_path, "r") as f:
                init_str = f.read()
                print(init_str)

        self.file = file_path
        self.crdt = HeapCRDT(
            randint(10, 1000000), init_str
        )

        if debug_mode:
            self.handle_change_text = self.__debug_handle_change_text
        else:
            self.handle_change_text = self.__handle_change_text

        self.oper_queue = deque()
        self.has_changes = False

    @property
    def websocket(self):
        return self._websocket

    async def connect(self, server):
        self._websocket = await websockets.connect(server)
        await self.on_message()

    @asyncSlot(dict)
    async def on_message(self):
        while True:
            message = await self.websocket.recv()
            try:
                message = Char.from_json(message)
            except:
                print(f"Ты идиот чё прислал {message}")
                continue
            self.crdt.set_char(message)
            self.has_changes = True

    @asyncSlot(dict)
    async def send_message(self, message):
        while self.websocket is None:
            await asyncio.sleep(1)
        data = json.dumps(message)
        await self.websocket.send(data)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.connect(server="ws://localhost:8000/ws"))
        loop.run_forever()

    def __handle_change_text(self, current_text, last_text):
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

    def __debug_handle_change_text(self, current_text, last_text):
        s1 = current_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    c = self.crdt.new_chr_sub_idx(None, i1)
                    self.__debug_print_oper(c, i1)
                    self.oper_queue.append(c)
            elif tag == "insert":
                for j in range(j1, j2):
                    c = self.crdt.new_chr_at_idx(s1[j], j)
                    self.__debug_print_oper(c, j)
                    self.oper_queue.append(c)

        self.__debug_text_matches(current_text)

    def __debug_text_matches(self, current_text: str):
        if str(self.crdt) != current_text:
            print()
            print("-----")
            print("CRDT and GUI text mismatch:")
            print(f"CRDT: {str(self.crdt)}")
            print()
            print(f"GUI: {current_text}")
            print("-----")
            print()

    def __debug_print_oper(self, char: Char, index: int):
        if char.value is None:
            print("delete", end=" ")
        else:
            print("insert", end=" ")
        print(char.value, index, char.pos_id)


class Frontend(QMainWindow):
    def __init__(self, file_path=None, debug_mode=False):
        super().__init__()

        self.backend = EditorBackend(file_path, debug_mode)
        self.text = str(self.backend.crdt)

        self.setWindowTitle("snail-text")
        self.text_widget = QTextEdit()
        self.text_widget.setPlainText(self.text)

        self.text_widget.textChanged.connect(self.text_change)
        self.setCentralWidget(self.text_widget)
        self.setup_menus()

        self.backend.dataChanged.connect(self.update_text)
        # self.backend.run()

    def text_change(self):
        current_text = self.text_widget.toPlainText()
        self.backend.handle_change_text(current_text, self.text)
        self.text = current_text

    def setup_menus(self):
        menu_bar = QMenuBar(parent=self)

        file_menu = menu_bar.addMenu("&File")

        open_action = file_menu.addAction("&Open")
        open_action.triggered.connect(self.open_file)

        save_action = file_menu.addAction("&Save")
        save_action.triggered.connect(self.save_file)

        self.setMenuBar(menu_bar)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )
        self.backend = EditorBackend(file_path)
        self.text = str(self.backend.crdt)
        self.text_widget.setPlainText(self.text)

    def save_file(self):
        if self.backend.file is None:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Text Files (*.txt);;All Files (*)"
            )
            if file_path:
                self.backend.file = file_path

        try:
            with open(self.backend.file, "w") as f:
                f.write(str(self.backend.crdt))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    async def update_text(self):
        return

        # while True:
        #     if not self.backend.has_changes:
        #         return
        #
        #     self.text = str(self.backend.crdt)
        #     self.text_widget.setPlainText(self.text)
        #     self.backend.has_changes = False
        #
        #     await asyncio.sleep(0.01)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = Frontend(debug_mode=True)
    window.show()
    # app.exec()
    loop.create_task(window.update_text())
    window.backend.run()
