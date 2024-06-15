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

URL = "https://api.openai.com/v1"

HEADER = {
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2",
    "Content-Type": "application/json",
}


async def create_chatbot_conversation(user_id: int, preferences: str, city: str):

    assistant = await client.beta.assistants.create(
        name="LucIA",
        description="Sos un asistente en una aplicación de planificación de viajes y visitas a atracciones.",
        tools=[{"type": "code_interpreter"}],
        instructions=set_up_instructions(preferences, city),
        model="gpt-4-turbo",
    )

    thread = await client.beta.threads.create()

    send_chat_information(user_id, thread.id, assistant.id)


async def send_user_message(thread_id: str, assistant_id: str, text: str):
    message = await client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=text
    )

    return await get_answer(thread_id, assistant_id)


async def get_answer(thread_id: str, assistant_id: str):
    run = await client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    while True:
        runInfo = await client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        )
        if runInfo.completed_at:
            break
        time.sleep(1)

    return await read_response(thread_id)


async def read_response(thread_id: str):
    messages = await client.beta.threads.messages.list(thread_id)
    last_message = messages.data[0]

    return AssistantResponse.model_construct(
        role=last_message.role, message=last_message.content[0].text.value
    )
