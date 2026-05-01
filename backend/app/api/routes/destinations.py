from fastapi import APIRouter, Query
from typing import Optional
from app.models.schemas import ResponseModel

router = APIRouter()

@router.get("/", response_model=ResponseModel)
def search_destinations(budget: Optional[float] = None, days: Optional[int] = None):
    """
    Search and discover destinations based on budget and days.
    """
    return ResponseModel(
        success=True,
        data={
            "search_criteria": {"budget": budget, "days": days},
            "destinations": [
                {
                    "id": "dest1", 
                    "name": "Prague, Czechia",
                    "description": "Affordable European gem.",
                    "estimated_cost_per_day": 50,
                    "image_url": "https://example.com/prague.jpg"
                },
                {
                    "id": "dest2", 
                    "name": "Budapest, Hungary",
                    "description": "Thermal baths and ruin bars.",
                    "estimated_cost_per_day": 40,
                    "image_url": "https://example.com/budapest.jpg"
                }
            ]
        }
    )

@router.get("/{destination_id}", response_model=ResponseModel)
def get_destination(destination_id: str):
    """
    Detailed information for a specific destination.
    """
    return ResponseModel(
        success=True,
        data={
            "id": destination_id, 
            "name": "Prague, Czechia", 
            "description": "Prague is known for its Old Town Square...",
            "places_to_visit": ["Prague Castle", "Charles Bridge"],
            "average_food_cost": 15
        }
    )
