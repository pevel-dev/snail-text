import json
from collections import defaultdict

from fastapi import WebSocket
from loguru import logger
from server.src.file import File

from crdt.heap import Char


class Server:
    def __init__(self):
        self.count_clients = 0
        self.clients = {}
        self.files = defaultdict(list)
        self.files_list = {}

    async def connect_client(
            self, client_id: int, file_id: str, websocket: WebSocket
    ) -> None:
        self.count_clients += 1
        if len(self.files[file_id]) == 0:
            file = File(file_id)
            self.files_list[file_id] = file
        else:
            file = self.files_list[file_id]
        self.clients[client_id] = {"file": file, "socket": websocket}
        self.files[file_id].append(client_id)
        for i in file.crdt:
            await websocket.send_text(json.dumps({"char": i.to_dict()},  ensure_ascii=False, default=str))

        logger.info(f"Подключён клиент: {client_id}. Работает с файлом: {file_id}")

    def disconnect_client(self, client_id: int, file_id: str) -> None:
        self.count_clients -= 1
        del self.clients[client_id]
        self.files[file_id].remove(client_id)
        logger.info(f"Отключён клиент: {client_id}. Работал с файлом: {file_id}")

    async def handle_update(self, update: dict, client_id: int,
                            file_id: str) -> None:
        logger.info(f"Обрабатываем update от {client_id}")

        self.clients[client_id]["file"].crdt.set_char(Char.from_dict(update))
        for i in self.files[file_id]:
            if i != client_id:
                await self.clients[i]["socket"].send_text(json.dumps({"char": update}))
