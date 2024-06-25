from datetime import date
from unittest.mock import patch

import pytest

from app.services.chatbot import set_up_instructions


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
