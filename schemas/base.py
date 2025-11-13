"""
Base Pydantic schemas
Students can inherit from these for consistent response formatting
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TimestampMixin(BaseModel):
    """Mixin for created/updated timestamps"""
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
