import requests
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.ext.open_ai import *
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

router = APIRouter()
security = HTTPBearer()

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")


@router.post(
    "/chatbot/init",
    tags=["Chatbot"],
    status_code=201,
    description="Start conversation",
    response_model=Conversation,
)
async def init_conversation(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    user_data = requests.get(
        f"{AUTHENTICATION_URL}/users",
        headers={"Authorization": f"Bearer {credentials.credentials}"},
    )
    return await init_chatbot_conversation(user_data.json()["preferences"])


@router.post(
    "/chatbot/send_message",
    tags=["Chatbot"],
    status_code=201,
    description="Send message to the assistant",
    response_model=AssistantResponse,
)
async def send_message(data: SendMessage):

    return await send_user_message(data.thread_id, data.assistant_id, data.message)
