from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import threading
from typing import Dict, Any

from app.orchestrator.state import OrchestratorState
from app.agents.health.kafka_consumer import start_health_kafka_listener


# Create router instance
router = APIRouter()

# Shared orchestrator state
state = OrchestratorState()
state["health_data"] = {}

# Lock to prevent race conditions (important for threading)
state_lock = threading.Lock()


# -------------------------------
# Start Kafka Listener Function
# -------------------------------
def start_kafka_background_listener():
    """
    Starts Kafka listener in a background thread.
    This will continuously consume health data
    and update shared orchestrator state.
    """
    print("Starting Kafka Listener Thread...")
    listener_thread = threading.Thread(
        target=start_health_kafka_listener,
        args=(state,),
        daemon=True
    )
    listener_thread.start()


# -------------------------------
# REST Endpoint (Optional - Debug)
# -------------------------------
@router.get("/latest")
def get_latest_health_data() -> Dict[str, Any]:
    """
    Returns the latest health data (for debugging/testing).
    """
    with state_lock:
        return state.get("health_data", {})


# -------------------------------
# WebSocket Endpoint
# -------------------------------
@router.websocket("/ws/health")
async def websocket_endpoint(ws: WebSocket):
    """
    WebSocket endpoint to stream health data
    to frontend in real-time.
    """
    await ws.accept()

    try:
        while True:
            with state_lock:
                health_data = state.get("health_data")

            if health_data:
                await ws.send_json(health_data)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print(f"WebSocket Error: {e}")
        await ws.close()

# from fastapi import FastAPI, WebSocket
# import asyncio
# import threading

# from app.orchestrator.state import OrchestratorState
# from app.agents.health.kafka_listener import start_health_kafka_listener


# app = FastAPI()

# # Shared orchestrator state
# state = OrchestratorState()
# state["health_data"] = {}


# # ✅ Start Kafka listener in background when API starts
# @app.on_event("startup")
# def startup_event():
#     listener_thread = threading.Thread(
#         target=start_health_kafka_listener,
#         args=(state,),
#         daemon=True
#     )
#     listener_thread.start()


# @app.websocket("/ws/health")
# async def websocket_endpoint(ws: WebSocket):
#     """
#     WebSocket endpoint to stream latest health data
#     to frontend in real-time.
#     """
#     await ws.accept()

#     try:
#         while True:
#             # Send latest health data every second
#             if state.get("health_data"):
#                 await ws.send_json(state["health_data"])

#             await asyncio.sleep(1)

#     except Exception as e:
#         await ws.close()