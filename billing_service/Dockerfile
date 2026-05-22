FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python setup_billing_db.py

EXPOSE 5001

CMD ["opentelemetry-instrument","python", "billing_service.py"]