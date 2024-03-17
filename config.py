import yaml
import os
from dotenv import load_dotenv

load_dotenv()


def read_yaml(file_path):
    with open(file_path, "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            return {}


config = read_yaml("config.yaml")

environment = os.getenv("ENVIRONMENT", "docker")
config_file = (
    f"config.{environment}.yaml" if environment != "default" else "config.yaml"
)

if os.path.exists(config_file):
    env_config = read_yaml(config_file)
    config.update(env_config)

MQTT_CONFIG = config["mqtt"]
OLLAMA_CONFIG = config["ollama"]
STORE_CONFIG = config["store"]
