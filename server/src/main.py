from endpoints import register_all_endpoints
from fastapi import FastAPI

app = FastAPI()
register_all_endpoints(app)
