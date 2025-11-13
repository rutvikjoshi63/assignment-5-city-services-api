"""
Bridge CRUD operations
Database operations for bridges
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from .models import Bridge, BridgeCondition
from .schemas import BridgeCreate, BridgeUpdate


def get_bridges(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    condition: Optional[BridgeCondition] = None,
    search: Optional[str] = None
) -> tuple[list[Bridge], int]:
    """
    Get list of bridges with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        condition: Filter by condition rating
        search: Search term for name or location

    Returns:
        Tuple of (list of bridges, total count)
    """
    query = db.query(Bridge)

    # Apply filters
    if condition:
        query = query.filter(Bridge.condition == condition)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Bridge.name.ilike(search_term),
                Bridge.location.ilike(search_term)
            )
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    bridges = query.offset(skip).limit(limit).all()

    return bridges, total


def get_bridge(db: Session, bridge_id: int) -> Optional[Bridge]:
    """
    Get a specific bridge by ID

    Args:
        db: Database session
        bridge_id: Bridge ID

    Returns:
        Bridge object or None if not found
    """
    return db.query(Bridge).filter(Bridge.id == bridge_id).first()


def create_bridge(db: Session, bridge_data: BridgeCreate) -> Bridge:
    """
    Create a new bridge

    Args:
        db: Database session
        bridge_data: Bridge creation data

    Returns:
        Created bridge object
    """
    bridge = Bridge(**bridge_data.model_dump())
    db.add(bridge)
    db.commit()
    db.refresh(bridge)
    return bridge


def update_bridge(
    db: Session,
    bridge_id: int,
    bridge_data: BridgeUpdate
) -> Optional[Bridge]:
    """
    Update an existing bridge

    Args:
        db: Database session
        bridge_id: Bridge ID
        bridge_data: Bridge update data

    Returns:
        Updated bridge object or None if not found
    """
    bridge = get_bridge(db, bridge_id)
    if not bridge:
        return None

    # Update only provided fields
    update_data = bridge_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bridge, field, value)

    db.commit()
    db.refresh(bridge)
    return bridge


def delete_bridge(db: Session, bridge_id: int) -> bool:
    """
    Delete a bridge

    Args:
        db: Database session
        bridge_id: Bridge ID

    Returns:
        True if deleted, False if not found
    """
    bridge = get_bridge(db, bridge_id)
    if not bridge:
        return False

    db.delete(bridge)
    db.commit()
    return True
