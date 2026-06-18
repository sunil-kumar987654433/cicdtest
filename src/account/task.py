import asyncio
from src.celery import celery_app
from src.account.models import UserBlackListToken
from pydantic import EmailStr
from src.db.database import SessionLocal

@celery_app.task
def logout_user(user_uid, jti):
    session = SessionLocal()
    try:
        instance = UserBlackListToken(
            user_uid=user_uid,
            jti_token=jti
        )
        session.add(instance)
        session.commit()
    finally:
        # pass
        session.close()


    

@celery_app.task
def user_register(email: EmailStr):
    print(f"user email:{email}")