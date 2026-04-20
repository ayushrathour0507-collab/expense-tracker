import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

import models
from database import Base, engine
from routes.auth_routes import router as auth_router
from routes.expense_routes import router as expense_router

app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure SQLAlchemy models are imported before table creation.
models  # noqa: B018


@app.get("/")
def root():
    return {"message": "Expense Tracker API", "docs": "/docs"}


app.include_router(auth_router)
app.include_router(expense_router)


@app.on_event("startup")
def on_startup() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        logging.exception(
            "Database initialization failed on startup. "
            "The API is running, but DB-backed endpoints will fail until DATABASE_URL is reachable: %s",
            exc,
        )
