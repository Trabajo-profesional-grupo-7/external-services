import os
import time

import openai
from openai import AsyncOpenAI, OpenAI

from app.schemas.chatbot import *
from app.services.chatbot import send_chat_information

API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=API_KEY)


async def init_chatbot_conversation(user_id: int, preferences: str):
    assistant = await client.beta.assistants.create(
        name="LucIA",
        instructions=f"You are an assistant in a travel application, where attractions are recommended, plans are made and trips are planned. You must help people with their questions. Your responses must be 100% based in these {preferences}.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-16k",
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
