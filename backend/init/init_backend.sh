#!/bin/bash

echo "Initializing database relations..."
python3 ../init_db.py

echo "Starting the Scrapy crawler..."
scrapy crawl ufc_crawler

echo "Updating Elo ratings..."

echo "Starting the backend server..."
uvicorn app.main:app --host 0.0.0.0 --port 5050
