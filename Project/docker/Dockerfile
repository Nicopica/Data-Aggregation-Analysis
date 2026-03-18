FROM python:3.9-slim
WORKDIR /app

COPY flask/server.py .
COPY sql/iot_data.db .

RUN pip install flask
CMD ["python", "server.py"]
