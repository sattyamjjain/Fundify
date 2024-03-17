import paho.mqtt.client as mqtt
import json
from langchain_community.llms import Ollama

import sys
import os

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import get_logger
from service import (
    parse_transactions,
    upload_categorized_transactions,
    upload_analyzed_statements,
)
from config import MQTT_CONFIG, OLLAMA_CONFIG


class MQTTSubscriber:
    def __init__(self):
        self.logger = get_logger()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.ollama = Ollama(base_url=OLLAMA_CONFIG['base_url'], model=OLLAMA_CONFIG["model_name"]) if OLLAMA_CONFIG.get('base_url') else Ollama(model=OLLAMA_CONFIG["model_name"])
        print(self.ollama)
        self.client.on_message = self.on_message

    def connect(self):
        self.logger.info("Initiated MQTT Subscriber")
        self.client.connect(MQTT_CONFIG["broker_address"], MQTT_CONFIG["port"])
        self.client.subscribe(MQTT_CONFIG["topic"])
        self.logger.info("MQTT Subscriber connected and listening...")
        self.client.loop_forever()

    def on_message(self, client, userdata, message):
        self.logger.debug(f"Received message on topic {message.topic}")
        payload = json.loads(message.payload)
        self.logger.info(f"Processing message with ID: {payload.get('statement_id')}")
        self.process_message_background(payload)

    def process_message_background(self, payload):
        try:
            _transactions = self._categorize_transactions(payload["transactions"])
            transactions_df = parse_transactions(_transactions)
            upload_categorized_transactions(payload["statement_id"], transactions_df)
            upload_analyzed_statements(payload["statement_id"])
            self.logger.info(
                f"Successfully processed ID: {payload.get('statement_id')}"
            )
        except Exception as e:
            self.logger.error(
                f"Error processing ID: {payload.get('statement_id')}: {e}"
            )

    def _categorize_transactions(self, transactions):
        _PROMPT = f"""
            Please categorize the following expenses. Each expense is followed by its description. 
            Respond with the expense and its respective category, separated by "::", in a list format. 
            Each entry should be separated by a comma and a newline. 
            The categories should be concise, ideally less than 4 words. 

            Here are some examples of the expected format:
                'UPI-UBER INDIA SYSTEMS P-UBERRIDES@HDFCBANK-HDFC0000499-309113902946-UBERRIDE' :: Transportation,
                'MOTHER DAIRY 404 NAN-PAYTMQR28100505010119ZOIRQ1GBS3@PAYTM-PYTM0123456-309886961815-PAYMENT FROM PHONE' :: Dairy,
                'PAI VIHAR-PAYTMQR281005050101161HREFI9S04@PAYTM-PYTM0123456-310268822788-PAYMENT FROM PHONE' :: Restaurant,
                'IRCTC APP UPI-PAYTM-IRCTCAPP@PAYTM-PYTM0123456-347203012804-OID100004097759424,0000347203012804' :: Transportation,
                'ZEE5-PAYTM-0064912@PAYTM-PYTM0123456-311187658794-PAYMENT FROM PHONE,0000311187658794' :: Entertainment,
                'VISION 9 BEAUTY LOUN-Q289494341@YBL-YESB0YBLUPI-346550373218-PAYMENT FROM PHONE' :: Wellness and Beauty,
                ...

            Here are the transactions to categorize:
                {transactions}
            """
        return self.ollama.invoke(_PROMPT)


if __name__ == "__main__":
    subscriber = MQTTSubscriber()
    subscriber.connect()
