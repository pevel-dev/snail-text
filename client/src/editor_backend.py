import asyncio
import difflib
import json
import random
from collections import deque

import websockets

from crdt.heap import Char, HeapCRDT


class EditorBackend:
    def __init__(self, file_path=None, debug_mode=False):
        self.differ = difflib.SequenceMatcher()
        init_str = ""
        if file_path is not None:
            with open(file_path, "r") as f:
                init_str = f.read()
                print(init_str)

        self.file = file_path

        self.client_id = random.randint(10, 1000000)

        self.crdt = HeapCRDT(self.client_id,
                             init_str)  # TODO: нормально получать id и пофиксить вставку

        if debug_mode:
            self.handle_change_text = self.__debug_handle_change_text
        else:
            self.handle_change_text = self.__handle_change_text

        self.oper_queue = deque()
        self.has_changes = False
        self.loop = asyncio.get_event_loop()

        self.socket = None

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

    async def __debug_handle_change_text(self, current_text, last_text):
        s1 = current_text
        self.differ.set_seqs(last_text, current_text)
        for tag, i1, i2, j1, j2 in reversed(self.differ.get_opcodes()):
            if tag == "delete":
                for i in range(i1, i2):
                    c = self.crdt.new_chr_sub_idx(None, i1)
                    task = self.loop.create_task(self.send_update(c))
                    await task
                    self.__debug_print_oper(c, i1)
                    self.oper_queue.append(c)
            elif tag == "insert":
                for j in range(j1, j2):
                    c = self.crdt.new_chr_at_idx(s1[j], j)
                    task = self.loop.create_task(self.send_update(c))
                    await task
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

    def apply_queue(self, oper_queue: deque):
        if oper_queue:
            self.has_changes = True

        while oper_queue:
            c = oper_queue.pop()
            self.crdt.set_char(c)

    async def connect(self):
        async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
            self.socket = websocket  # TODO: КОЛИЧЕСТВО ВОЗМОЖНЫХ ПРИКОЛОВ ЗАШКАЛИВАЕТ
            while True:
                update = await websocket.recv()
                update = json.dumps(update)
                self.crdt.set_char(Char.from_json(update["char"]))
                self.has_changes = True


    async def send_update(self, c):
        await self.socket.send_json(
            {"update": c.to_json(), "client_id": self.client_id, "file_id": 0})
