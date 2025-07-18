"""
OneDrive Router
This module defines the API endpoints for interacting
with OneDrive resources using Microsoft Graph.
"""

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


@router.get("/users/{user_id}")
async def get_user_onedrive(user_id: str):
    """Endpoint to retrieve the OneDrive information for a specific user."""
    try:
        result = await graph_client.users.by_user_id(user_id).drive.get()
        if result:
            return {
                "id": result.id,
                "name": result.name,
                "drive_type": result.drive_type,
                "owner": (
                    result.owner.user.display_name
                    if result.owner and result.owner.user
                    else None
                ),
                "quota": (
                    {
                        "total": result.quota.total if result.quota else None,
                        "used": result.quota.used if result.quota else None,
                        "remaining": result.quota.remaining if result.quota else None,
                    }
                    if result.quota
                    else None
                ),
                "web_url": result.web_url,
            }
        return {"error": "Drive not found for user"}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve OneDrive information: {str(e)}"}


@router.get("/users/{user_id}/items/root")
async def get_user_onedrive_items_root(user_id: str):
    """Endpoint to retrieve all items in the OneDrive of a specific user."""
    try:
        # Use the correct syntax to get root folder children
        root_drive = await get_user_onedrive(user_id)
        items = (
            await graph_client.drives.by_drive_id(root_drive["id"])
            .items.by_drive_item_id("root")
            .children.get()
        )

        if items and items.value:
            return {
                "items": [
                    {
                        "id": item.id,
                        "name": item.name,
                        "size": item.size,
                        "created_datetime": item.created_date_time,
                        "modified_datetime": item.last_modified_date_time,
                        "web_url": item.web_url,
                        "folder": item.folder is not None,
                        "file": item.file is not None,
                    }
                    for item in items.value
                ]
            }
        return {"items": []}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve OneDrive items: {str(e)}"}


@router.get("/users/{user_id}/items/all")
async def get_user_onedrive_items_all(user_id: str):
    """Endpoint to retrieve all items in the OneDrive of a specific user."""
    try:
        # Get the user's drive information first
        root_drive = await get_user_onedrive(user_id)

        if "error" in root_drive:
            return root_drive

        drive_id = root_drive["id"]
        all_items = []

        # Recursive function to get all items from a folder and its subfolders
        async def get_items_recursive(
            drive_id: str, item_id: str = "root", path: str = ""
        ):
            try:
                # Get children of the current folder
                children = (
                    await graph_client.drives.by_drive_id(drive_id)
                    .items.by_drive_item_id(item_id)
                    .children.get()
                )

                if children and children.value:
                    for item in children.value:
                        # Add current item to results
                        item_data = {
                            "id": item.id,
                            "name": item.name,
                            "size": item.size,
                            "created_datetime": item.created_date_time,
                            "modified_datetime": item.last_modified_date_time,
                            "web_url": item.web_url,
                            "folder": item.folder is not None,
                            "file": item.file is not None,
                            "path": f"{path}/{item.name}" if path else item.name,
                        }
                        all_items.append(item_data)

                        # If this is a folder, recursively get its contents
                        if item.folder is not None:
                            await get_items_recursive(
                                drive_id,
                                item.id,
                                f"{path}/{item.name}" if path else item.name,
                            )

            except (ValueError, AttributeError, TypeError) as e:
                # Log the error but continue processing other items
                print(f"Error processing folder {path}: {str(e)}")

        # Start the recursive traversal from the root
        await get_items_recursive(drive_id)

        return {"items": all_items, "total_count": len(all_items)}

    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve all OneDrive items: {str(e)}"}


@router.get("/drives/{drive_id}")
async def get_drive_by_id(drive_id: str):
    """Endpoint to retrieve a specific drive by its ID."""
    try:
        result = await graph_client.drives.by_drive_id(drive_id).get()
        if result:
            return {
                "id": result.id,
                "name": result.name,
                "drive_type": result.drive_type,
                "owner": (
                    result.owner.user.display_name
                    if result.owner and result.owner.user
                    else None
                ),
                "quota": (
                    {
                        "total": result.quota.total if result.quota else None,
                        "used": result.quota.used if result.quota else None,
                        "remaining": result.quota.remaining if result.quota else None,
                    }
                    if result.quota
                    else None
                ),
                "web_url": result.web_url,
            }
        return {"error": "Drive not found"}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve drive information: {str(e)}"}


@router.get("/drives/{drive_id}/items/root")
async def get_drive_items_root(drive_id: str):
    """Endpoint to retrieve all items in a specific drive."""
    try:
        # Use the correct syntax to get root folder children
        result = (
            await graph_client.drives.by_drive_id(drive_id)
            .items.by_drive_item_id("root")
            .children.get()
        )

        if result and result.value:
            return {
                "items": [
                    {
                        "id": item.id,
                        "name": item.name,
                        "size": item.size,
                        "created_datetime": item.created_date_time,
                        "modified_datetime": item.last_modified_date_time,
                        "web_url": item.web_url,
                        "folder": item.folder is not None,
                        "file": item.file is not None,
                    }
                    for item in result.value
                ]
            }
        return {"items": []}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve drive items: {str(e)}"}


