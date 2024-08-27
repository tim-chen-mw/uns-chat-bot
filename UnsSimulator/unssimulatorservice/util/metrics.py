"""All metrics provided by the app"""

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Summary
from fastapi import Response

# Each metric should be defined in this place to easily keep track of them
ENDPOINT_DO_SOMETHING = Summary("endpoint_do_something", "Time spent doing something")
DB_INSERT_COUNT = Counter("db_insert_count", "Number of DB inserts done")
# Values for the labels are set when incrementing the counter
# Labels should be low-cardinality (e.g. API endpoint is ok, user id not)
PROCESSED_MQTT_MESSAGES = Counter("processed_mqtt_messages_count", "Number of successfully processed mqtt messages", labelnames=["topic"])
INVALID_MQTT_MESSAGE_COUNT = Counter("invalid_mqtt_message", "Number of invalid mqtt messages", labelnames=["topic"])


def metrics_response():
    """Generate an API Response containing all current metrics in text format"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
