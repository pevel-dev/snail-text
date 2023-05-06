from endpoints.api import home
from endpoints.websockets import  websocket_endpoint
from fastapi import FastAPI


def register_all_endpoints(app: FastAPI) -> None:
    app.add_api_route(path="/", endpoint=home)
    app.add_api_websocket_route(path="/ws", endpoint=websocket_endpoint)
