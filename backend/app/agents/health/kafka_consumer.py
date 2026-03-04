# from kafka import KafkaConsumer, KafkaProducer
# import json
# from rules import detect_anomaly
# from app.orchestrator.state import OrchestratorState


# # Initialize state
# state = OrchestratorState()
# state["health_data"] = {}

# consumer = KafkaConsumer(
#     'health_data',
#     bootstrap_servers='localhost:9092',
#     value_deserializer=lambda m: json.loads(m.decode('utf-8'))
# )

# alert_producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# for message in consumer:
#     data = message.value
#     processed = detect_anomaly(data)
#     alert_producer.send('health_alerts', processed)
#     state["health_data"][processed["timestamp"]] = processed

import json
import logging
import asyncio
from kafka import KafkaConsumer, KafkaProducer
from app.orchestrator.state import OrchestratorState
from app.agents.health.rules import detect_anomaly
from app.agents.health.utils import setup_logger
from app.routers.realtime import manager
from app.agents.health.start_db_fallback_listener import start_db_fallback_listener

logger = setup_logger(__name__)

def start_health_kafka_listener(state: OrchestratorState, main_loop: asyncio.AbstractEventLoop) -> None:
    """
    Starts Kafka listener, applies anomaly detection, and falls back to DB if Kafka not available.
    """
    try:
        consumer = KafkaConsumer(
            "health_data",
            bootstrap_servers="localhost:29092",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True
        )

        alert_producer = KafkaProducer(
            bootstrap_servers="localhost:29092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        logger.info("✅ Health Kafka Listener started successfully.")

        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        for message in consumer:
            try:
                data = message.value
                logger.info(f"Received health data: {data}")
                state["health_metrics"] = data

                processed = detect_anomaly(data)
                logger.info(f"Processed health data: {processed}")

                # Broadcast to WS clients safely
                if main_loop:
                    asyncio.run_coroutine_threadsafe(
                        manager.broadcast(processed),
                        main_loop
                    )
                else:
                    loop.create_task(manager.broadcast(processed))

                # Update orchestrator state
                state["health_data"] = processed
                state["anomaly_detected"] = processed.get("alert_level") != "normal"
                state["emergency_level"] = processed.get("alert_level")

                # Send alert to Kafka topic
                alert_producer.send("health_alerts", processed)

            except Exception as processing_error:
                logger.error(
                    f"Error processing health message: {processing_error}",
                    exc_info=True
                )

    except Exception as kafka_error:
        logger.error(
            "❌ Failed to connect to Kafka. Switching to DB fallback mode.",
            exc_info=True
        )
        try:
            if main_loop is None:
                main_loop = asyncio.get_event_loop()
            # Start DB fallback safely
            asyncio.run_coroutine_threadsafe(
                start_db_fallback_listener(state, manager),
                main_loop
            )
            logger.info("✅ DB fallback listener started.")
        except Exception as fallback_error:
            logger.critical(
                f"Failed to start DB fallback listener: {fallback_error}",
                exc_info=True
            )
# import json
# import logging
# from kafka import KafkaConsumer, KafkaProducer
# from app.orchestrator.state import OrchestratorState
# from app.agents.health.rules import detect_anomaly
# from app.agents.health.utils import setup_logger
# import asyncio
# from app.routers.realtime import manager
# from app.agents.health.start_db_fallback_listener import start_db_fallback_listener


# logger = setup_logger(__name__)




# def start_health_kafka_listener(state: OrchestratorState, main_loop: asyncio.AbstractEventLoop) -> None:
#     """
#     Starts Kafka consumer to listen for health data continuously.

#     This function:
#     - Listens to 'health_data' topic
#     - Applies anomaly detection rules
#     - Clears previous state
#     - Stores only latest health data
#     - Publishes alert to 'health_alerts' topic
#     - Handles exceptions safely

#     Args:
#         state (OrchestratorState): Shared orchestrator state
#     """

#     try:
#         consumer = KafkaConsumer(
#             "health_data",
#             bootstrap_servers="localhost:29092",
#             value_deserializer=lambda m: json.loads(m.decode("utf-8")),
#             auto_offset_reset="latest",
#             enable_auto_commit=True
#         )

#         alert_producer = KafkaProducer(
#             bootstrap_servers="localhost:29092",
#             value_serializer=lambda v: json.dumps(v).encode("utf-8")
#         )

#         logger.info("Health Kafka Listener started successfully.")

#         # Get the event loop (FastAPI runs in asyncio)
#         # loop = asyncio.get_event_loop()
#           # Create a new event loop for this thread
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         for message in consumer:
#             try:
#                 data = message.value
#                 logger.info(f"Received health data: {data}")
#                 state["health_metrics"] = data

#                 # Apply anomaly detection
#                 processed = detect_anomaly(data)
#                 print("Broadcasting to WS:", processed)

#                 # Broadcast to WebSocket clients
                
#                 try:
#                     # asyncio.run(manager.broadcast(processed))
#                     # loop.create_task(manager.broadcast(processed))
#                    # Broadcast to WS clients safely from thread
#                     asyncio.run_coroutine_threadsafe(
#                         manager.broadcast(processed),
#                         main_loop
#                     )
#                 except RuntimeError:
#                     # If already inside event loop
#                     try:
#                         print("Already in event loop, broadcasting directly.")
#                         loop = asyncio.get_event_loop()
#                         loop.create_task(manager.broadcast(processed))
#                     except Exception as e:
#                         logger.exception("Kafka listener failed, starting DB fallback")
#                         # Start DB fallback safely from the same thread
#                         import asyncio
#                         loop = main_loop or asyncio.get_event_loop()
#                         asyncio.run_coroutine_threadsafe(
#                             start_db_fallback_listener(state, manager),
#                             loop
#                         )

#     #             try:
#     #     start_health_kafka_listener(state, main_loop)
#     # except Exception as e:
#     #     import logging
#     #     logger = logging.getLogger("HealthKafkaListener")
#     #     logger.exception("Kafka listener failed, starting DB fallback")
#     #     # Start DB fallback safely from the same thread
#     #     import asyncio
#     #     loop = main_loop or asyncio.get_event_loop()
#     #     asyncio.run_coroutine_threadsafe(
#     #         start_db_fallback_listener(state, manager),
#     #         loop
#     #     )

#                 # ✅ Clear old data and store only latest
#                 state["health_data"] = processed
#                 state["anomaly_detected"] = (
#                     processed.get("alert_level") != "normal"
#                 )
#                 state["emergency_level"] = processed.get("alert_level")

#                 # Send alert to Kafka topic
#                 alert_producer.send("health_alerts", processed)
#                 if processed["alert_level"] == "critical":
#                     send_emergency_sms(
#                              "+971XXXXXXXXX",
#                              "🚨 Critical health emergency detected!"
#                             )

#                 logger.info(f"Updated state with latest health data: {processed}")


#             except Exception as processing_error:
#                 logger.error(
#                     f"Error processing health message: {processing_error}",
#                     exc_info=True
#                 )

#     except Exception as e:
        
#         logger.error("Failed to connect to Kafka. Switching to DB fallback mode.", exc_info=True)

#         # 🔁 Switch to DB fallback mode
#         # asyncio.run_coroutine_threadsafe(
#         #      start_db_fallback_listener(state, manager),
#         #     main_loop
#         #     )
#         # raise