from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates("src/templates")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        "shared/error_banner.html",
        {
            "request": request,
            "error_message": "Invalid input data. Please correct and try again.",
        },
        status_code=422,
    )


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(
        "shared/error_banner.html",
        {"request": request, "error_message": str(exc.detail)},
        status_code=exc.status_code,
    )
