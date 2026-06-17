from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from src.account.services import GenerateJWTToken, UserService
from src.redis import token_in_blacklist

class TokenBearer(HTTPBearer):
    
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request):
        data =  await super().__call__(request)
        token = data.credentials.split(" ")[-1]
        if not await self.is_token_valid(token):
            raise HTTPException(
                detail={
                    "error": "This token is invalid or expired.",
                    'resolution': "Please get new token."
                },
                status_code=status.HTTP_403_FORBIDDEN
            )
        token_details = GenerateJWTToken.verify_token(token)
        if await token_in_blacklist(token_details['jti']):
            raise HTTPException(
                detail={
                    "error": "This token is invalid or has been invoked.",
                    'resolution': "Please get new token."
                },
                status_code=status.HTTP_403_FORBIDDEN
            )
        self.verify_token_data(token_details)
        # return token_details
        return {
            "token_detail": token_details,
            "token": token
        }

    def verify_token_data(self, token_details: dict):
        raise NotImplemented("Please override this method")
        

    async def is_token_valid(self, token):
        return True if GenerateJWTToken.verify_token(token) is not None else False
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_details)->dict:
        print("token_details==AccessTokenBearer===\n\n", token_details)
        if token_details and token_details.get("type") != "access":
            raise HTTPException(
                detail="Not a valid access token.",
                status_code=status.HTTP_403_FORBIDDEN
            )
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_details)->dict:
        if token_details and token_details.get("type") != "refresh":
            raise HTTPException(
                detail="Not a valid refresh token.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        