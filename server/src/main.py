from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from server import Server

app = FastAPI()
server = Server()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    hello_data = await websocket.receive_json()
    server.connect_client(
        hello_data["client_id"], hello_data["file_id"], websocket
    )
    try:
        while True:
            data = await websocket.receive_json()
            server.handle_update(
                data["update"], hello_data["client_id"], hello_data["file_id"]
            )
            # await websocket.send_text({data})
    except WebSocketDisconnect:
        server.disconnect_client(
            hello_data["client_id"], hello_data["file_id"]
        )
