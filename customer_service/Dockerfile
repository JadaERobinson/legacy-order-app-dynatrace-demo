FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5003

CMD ["opentelemetry-instrument","python", "customer_service.py"]