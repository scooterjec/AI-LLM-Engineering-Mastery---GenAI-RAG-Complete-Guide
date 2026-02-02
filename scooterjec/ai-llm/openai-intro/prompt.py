from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", 
             "content": """Translate these sentences:
             1. Hello -> Hola
             2. Goodbye -> Adiós
             Now translate: "Thank you" -> """}
        ]
    )

# print(completion.choices[0].message.content)

# Direct prompting without openai
completion_direct = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", 
             "content": """You are a helpful assistant."""},
            {"role": "user", 
             "content": """What is the capital of Andorra?"""}
        ]
    )
# print(completion_direct.choices[0].message.content)

# Chain of thought prompting
completion_chain = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", 
             "content": """You are a math tutor."""},
            {"role": "user", 
             "content": """Solve the following problem step by step:
                If John has 5 apples and gives 2 to Mary, how many apples does he have left?"""}
            ]
        )
# print(completion_chain.choices[0].message.content)

# Instructional prompting
completion_instruction = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
                "content": """You are a knowledgeable personal trainer and trainer."""},
            {"role": "user",
                "content": """Write a 300-word summary of the benefits of exercise, using bullet points."""}
            ]
        )
# print(completion_instruction.choices[0].message.content)

# Role playing prompting
completion_role = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
                "content": """You are a character in a fantasy novel."""},
            {"role": "user",
                "content": """You are a brave knight on a quest to find a lost treasure. Describe your journey."""}
            ]
        )
# print(completion_role.choices[0].message.content)

# Open-ended prompting
completion_open = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
                "content": """You are a philosopher."""},
            {"role": "user",
                "content": """What is the meaning of life?"""}
            ]
        )
# print(completion_open.choices[0].message.content)

# Temperature and top-p sampling
completion_sampling = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
                "content": """You are a creative marketing assistant."""},
            {"role": "user",
                "content": """Write a creative tagline for a basketball team from Arganda del Rey (Madrid)."""}
            ],
        # temperature=0.9, # controls randomness
        top_p=0.9, # Adjusts the diversity of the output
        )
# print(completion_sampling.choices[0].message.content)

# Combining techniques and streaming
completion_combined = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
                "content": """You are a travel blogger."""},
            {"role": "user",
                "content": """Describe a day in Paris, including historical landmarks, local cuisine, and cultural experiences. Ensure to give a step-by-step itinerary. Use a friendly and engaging tone."""}
            ],
            temperature=0.9,
            stream = True,
            # top_p=0.9,
            )
# print(completion_combined.choices[0].message.content)
for chunk in completion_combined:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
    print("\n")

