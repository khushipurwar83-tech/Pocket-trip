from fastapi import APIRouter
from app.models.schemas import ResponseModel
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class ItinerarySaveRequest(BaseModel):
    trip_id: str
    days: List[Dict[str, Any]]

@router.get("/{trip_id}", response_model=ResponseModel)
def get_itinerary(trip_id: str):
    """
    Get the schedule and itinerary for a trip.
    """
    return ResponseModel(
        success=True,
        data={
            "trip_id": trip_id,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2024-12-01",
                    "activities": [
                        {"time": "09:00", "title": "Breakfast at Cafe", "cost": 10},
                        {"time": "11:00", "title": "Visit Eiffel Tower", "cost": 30}
                    ]
                }
            ]
        }
    )

@router.post("/save", response_model=ResponseModel)
def save_itinerary(payload: ItinerarySaveRequest):
    """
    Update or save the entire itinerary.
    """
    # TODO: invoke offline_sync.add_to_queue(...)
    return ResponseModel(
        success=True,
        data={
            "message": "Itinerary saved successfully.",
            "trip_id": payload.trip_id
        }
    )
