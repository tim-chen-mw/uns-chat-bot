FROM python:3.12-slim

# Set SHELL option -o pipefail
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Set WORKDIR before COPY
WORKDIR /src

# Install Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Poetry files and install dependencies
COPY pyproject.toml poetry.lock /src/
RUN poetry install --no-root

# Copy application source code
COPY src /src

EXPOSE 8502

ENTRYPOINT ["poetry", "run", "streamlit", "run", "frontend/app.py", "--server.port=8502", "--server.address=0.0.0.0"]
