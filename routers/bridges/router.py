"""
Bridge Router
FastAPI endpoints for bridge management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import BridgeCondition
from .schemas import BridgeCreate, BridgeUpdate, BridgeResponse, BridgeListResponse
from . import crud

router = APIRouter()


@router.get("/", response_model=BridgeListResponse)
def list_bridges(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    condition: Optional[BridgeCondition] = Query(None, description="Filter by condition"),
    search: Optional[str] = Query(None, description="Search in name or location"),
    db: Session = Depends(get_db)
):
    """
    List all bridges with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **condition**: Filter by condition rating (excellent, good, fair, poor, critical)
    - **search**: Search term for name or location (case-insensitive)
    """
    bridges, total = crud.get_bridges(
        db=db,
        skip=skip,
        limit=limit,
        condition=condition,
        search=search
    )
    return BridgeListResponse(total=total, bridges=bridges)


@router.post("/", response_model=BridgeResponse, status_code=status.HTTP_201_CREATED)
def create_bridge(
    bridge: BridgeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new bridge
    Provide all required bridge information including:
    - Name and location
    - Physical dimensions (length, width)
    - Load rating
    - Current condition
    """
    return crud.create_bridge(db=db, bridge_data=bridge)


@router.get("/{bridge_id}", response_model=BridgeResponse)
def get_bridge(
    bridge_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific bridge by ID
    Returns detailed information about a single bridge.
    """
    bridge = crud.get_bridge(db=db, bridge_id=bridge_id)
    if not bridge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bridge with id {bridge_id} not found"
        )
    return bridge


@router.put("/{bridge_id}", response_model=BridgeResponse)
def update_bridge(
    bridge_id: int,
    bridge: BridgeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing bridge
    All fields are optional - only provided fields will be updated.
    Use this to update inspection dates, condition ratings, or any other bridge information.
    """
    updated_bridge = crud.update_bridge(db=db, bridge_id=bridge_id, bridge_data=bridge)
    if not updated_bridge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bridge with id {bridge_id} not found"
        )
    return updated_bridge


@router.delete("/{bridge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bridge(
    bridge_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a bridge
    Permanently removes a bridge from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_bridge(db=db, bridge_id=bridge_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bridge with id {bridge_id} not found"
        )
    return None
