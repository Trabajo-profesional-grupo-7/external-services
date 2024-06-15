import os

import requests

from app.schemas.chatbot import ChatIDs
from app.utils.api_exception import APIException, APIExceptionToHTTP, HTTPException
from app.utils.constants import SEND_CHAT_INFORMATION_ERROR

AUTHENTICATION_URL = os.getenv("AUTHENTICATION_URL")
ATTRACTIONS_URL = os.getenv("ATTRACTIONS_URL")


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
    response = requests.get(
        f"{AUTHENTICATION_URL}/users/{id}",
    )
    return response.json()["preferences"]


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


def set_up_instructions(preferences, city):
    instruction = f"""

    Actúa como si fueras un experto en turismo.

    Asegúrate de:
    - Recomendar atracciones y lugares de comida en {city}.
    - Explicar por qué debería el usuario visitar esos lugares.
    - Hablar de modo amigable, no formal.

    Realiza recomendaciones al usuario teniendo en cuenta que:
    - Tiene prioridad en hacer actividades que incluyan solamente {preferences}.

    El usuario ya ha proporcionado toda la información necesaria y espera respuestas directas. Aquí está la solicitud específica del usuario:
    - Ciudad: {city}
    - Preferencias: {preferences}

    Por favor, responde directamente a cualquier pregunta sobre recomendaciones, sin pedir más información adicional.
    """

    return instruction
