import json
import paho.mqtt.client as mqtt
from config import MQTT_CONFIG
from utils import hop, get_logger


class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.logger = get_logger()

        self.logger.info("Connecting to MQTT broker...")
        self.client.connect(MQTT_CONFIG["broker_address"], MQTT_CONFIG["port"])
        self.logger.info("MQTT Publisher initialized.")

    def publish(self, topic, message):
        try:
            self.client.publish(topic, json.dumps(message))
            self.logger.debug(f"Published message to topic {topic}")
        except Exception as e:
            self.logger.error(f"MQTT Publish Error: {e}")

    def initiate_statement_analyzer(
        self, statement_id, unique_transactions, chunk_size=10
    ):
        index_list = list(hop(0, len(unique_transactions), chunk_size))

        for i in range(len(index_list) - 1):
            transaction_subset = unique_transactions[index_list[i] : index_list[i + 1]]
            formatted_transactions = ",\n".join([f"'{t}'" for t in transaction_subset])
            self.publish(
                MQTT_CONFIG["topic"],
                {"statement_id": statement_id, "transactions": formatted_transactions},
            )
