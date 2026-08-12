"""
http://127.0.0.1:8000/docs
"""

from fastapi import APIRouter, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.controllers import (
    account_controller,
    branch_controller,
    customer_controller,
    transaction_controller,
)

app = FastAPI(
    title="Daniel's Digital Bank API",
    description="REST API for managing customers, accounts, branches, and transactions.",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    # FastAPI defaults invalid-payload responses to 422; overridden to 400
    # to match this project's REST status-code convention.
    return JSONResponse(status_code=400, content={"detail": jsonable_encoder(exc.errors())})


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(customer_controller.router)
api_v1.include_router(account_controller.router)
api_v1.include_router(branch_controller.router)
api_v1.include_router(transaction_controller.router)

app.include_router(api_v1)


@app.get("/", tags=["health"])
def root():
    return {"message": "Daniel's Digital Bank API is running. See /docs for the API."}
