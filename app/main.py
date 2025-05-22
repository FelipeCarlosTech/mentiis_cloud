"""
Main entry point for the Mentiis Cloud API.
Initializes and configures the FastAPI application.
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from api.health import router as health_router
from api.users import router as users_router

# Import custom middleware
from core.middleware import LoggingMiddleware
from core.logger import get_logger

# Import database
from db.database import engine
from db.models import Base

# Initialize logger
logger = get_logger()

# Create FastAPI application
app = FastAPI(
    title="Mentiis Cloud API",
    description="Python microservice for managing cloud resources",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

# Register API routers
app.include_router(health_router)
app.include_router(users_router)

@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Mentiis Cloud API starting up")
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Mentiis Cloud API shutting down")

if __name__ == "__main__":
    logger.info("Starting Mentiis Cloud API server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)