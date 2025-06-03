import sys
from loguru import logger
from src.infrastructure.settings import settings


def configure_logging():
    """Configure loguru logger with custom settings from configuration."""
    # Remove default logger
    logger.remove()
    
    # Console format with color for request_id logs
    console_format_with_request_id = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<yellow>{extra[request_id]}</yellow> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # Console format with color for non-request_id logs
    console_format_without_request_id = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # File format (no colors)
    file_format_with_request_id = (
        "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
        "{extra[request_id]} | {name}:{function}:{line} - {message}"
    )
    
    # Add console handler with request_id
    logger.add(
        sys.stdout,
        format=console_format_with_request_id,
        level=settings.log_level,
        filter=lambda record: "request_id" in record["extra"]
    )
    
    # Add console handler without request_id (for startup/shutdown logs)
    logger.add(
        sys.stdout,
        format=console_format_without_request_id,
        level=settings.log_level,
        filter=lambda record: "request_id" not in record["extra"]
    )
    
