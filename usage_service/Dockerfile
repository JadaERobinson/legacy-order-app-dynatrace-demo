FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python setup_usage_db.py

EXPOSE 5002

CMD ["opentelemetry-instrument","python", "usage_service.py"]

