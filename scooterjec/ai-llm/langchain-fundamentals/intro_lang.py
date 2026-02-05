import getpass
import os

from dotenv import load_dotenv

load_dotenv()


from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-4o-mini", model_provider = "openai")

response = model.invoke("Hello how are you?")
print(response)
