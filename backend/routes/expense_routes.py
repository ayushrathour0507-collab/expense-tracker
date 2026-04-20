from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/summary", response_model=list[schemas.CategorySummaryItem])
def get_expense_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    rows = (
        db.query(
            models.Expense.category,
            func.sum(models.Expense.amount).label("total_amount"),
        )
        .filter(models.Expense.owner_id == current_user.id)
        .group_by(models.Expense.category)
        .order_by(models.Expense.category.asc())
        .all()
    )
    return [
        schemas.CategorySummaryItem(category=row.category, total_amount=float(row.total_amount))
        for row in rows
    ]


@router.post("", response_model=schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = models.Expense(
        amount=payload.amount,
        category=payload.category.strip(),
        date=payload.date,
        note=payload.note,
        owner_id=current_user.id,
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[schemas.ExpenseOut])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Expense)
        .filter(models.Expense.owner_id == current_user.id)
        .order_by(models.Expense.date.desc(), models.Expense.id.desc())
        .all()
    )


@router.put("/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(
    expense_id: int,
    payload: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id, models.Expense.owner_id == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    updates = payload.model_dump(exclude_unset=True)
    if "category" in updates and updates["category"] is not None:
        updates["category"] = updates["category"].strip()

    for key, value in updates.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id, models.Expense.owner_id == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return None
