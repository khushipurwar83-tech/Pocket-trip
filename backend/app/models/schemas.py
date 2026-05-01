from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from enum import Enum

class ResponseModel(BaseModel):
    success: bool
    data: Dict[str, Any] = {}
    error: Optional[str] = None

class SplitType(str, Enum):
    EQUAL = "EQUAL"
    CUSTOM = "CUSTOM"

class ExpenseCreate(BaseModel):
    amount: float
    paid_by: str
    split_type: SplitType
    split_details: Optional[Dict[str, float]] = None
    description: str

class BudgetCalculateRequest(BaseModel):
    total: float
    days: int
    people: int
