from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from pydantic import BaseModel


class Conversation(BaseModel):
    assistant_id: str
    thread_id: str


class ChatIDs(BaseModel):
    thread_id: str
    assistant_id: str


class SendMessage(BaseModel):
    message: str


class Thread(BaseModel):
    thread_id: str


class AssistantResponse(BaseModel):
    role: str
    message: str
