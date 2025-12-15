from openai import OpenAI
import logging as l
import var, gui

client_openrouter = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=var.OPENROUTER_API_KEY
)

def reply(prompt=None):

    model = var.OPENROUTER_MODEL
    if not var.openrouter_available or not model:
        raise Exception("OpenRouter is not available. Please check your API key and model configuration.")
    
    if prompt:
        var.messages.append({"role": "user", "content": prompt})
        l.info(f"Replying to prompt: {prompt}")
    elif var.messages[-1]["role"] != "user":
        raise Exception("No prompt provided and the last message is not from the user.")

    completion = client_openrouter.chat.completions.create(
        model=model,
        messages=var.messages
    )

    var.messages.append(completion.choices[0].message)
    gui.update_messages()
