import asyncio
import difflib
import json
from collections import deque
from random import randint

import websockets
from PyQt6 import QtCore
from qasync import asyncSlot

from client.src.heap import HeapCRDT, Char


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
        if self.file is None:
            self.name_file = "test"
        else:
            self.name_file = self.file.split()[-1]

        self.client_id = randint(10, 1000000)
        self.crdt = HeapCRDT(
            self.client_id, init_str
        )

        if debug_mode:
            self.handle_change_text = self.__debug_handle_change_text
        else:
            self.handle_change_text = self.__handle_change_text

        self.changes = HeapCRDT(self.client_id)

    @property
    def websocket(self):
        return self._websocket

    async def connect(self, server):
        self._websocket = await websockets.connect(server)
        await self.send_hello_data(self._websocket)
        await self.on_message()

    async def send_hello_data(self, websocket):
        await websocket.send(json.dumps({"client_id": self.client_id, "file_id": self.name_file}))


    @asyncSlot(dict)
    async def on_message(self):
        while True:
            message = await self.websocket.recv()
            try:
                message = json.loads(message)
                message = Char.from_dict(message["char"])
            except:
                print(f"Ты идиот чё прислал {message}")
                continue
            self.crdt.set_char(message)
            if self.changes is None:
                self.changes = HeapCRDT(self.client_id)

            self.changes.set_char(message)


    @asyncSlot(dict)
    async def send_update(self, char: Char):
        data = {"client_id": self.client_id, "file_id": self.name_file, "char": char.to_dict()}
        await self.websocket.send(json.dumps(data, ensure_ascii=False, default=str))

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
                    self.send_update(c)
            elif tag == "insert":
                for j in range(j1, j2):
                    c = self.crdt.new_chr_at_idx(s1[j], j)
                    self.send_update(c)

    def __debug_handle_change_text(self, current_text, last_text):
        s1 = current_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    c = self.crdt.new_chr_sub_idx(None, i1)
                    self.__debug_print_oper(c, i1)
                    self.send_update(c)
            elif tag == "insert":
                for j in range(j1, j2):
                    c = self.crdt.new_chr_at_idx(s1[j], j)
                    self.__debug_print_oper(c, j)
                    self.send_update(c)

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
