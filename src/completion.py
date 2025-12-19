from openrouter import OpenRouter
from openrouter.components import UserMessage
import logging as l
import gui
import common as c

client_openrouter = OpenRouter(
    api_key=c.OPENROUTER_API_KEY
)

def reply(prompt=None):
    model = c.OPENROUTER_MODEL
    if not c.openrouter_available or not model:
        raise Exception("OpenRouter is not available. Please check your API key and model configuration.")
    
    if prompt:
        c.chat.append(UserMessage(content=prompt))
        l.debug(f"Replying to prompt: {prompt}")
    elif type(c.chat[-1]) != UserMessage:
        raise Exception("No prompt provided and the last message is not from the user.")

    completion = client_openrouter.chat.send(
        model=model,
        messages = c.chat_dict()
    )

    l.debug(f"Completion response: {completion}")

    c.chat.append(completion)
    gui.update_messages()
