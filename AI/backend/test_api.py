import os
import sys
import json
import tempfile
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Add path
sys.path.append(os.getcwd())

print("Testing Endpoints and Persistence...")

# Patch get_llm to avoid real API calls and avoid dependent failure
with patch('app.services.llm_factory.get_llm') as mock_get_llm:
    # Setup mock LLM
    mock_llm = MagicMock()
    # Return an object that has .content
    mock_response = MagicMock()
    mock_response.content = "This is a mock response."
    mock_llm.invoke.return_value = mock_response
    mock_get_llm.return_value = mock_llm
    
    try:
        from app.main import app
        import app.main
    except ImportError as e:
        print(f"Import Error: {e}")
        sys.path.append(os.path.dirname(os.getcwd()))
        from app.main import app
        import app.main

    # Override SESSIONS_FILE to a temp file
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    
    original_file = app.main.SESSIONS_FILE
    app.main.SESSIONS_FILE = temp_path
    app.main.SESSIONS = {} 
    
    try:
        client = TestClient(app)
        
        # 1. Test POST /chat
        print("1. Testing POST /chat...")
        resp = client.post("/chat", json={"message": "Hello AI"})
        if resp.status_code != 200:
            print(f"FAIL: /chat failed: {resp.text}")
            sys.exit(1)
            
        data = resp.json()
        session_id = data.get("session_id")
        print(f"   Chat Response OK. Session ID: {session_id}")
        
        if not session_id:
            print("FAIL: No session_id returned")
            sys.exit(1)

        # 2. Test GET /sessions
        print("2. Testing GET /sessions...")
        resp = client.get("/sessions")
        if resp.status_code != 200:
             print(f"FAIL: /sessions failed: {resp.text}")
             sys.exit(1)
             
        sessions = resp.json()
        print(f"   Sessions found: {len(sessions)}")
        if len(sessions) != 1 or sessions[0]["id"] != session_id:
            print("FAIL: Session not found in list")
            sys.exit(1)
            
        # 3. Test Persistence (Save)
        print("3. Testing Persistence (Save to file)...")
        if os.path.exists(temp_path):
            with open(temp_path, 'r') as f:
                content = f.read()
                if session_id not in content:
                    print("FAIL: Session ID not found in file")
                    sys.exit(1)
                else:
                    print("   File contains session ID.")
        else:
            print("FAIL: Sessions file not created")
            sys.exit(1)
            
        # 4. Test Load (Simulate restart)
        print("4. Testing Load (Simulate restart)...")
        app.main.SESSIONS = {}
        app.main.load_sessions()
        
        if session_id not in app.main.SESSIONS:
            print("FAIL: Session not loaded after restart simulation")
            sys.exit(1)
        else:
            print("   Session loaded successfully.")
            
        print("\n>>> PASS: Endpoints and Persistence verified.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                print("Cleanup: Temp file removed.")
            except:
                pass
