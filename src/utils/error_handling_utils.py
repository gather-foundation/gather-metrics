from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

ERROR_MESSAGES = {
    HTTPException: "An error occurred. Please try again later.",
    Exception: "An unexpected error occurred. Please try again later.",
}


def is_htmx_request(request: Request) -> bool:
    return request.headers.get("HX-Request") is not None


async def render_error_template(request: Request, message: str, status_code: int):
    return templates.TemplateResponse(
        "shared/error_banner.html",
        {"request": request, "error_message": message},
        status_code=status_code,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    message = exc.detail or ERROR_MESSAGES.get(
        type(exc), "An unexpected error occurred."
    )
    print(exc)
    if is_htmx_request(request):
        return await render_error_template(request, message, exc.status_code)
    return JSONResponse(content="An unexpected error occurred.", status_code=500)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract and format error details into a single string
    print("hello")
    error_messages = []
    for error in exc.errors():
        loc = " -> ".join(map(str, error["loc"]))  # Location of the error
        msg = error["msg"]  # Error message
        error_message = f"{loc}: {msg}"
        error_messages.append(error_message)

    # Join all error messages into a single string separated by periods
    error_details = ". ".join(error_messages) + "."

    if is_htmx_request(request):
        # Use the formatted error details in the error banner for HTMX requests
        return await render_error_template(request, error_details, 422)

    # For non-HTMX requests, return the error details as JSON
    return JSONResponse(content={"detail": error_messages}, status_code=422)
