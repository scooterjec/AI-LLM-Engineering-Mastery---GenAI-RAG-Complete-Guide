from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
# model = init_chat_model("gpt-4o-mini", model_provider = "openai")
model = init_chat_model("llama3.2", model_provider = "ollama")

# Create the chat prompt
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# Chain the prompt, model and output parser together
chain = prompt | model | StrOutputParser()

# Invoke the chain with a topic
response = chain.invoke({"topic": "programming"})
print(response)

