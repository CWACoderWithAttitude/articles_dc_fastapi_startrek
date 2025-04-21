from typing import Any, Generator
from fastapi import FastAPI, HTTPException
from fastapi import Depends, status
from prometheus_fastapi_instrumentator import Instrumentator
from sqlmodel import Field, SQLModel, Session, create_engine, select
from routers.ships_router import router as ships_router


app = FastAPI()

Instrumentator().instrument(app).expose(app)
app.include_router(ships_router)


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000)
