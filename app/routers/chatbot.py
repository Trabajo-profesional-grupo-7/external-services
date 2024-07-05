import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.ext.open_ai import *
from app.services.chatbot import (
    get_location,
    get_thread_and_assistant_id,
    get_user_data,
    notify_user,
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
def create_conversation(user_id: int):
    try:
        create_chatbot_conversation(user_id)
    except HTTPException as e:
        raise e
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)


@router.post(
    "/chatbot/init",
    tags=["Chatbot"],
    status_code=201,
    description="Init conversation",
)
def init_conversation(user_id: int, latitude: str, longitude: str):
    try:
        username, preferences = get_user_data(user_id)
        city = get_location(latitude, longitude)
        chats_ids = get_thread_and_assistant_id(user_id)
        init_chatbot_conversation(user_id, chats_ids, username, preferences, city)
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
def send_message(user_id: int, data: SendMessage):
    chats_ids = get_thread_and_assistant_id(user_id)
    assistant_response = send_user_message(chats_ids, data.message)
    notify_user(user_id, assistant_response.message)
    return assistant_response
