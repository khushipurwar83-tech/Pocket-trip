from fastapi import APIRouter, HTTPException
from app.models.schemas import ResponseModel, BudgetCalculateRequest

router = APIRouter()

@router.get("/{trip_id}", response_model=ResponseModel)
def get_budget(trip_id: str):
    """
    Get the overall budget breakdown for a trip.
    """
    # Provide highly actionable mock response for frontend developer
    return ResponseModel(
        success=True,
        data={
            "trip_id": trip_id,
            "total_budget": 1000,
            "spent": 350,
            "categories": {
                "accommodation": {"budgeted": 400, "spent": 200},
                "food": {"budgeted": 300, "spent": 100},
                "transport": {"budgeted": 200, "spent": 50},
                "activities": {"budgeted": 100, "spent": 0}
            }
        }
    )

@router.post("/calculate", response_model=ResponseModel)
def calculate_budget(request: BudgetCalculateRequest):
    """
    Recommend a budget breakdown based on total budget, days, and people.
    """
    daily_total = request.total / request.days
    per_person = request.total / request.people
    
    # Simple recommendation breakdown
    breakdown = {
        "accommodation": round(request.total * 0.4, 2),
        "food": round(request.total * 0.3, 2),
        "transportation": round(request.total * 0.2, 2),
        "activities": round(request.total * 0.1, 2)
    }
    
    return ResponseModel(
        success=True,
        data={
            "suggested_breakdown": breakdown,
            "daily_budget": round(daily_total, 2),
            "per_person": round(per_person, 2)
        }
    )

@router.put("/{trip_id}", response_model=ResponseModel)
def update_budget(trip_id: str, new_total: float):
    """
    Update the total budget for a specific trip.
    """
    return ResponseModel(
        success=True,
        data={"trip_id": trip_id, "updated_total": new_total}
    )
