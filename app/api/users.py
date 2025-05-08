"""
User API routes module.
Provides endpoints for user management operations.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from core.logger import get_logger
import uuid

logger = get_logger()

# Create router for user-related endpoints
router = APIRouter(prefix="/users", tags=["users"])

# In-memory storage for demo purposes
# In a real application, this would be replaced with a database
users_db = []

class UserBase(BaseModel):
    """Base user data model."""
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)
    role: str = Field(default="user", min_length=2, max_length=50)

class UserCreate(UserBase):
    """User creation model."""
    pass

class User(UserBase):
    """User response model."""
    id: str

@router.post("", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    Args:
        user: User data
        
    Returns:
        Created user with ID
    """
    logger.info(f"Creating user with email: {user.email}")
    
    # Check if email already exists
    if any(u["email"] == user.email for u in users_db):
        logger.warning(f"User creation failed: email already exists - {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with UUID
    new_user = {
        "id": str(uuid.uuid4()),
        **user.dict()
    }
    users_db.append(new_user)
    
    logger.info(f"User created successfully with ID: {new_user['id']}")
    return new_user

@router.get("", response_model=List[User])
async def get_users():
    """
    Get all users.
    
    Returns:
        List of all users
    """
    logger.info("Fetching all users")
    return users_db

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """
    Get user by ID.
    
    Args:
        user_id: UUID of the user
        
    Returns:
        User data
    """
    logger.info(f"Fetching user with ID: {user_id}")
    
    # Find user by ID
    for user in users_db:
        if user["id"] == user_id:
            return user
            
    logger.warning(f"User not found with ID: {user_id}")
    raise HTTPException(status_code=404, detail="User not found")