@router.get("/drives/{drive_id}/items/all")
async def get_drive_items_all(drive_id: str):
    """Endpoint to retrieve all items in a specific drive recursively."""
    try:
        # First verify the drive exists
        drive_info = await graph_client.drives.by_drive_id(drive_id).get()
        if not drive_info:
            return {"error": "Drive not found"}

        all_items = []

        # Recursive function to get all items from a folder and its subfolders
        async def get_items_recursive(
            drive_id: str, item_id: str = "root", path: str = ""
        ):
            try:
                # Get children of the current folder
                children = (
                    await graph_client.drives.by_drive_id(drive_id)
                    .items.by_drive_item_id(item_id)
                    .children.get()
                )

                if children and children.value:
                    for item in children.value:
                        # Add current item to results
                        item_data = {
                            "id": item.id,
                            "name": item.name,
                            "size": item.size,
                            "created_datetime": item.created_date_time,
                            "modified_datetime": item.last_modified_date_time,
                            "web_url": item.web_url,
                            "folder": item.folder is not None,
                            "file": item.file is not None,
                            "path": f"{path}/{item.name}" if path else item.name,
                        }
                        all_items.append(item_data)

                        # If this is a folder, recursively get its contents
                        if item.folder is not None:
                            await get_items_recursive(
                                drive_id,
                                item.id,
                                f"{path}/{item.name}" if path else item.name,
                            )

            except (ValueError, AttributeError, TypeError) as e:
                # Log the error but continue processing other items
                print(f"Error processing folder {path}: {str(e)}")

        # Start the recursive traversal from the root
        await get_items_recursive(drive_id)

        return {
            "drive_id": drive_id,
            "drive_name": drive_info.name,
            "drive_type": drive_info.drive_type,
            "items": all_items,
            "total_count": len(all_items),
        }

    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve all drive items: {str(e)}"}


@router.get("/sites/{site_id}/drive")
async def get_site_onedrive(site_id: str):
    """Endpoint to retrieve the OneDrive information for a specific SharePoint site."""
    try:
        result = await graph_client.sites.by_site_id(site_id).drive.get()
        if result:
            return {
                "id": result.id,
                "name": result.name,
                "drive_type": result.drive_type,
                "owner": (
                    result.owner.user.display_name
                    if result.owner and result.owner.user
                    else None
                ),
                "quota": (
                    {
                        "total": result.quota.total if result.quota else None,
                        "used": result.quota.used if result.quota else None,
                        "remaining": result.quota.remaining if result.quota else None,
                    }
                    if result.quota
                    else None
                ),
                "web_url": result.web_url,
            }
        return {"error": "Drive not found for site"}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve site OneDrive information: {str(e)}"}


@router.get("/sites/{site_id}/drive/items/root")
async def get_site_onedrive_items_root(site_id: str):
    """Endpoint to retrieve all items in the root OneDrive folder of a specific SharePoint site."""
    try:
        # First get the site drive information to get the drive ID
        site_drive = await get_site_onedrive(site_id)

        if "error" in site_drive:
            return site_drive

        drive_id = site_drive["id"]

        # Use the correct syntax to get root folder children
        result = (
            await graph_client.drives.by_drive_id(drive_id)
            .items.by_drive_item_id("root")
            .children.get()
        )

        if result and result.value:
            return {
                "items": [
                    {
                        "id": item.id,
                        "name": item.name,
                        "size": item.size,
                        "created_datetime": item.created_date_time,
                        "modified_datetime": item.last_modified_date_time,
                        "web_url": item.web_url,
                        "folder": item.folder is not None,
                        "file": item.file is not None,
                    }
                    for item in result.value
                ]
            }
        return {"items": []}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve site OneDrive items: {str(e)}"}


@router.get("/sites/{site_id}/drive/items/all")
async def get_site_onedrive_items_all(site_id: str):
    """Endpoint to retrieve all items in the OneDrive of a specific SharePoint site recursively."""
    try:
        # First get the site drive information to get the drive ID
        site_drive = await get_site_onedrive(site_id)

        if "error" in site_drive:
            return site_drive

        drive_id = site_drive["id"]
        all_items = []

        # Recursive function to get all items from a folder and its subfolders
        async def get_items_recursive(
            drive_id: str, item_id: str = "root", path: str = ""
        ):
            try:
                # Get children of the current folder
                children = (
                    await graph_client.drives.by_drive_id(drive_id)
                    .items.by_drive_item_id(item_id)
                    .children.get()
                )

                if children and children.value:
                    for item in children.value:
                        # Add current item to results
                        item_data = {
                            "id": item.id,
                            "name": item.name,
                            "size": item.size,
                            "created_datetime": item.created_date_time,
                            "modified_datetime": item.last_modified_date_time,
                            "web_url": item.web_url,
                            "folder": item.folder is not None,
                            "file": item.file is not None,
                            "path": f"{path}/{item.name}" if path else item.name,
                        }
                        all_items.append(item_data)

                        # If this is a folder, recursively get its contents
                        if item.folder is not None:
                            await get_items_recursive(
                                drive_id,
                                item.id,
                                f"{path}/{item.name}" if path else item.name,
                            )

            except (ValueError, AttributeError, TypeError) as e:
                # Log the error but continue processing other items
                print(f"Error processing folder {path}: {str(e)}")

        # Start the recursive traversal from the root
        await get_items_recursive(drive_id)

        return {
            "site_id": site_id,
            "drive_id": drive_id,
            "drive_name": site_drive["name"],
            "drive_type": site_drive["drive_type"],
            "items": all_items,
            "total_count": len(all_items),
        }

    except (ValueError, AttributeError, TypeError) as e:
        return {"error": f"Failed to retrieve all site OneDrive items: {str(e)}"}
