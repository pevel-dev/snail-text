from fastapi import WebSocket, WebSocketDisconnect


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("HELLO!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text({data})
    except WebSocketDisconnect:
        pass
