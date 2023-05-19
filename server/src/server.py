from collections import defaultdict

from fastapi import WebSocket
from server.src.file import File

from crdt.heap import Char


class Server:
    def __init__(self):
        self.count_clients = 0
        self.clients = {}
        self.files = defaultdict(list)

    def connect_client(
            self, client_id: int, file_id: int, websocket: WebSocket
    ) -> None:
        self.count_clients += 1
        self.clients[client_id] = {"file": File(file_id), "socket": websocket}
        self.files[file_id].append(client_id)

    def disconnect_client(self, client_id: int, file_id: int) -> None:
        self.count_clients -= 1
        del self.clients[client_id]

    async def handle_update(self, update: dict, client_id: int,
                      file_id: int) -> None:
        self.clients[client_id]["file"].crdt.set_char(
            Char.from_json(update["char"]))
        for i in self.files[file_id]:
            if i != client_id:
                await self.clients[i]["socket"].send_json(
                    {"char": update["char"]})
