from fastapi import APIRouter
from app.models.schemas import ResponseModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TripCreateRequest(BaseModel):
    user_id: str
    name: str
    destination: str
    start_date: str
    end_date: str

@router.get("/{user_id}", response_model=ResponseModel)
def get_trips(user_id: str):
    """
    Retrieve all trips for a specific user.
    """
    return ResponseModel(
        success=True,
        data={
            "trips": [
                {
                    "id": "trip1", 
                    "name": "Paris Winter Getaway", 
                    "destination": "Paris", 
                    "start_date": "2024-12-01",
                    "end_date": "2024-12-07",
                    "budget": 1000
                }
            ]
        }
    )

@router.post("/", response_model=ResponseModel)
def create_trip(payload: TripCreateRequest):
    """
    Create a new trip.
    """
    # TODO: invoke offline_sync.add_to_queue(...)
    return ResponseModel(
        success=True,
        data={
            "message": "Trip created successfully",
            "trip": {
                "id": "new_trip_1",
                "name": payload.name,
                "destination": payload.destination
            }
        }
    )

@router.delete("/{trip_id}", response_model=ResponseModel)
def delete_trip(trip_id: str):
    """
    Delete an existing trip.
    """
    return ResponseModel(
        success=True,
        data={"message": f"Trip {trip_id} deleted successfully"}
    )
