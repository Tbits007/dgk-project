from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, HTTPException

from app.application.interactors import user_interactors
from app.domain.exceptions.user import UserNotFoundError
from app.infrastructure.auth.authentication import get_user_email
from app.presentation.controllers.http.user.schemas import request as request_schemas
from app.presentation.controllers.http.user.schemas import response as response_schemas

user_router = APIRouter()


@user_router.get("/me")
@inject
async def get_user(
    interactor: FromDishka[user_interactors.GetUserInteractor],
    user_email: str = Depends(get_user_email),
) -> response_schemas.UserResponse:
    try:
        user = await interactor(user_email)
        return response_schemas.UserResponse(email=user.email, username=user.username)
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )


@user_router.patch("/me")
@inject
async def update_user(
    updates: request_schemas.UpdateUserRequest,
    interactor: FromDishka[user_interactors.UpdateUserInteractor],
    user_email: str = Depends(get_user_email),
) -> response_schemas.UserResponse:
    try:
        user = await interactor(user_email, dict(updates))
        return response_schemas.UserResponse(email=user.email, username=user.username)
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
