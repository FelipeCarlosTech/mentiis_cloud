"""
Middleware module for request/response logging.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import get_logger

logger = get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request and response data."""
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the request, log request and response data.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware or endpoint handler
            
        Returns:
            The HTTP response
        """
        start_time = time.time()
        
        # Log request details
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent", ""),
            }
        )
        
        # Process the request through the next middleware or route handler
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response details
        logger.info(
            f"Request completed: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "processing_time": process_time,
            }
        )
        
        return response