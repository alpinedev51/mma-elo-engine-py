# FastAPI Backend

This repository contains a FastAPI backend that can be run with Uvicorn.

## Initialization

### Scraping

- Go to `app` directory of backend project.
- `scrapy crawl ufc_spider`
- This will take a while to run (~10 minutes).
- `docker exec -w /app/app backend_service scrapy crawl ufc_spider`

### Calculating Elo

- Go to root directory of backend project.
- `python -m app.elo_engine.update_db_elo`
- This shouldn't take very long (<15 seconds).
- `docker exec backend_service python -m app.elo_engine.update_db_elo`

## Requirements

- Python 3.10+
- Install dependencies:  

    ```bash
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```
