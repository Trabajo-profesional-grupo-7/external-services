import os

import requests

from app.schemas.chatbot import ChatIDs
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import SEND_CHAT_INFORMATION_ERROR

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")
ATTRACTIONS_URL = os.getenv("ATTRACTIONS_URL")
NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL")


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


def get_user_data(id):
    response = requests.get(
        f"{AUTHENTICATION_URL}/users/{id}",
    )
    return response.json()["username"], response.json()["preferences"]


def get_location(latitud, longitud):
    city = None

    response = requests.post(
        f"{ATTRACTIONS_URL}/attractions/nearby/{latitud}/{longitud}/5000"
    )

    attraccions = response.json()

    if attraccions:
        city = attraccions[0]["city"]

    return city


def get_thread_and_assistant_id(user_id: int):
    response = requests.get(f"{AUTHENTICATION_URL}/users/{user_id}/chat")

    chat_data = dict(response.json())

    return ChatIDs.model_construct(
        thread_id=chat_data["thread_id"],
        assistant_id=chat_data["assistant_id"],
    )


def set_up_instructions(username: str, preferences: str, city: str):

    instruction = f"""
    
    You're a tourism expert.

    Make sure to:
    - Call him by his name: {username}
    - Recommend attractions and dining places in {city}.
    - Explain why the user should visit those places.
    - Speak in a friendly, informal manner.
    - Do not ask for or store sensitive personal information.
    - Ensure user data is handled with confidentiality and security.

    Make recommendations to the user considering:
    - They prioritize activities that include only {preferences}.

    The user has already provided all the necessary information and expects direct answers. Here is the user's specific request:
    - City: {city}
    - Preferences: {preferences}

    Please respond directly to any questions about recommendations without asking for any additional information.

    """

    return instruction


def notify_user(user_id: int, assistant_response: str):
    notification_data = {
        "user_id": user_id,
        "title": "New message from gIAn",
        "body": assistant_response,
    }

    return requests.post(
        url=f"{NOTIFICATIONS_URL}/notifications/notify", json=notification_data
    )
