"""
Database models module.
"""
import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class User(Base):
    """User database model."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, default="user")
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "role": self.role
        }