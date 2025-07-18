"""User management routes for the application."""

from fastapi import APIRouter
from app.dependencies import graph_client

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)], # Uncomment if you want to enforce token validation
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_users():
    """Endpoint to retrieve all user information in the tenant."""
    try:
        result = await graph_client.users.get()
        return {"users": list(result.value)}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": str(e)}


@router.get("/display-names")
async def get_all_users_display_names():
    """Endpoint to retrieve all users in the tenant."""
    try:
        result = await graph_client.users.get()
        return {"users": [user.display_name for user in result.value]}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": str(e)}


@router.get("/ids")
async def get_all_users_ids():
    """Endpoint to retrieve all user IDs in the tenant."""
    try:
        result = await graph_client.users.get()
        return {"user_ids": [user.id for user in result.value]}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": str(e)}


@router.get("/user-principal-names")
async def get_all_users_user_principal_names():
    """Endpoint to retrieve all user principal names in the tenant."""
    try:
        result = await graph_client.users.get()
        return {
            "user_principal_names": [user.user_principal_name for user in result.value]
        }
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": str(e)}
