"""This file is part of Project Synapse."""

import os
from typing import Annotated
from azure.identity.aio import ClientSecretCredential
from msgraph.graph_service_client import GraphServiceClient
from dotenv import load_dotenv
from fastapi import Header, HTTPException


load_dotenv()

scopes = ["https://graph.microsoft.com/.default"]

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
    raise ValueError("Missing required Azure credentials in environment variables")

# azure.identity
credential = ClientSecretCredential(
    tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
graph_client = GraphServiceClient(credential, scopes)


async def get_token_header(x_token: Annotated[str, Header()]):
    """Dependency to check the X-Token header."""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
