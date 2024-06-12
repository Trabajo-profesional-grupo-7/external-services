import os

import requests

from app.schemas.chatbot import ChatIDs
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import SEND_CHAT_INFORMATION_ERROR

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")


def send_chat_information(user_id: int, thread_id: str, assistant_id: str):
    response = requests.post(
        f"{AUTHENTICATION_URL}/users/chat",
        json={
            "user_id": user_id,
            "thread_id": thread_id,
            "assistant_id": assistant_id,
        },
    )

    if response.status_code != 200:
        raise APIException(
            code=SEND_CHAT_INFORMATION_ERROR, msg="Error sending chat information"
        )


def get_preferences(id):
    return requests.get(
        f"{AUTHENTICATION_URL}/users/{id}",
    )


def get_thread_and_assistant_id(user_id: int):
    response = requests.get(f"{AUTHENTICATION_URL}/users/{user_id}/chat")

    chat_data = dict(response.json())

    return ChatIDs.model_construct(
        thread_id=chat_data["thread_id"],
        assistant_id=chat_data["assistant_id"],
    )
