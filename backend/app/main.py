"""
Main FastAPI Application Entry Point
-----------------------------------
Initializes the FastAPI application, configures middleware,
starts background services, and registers all API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import asyncio
import threading
import os
from dotenv import load_dotenv

# Database
from app.database import engine, Base

# Routers
from app.routers import user, meal, meal_approval, grocery, health, mental
from app.routers.mental import router as stt_router
from app.routers import user_profile
from app.routers import exercise


# Logging
from app.core.logging_config import setup_logger

# ---------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------

load_dotenv()

# Initialize logger
logger = setup_logger(__name__)

# ---------------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------------

app = FastAPI(
    title="Wellness Guidance System",
    version="1.0.0"
)

logger.info("Starting Wellness Guidance System API")

  
# ---------------------------------------------------------
# Middleware Configuration
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured")


# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------

try:
    # Drop all tables
    # Base.metadata.drop_all(bind=engine)

    # Recreate all tables fresh
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

except Exception:
    logger.exception("Database initialization failed")


# ---------------------------------------------------------
# Router Registration
# ---------------------------------------------------------

logger.info("Registering API routers")

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(meal.router, prefix="/nutrition", tags=["Nutrition"])
app.include_router(meal_approval.router, prefix="/meal-approval", tags=["Meal Approval"])
app.include_router(grocery.router, prefix="/grocery", tags=["Grocery"])
# app.include_router(router, prefix="/api")
app.include_router(health.router, prefix="/health", tags=["Health"])
# app.include_router(realtime_router, prefix="/realtime")
app.include_router(stt_router)
app.include_router(user_profile.router)
app.include_router(exercise.router, prefix="/exercise", tags=["Exercise"])

logger.info("All routers registered successfully")




