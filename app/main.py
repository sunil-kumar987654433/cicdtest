from fastapi import FastAPI, status
from .middleware import register_middleware
app = FastAPI()
register_middleware(app)


@app.get("/")
async def get_data():
    return {
        "message": "hello bro...",
        "status": "healthy"
    }


@app.get("/health")
async def get_health():
    return {
        "status": 'ok'
    }