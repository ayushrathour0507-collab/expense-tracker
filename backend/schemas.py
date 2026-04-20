from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    date: date
    note: Optional[str] = Field(default=None, max_length=1000)


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date: Optional[date] = None
    note: Optional[str] = Field(default=None, max_length=1000)


class ExpenseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: float
    category: str
    date: date
    note: Optional[str] = None
    created_at: datetime


class CategorySummaryItem(BaseModel):
    category: str
    total_amount: float
    note: Optional[str] = None
    owner_id: int
    created_at: datetime


class CategorySummaryItem(BaseModel):
    category: str
    total_amount: float
