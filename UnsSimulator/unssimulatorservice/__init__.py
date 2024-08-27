import logging
from pythonjsonlogger import jsonlogger
from .api.app import run_api
from .services.mainservice import MainService
from .services.update_service import UnsUpdateService
from .mqtt.publisher import MqttPublisher
from .util.settings import LOG_MODE, LOG_LEVEL
from threading import Event


def run():
    """Main entrypoint of the app"""
    # First configure logging
    init_logging()

    thread_event = Event()
    # Then init all services
    mqtt = MqttPublisher()
    unsupdateservice = UnsUpdateService(thread_event,mqtt)
    mainservice = MainService(mqtt)
    # Finally run mqtt and api
    mqtt.connect_and_start() # Launch MQTT in the background
    unsupdateservice.start()
    run_api(mainservice) # API stays in the foreground and blocks


def init_logging():
    # Allow changing the minimum log level at startup
    level = getattr(logging,LOG_LEVEL.upper(),None)
    if not level:
        level = logging.INFO

    # Configure logging mode
    if LOG_MODE == "json":
        logger = logging.getLogger()
        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter()
        logHandler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(logHandler)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', level=level)
