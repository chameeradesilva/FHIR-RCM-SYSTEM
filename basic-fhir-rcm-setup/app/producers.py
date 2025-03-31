import json
import logging
from kafka import KafkaProducer

# Set up basic logging.
logging.basicConfig(level=logging.INFO)

# Kafka broker address (adjust if needed)
KAFKA_BROKER = "localhost:9092"

# Create a Kafka producer with JSON serialization.
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

def send_message(topic, message):
    """
    Send a message to the specified Kafka topic.
    """
    try:
        producer.send(topic, message)
        producer.flush()
        logging.info(f"Message sent to topic '{topic}': {message}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")

# For testing purposes.
if __name__ == "__main__":
    test_message = {"example": "This is a new test message"}
    send_message("test_topic", test_message)
