"""This file is part of Project Synapse."""
import os
from fastapi import FastAPI
from azure.identity.aio import ClientSecretCredential
from msgraph.graph_service_client import GraphServiceClient
from dotenv import load_dotenv

load_dotenv()

scopes = ["https://graph.microsoft.com/.default"]

TENANT_ID = os.getenv('AZURE_TENANT_ID')
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError("Missing required Azure credentials in environment variables")

# azure.identity
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
graph_client = GraphServiceClient(credential, scopes)

app = FastAPI(
    title="Project Synapse API",
    description="API for Project Synapse.",
    version="0.1.0",
)

@app.get("/")
async def root():
    """Root endpoint that returns a greeting message."""
    return {"message": "Hello World"}

@app.get("/emails")
async def get_all_emails():
    """Endpoint to retrieve all emails in the tenant."""
    return {"emails": ["example1@example.com", "example2@example.com"]}

@app.get("/users")
async def get_all_users():
    """Endpoint to retrieve all users in the tenant."""
    try:
        result = await graph_client.users.get()
        return {"users": [user.display_name for user in result.value]}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": str(e)}
