from fastapi import FastAPI, Depends
from app.auth.router import router as auth_router

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

app = FastAPI(
    title="Payment Platform Gateway",
)
app.include_router(auth_router)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/db-health")
async def db_health(
    session: AsyncSession = Depends(get_session),
) -> dict:
    result = await session.execute(
        text("SELECT 1")
    )

    return {
        "db": result.scalar_one()
    }