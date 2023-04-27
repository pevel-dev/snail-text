from fastapi import FastAPI

from endpoints.api import home
from endpoints.websockets import websocket_endpoint, get


def register_all_endpoints(app: FastAPI) -> None:
    app.add_api_route(path="/", endpoint=home)
    app.add_route(path="/web", route=get)
    app.add_api_websocket_route(path="/ws", endpoint=websocket_endpoint)
