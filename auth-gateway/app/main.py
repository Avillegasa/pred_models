"""
Auth Gateway API - Main Application
Central authentication and authorization gateway for the cybersecurity prediction system
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, SessionLocal
from .routers import auth_router, users_router, files_router, reports_router, alerts_router
from .services.auth_service import create_default_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup: Initialize database and create default users
    init_db()
    db = SessionLocal()
    try:
        create_default_users(db)
    finally:
        db.close()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Auth Gateway API",
    description="Central authentication and authorization gateway for the cybersecurity prediction system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(files_router)
app.include_router(reports_router)
app.include_router(alerts_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-gateway"}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Auth Gateway API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "auth": "/auth/login, /auth/me",
            "users": "/users (admin only)",
            "files": "/files (admin only)",
            "reports": "/reports",
            "alerts": "/alerts"
        }
    }
