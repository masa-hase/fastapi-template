from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.infrastructure.lifespan import lifespan
from src.infrastructure.logging import configure_logging
from src.infrastructure.app_setup import setup_middleware, setup_exception_handlers
from src.infrastructure.settings import settings
from src.presentation.api.greeting_router import router as greeting_router

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,  # Use orjson for faster JSON serialization
    openapi_url="/openapi.json" if settings.environment != "production" else None,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

# Setup middleware and exception handlers
setup_middleware(app)
setup_exception_handlers(app)

# Include routers with API prefix
app.include_router(greeting_router, prefix=settings.api_prefix)