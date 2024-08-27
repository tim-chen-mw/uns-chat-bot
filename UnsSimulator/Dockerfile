FROM python:3.11-slim

# First install requirements
RUN mkdir /app && chown nobody /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# it is always a good idea to use a non-root user to limit the impact of an attacker gaining access to the running container
USER 65534

# Then copy in source code
# By splitting requirements and source code we can take advantage of docker layer caching
# to get faster docker builds when only the sourcecode changes
COPY main.py /app/
COPY unssimulatorservice /app/unssimulatorservice

WORKDIR /app
CMD ["python", "main.py"]
