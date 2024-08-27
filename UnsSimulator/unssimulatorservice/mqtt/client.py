import logging
import paho.mqtt.client as mqtt
import ssl
from ..util import settings


class MqttClient:
    """Class to handle connection to a mqtt broker. Low-level abstraction over the Paho library
    
    This class uses the paho mqtt library and manages and uses an instance of paho.mqtt.client.Client.
    The connection to the mqtt broker can be established persistent of clean. To establish a persistent connection, 
    use a mqtt_client_id other than '' in the initializer.
    The Client can initialize multiple subscriptions and the subscriptions are refreshed on re-connections after connection-losses.
    """

    def __init__(self):
        self._client = mqtt.Client(client_id=settings.MQTT_CLIENTID, clean_session=True)
        self._client.on_connect = self._on_connect
        self._client.on_connect_fail = self._on_connect_fail
        
    def connect(self):
        logging.info("Connecting to MQTT broker")
        # Configure TLS without certificate
        self._client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
        self._client.tls_insecure_set(True)  # Allows TLS communication even without a CA certificate
        self._client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        self._client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

    def start(self):
        """Start the MqttClient subscriptions asynchronously in a new thread"""
        self._client.loop_start()

    def stop(self):
        """Stop a running MqttClient and end the connection to the mqtt broker gracefully"""
        self._client.loop_stop()
        self._client.disconnect()
        logging.info("Disconnected MQTT Client.")

    def send_message(self, topic: str, payload: str, qos=1, retain=False):
        """Publish a message to the broker with the payload on the given topic"""
        info = self._client.publish(topic, payload, qos=qos, retain=retain)
        info.wait_for_publish(timeout=10)

    def _on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            logging.error("Connection to MQTT broker was not successful: rc=%d", rc)
            return
        logging.info("Connected to mqtt broker")

    def _on_connect_fail(self, client, userdata):
        logging.error("Failed to connect to MQTT broker")
