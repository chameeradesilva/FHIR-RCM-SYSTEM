import json
import logging
import requests
from producers import send_message

logging.basicConfig(level=logging.INFO)

def fetch_fhir_patient(patient_id):
    """
    Fetch a FHIR Patient resource from the HAPI FHIR test server.
    """
    url = f"https://hapi.fhir.org/baseR4/Patient/{patient_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        patient_data = response.json()
        logging.info("Successfully fetched FHIR patient data.")
        return patient_data
    except Exception as e:
        logging.error(f"Error fetching FHIR patient: {e}")
        return None

def main():
    # Fetch a FHIR Patient resource.
    patient_data = fetch_fhir_patient("44786036")
    if patient_data:
        # Send the data to a Kafka topic.
        send_message("patient_intake_fhir", patient_data)

if __name__ == "__main__":
    main()