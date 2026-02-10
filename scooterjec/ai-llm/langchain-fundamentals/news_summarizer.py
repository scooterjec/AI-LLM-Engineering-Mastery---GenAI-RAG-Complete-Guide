import os
from typing import Optional
from langchain.chains.llm import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

from langchain.schema import Document
from newspaper import Article
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

class NewsArticleSummarizer:
    def __init__(self, api_key: str = None, model_type: str = "openai", model_name: str = "gpt-4o-mini"):
        """
        Initialize the summarizer with choice of model
        Args:
            api_key: OpenAI API KEY (required for OpenAI models)
            model_type: 'openai' or 'ollama'
            model_name: specific model name
        """
        self.model_type = model_type
        self.model_name = model_name

        # Setup LLM based on model_type
        if model_type == "openai":
            if not api_key:
                raise ValueError("API key is required for OpenAI models")
            self.llm = ChatOpenAI(model=model_name, temperature=0)
        elif model_type == "ollama":
            self.llm = ChatOllama(model=model_name, temperature=0, format="json", timeout=120)
        else:
            raise ValueError(f"Unsupported {model_type}. Choose 'openai' or 'ollama'.")


