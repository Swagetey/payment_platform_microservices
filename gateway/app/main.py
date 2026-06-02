from fastapi import FastAPI

app = FastAPI(
    title="Payment Platform Gateway",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
