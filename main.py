from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000)
