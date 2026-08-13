# bank_App
A banking app created to simulate its real counterpart.

## Setup

```
pip install -r requirements.txt
cp .env.example .env   # then fill in your MongoDB Atlas connection string
```

## Run

```
uvicorn app.main:app --reload
```

API docs at http://127.0.0.1:8000/docs

## Architecture

Layered / MVC-style: `Controller -> Service -> Model (repository)`.

```
app/
├── controllers/   # FastAPI routers - request/response only, no business logic
├── services/      # Business rules, validation, filtering/sorting
├── models/        # Entity classes, Mongo data access, Pydantic schemas
├── db.py          # Mongo connection + sequential id counters
└── main.py        # App wiring, /api/v1 routes, exception handlers
```

## API

All routes are under `/api/v1`.

- `POST /customers`, `GET /customers`, `GET /customers/{id}`, `PUT /customers/{id}`, `DELETE /customers/{id}` (soft-delete/deactivate)
- `POST /accounts`, `GET /accounts`, `GET /accounts/{id}`, `PUT /accounts/{id}`, `DELETE /accounts/{id}`, `POST /accounts/{id}/add-interest`
- `POST /branches`, `GET /branches`, `GET /branches/{id}`, `PUT /branches/{id}`, `DELETE /branches/{id}`
- `POST /transactions/transfer`, `GET /transactions`

Filtering/sorting via query params, e.g. `GET /accounts?branch_id=1&min_balance=1000` or `GET /transactions?start_date=2026-01-01&type=TRANSFER`.

## Frontend

A React (Vite + TypeScript) UI in `frontend/` consumes this API — Customers, Accounts, Branches, and Transactions pages with filtering, creation forms, and account/transfer actions.

```
cd frontend
npm install
cp .env.example .env   # VITE_API_BASE_URL, defaults to http://127.0.0.1:8000/api/v1
npm run dev
```

Runs at http://localhost:5173. The backend must be running (`uvicorn app.main:app --reload`) and its CORS config in `app/main.py` must allow the frontend's origin.
