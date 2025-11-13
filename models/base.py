"""
Base SQLAlchemy models
"""
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps"""
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class BaseModel(Base, TimestampMixin):
    """
    Abstract base model with id and timestamps
    All student models should inherit from this
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
