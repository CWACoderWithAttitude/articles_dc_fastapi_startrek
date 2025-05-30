from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
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
