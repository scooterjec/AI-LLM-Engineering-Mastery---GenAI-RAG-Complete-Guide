import requests

def create_simple_llm():
    """
    Creates a simple LLM client that talks to a Docker Model Runner
    serving ai/llama3.2 over HTTP.
    """

    API_URL = "http://127.0.0.1:12434/engines/v1/completions"
    MODEL_NAME = "ai/llama3.2"

    def generate(prompt: str,
                 max_new_tokens: int = 128,
                 temperature: float = 0.7) -> str:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }

        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Formato típico del Docker Model Runner
        # Ajusta si ves una estructura distinta con print(data)
        if isinstance(data, dict):
            return (
                data.get("generated_text")
                or data.get("choices", [{}])[0].get("text")
                or data.get("text")
                or data.get("response")
                or str(data)
            )

        return str(data)

    return generate

# Ejemplo de uso
if __name__ == "__main__":
    llm = create_simple_llm()
    prompt = "Once upon a time"
    output = llm(
        prompt,
        max_new_tokens=60,
        temperature=0.5
    )
    print("Respuesta del LLM:", output)
    


