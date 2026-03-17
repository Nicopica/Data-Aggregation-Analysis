FROM python:3.9-slim
WORKDIR /app
COPY ../flask/server.py .
RUN pip install flask
CMD ["python", "server.py"]
