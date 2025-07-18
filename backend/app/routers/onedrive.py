"""OneDrive Router
This module defines the API endpoints for interacting with OneDrive resources using Microsoft Graph."""
from fastapi import APIRouter
from app.dependencies import graph_client

router = APIRouter(
    prefix="/onedrive",
    tags=["onedrive"],
    # dependencies=[Depends(get_token_header)], # Uncomment if you want to enforce token validation
    responses={404: {"description": "Not found"}},
)

"""
    These are all the possible endpoints to retrieve items in OneDrive:
    GET /drives/{drive-id}/items/{item-id}
    GET /drives/{drive-id}/root:/{item-path}
    GET /groups/{group-id}/drive/items/{item-id}
    GET /groups/{group-id}/drive/root:/{item-path}
    GET /me/drive/items/{item-id}
    GET /me/drive/root:/{item-path}
    GET /sites/{site-id}/drive/items/{item-id}
    GET /sites/{site-id}/drive/root:/{item-path}
    GET /sites/{site-id}/lists/{list-id}/items/{item-id}/driveItem
    GET /users/{user-id}/drive/items/{item-id}
    GET /users/{user-id}/drive/root:/{item-path}
"""

@router.get("/users/{user_id}/drive")
async def get_user_onedrive(user_id: str):
    """Endpoint to retrieve the OneDrive information for a specific user."""
    result = await graph_client.users.by_user_id(user_id).drive.get()
    return result

@router.get("/users/{user_id}/drive/items")
async def get_user_onedrive_items(user_id: str):
    """Endpoint to retrieve all items in the OneDrive of a specific user."""

    result = await graph_client.users.by_user_id(user_id).drive.items.get()
    return result

@router.get("/sites/{site_id}/drive")
async def get_site_onedrive(site_id: str):
    """Endpoint to retrieve the OneDrive information for a specific SharePoint site."""
    result = await graph_client.sites.by_site_id(site_id).drive.get()
    return result

@router.get("/sites/{site_id}/drive/items")
async def get_site_onedrive_items(site_id: str):
    """Endpoint to retrieve all items in the OneDrive of a specific SharePoint site."""
    result = await graph_client.sites.by_site_id(site_id).drive.items.get()
    return result