from dotenv import load_dotenv
import os
import logging

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
openrouter_available = OPENROUTER_API_KEY is not None

if openrouter_available and OPENROUTER_MODEL is None:
    logging.warning("OpenRouter model is not set. OpenRouter will be unavailable.")
    openrouter_available = False

messages = []