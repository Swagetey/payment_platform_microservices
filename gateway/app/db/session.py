from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from app.core.config import settings

DATABASE_URL = (f"postgresql+asyncpg://"
                f"{settings.postgres_user}:"
                f"{settings.postgres_password}@"
                f"{settings.postgres_host}:"
                f"{settings.postgres_port}/"
                f"{settings.postgres_db}")

engine = create_async_engine(
        DATABASE_URL,
        echo=False,
    )

session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

print(DATABASE_URL)
async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session