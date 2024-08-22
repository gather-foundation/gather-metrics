from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import router

app = FastAPI()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
