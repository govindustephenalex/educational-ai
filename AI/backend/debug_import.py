import sys
import os
sys.path.append(os.getcwd())

print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    # Try importing app.main
    import app.main
    print(f"Imported app.main: {app.main}")
    
    from app.main import app
    print(f"Imported app: {app}")
    print(f"Type of app: {type(app)}")
    
    from fastapi import FastAPI
    if isinstance(app, FastAPI):
        print("SUCCESS: app is a FastAPI instance.")
    else:
        print("FAILURE: app is NOT a FastAPI instance.")
        
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"ERROR: {e}")
