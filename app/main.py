"""
http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import customers, accounts
from app import store


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.seed()
    yield


app = FastAPI(
    title="Daniel's Digital Bank API",
    description="REST API for managing customers and their bank accounts.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(customers.router)
app.include_router(accounts.router)


@app.get("/", tags=["health"])
def root():
    return {"message": "Daniel's Digital Bank API is running. See /docs for the API."}
