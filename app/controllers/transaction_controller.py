"""
GET /api/v1/transactions supports filtering, e.g.:
  GET /api/v1/transactions?start_date=2026-01-01&type=TRANSFER
"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.schemas import TransactionCreate, TransactionOut
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/transfer", response_model=TransactionOut, status_code=201)
def transfer(payload: TransactionCreate):
    return TransactionOut(**vars(transaction_service.transfer(payload)))


@router.get("", response_model=List[TransactionOut])
def list_transactions(
    start_date: Optional[date] = Query(
        default=None, description="Filter: only transactions on/after this date"
    ),
    type: Optional[str] = Query(default=None, description="Filter: only this transaction type"),
):
    results = transaction_service.list_transactions(start_date=start_date, type=type)
    return [TransactionOut(**vars(t)) for t in results]
