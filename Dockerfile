FROM python:3.9
LABEL owner=albertocurro


WORKDIR /app
COPY requirements.txt /tmp

RUN useradd apiuser && chown user /app && apt update -y && pip install -r requirements.txt
USER apiuser

COPY . /app

EXPOSE 8888
ENTRYPOINT ["entrypoint.sh"]

