import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.ext.open_ai import *
from app.services.chatbot import (
    get_location,
    get_preferences,
    get_thread_and_assistant_id,
)
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import *

router = APIRouter()
security = HTTPBearer()

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")


@router.post(
    "/chatbot/create",
    tags=["Chatbot"],
    status_code=201,
    description="Create assistant and thread from Open AI",
)
async def create_conversation(user_id: int, latitud: str, longitud: str):
    try:
        preferences = get_preferences(user_id)
        city = get_location(latitud, longitud)
        await create_chatbot_conversation(user_id, preferences, city)
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.post(
    "/chatbot/send_message/{user_id}",
    tags=["Chatbot"],
    status_code=201,
    description="Send message to the assistant",
    response_model=AssistantResponse,
)
async def send_message(user_id: int, data: SendMessage):
    chats_ids = get_thread_and_assistant_id(user_id)
    return await send_user_message(
        chats_ids.thread_id, chats_ids.assistant_id, data.message
    )
