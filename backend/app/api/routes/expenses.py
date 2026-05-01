from fastapi import APIRouter, HTTPException
from app.models.schemas import ResponseModel, ExpenseCreate, SplitType
from app.services.expense_splitter import split_equal, split_custom, calculate_balances

router = APIRouter()

@router.get("/{trip_id}", response_model=ResponseModel)
def get_expenses(trip_id: str):
    """
    Get all expenses for a trip.
    """
    return ResponseModel(
        success=True,
        data={
            "trip_id": trip_id,
            "expenses": [
                {
                    "id": "exp1", 
                    "amount": 100.0, 
                    "paid_by": "user1", 
                    "description": "Dinner in Rome",
                    "splits": {"user1": 40.0, "user2": 60.0}
                },
                {
                    "id": "exp2", 
                    "amount": 50.0, 
                    "paid_by": "user2", 
                    "description": "Taxi",
                    "splits": {"user1": 25.0, "user2": 25.0} # Even split
                }
            ]
        }
    )

@router.post("/{trip_id}", response_model=ResponseModel)
def add_expense(trip_id: str, expense: ExpenseCreate):
    """
    Add a new expense and calculate the splits.
    """
    try:
        splits = {}
        if expense.split_type == SplitType.EQUAL:
            # Assuming dummy participants for equal split mock
            splits = split_equal(expense.amount, ["user1", "user2"]) 
        elif expense.split_type == SplitType.CUSTOM:
            splits = split_custom(expense.amount, expense.split_details or {})
            
        # TODO: call offline_sync.add_to_queue('create', 'expenses', new_id, {...})
        
        return ResponseModel(
            success=True,
            data={
                "message": "Expense added successfully",
                "expense_id": "new_exp_123",
                "expense_details": {
                    "amount": expense.amount,
                    "paid_by": expense.paid_by,
                    "description": expense.description,
                    "splits": splits
                }
            }
        )
    except ValueError as e:
        return ResponseModel(success=False, error=str(e))

@router.get("/balances/{trip_id}", response_model=ResponseModel)
def get_balances(trip_id: str):
    """
    Calculates who owes who across all expenses in a trip.
    """
    # Mock data equivalent to what get_expenses returns initially
    mock_expenses = [
        {
            "id": "exp1", "amount": 100.0, "paid_by": "user1", 
            "splits": {"user1": 40.0, "user2": 60.0}
        },
        {
            "id": "exp2", "amount": 50.0, "paid_by": "user2", 
            "splits": {"user1": 25.0, "user2": 25.0}
        }
    ]
    balances = calculate_balances(mock_expenses)
    
    return ResponseModel(
        success=True,
        data={
            "trip_id": trip_id,
            "balances": balances # e.g. {"user1": {"user2": 15.0}} means user1 owes user2 15.0
        }
    )
