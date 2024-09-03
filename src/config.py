import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GATHER Metrics"
    description: str = (
        "Gather Metrics is a lightweight web application designed to assist clinicians in quickly calculating head circumference percentiles based on the latest available data."
    )
    version: str = "1.0.0"
    environment: str = "development"
    origins: list[str] = [
        "https://metrics.gatherfoundation.ch",
        "http://127.0.0.1:8000",
    ]

    # CSP Policy
    csp_policy: str = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js 'sha256-QOOQu4W1oxGqd2nbXbxiA1Di6OHQOLQD+o+G9oWL8YY='; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com/ https://fonts.gstatic.com/; "
        "img-src 'self' data: https://fastapi.tiangolo.com; "
        "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com/; "
        "connect-src 'self'; "
        "frame-src 'none'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "block-all-mixed-content; "
        "upgrade-insecure-requests"
    )

    # Use model_config for Pydantic v2
    model_config = SettingsConfigDict(env_file=".env")


# Instantiate the settings
settings = Settings()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
