import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from server.src.server import Server

app = FastAPI()
server = Server()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    data = dict(json.loads(data))
    await server.connect_client(data["client_id"], data["file_id"], websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = dict(json.loads(data))
            await server.handle_update(
                data["char"], data["client_id"], data["file_id"]
            )
    except WebSocketDisconnect:
        server.disconnect_client(data["client_id"], data["file_id"])
