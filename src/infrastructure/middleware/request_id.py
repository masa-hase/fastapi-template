import uuid
from fastapi import Request
from loguru import logger


async def add_request_id(request: Request, call_next):
    """Middleware to add request ID to all requests and responses."""
    request_id = str(uuid.uuid4())
    
    # Store request ID in request state for access in exception handlers
    request.state.request_id = request_id
    
    # Add request ID to loguru context for all logs in this request
    with logger.contextualize(request_id=request_id):
        logger.info(f"Request started: {request.method} {request.url.path}")
        
        # Process the request
        response = await call_next(request)
        
        # Log completion
        logger.info(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}")
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response