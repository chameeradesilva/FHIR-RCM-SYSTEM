"""
Kafka configuration utilities for the FHIR-RCM system.
"""
import os
import json
import logging
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer, KafkaConsumer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Topics configuration
TOPICS = {
    'patient_intake': {'partitions': 3, 'replication_factor': 1},
    'clinical_data': {'partitions': 3, 'replication_factor': 1},
    'claims': {'partitions': 3, 'replication_factor': 1},
    'payments': {'partitions': 3, 'replication_factor': 1},
    'denials': {'partitions': 3, 'replication_factor': 1},
    'reporting': {'partitions': 3, 'replication_factor': 1},
    'notifications': {'partitions': 3, 'replication_factor': 1},
}

def create_topics():
    """Create Kafka topics if they don't exist."""
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id='fhir-rcm-admin'
        )
        
        # Get existing topics
        existing_topics = admin_client.list_topics()
        
        # Create new topics that don't exist
        new_topics = []
        for topic_name, config in TOPICS.items():
            if topic_name not in existing_topics:
                new_topics.append(NewTopic(
                    name=topic_name,
                    num_partitions=config['partitions'],
                    replication_factor=config['replication_factor']
                ))
        
        if new_topics:
            admin_client.create_topics(new_topics=new_topics)
            logger.info(f"Created topics: {[topic.name for topic in new_topics]}")
        else:
            logger.info("All topics already exist")
            
        admin_client.close()
        return True
    except Exception as e:
        logger.error(f"Error creating Kafka topics: {e}")
        return False

def get_producer(client_id='fhir-rcm-producer'):
    """Get a configured Kafka producer."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            client_id=client_id,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=1
        )
        return producer
    except Exception as e:
        logger.error(f"Error creating Kafka producer: {e}")
        raise

def get_consumer(topics, group_id='fhir-rcm-consumer', auto_offset_reset='earliest'):
    """Get a configured Kafka consumer."""
    try:
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            enable_auto_commit=True,
            auto_commit_interval_ms=5000
        )
        return consumer
    except Exception as e:
        logger.error(f"Error creating Kafka consumer: {e}")
        raise

if __name__ == "__main__":
    # Create topics when script is run directly
    create_topics()