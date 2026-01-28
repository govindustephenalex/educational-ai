import os
import sys
import tempfile
import json
from fastapi.testclient import TestClient

sys.path.append(os.getcwd())

try:
    from app.main import app
    import app.main
    
    # Use a temp file for sessions to avoid overwriting real data
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    print(f"Using temp sessions file: {temp_path}")
    
    # Override in the module
    app.main.SESSIONS_FILE = temp_path
    app.main.SESSIONS = {}
    
    client = TestClient(app)
    
    print("1. Sending message...")
    resp = client.post("/chat", json={"message": "Persistence Test"})
    if resp.status_code != 200:
        print(f"FAIL: Chat endpoint failed: {resp.text}")
        sys.exit(1)
        
    data = resp.json()
    session_id = data["session_id"]
    print(f"   Session ID: {session_id}")
    
    print("2. Checking persistence...")
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as f:
            content = f.read()
            print(f"   File content len: {len(content)}")
            if session_id in content and "Persistence Test" in content:
                print("PASS: Session saved to file.")
            else:
                print(f"FAIL: Session data missing from file. Content: {content}")
    else:
        print("FAIL: File not created.")
        
    # Cleanup
    try:
        os.remove(temp_path)
    except:
        pass
        
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"ERROR: {e}")
