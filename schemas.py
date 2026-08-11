
from pydantic import BaseModel, Field
from typing import Optional, List


class AccountCreate(BaseModel):
    customer_id: int
    account_type: str = Field(..., pattern="^(checking|savings)$")
    balance: float = 0


class AccountUpdate(BaseModel):
    account_type: Optional[str] = Field(default=None, pattern="^(checking|savings)$")
    balance: Optional[float] = None


class AccountOut(BaseModel):
    id: int
    customer_id: int
    account_type: str
    balance: float


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


class CustomerWithAccountsOut(CustomerOut):
    accounts: List[AccountOut] = []
