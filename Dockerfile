FROM python:3.9
ENV LISTEN_HOST="127.0.0.1"
ENV LISTEN_PORT=8888
ENV DEBUG=false
ENV CFG_FILE="config/docker.json"
ENV LOG_LEVEL="INFO"
ENV LOG_FILE=""

WORKDIR /app
RUN useradd apiuser -m && chown apiuser /app && pip install virtualenv

COPY requirements.txt /home/apiuser

USER apiuser
RUN virtualenv venv && venv/bin/pip install --upgrade pip setuptools wheel \
    && venv/bin/pip install -r /home/apiuser/requirements.txt

COPY . /app

EXPOSE $LISTEN_PORT
CMD ["venv/bin/python", "main.py"]
