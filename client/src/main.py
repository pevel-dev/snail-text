#!/usr/bin/env python
import asyncio
from websockets.client import connect


class Client:
    def __init__(self, client_id):
        self.path = "ws://localhost:8000/ws"
        self.connected = False
        self.socket = None
        self.client_id = client_id
        self.socket = None
        self.receive_queue = list()

    async def run(self):
        self.socket = connect(self.path)

        async with connect(self.path) as socket:
            while True:
                a = await socket.recv()
                await self.update_handle(a)

    async def update_handle(self, update):
        pass

    async def send(self, message):
        self.socket.send(message)


async def b():
    await asyncio.sleep(5)
    print('XUI')


if __name__ == "__main__":
    import random
    c = Client(random.randint(-2**31, 2**31 - 1))
    loop = asyncio.get_event_loop()
    loop.create_task(c.run())
    loop.create_task(b())
    loop.run_forever()
