import sys
import os
sys.path.append(os.getcwd())

try:
    from app.main import app
    from fastapi.testclient import TestClient
    
    print("Creating TestClient...")
    client = TestClient(app)
    print("Client created.")
    
    print("Getting /health...")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"ERROR: {e}")
