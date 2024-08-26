# semantic-search-service

## Installation

Install Poetry if you havent already, refer to [Poetry Installation](https://python-poetry.org/docs/#installation)

Once you have Poetry installed, you can install the dependencies by running:
```bash
poetry install
```

## Adding packages

You can add packages using Poetry:
```bash
poetry add <package-name>
```


## Environment Variables

copy the .env.example file or the variables below to .env and fill in the required environment variables. IoT has an Azure OpenAI Service for RnD Purposes.

```bash
PYTHONPATH=.
# Azure:
AZURE_OPENAI_ENDPOINT=
OPENAI_API_VERSION=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT_NAME=

MQTT_HOST=
MQTT_PORT=
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_CLIENTID=
MQTT_TOPICS=
MQTT_BASE_TOPIC=
UNS_PUBLISH_PERIOD=

CHAT_API_URL=http://backend:8001




```

## Launch the service

Best use the docker compose file for development, as it comes with an UNS: `docker compose up --build`

You can start the API Service itself using
```bash
python backend/api_server.py
```
You can start the Frontend itself using
```bash
streamlit run frontend/app.py
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your service.

### Building the Image

To build the image, you simply:

```shell
docker build . -t <tag>
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Docker compose
A docker compose has been prepared to run the application with a pgVector database locally. You can run the following command to start the service:

```shell
docker-compose up --build
```

