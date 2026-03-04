import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.exercise import ExerciseEntry
from app.agents.health.rules import detect_anomaly
from app.orchestrator.state import OrchestratorState
from app.agents.health.utils import setup_logger
import logging
from app.routers.realtime import ConnectionManager

logger = setup_logger(__name__)

async def start_db_fallback_listener(state: OrchestratorState, manager:ConnectionManager):
    logger.warning("⚠ Kafka not available. Switching to DB polling mode...")

    last_id = None

    while True:
        try:
            db: Session = SessionLocal()

              # Get all entries ordered by id
            entries = db.query(ExerciseEntry).order_by(ExerciseEntry.id.asc()).all()
            db.close()

            if not entries:
                logger.warning("No DB entries found to replay.")
                return
            

            for entry in entries:
                if entry is None:
                    logger.warning("Skipping None entry from DB.")
                    continue
                data = {
                    "heart_rate": entry.heart_rate,
                    "spo2": entry.spo2,
                    "bp_systolic": entry.bp_systolic,
                    "bp_diastolic": entry.bp_diastolic,
                    "steps": entry.steps,
                    "workout_duration_minutes": entry.workout_duration_minutes,
                    "timestamp": str(entry.date_created)
                }

                processed = detect_anomaly(data)

                # Broadcast to all connected WebSocket clients
                if manager.active_connections:
                    await manager.broadcast(processed)
                    logger.info(f"Broadcasted entry id={entry.id} to WS clients.")

                # Update shared state
                state["health_data"] = processed
                state["anomaly_detected"] = processed.get("alert_level") != "normal"
                state["emergency_level"] = processed.get("alert_level")
                print("state updated",state["health_data"])
                # Small delay to simulate streaming
                await asyncio.sleep(1)  # 1 second per entry (adjust as needed)

        except Exception as e:
            logger.error(f"DB fallback error: {e}", exc_info=True)
            await asyncio.sleep(5)
# import time
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models.exercise import ExerciseEntry
# from app.agents.health.rules import detect_anomaly
# from app.orchestrator.state import OrchestratorState
# from app.agents.health.utils import setup_logger
# import logging
# import asyncio

# logger = setup_logger(__name__)

# def start_db_fallback_listener(state: OrchestratorState, main_loop: asyncio.AbstractEventLoop):
#     logger.warning("⚠ Kafka not available. Switching to DB polling mode...")

#     db = next(get_db())

#     last_id = None

#     while True:
#         try:
#             query = db.query(ExerciseEntry).order_by(ExerciseEntry.id.desc())

#             if last_id:
#                 query = query.filter(ExerciseEntry.id > last_id)

#             latest_entry = query.first()

#             if latest_entry:
#                 last_id = latest_entry.id

#                 data = {
#                     "heart_rate": latest_entry.heart_rate,
#                     "spo2": latest_entry.spo2,
#                     "bp_systolic": latest_entry.bp_systolic,
#                     "bp_diastolic": latest_entry.bp_diastolic,
#                     "timestamp": str(latest_entry.date_created)
#                 }

#                 processed = detect_anomaly(data)

#                 asyncio.run_coroutine_threadsafe(
#                     manager.broadcast(processed),
#                     main_loop
#                 )

#                 state["health_data"] = processed

#                 logger.info("Processed data from DB fallback mode")

#             time.sleep(3)  # Poll every 3 seconds

#         except Exception as e:
#             logger.error(f"DB fallback error: {e}", exc_info=True)
#             time.sleep(5)