import time
import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Body
from src.account.schema import UserCreate, UserResponse, UserLogin
from src.account.services import UserService
from src.account.task import logout_user, user_register
from src.db.database import get_session
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.account.dependancy import AccessTokenBearer, RefreshTokenBearer
from src.redis import add_jti_to_blocklist
from .services import GenerateJWTToken
account_router = APIRouter()

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

user_service = UserService()

async def get_current_user(token_detail_data: dict =Depends(access_token_bearer), session: AsyncSession= Depends(get_session)):
    token_detail = token_detail_data['token_detail']
    user_uuid = token_detail.get("user")['sub']
    jti = token_detail['jti']
    await user_service.check_user_blacklist(jti, session)
    user =  await user_service.get_user_by_email_key(key=user_uuid, session=session)
    if user.is_active is False:
        raise HTTPException(
                detail="Inactive user",
                status_code=status.HTTP_403_FORBIDDEN
            )
    return user
    

@account_router.get("/all-user", response_model=list[UserResponse])
async def all_user(session: AsyncSession= Depends(get_session)):
    return await user_service.FetchUser(session)
    

@account_router.post("/create-user", response_model=UserResponse)
async def create_user(data: UserCreate, session: AsyncSession= Depends(get_session)):
    result =  await user_service.CreateUser(data, session)
    user_register.delay(result.email)
    return result



@account_router.post("/signin-user")
async def signin_user(data: UserLogin, session: AsyncSession= Depends(get_session)):
    return await user_service.SigninUser(data, session)


@account_router.get("/me")
async def me(current_user = Depends(get_current_user), session: AsyncSession= Depends(get_session)):
    return current_user


@account_router.get("/refresh-token")
async def refresh_token(token_data = Depends(refresh_token_bearer), session: AsyncSession= Depends(get_session)):
    user_uuid = token_data['token_detail']["user"]['sub']
    jti = token_data['token_detail']['jti']
    data={"user":{
                    "sub": str(user_uuid),
                },
                "jti": jti
                
            }
    return GenerateJWTToken.create_token(data=data)

@account_router.get("/logout")
async def revoke(
    access_token_detail = Depends(access_token_bearer)):

    access_token_data = access_token_detail['token_detail']

    jti = access_token_data['jti']
    result = await add_jti_to_blocklist(jti)
    user_uid = access_token_data['user']['sub']
    logout_user.delay(
        user_uid, 
        jti
        )
    return JSONResponse(
        content="User logout successfully",
        status_code=status.HTTP_200_OK
    )
