import json
import time
import random
import logging
from kafka import KafkaProducer
from typing import Callable, Dict, List

from app.services.health_data_gen import (
    generate_normal_health_data,
    generate_slight_variation_health_data,
    generate_critical_health_data,
    generate_exercise_health_data
)

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------
# Kafka Producer Configuration
# -------------------------------
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=10,
    retries=3
)

TOPIC_NAME = "health_data"

# -------------------------------
# Context Mapping
# -------------------------------
HEALTH_GENERATORS: Dict[str, Callable[..., List[Dict]]] = {
    "normal": generate_normal_health_data,
    "slight_variation": generate_slight_variation_health_data,
    "critical": generate_critical_health_data,
    "exercise": generate_exercise_health_data,
}


def stream_health_data(interval_sec: int = 1) -> None:
    """
    Continuously generate health data and stream to Kafka topic.
    """

    try:
        logger.info("Starting Health Data Stream...")

        while True:
            # Randomly select a health context
            context = random.choice(list(HEALTH_GENERATORS.keys()))
            generator = HEALTH_GENERATORS[context]

            # Generate small batch (1 minute data)
            data_batch = generator(minutes=1, interval_sec=30)

            for data_point in data_batch:
                data_point["context"] = context

                producer.send(TOPIC_NAME, value=data_point)
                logger.info(f"Sent to Kafka ({context}): {data_point}")

                time.sleep(interval_sec)

    except KeyboardInterrupt:
        logger.info("Streaming stopped manually.")

    except Exception as e:
        logger.exception(f"Error in Kafka Producer: {e}")

    finally:
        producer.flush()
        producer.close()
        logger.info("Kafka producer closed.")


if __name__ == "__main__":
    stream_health_data()
