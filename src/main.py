from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from .config import logger, settings
from .routes import router
from .utils.rate_limiter import setup_rate_limiter

############# FASTAPI APP ###############
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
)


############# MIDDLEWARE TO LOG EXCEPTIONS ###############
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        # Log the error with traceback
        logger.error("Exception occurred", exc_info=e)
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )


############# MIDDLEWARE TO FORCE HTTPS ###############
if settings.environment != "development":
    # Middleware to force HTTPS in production
    app.add_middleware(HTTPSRedirectMiddleware)

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        logger.info(f"New request: {request.method} {request.url}")
        # Process the request and get the response
        response = await call_next(request)

        # Add HSTS header in production
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )

        return response


############# MIDDLEWARE FOR SECURITY ###############
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = settings.csp_policy
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


app.add_middleware(SecurityHeadersMiddleware)

############# CORS POLICY ###############
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############# RATE LIMITER ###############
setup_rate_limiter(app)

############# ROUTER ###############
app.include_router(router)

############# STATIC FILES ###############
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory="data"), name="data")
