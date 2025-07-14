"""This file is part of Project Synapse."""
from fastapi import FastAPI
from app.routers import users

app = FastAPI(
    title="Project Synapse API",
    description="API for Project Synapse.",
    version="0.1.0",
)

app.include_router(users.router)

@app.get("/")
async def root():
    """Root endpoint that returns a greeting message."""
    return {"message": "Welcome to Project Synapse API!"}
