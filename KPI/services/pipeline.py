from KPI.services.ingestor import DataIngestor
from KPI.services.processing_engine import ProcessingEngine
from KPI.services.producer import MessageProducer
from KPI.models import KPI

def run_data_pipeline(file_path, equation, kpi_id):
    # Initialize the data ingestion component
    ingestor = DataIngestor(file_path)
    # Set up the processing engine with the provided equation
    processing_engine = ProcessingEngine(equation)
    # Fetch the specific KPI to link results
    kpi = KPI.objects.get(id=kpi_id)
    # Initialize the message producer to store processed results
    producer = MessageProducer(kpi)

    # Read, process, and store each message
    for message in ingestor.read_messages():
        processed_value = processing_engine.process(message)
        result = producer.produce_message(message["asset_id"], processed_value)
        print("Processed Message:", result)
