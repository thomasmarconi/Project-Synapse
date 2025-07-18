"""SharePoint Router
This module defines the API endpoints for interacting with SharePoint resources using Microsoft Graph."""
from fastapi import APIRouter
from app.dependencies import graph_client

router = APIRouter(
    prefix="/sharepoint",
    tags=["sharepoint"],
    # dependencies=[Depends(get_token_header)], # Uncomment if you want to enforce token validation
    responses={404: {"description": "Not found"}},
)

@router.get("/sites")
async def get_all_sharepoint_sites():
    """Endpoint to retrieve all SharePoint sites in the tenant."""
    result = await graph_client.sites.get_all_sites.get()
    return result

@router.get("/sites/{site_id}/lists")
async def get_sharepoint_lists(site_id: str):
    """Endpoint to retrieve all SharePoint lists for a specific site."""
    result = await graph_client.sites.by_site_id(site_id).lists.get()
    return result

@router.get("/sites/{site_id}/lists/{list_id}/items")
async def get_sharepoint_list_items(site_id: str, list_id: str):
    """Endpoint to retrieve all items from a specific SharePoint list."""
    result = await graph_client.sites.by_site_id(site_id).lists.by_list_id(list_id).items.get()
    return result