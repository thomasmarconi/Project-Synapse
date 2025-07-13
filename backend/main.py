"""This is the main api app file of Project Synapse."""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint that returns a greeting message."""
    return {"message": "Hello World"}
