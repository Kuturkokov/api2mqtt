from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Variables:
    """This is for all the changing variables used by the process"""
    MQTT_SERVER = getenv("MQTT_SERVER", None)
    MQTT_USER = getenv("MQTT_USER", None)
    MQTT_PASS = getenv("MQTT_PASS", None)
    MQTT_PORT = int(getenv("MQTT_PORT", 1883))
    SECRET_KEY = getenv("SECRET_KEY")
    LOG_AGE = int(getenv("LOG_AGE", 15))
    REG_OPEN = getenv("REG_OPEN", "false").lower() in ('true', '1', 't')

variables = Variables
