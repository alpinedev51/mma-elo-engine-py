FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app/main.py", "app/mma_scraper", "app/elo_engine/update_db_elo.py", "app/database.py", "app/create_database.py"]