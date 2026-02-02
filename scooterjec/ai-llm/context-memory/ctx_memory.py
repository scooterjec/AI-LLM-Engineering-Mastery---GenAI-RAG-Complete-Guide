from typing import Dict, List
import json
import os
from openai import OpenAI
import sys
from dotenv import load_dotenv

load_dotenv()

def initialize_client(use_ollama: bool = False) -> OpenAI:
    """
    Initialize the OpenAI client for either OpenAI or Ollama
    """
    if use_ollama:
        return OpenAI(base_url="http://localhost:11434/v1/", api_key='fake_key')
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_initial_context() -> List[Dict[str, str]]:
    """Create the initial messages for the context memory."""
    return [
        {"role":"system", "content": "You are a helpful assistant"}
    ]

def chat (
    user_input:str, messages:List[Dict[str,str]], client:OpenAI, model_name:str
    ) -> str:
    """ Handle user inputs and generates responses"""
    # Append user message to the conversation:
    messages.append({"role":"user", "content": user_input})

    try:
        # Generate a response using the API
        response = client.chat.completions.create(
            model=model_name, messages=messages
        )

        # Append assistant's response to the conversation
        assistant_response = response.choices[0].message.content
        messages.append({"role":"assistant", "content": assistant_response})

        return assistant_response
    except Exception as e:
        return f"Error with API: {str(e)}"

def summarize_messages(messages: List[Dict[str,str]]) -> List[Dict[str,str]]:
    """ Summarize older messages to save tokens """
    summary = "Previous conversation summarized: " + " ".join(
        [m["content"][:50] + "..." for m in messages[-5:]]
    )
    return [{"role":"system", "content": summary}] + messages[-5:]

def save_conversation(
        messages: List[Dict[str,str]], filename: str="conversation_history.json"
    ) -> None:
    """ Save the conversation history to a file """
    with open(filename, "w") as f:
        json.dump(messages, f, indent=4)

def load_conversation( filename: str = "conversation_history.json"
    ) -> List[Dict[str,str]]:
    """ Load the conversation history from a file """
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading conversation file {filename}: {str(e)}")
        return create_initial_context()

def main():
    # Model selection
    print("=== Chatbot WITH memory/context management ===")
    print("Select model type:")
    print("1. OpenAI GPT-4")
    print("2. Ollama (local)")

    while True:
        choice = input ("Enter choice (1 or 2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Please enter either 1 or 2")

    use_ollama = choice == "2"
    client = initialize_client(use_ollama)
    model_name = "llama3.2" if use_ollama else "gpt-4o-mini"

    # Load previous conversation or create new context
    messages = load_conversation()
    print(f"loaded (or initial) messages: {messages}")

    # Print instructions
    print("=== Chat session started ===")
    print(f"\nUsing {'OLLAMA Llama3.2' if use_ollama else 'OpenAI GPT-4o-mini'} model")
    print("Available commands: ")
    print(" - 'save': Save the conversation history to a file")
    print(" - 'load': Load the conversation history from a file")
    print(" - 'summary': Summarize the conversation to reduce context length")
    print(" - 'quit' or 'exit': end the conversation")
    print(" - 'clear': clear the screen")
    print("The bot will remember previous messages in this session.")

    # Main chat loop
    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Check for exit commands
        if user_input.lower() in ["quit","exit"]:
            print("\nGoodbye!! 👋🏻")
            save_conversation(messages)
            sys.exit()
        
        # Clear screen command
        elif user_input.lower() == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        # Save conversation command
        elif user_input.lower() == "save":
            save_conversation(messages)
            print("Conversation history saved.")
            continue
        # Load conversation command
        elif user_input.lower() == "load":
            messages = load_conversation()
            print("Conversation history loaded.")
            continue
        # Summarize conversation command
        elif user_input.lower() == "summary":
            messages = summarize_messages(messages)
            print("Conversation summarized.")
            continue

        # Generate and display response
        response = chat(user_input, messages, client, model_name)
        print(f"Bot: {response}")

        # Summarize messages if too long
        if len(messages) > 10:
            messages = summarize_messages(messages)
            print("\n [Conversation automatically summarized to save context length]\n")

if __name__ == "__main__":
    main()
