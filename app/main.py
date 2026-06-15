from fastapi import FastAPI, status

app = FastAPI()

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