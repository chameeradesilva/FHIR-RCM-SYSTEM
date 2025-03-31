"""
Script to create Kafka topics for the FHIR-RCM system.
Run this script to initialize all required Kafka topics.
"""
import os
import sys
import logging
from pathlib import Path
from kafka_setup.kafka_config import create_topics

# Add the parent directory to sys.path to import kafka_config
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("Initializing Kafka topics for FHIR-RCM system...")
    
    # Create topics
    success = create_topics()
    
    if success:
        logger.info("Kafka topics created or verified successfully")
    else:
        logger.error("Failed to create Kafka topics")
        sys.exit(1)
    
    logger.info("Kafka setup complete")