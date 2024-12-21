FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY . .
EXPOSE 5050

CMD ["bash", "-c", "python3 -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 5050"]
