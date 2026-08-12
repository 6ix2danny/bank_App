
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---- Branches ----

class BranchCreate(BaseModel):
    name: str
    address: str


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class BranchOut(BaseModel):
    id: int
    name: str
    address: str


# ---- Accounts ----

class AccountCreate(BaseModel):
    customer_id: int
    branch_id: int
    account_type: str = Field(..., pattern="^(checking|savings)$")
    balance: float = 0


class AccountUpdate(BaseModel):
    account_type: Optional[str] = Field(default=None, pattern="^(checking|savings)$")
    balance: Optional[float] = None


class AccountOut(BaseModel):
    id: int
    customer_id: int
    branch_id: int
    account_type: str
    balance: float


# ---- Customers ----

class CustomerCreate(BaseModel):
    name: str
    username: str
    password: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class CustomerOut(BaseModel):
    id: int
    name: str
    username: str
    is_active: bool


class CustomerWithAccountsOut(CustomerOut):
    accounts: List[AccountOut] = []


# ---- Transactions ----

class TransactionCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float = Field(..., gt=0)


class TransactionOut(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount: float
    type: str
    status: str
    created_at: datetime
