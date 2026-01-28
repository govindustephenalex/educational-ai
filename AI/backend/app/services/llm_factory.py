from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from app.core.config import settings

class MockChatOpenAI:
    def invoke(self, messages):
        last_msg = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
        return AIMessage(content=f"**[MOCK MODE]** I received your message: '{last_msg}'. \n\nI am currently running in Mock Mode because the `OPENAI_API_KEY` is missing in `backend/.env`.\n\nPlease add your API Key to get real educational responses!")

def get_llm():
    key = settings.OPENAI_API_KEY
    # Check for empty, whitespace, or placeholder values
    if not key or not key.strip() or len(key) < 10 or "your_api_key" in key:
        print(f"LLM Factory: Key seems invalid (len={len(key) if key else 0}). Using MockChatOpenAI.")
        return MockChatOpenAI()
    
    print(f"LLM Factory: Key seems valid (len={len(key)}). Creating ChatOpenAI.")
    try:
        if key.startswith("gsk_"):
            print("LLM Factory: Detected Groq API Key. Configuring for Groq.")
            return ChatOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=key,
                model="llama-3.3-70b-versatile",
                temperature=0.7
            )
        else:
            return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=key)
    except Exception as e:
        print(f"LLM Factory: Error creating ChatOpenAI: {e}")
        return None
