from watchfiles import awatch

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

from app.db.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(
            self,
            repository: UserRepository
    ):
        self._repository = repository

    async def register(
            self,
            user_name: str,
            email: str,
            password: str,
    ) -> User:
        """Registration process"""
        existing_user = await self._repository.get_by_email(email)
        if existing_user:
            raise ValueError("user already exists")

        user = User(
            username=user_name,
            email=email,
            password_hash=hash_password(password),
            role="USER",
        )

        return await self._repository.create(user)

    async def login(
            self,
            email: str,
            password: str
    ):
        """Login process"""
        user = await self._repository.get_by_email(email)
        if user is None:
            raise ValueError(
                "Invalid credentials"
            )
        if not verify_password(
                plain_password=password,
                hashed_password=user.password_hash
        ):
            raise ValueError("Invalid password")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
