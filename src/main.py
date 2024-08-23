from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from routes import router
from utils.validator_exception_handler import (
    custom_http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="GATHER Metrics",
    description="Tool to calculate head circumference percentiles",
    version="0.0.1",
)

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")

# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
