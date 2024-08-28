from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


# Custom rate limit handler if you need to wrap it
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    # Check if the request is an API request (likely JSON) or HTML
    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            content={"detail": "Rate limit exceeded. Please try again later."},
            status_code=429,
        )
    else:
        # Redirect to the custom 429 page route
        return RedirectResponse(url="/too-many-requests", status_code=302)


# A utility function to add middleware and exception handler to the app
def setup_rate_limiter(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
