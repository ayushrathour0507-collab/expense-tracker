import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

import models
from database import Base, engine
from routes.auth_routes import router as auth_router
from routes.expense_routes import router as expense_router

load_dotenv()

allowed_origins_env = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure SQLAlchemy models are imported before table creation.
models  # noqa: B018


@app.get("/")
def root():
    return {"message": "Expense Tracker API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """Health check endpoint to verify database connection and environment."""
    try:
        from database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "jwt_secret": bool(os.getenv("JWT_SECRET")),
            "allowed_origins": allowed_origins
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": f"error: {str(e)}",
            "jwt_secret": bool(os.getenv("JWT_SECRET")),
            "allowed_origins": allowed_origins
        }


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
