import json
import logging
from kafka import KafkaConsumer
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

# Kafka and MongoDB configurations
KAFKA_BROKER = "localhost:9092"
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client.healthcare  # Using "healthcare" database

def save_to_mongo(collection, data):
    """
    Save data to a MongoDB collection.
    """
    try:
        result = db[collection].insert_one(data)
        logging.info(f"Data saved to MongoDB collection '{collection}' with id {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error saving to MongoDB: {e}")

def consume_topic(topic):
    """
    Consume messages from a Kafka topic and save them to MongoDB.
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    logging.info(f"Listening for messages on topic '{topic}'...")
    for message in consumer:
        logging.info(f"Received message from topic '{topic}': {message.value}")
        save_to_mongo("patient", message.value)

if __name__ == "__main__":
    consume_topic("patient_intake_fhir")