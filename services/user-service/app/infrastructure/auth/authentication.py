from fastapi import Depends, HTTPException, Request

from app.domain.exceptions.access import AuthenticationError
from app.infrastructure.adapters.jwt_processor_impl import JwtTokenProcessor, TokenType


class JwtTokenAuthentication:
    def __init__(self):
        self.jwt_token_processor = JwtTokenProcessor()

    async def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            email = self.jwt_token_processor.verify_token(
                token=authorization.split("Bearer ")[1],
                token_type=TokenType.ACCESS,
            )
            return email
        except AuthenticationError:
            raise HTTPException(status_code=401, detail="Unauthorized")


def get_user_email(email: str = Depends(JwtTokenAuthentication())) -> str:
    return email
