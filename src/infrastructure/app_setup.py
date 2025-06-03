"""Application setup functions for middleware and exception handlers."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger
from src.infrastructure.middleware.request_id import add_request_id
from src.infrastructure.settings import settings


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware for the application."""
    
    # CORS middleware
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=settings.cors_credentials,
            allow_methods=settings.cors_methods,
            allow_headers=settings.cors_headers,
        )
    
    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        return await add_request_id(request, call_next)


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup all exception handlers for the application."""
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions and log them."""
        request_id = getattr(request.state, "request_id", "unknown")
        
        with logger.contextualize(request_id=request_id):
            logger.error(
                f"HTTP error occurred: {exc.status_code} - {exc.detail} | "
                f"Path: {request.url.path} | Method: {request.method}"
            )
        
        response = ORJSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": str(exc.detail),
                    "status_code": exc.status_code,
                    "path": request.url.path
                }
            }
        )
        
        if request_id != "unknown":
            response.headers["X-Request-ID"] = request_id
        
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors and log them."""
        request_id = getattr(request.state, "request_id", "unknown")
        
        with logger.contextualize(request_id=request_id):
            logger.error(
                f"Validation error occurred | Path: {request.url.path} | "
                f"Method: {request.method} | Errors: {exc.errors()}"
            )
        
        response = ORJSONResponse(
            status_code=422,
            content={
                "error": {
                    "message": "Validation error",
                    "status_code": 422,
                    "path": request.url.path,
                    "details": exc.errors()
                }
            }
        )
        
        if request_id != "unknown":
            response.headers["X-Request-ID"] = request_id
        
        return response

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions and log them."""
        request_id = getattr(request.state, "request_id", "unknown")
        
        with logger.contextualize(request_id=request_id):
            logger.exception(
                f"Unhandled exception occurred | Path: {request.url.path} | "
                f"Method: {request.method} | Exception: {type(exc).__name__}: {str(exc)}"
            )
        
        response = ORJSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": "Internal server error",
                    "status_code": 500,
                    "path": request.url.path
                }
            }
        )
        
        if request_id != "unknown":
            response.headers["X-Request-ID"] = request_id
        
        return response