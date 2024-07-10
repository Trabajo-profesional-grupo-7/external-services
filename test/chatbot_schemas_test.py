import unittest
from unittest.mock import Mock, patch

from pydantic import ValidationError

from app.schemas.chatbot import (
    AssistantResponse,
    ChatIDs,
    Conversation,
    SendMessage,
    Thread,
)


class TestConversationSchema(unittest.TestCase):

    def test_conversation_model_valid(self):
        data = {"assistant_id": "assistant_id", "thread_id": "thread_id"}

        conversation = Conversation(**data)
        self.assertEqual(conversation.assistant_id, "assistant_id")
        self.assertEqual(conversation.thread_id, "thread_id")

    def test_conversation_model_missing_fields(self):
        data = {"thread_id": "thread_id"}

        with self.assertRaises(ValidationError):
            Conversation(**data)


class TestChatIDsSchema(unittest.TestCase):

    def test_chat_ids_model_valid(self):
        data = {"thread_id": "thread_id", "assistant_id": "assistant_id"}

        chat_ids = ChatIDs(**data)
        self.assertEqual(chat_ids.thread_id, "thread_id")
        self.assertEqual(chat_ids.assistant_id, "assistant_id")

    def test_chat_ids_model_missing_fields(self):
        data = {"thread_id": "thread_id"}

        with self.assertRaises(ValidationError):
            ChatIDs(**data)


class TestSendMessageSchema(unittest.TestCase):

    def test_send_message_model_valid(self):
        data = {"message": "Hello World!"}

        send_message = SendMessage(**data)
        self.assertEqual(send_message.message, "Hello World!")

    def test_send_message_model_missing_fields(self):
        data = {}

        with self.assertRaises(ValidationError):
            SendMessage(**data)


class TestThreadSchema(unittest.TestCase):

    def test_thread_model_valid(self):
        data = {"thread_id": "thread_id"}

        thread = Thread(**data)
        self.assertEqual(thread.thread_id, "thread_id")

    def test_thread_model_missing_fields(self):
        data = {}

        with self.assertRaises(ValidationError):
            Thread(**data)


class TestAssistantResponseSchema(unittest.TestCase):

    def test_assistant_response_model_valid(self):
        data = {"role": "assistant", "message": "How can I help you?"}

        assistant_response = AssistantResponse(**data)
        self.assertEqual(assistant_response.role, "assistant")
        self.assertEqual(assistant_response.message, "How can I help you?")

    def test_assistant_response_model_missing_fields(self):
        data = {"role": "assistant"}

        with self.assertRaises(ValidationError):
            AssistantResponse(**data)
