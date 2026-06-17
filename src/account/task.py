import asyncio
from src.celery import celery_app
from src.account.models import UserBlackListToken
from pydantic import EmailStr
from src.db.database import async_session

@celery_app.task
def logout_user(user_uid, jti):
    async def _run():
        async with async_session() as session:
            instance = UserBlackListToken(
                user_uid=user_uid,
                jti_token=jti
            )
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
    asyncio.run(_run())
    

@celery_app.task
def user_register(email: EmailStr):
    print(f"user email:{email}")