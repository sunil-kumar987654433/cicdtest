from datetime import datetime, timedelta, timezone
import uuid
import time
import jwt
import logging

from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from starlette.exceptions import HTTPException
from fastapi import status, Depends
from pydantic import EmailStr
from .models import User, UserBlackListToken
from src.account.schema import UserCreate, UserLogin
from pwdlib import PasswordHash
from src.config import Config

class UserPassword:
    password_hash = PasswordHash.recommended()

    @classmethod
    def create_hash_password(cls, password: str)->str:
        return cls.password_hash.hash(password)
    
    @classmethod
    def verify_password(cls, password, hashed_password):
        return cls.password_hash.verify(password, hashed_password)
    
class GenerateJWTToken:

    @classmethod
    def create_token(cls, data: dict, expires_delta: timedelta | None = None, type: str = 'access'):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            if type == "access":
                expire = datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRED)
            elif type == "refresh":
                expire = datetime.now(timezone.utc) + timedelta(days=Config.REFRESH_TOKEN_EXPIRED)
        to_encode.update({"type": type})
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET.get_secret_value(), algorithm=Config.JWT_ALGORITHAM.get_secret_value())
        return {
            "token": encoded_jwt,
            "expire": expire
        }
    
    @classmethod
    def verify_token(cls, token: str)->bool:
        print("str---------------", token)
        try:
            return jwt.decode(token, key=Config.JWT_SECRET.get_secret_value(), algorithms=[Config.JWT_ALGORITHAM.get_secret_value()])
        except jwt.PyJWTError as e:
            logging.exception(str(e))
            return None
        # except InvalidTokenError as e:
        #     raise HTTPException(
        #         detail=str(e),
        #         status_code=status.HTTP_403_FORBIDDEN
        #     )
        # except Exception as e:
        #     raise HTTPException(
        #         detail=str(e),
        #         status_code=status.HTTP_403_FORBIDDEN
        #     )



class UserService:
    async def get_user_by_email_key(self, email: EmailStr | None = None, key: uuid.UUID| None = None, session: AsyncSession = Depends()):
        statement = select(User).where(
            or_(
                User.email==email,
                User.key == key
            )
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    async def check_user_blacklist(self, jti: str, session: AsyncSession):
        statement = select(UserBlackListToken).where(UserBlackListToken.jti_token == jti)
        result = await session.execute(statement)
        response = result.scalar_one_or_none()
        if response:
            raise HTTPException(
                detail="Unauthenticated or invalid user.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    async def SigninUser(self, data: UserLogin, session: AsyncSession):
        user = await self.get_user_by_email_key(email=data.email, session=session)
        print("user============", user)
        if user is None:
            raise HTTPException(
                detail="Invalid user or password",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        is_password_match =  UserPassword.verify_password(data.password, user.hashed_password)
        print("is_password_match===============", is_password_match)
        print("===================",type(Config.JWT_ALGORITHAM.get_secret_value()), '===========', Config.JWT_ALGORITHAM.get_secret_value())
        if is_password_match is False:
            raise HTTPException(
                detail="Invalid user or password",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        jti = f"{str(int(time.time()))}-{str(uuid.uuid4())}"
        access_token_data = GenerateJWTToken.create_token(
            data={
                "user":{
                    "sub": str(user.key),
                    "email": user.email
                },
                "jti": jti,
                "type": 'access'
            },
            type= 'access'
        )
        refresh_token_data = GenerateJWTToken.create_token(
            data={
                "user":{
                    "sub": str(user.key),
                    "email": user.email
                },
                "jti": jti,
                "type": 'refresh'
            },
            type='refresh'
        )
        return {
            "access_token_data": access_token_data,
            "refresh_token_data": refresh_token_data,
        }

        
        

    async def CreateUser(self, data: UserCreate, session: AsyncSession):
        is_user = await self.get_user_by_email_key(email=data.email, session=session)
        if is_user:
            raise HTTPException(
                detail="email already exist for this user",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user = User()
        for k, v in data.model_dump(exclude_unset=True).items():
            if k == "password1":
                setattr(user, "hashed_password", UserPassword.create_hash_password(v))
            else:
                setattr(user, k, v)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user