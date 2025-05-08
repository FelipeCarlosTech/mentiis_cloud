"""
Health check API routes module.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.logger import get_logger

logger = get_logger()

# Create router for health-related endpoints
router = APIRouter(tags=["health"])

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the status and version of the API.
    """
    logger.info("Health check endpoint called")
    return {"status": "healthy", "version": "0.1.0"}