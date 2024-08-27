from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import router

app = FastAPI(
    title="GATHER Metrics",
    description="Tool to calculate head circumference percentiles",
    version="0.0.1",
)

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
