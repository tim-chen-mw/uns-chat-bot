import json
import ssl
import time
import paho.mqtt.client as mqtt
from config.logger import logger
from config.config import MQTT_HOST, MQTT_PASSWORD, MQTT_PORT, MQTT_USERNAME

mqtt_latest_messages = {}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker!")
        client.subscribe("#")
    else:
        logger.error(f"Failed to connect to MQTT broker, return code {rc}")


def on_message(client, userdata, msg):
    try:
        parsed_payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        parsed_payload = msg.payload.decode()

    mqtt_latest_messages[msg.topic] = parsed_payload


def save_snapshot():
    try:
        with open("mqtt_snapshot.json", "w") as f:
            json.dump(mqtt_latest_messages, f, indent=4)
        logger.debug("Saved MQTT snapshot to mqtt_snapshot.json")
    except Exception as e:
        logger.exception(f"Failed to save MQTT snapshot: {e}")


def mqtt_loop():
    client = mqtt.Client()

    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        logger.debug("Connecting to MQTT broker with TLS...")
        client.connect(MQTT_HOST, int(MQTT_PORT), 30)
        logger.debug("MQTT client loop started")
        client.loop_forever()
    except Exception as e:
        logger.exception(f"Failed to start MQTT loop: {e}")


def periodic_snapshot_saver(interval):
    while True:
        save_snapshot()
        time.sleep(interval)
