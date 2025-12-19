from dotenv import load_dotenv
import os
import logging
from openrouter.components import Message, ChatResponse

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
openrouter_available = OPENROUTER_API_KEY is not None

def init():
    """Initialize common configurations and validate settings."""
    global openrouter_available
    if openrouter_available and OPENROUTER_MODEL is None:
        logging.warning("OpenRouter model is not set. OpenRouter will be unavailable.")
        openrouter_available = False

chat: list[Message | ChatResponse] = []

def chat_dict() -> list:
    """Convert the chat list to a list of dictionaries for API consumption."""
    dict_list = []
    for msg in chat:
        if type(msg) == ChatResponse:
            dict_list.append({
                "role": "assistant",
                "content": msg.choices[0].message.content
            })
        else:
            assert not isinstance(msg, ChatResponse)
            dict_list.append({
                "role": msg.ROLE,
                "content": msg.content
            })
    return dict_list

def is_user_message(msg) -> bool:
    if isinstance(msg, dict):
        return msg.get("role") == "user"
    else:
        return getattr(msg, 'role', None) == "user"