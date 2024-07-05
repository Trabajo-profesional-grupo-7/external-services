import os
import time

import openai
import requests
from openai import AsyncOpenAI, OpenAI

from app.schemas.chatbot import *
from app.services.chatbot import send_chat_information, set_up_instructions
from app.utils.api_exception import APIException
from app.utils.constants import *

API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=API_KEY)

ASSISTANT_URL = "https://api.openai.com/v1"
THREADS_ULR = "https://api.openai.com/v1"

HEADER = {
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2",
    "Content-Type": "application/json",
}


def create_chatbot_conversation(user_id: int):

    data = {
        "name": "IAn",
        "description": "You're an assistant in a travel planning and attraction visiting app.",
        "tools": [{"type": "code_interpreter"}],
        "model": "gpt-4-turbo",
        "temperature": 0.2,
    }

    assistant_response = requests.post(
        f"{ASSISTANT_URL}/assistants", json=data, headers=HEADER
    )

    thread_response = requests.post(f"{THREADS_ULR}/threads", headers=HEADER)

    if assistant_response.status_code == 200 and thread_response.status_code == 200:
        assistant_id = assistant_response.json()["id"]
        thread_id = thread_response.json()["id"]
    else:
        raise APIException(
            code=OPENAI_ERROR,
            msg="Create assistant or thread error",
        )

    send_chat_information(user_id, thread_id, assistant_id)


def init_chatbot_conversation(
    user_id: int,
    chats_ids: ChatIDs,
    username: str,
    preferences: str,
    city: str,
):
    instruction = set_up_instructions(username, preferences, city)
    data = {"instructions": instruction}

    assistant_config = requests.post(
        f"{ASSISTANT_URL}/assistants/{chats_ids.assistant_id}",
        json=data,
        headers=HEADER,
    )

    if assistant_config.status_code != 200:
        raise APIException(code=OPENAI_ERROR, msg="Error assistant configuration")
    send_chat_information(user_id, chats_ids.thread_id, chats_ids.assistant_id)


def send_user_message(chats_ids: ChatIDs, text: str):

    payload = {
        "role": "user",
        "content": text,
    }

    message_in_thread = requests.post(
        url=f"{THREADS_ULR}/threads/{chats_ids.thread_id}/messages",
        json=payload,
        headers=HEADER,
    )

    payload = {"assistant_id": chats_ids.assistant_id}
    thread_runs = requests.post(
        url=f"{THREADS_ULR}/threads/{chats_ids.thread_id}/runs",
        json=payload,
        headers=HEADER,
    )

    if message_in_thread.status_code != 200 or thread_runs.status_code != 200:
        raise APIException(code=OPENAI_ERROR, msg="Error running thread")

    return get_answer(chats_ids.thread_id, thread_runs.json()["id"])


def get_answer(thread_id: str, run_id: str):

    while True:
        response = requests.get(
            url=f"{THREADS_ULR}/threads/{thread_id}/runs/{run_id}", headers=HEADER
        )

        if response.status_code != 200:
            raise APIException(code=OPENAI_ERROR, msg="Error waiting response")

        if response.json()["completed_at"]:
            break
        time.sleep(1)

    return read_response(thread_id)


def read_response(thread_id: str):

    assistant_response = requests.get(
        url=f"{THREADS_ULR}/threads/{thread_id}/messages", headers=HEADER
    )

    if assistant_response.status_code != 200:
        raise APIException(code=OPENAI_ERROR, msg="Error in message list from Open AI")

    messages = assistant_response.json()
    assistant_response = messages["data"][0]["content"][0]["text"]["value"]

    return AssistantResponse.model_construct(
        role="Assistant", message=assistant_response
    )
