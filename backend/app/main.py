from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the MMA ELO Engine API"}

# Add additional endpoints here