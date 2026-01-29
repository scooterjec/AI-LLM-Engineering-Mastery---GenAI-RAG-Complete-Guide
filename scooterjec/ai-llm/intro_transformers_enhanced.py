from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

def create_simple_llm():
    """
    Creates a simple LLM using a small GPT-2 model.
    GPT-2 (smallest version) is lightweight and can run on most machines.
    """

    # Initialize model and tokenizer
    model_name = "gpt2"  # Smallest GPT-2 model

    # Create de generator pipeline
    generator = pipeline(
        "text-generation",
        model=model_name,
        pad_token_id=50256  # GPT-2's padding token
    )

    return generator

def generate_test(generator, prompt, max_length=1000):
    # Generate text
    result = generator(prompt, max_length, num_return_sequences=1, do_sample=True, temperature=0.7)
    return result[0]['generated_text']

def run_llm_demo():
    """ Demonstrate basic LLM functionality with explanations. """
    print("🤖 Loading Simple LLM Model...")
    generator = create_simple_llm()

    print("\n✨ Simple LLM Demo ✨")
    print("This demo shows basic text generation using a small language model (GPT-2).")

    # Example prompts to demonstrate different capabilities
    prompts = [
            "The quick brown fox",
            "Once upon a time",
            "Python programming is",
        ]

    for prompt in prompts:
        print(f"\n➡️ Prompt: {prompt}")
        print("➡️ Generated: ", generate_test(generator, prompt))
        input("\nPress Enter to continue...")

def interactive_demo():
    """ Allows user to inteact with the model """
    generator = create_simple_llm()

    print("\n🤖 Interactive LLM Demo 🤖")
    print("Type your prompts or 'quit' to quit.")

    while True:
        prompt = input("\n➡️ Your prompt: ")
        if prompt.lower() in ['quit', 'exit']:
            print("➡️ Exiting interactive demo.")
            break
        print("➡️ Generated: ", generate_test(generator, prompt))


def explain_process():
    """ Explain the LLM process with a simple example. """

    print("\nHow it works: ")
    print("1. Input text -> Tokenization -> Numbers")
    print("2. Numbers -> Model Processing -> Prediciton")
    print("3. Prediction -> New Token -> Output text")

    # Simple Tokenization example
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    text = "Hello World!!!"
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)

    print(f"\nExample Tokenization:")
    print(f"➡️ Original Text: {text}")
    print(f"➡️ As Tokens (numbers): {tokens}")
    print(f"➡️ Decoded back: {decoded}")

if __name__ == "__main__":
    print("Choose a demo:")
    print("1. Basic LLM Demo")
    print("2. Interactive LLM Demo")
    print("3. Explain LLM Process")

    choice = input("Enter 1, 2, or 3: ")

    if choice == '1':
        run_llm_demo()
    elif choice == '2':
        interactive_demo()
    elif choice == '3':
        explain_process()
    else:
        print("Invalid choice. Exiting.")
