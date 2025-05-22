"""
User API routes module.
Provides endpoints for user management operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.logger import get_logger
from db.database import get_db
from db.models import User as UserModel

logger = get_logger()

# Create router for user-related endpoints
router = APIRouter(prefix="/users", tags=["users"])

class UserBase(BaseModel):
    """Base user data model."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
    role: str = Field(default="user", min_length=2, max_length=50)

class UserCreate(UserBase):
    """User creation model."""
    pass

class User(UserBase):
    """User response model."""
    id: str

@router.post("", response_model=User, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user: User data
        db: Database session

    Returns:
        Created user with ID
    """
    logger.info(f"Creating user with email: {user.email}")

    try:
        # Create new user in database
        db_user = UserModel(
            name=user.name,
            email=user.email,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User created successfully with ID: {db_user.id}")
        return db_user.to_dict()
    
    except IntegrityError:
        db.rollback()
        logger.warning(f"User creation failed: email already exists - {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

@router.get("", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """
    Get all users.

    Returns:
        List of all users
    """
    logger.info("Fetching all users")
    users = db.query(UserModel).all()
    return [user.to_dict() for user in users]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Get user by ID.

    Args:
        user_id: UUID of the user
        db: Database session

    Returns:
        User data
    """
    logger.info(f"Fetching user with ID: {user_id}")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.to_dict()

