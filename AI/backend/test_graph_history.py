import sys
import os
from dotenv import load_dotenv

# Load env from current directory
load_dotenv(".env")

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

try:
    # Attempt import
    from app.services.graph import app_graph
    # from langchain_core.messages import HumanMessage, AIMessage # Not needed for invocation dict
except ImportError as e:
    print(f"Import Error: {e}")
    # Try adding parent directory if running from inside backend
    sys.path.append(os.path.dirname(os.getcwd()))
    from app.services.graph import app_graph

print("Testing Chat History Context...")

# Simulate history
chat_history = [
    {"role": "user", "content": "Hi, my name is Alice."},
    {"role": "bot", "content": "Hello Alice! How can I help you today?"}
]

question = "What is my name?"
print(f"User History: {[msg['content'] for msg in chat_history]}")
print(f"User New Question: {question}")

try:
    result = app_graph.invoke({
        "input": question,
        "chat_history": chat_history
    })
    
    response = result.get("response", "")
    print(f"Bot Response: {response}")
    
    if "Alice" in response:
        print("\n>>> PASS: History was used correctly.")
    else:
        print("\n>>> FAIL: History was NOT used (or name not found in response).")

except Exception as e:
    print(f"\n>>> ERROR: {e}")
