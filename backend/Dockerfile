FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000


# Set the command to run your application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]