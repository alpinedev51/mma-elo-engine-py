from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import fighters_router, events_router, elo_records_router, fights_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mma-elo-engine-frontend.vercel.app", "https://mma-elo-engine-py.vercel.app", "https://mma.marmotspace.com"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"]
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Welcome to the MMA ELO Engine API"}

app.include_router(fighters_router)
app.include_router(events_router)
app.include_router(elo_records_router)
app.include_router(fights_router)

