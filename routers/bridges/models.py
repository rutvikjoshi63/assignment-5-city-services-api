"""
Bridge database model
"""
from sqlalchemy import Column, String, Float, Date, Enum as SQLEnum
from models.base import BaseModel
import enum


class BridgeCondition(str, enum.Enum):
    """Bridge condition ratings"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class Bridge(BaseModel):
    """
    Bridge infrastructure model
    Tracks bridge inspections, conditions, and maintenance
    """
    __tablename__ = "bridges"

    # Basic Information
    name = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)

    # Technical Specifications
    length_meters = Column(Float, nullable=False)
    width_meters = Column(Float, nullable=False)
    max_load_rating_tons = Column(Float, nullable=False)

    # Condition and Maintenance
    condition = Column(SQLEnum(BridgeCondition), nullable=False, default=BridgeCondition.GOOD)
    last_inspection_date = Column(Date, nullable=True)
    next_inspection_date = Column(Date, nullable=True)

    # Construction Details
    year_built = Column(String, nullable=True)
    material = Column(String, nullable=True)  # e.g., "steel", "concrete", "composite"

    # Notes
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Bridge(id={self.id}, name='{self.name}', condition='{self.condition}')>"
