import redis.asyncio as aioredis
from src.config import Config


JTI_TOKEN_EXPIRY = 150

redis_client = aioredis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    decode_responses=True,
    db=0,
    socket_connect_timeout=5,
    retry_on_timeout=True
    )


async def add_jti_to_blocklist(jti: str)->None:
    await redis_client.set(
        name=jti,
        value='',
        ex=JTI_TOKEN_EXPIRY
    )


async def token_in_blacklist(jti: str):
    jti = await redis_client.get(jti)
    return jti is not None



