import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from config import logger, variables


def get_result(topic):
    if variables.MQTT_USER:
        auth = {'username': variables.MQTT_USER, 'password': variables.MQTT_PASS}
    else:
        auth = {}
    msg = subscribe.simple(topics=topic,
                           hostname=variables.MQTT_SERVER,
                           port=variables.MQTT_PORT,
                           auth=auth,
                           client_id="api_server")
    msg=str(msg.payload.decode("utf-8"))
    return msg


def post_msg(topic='', mssg='', rtn=True):
    try:
        client = mqtt.Client("api_server")
        if variables.MQTT_USER:
            client.username_pw_set(username=variables.MQTT_USER, password=variables.MQTT_PASS)
        client.connect(host=variables.MQTT_SERVER, port=variables.MQTT_PORT)
        client.publish(topic, mssg, retain=rtn)
        client.disconnect()
        return "ok"
    except Exception as mqtt_error:
        logger.error(str(mqtt_error))
        return "failed"
