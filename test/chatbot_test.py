import os
import unittest
from datetime import date
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import RequestException

import app
from app.schemas.chatbot import *
from app.services.chatbot import set_up_instructions
from app.utils.api_exception import *
from app.utils.constants import *

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")


def test_set_up_instructions():
    expected_output = """
    
    You're a tourism expert.

    Make sure to:
    - Call him by his name: Lucia
    - Recommend attractions and dining places in Buenos Aires.
    - Explain why the user should visit those places.
    - Speak in a friendly, informal manner.
    - Do not ask for or store sensitive personal information.
    - Ensure user data is handled with confidentiality and security.

    Make recommendations to the user considering:
    - They prioritize activities that include only [museums, parks].

    The user has already provided all the necessary information and expects direct answers. Here is the user's specific request:
    - City: Buenos Aires
    - Preferences: [museums, parks]

    Please respond directly to any questions about recommendations without asking for any additional information.

    """
    result = set_up_instructions("Lucia", "[museums, parks]", "Buenos Aires")

    normalized_expected_output = " ".join(expected_output.split())
    normalized_result = " ".join(result.split())

    assert normalized_result == normalized_expected_output


class TestGetThreadAndAssistantId(unittest.TestCase):

    @patch("app.services.chatbot.requests.get")
    @patch("app.schemas.chatbot.ChatIDs")
    def test_get_thread_and_assistant_id_success(self, MockChatIDs, mock_requests_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "thread_id": "thread123",
            "assistant_id": "assistant456",
        }
        mock_requests_get.return_value = mock_response

        mock_chat_ids_instance = Mock(spec=ChatIDs)
        mock_chat_ids_instance.thread_id = "thread123"
        mock_chat_ids_instance.assistant_id = "assistant456"

        MockChatIDs.model_construct.return_value = mock_chat_ids_instance

        result = app.services.chatbot.get_thread_and_assistant_id(1)

        self.assertEqual(result.thread_id, mock_chat_ids_instance.thread_id)
        self.assertEqual(result.assistant_id, mock_chat_ids_instance.assistant_id)

    @patch("app.services.chatbot.requests.get")
    def test_get_thread_and_assistant_id_request_exception(self, mock_requests_get):
        mock_requests_get.side_effect = RequestException("Request failed")

        with self.assertRaises(RequestException):
            app.services.chatbot.get_thread_and_assistant_id(1)


class TestGetLocation(unittest.TestCase):

    @patch("app.services.chatbot.requests.post")
    def test_get_location_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"city": "New York", "distance": 2000},
            {"city": "Los Angeles", "distance": 4000},
        ]
        mock_post.return_value = mock_response

        result = app.services.chatbot.get_location(40.7128, -74.0060)

        self.assertEqual(result, "New York")

    @patch("app.services.chatbot.requests.post")
    def test_get_location_no_attractions_found(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_post.return_value = mock_response

        result = app.services.chatbot.get_location(34.0522, -118.2437)

        self.assertIsNone(result)

    @patch("app.services.chatbot.requests.post")
    def test_get_location_empty_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = None
        mock_post.return_value = mock_response

        result = app.services.chatbot.get_location(51.5074, -0.1278)
        self.assertIsNone(result)


class TestSendChatInformation(unittest.TestCase):

    @patch("app.services.chatbot.requests.post")
    def test_send_chat_information_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        app.services.chatbot.send_chat_information(1, "thread123", "assistant456")

        mock_post.assert_called_once_with(
            f"{AUTHENTICATION_URL}/users/chat",
            json={
                "user_id": 1,
                "thread_id": "thread123",
                "assistant_id": "assistant456",
            },
        )

    @patch("app.services.chatbot.requests.post")
    def test_send_chat_information_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500  # Server error
        mock_post.return_value = mock_response

        with self.assertRaises(APIException) as context:
            app.services.chatbot.send_chat_information(1, "thread123", "assistant456")

        self.assertEqual(context.exception.code, SEND_CHAT_INFORMATION_ERROR)


class TestGetUserData(unittest.TestCase):

    @patch("app.services.chatbot.requests.get")
    def test_get_user_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "username": "username",
            "preferences": ["Cafe", "Library"],
        }
        mock_get.return_value = mock_response

        username, preferences = app.services.chatbot.get_user_data(1)

        self.assertEqual(username, "username")
        self.assertEqual(preferences, ["Cafe", "Library"])
