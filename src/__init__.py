from fastapi import FastAPI, status, Depends, HTTPException
from  sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi.responses import JSONResponse
from .middleware import register_middleware
from contextlib import asynccontextmanager
from .redis import redis_client
from src.db.database import async_engine, get_session
from src.account.routs import account_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server start....")
    yield

    #close redis server
    await redis_client.aclose()

    #shuding down database
    await async_engine.dispose()
    print("server end....")


app = FastAPI()
register_middleware(app)
app.include_router(account_router, tags=['account'], prefix="/account")

@app.get("/")
async def get_data():
    return {
        "message": "hello bro...",
        "status": "healthy"
    }

@app.get("/health")
async def health(
    session: AsyncSession = Depends(get_session)
):
    try:
        await session.execute(text("SELECT 1"))
        return JSONResponse(
            content="connected",
            status_code=status.HTTP_200_OK
        )

    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected"
            }
        )