from app.services.graph import app_graph
import asyncio

async def test_graph():
    print("Testing Graph...")
    inputs = {"input": "Explain Newton's second law", "chat_history": []}
    try:
        result = await app_graph.ainvoke(inputs)
        print("\n--- Response ---")
        print(f"Grade: {result.get('grade')}")
        print(f"Subject: {result.get('subject')}")
        print(f"Response: {result.get('response')}")
        
        if "Mock Mode" in result.get('response', ''):
             print("\n[WARN] LLM is in Mock Mode. Check API Key.")
        else:
             print("\n[SUCCESS] LLM generated a real response.")
             
    except Exception as e:
        print(f"\n[ERROR] Graph invocation failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_graph())
