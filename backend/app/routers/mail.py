"""Mail management routes for the application."""
import asyncio
import logging
from fastapi import APIRouter
from app.dependencies import graph_client

router = APIRouter(
    prefix="/mail",
    tags=["mail"],
    # dependencies=[Depends(get_token_header)], # Uncomment if you want to enforce token validation
    responses={404: {"description": "Not found"}},
)


@router.get("/messages/all")
async def get_all_mail_messages():
    """Endpoint to retrieve all mail messages for all users."""
    try:
        # Get all users
        all_users = await graph_client.users.get()
        if not all_users.value:
            return {"messages": []}

        # Fetch messages for all users concurrently
        user_ids = [user.id for user in all_users.value]
        message_lists = await asyncio.gather(
            *[get_user_messages(user_id) for user_id in user_ids],
            return_exceptions=True
        )

        # Flatten the list of message lists, filtering out exceptions
        messages = [
            message
            for message_list in message_lists
            if isinstance(message_list, list)
            for message in message_list
        ]

        return {"messages": messages}
    except (ValueError, AttributeError, TypeError) as e:
        return {"error": str(e)}

@router.get("/messages/{user_id}")
async def get_user_messages(user_id: str):
    """Function to get messages for a single user."""
    try:
        user_messages = await graph_client.users.by_user_id(user_id).messages.get()
        return [message for message in user_messages.value]
    except (ValueError, AttributeError, TypeError) as e:
        logging.warning("Failed to fetch messages for user %s: %s", user_id, e)
        return []  # Return empty list if user messages fail, don't fail entire operation
