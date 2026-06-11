from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self._sesseion = session

    async def get_by_email(
            self,
            email: str
    ) -> User | None:
        """Receive by email"""
        stmt = select(User).where(User.email == email)
        result = await self._sesseion.execute(stmt)

        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Create User"""
        self._sesseion.add(user)
        await self._sesseion.commit()
        await self._sesseion.refresh(user)

        return user


