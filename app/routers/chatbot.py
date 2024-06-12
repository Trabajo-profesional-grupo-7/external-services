import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.ext.open_ai import *
from app.services.chatbot import get_preferences, get_thread_and_assistant_id
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import *

router = APIRouter()
security = HTTPBearer()

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")


@router.post(
    "/chatbot/init",
    tags=["Chatbot"],
    status_code=201,
    description="Start conversation",
)
async def init_conversation(
    user_id: int,
):
    try:
        user_data = get_preferences(user_id)
        await init_chatbot_conversation(user_id, user_data.json()["preferences"])
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
