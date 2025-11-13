"""
Bridge Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from .models import BridgeCondition


class BridgeBase(BaseModel):
    """Base bridge schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Bridge name")
    location: str = Field(..., min_length=1, max_length=300, description="Bridge location/address")
    length_meters: float = Field(..., gt=0, description="Bridge length in meters")
    width_meters: float = Field(..., gt=0, description="Bridge width in meters")
    max_load_rating_tons: float = Field(..., gt=0, description="Maximum load rating in tons")
    condition: BridgeCondition = Field(..., description="Current condition rating")
    last_inspection_date: Optional[date] = Field(None, description="Date of last inspection")
    next_inspection_date: Optional[date] = Field(None, description="Date of next scheduled inspection")
    year_built: Optional[str] = Field(None, max_length=4, description="Year bridge was built")
    material: Optional[str] = Field(None, max_length=100, description="Primary construction material")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")


class BridgeCreate(BridgeBase):
    """Schema for creating a new bridge"""
    pass


class BridgeUpdate(BaseModel):
    """Schema for updating a bridge - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=300)
    length_meters: Optional[float] = Field(None, gt=0)
    width_meters: Optional[float] = Field(None, gt=0)
    max_load_rating_tons: Optional[float] = Field(None, gt=0)
    condition: Optional[BridgeCondition] = None
    last_inspection_date: Optional[date] = None
    next_inspection_date: Optional[date] = None
    year_built: Optional[str] = Field(None, max_length=4)
    material: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=1000)


class BridgeResponse(BridgeBase):
    """Schema for bridge response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BridgeListResponse(BaseModel):
    """Schema for list of bridges"""
    total: int
    bridges: list[BridgeResponse]
