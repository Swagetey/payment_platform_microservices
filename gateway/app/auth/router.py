from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.auth.service import AuthService
from app.db.session import get_session
from app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_auth_service(
        session: AsyncSession = Depends(get_session)
) -> AuthService:
    repository = UserRepository(session)

    return AuthService(repository)


@router.post("/register")
async def register(
        request: RegisterRequest,
        service: AuthService = Depends(get_auth_service)
):
    try:
        user = await service.register(
            user_name=request.user_name,
            email=request.email,
            password=request.password,
        )
        return {
            "id": user.id,
            "email": user.email,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
        request: LoginRequest,
        service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await service.login(
            email=request.email,
            password=request.password,
        )

        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc)
        )