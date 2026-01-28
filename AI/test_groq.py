import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv("backend/.env", override=True)
key = os.getenv("OPENAI_API_KEY")

print(f"Key: {key[:10]}...")

models_to_test = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "llama3-8b-8192",
    "gemma2-9b-it"
]

for model in models_to_test:
    print(f"\nTesting model: {model}")
    try:
        chat = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=key,
            model=model,
            temperature=0
        )
        response = chat.invoke("Hello")
        print(f"SUCCESS: {response.content}")
        break
    except Exception as e:
        print(f"FAILED: {e}")
