from fastapi import FastAPI
from app.routers import user, meal,meal_approval,grocery,health,mental
from app.routers.routes import router
from app.routers.realtime import router as realtime_router
from app.routers.health import start_kafka_background_listener
from app.routers.mental import router as stt_router
from app.database import engine, Base
from app.agents.health.kafka_consumer import start_health_kafka_listener
import os
import threading
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.orchestrator.state import OrchestratorState
import asyncio
from app.routers import user_profile
from app.routers import exercise
from app.core.logging_config import setup_logger
from app.database import get_db




load_dotenv()
# os.remove("wellness.db")

app = FastAPI(
    title="Wellness Guidance System",
    version="1.0.0")

# @app.on_event("startup")
# def startup_event():
#     start_kafka_background_listener()
state = OrchestratorState()

# @app.on_event("startup")
# def startup_event():
    # global main_loop
    # main_loop = asyncio.get_running_loop()
    # threading.Thread(
    #     target=start_health_kafka_listener,
    #     args=(state,),
    #     daemon=True
    # ).start() 
    # 
main_loop: asyncio.AbstractEventLoop = None

@app.on_event("startup")
async def startup_event():
    try:
        global main_loop
        main_loop = asyncio.get_running_loop()

        # Start Kafka listener in a separate thread
        thread = threading.Thread(
            target=start_health_kafka_listener,
            args=(state, main_loop),
            daemon=True
        )
        thread.start() 
    except:
        logger.exception("Failed to start Kafka listener on startup")
         
        
        # asyncio.create_task(
        #     start_db_fallback_listener(state, manager)
        # )  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)


# Include routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(meal.router, prefix="/nutrition", tags=["Nutrition"])
app.include_router(meal_approval.router, prefix="/meal-approval", tags=["Meal Approval"])
app.include_router(grocery.router, prefix="/grocery", tags=["Grocery"])
app.include_router(router, prefix="/api")
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(realtime_router, prefix="/realtime") 
app.include_router(stt_router)
app.include_router(user_profile.router)
app.include_router(exercise.router, prefix="/exercise", tags=["Exercise"])