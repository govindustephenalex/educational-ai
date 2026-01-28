from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.chat import ChatRequest, ChatResponse
from app.services.graph import app_graph
from app.core.config import settings

import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any
from contextlib import asynccontextmanager

SESSIONS: Dict[str, Dict[str, Any]] = {}
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")

def load_sessions():
    """Load sessions from JSON file."""
    global SESSIONS
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                SESSIONS = json.load(f)
                print(f"Loaded {len(SESSIONS)} sessions.")
    except Exception as e:
        print(f"Error loading sessions: {e}")
        SESSIONS = {}

def save_sessions():
    """Save sessions to JSON file."""
    try:
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(SESSIONS, f, indent=4)
    except Exception as e:
        print(f"Error saving sessions: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_sessions()
    yield

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EduChat AI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/sessions")
async def get_sessions():
    """Get all chat sessions sorted by newest first."""
    # Convert dict to list and sort
    session_list = list(SESSIONS.values())
    session_list.sort(key=lambda x: x["timestamp"], reverse=True)
    return session_list

@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    """Get message history for a specific session."""
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    return SESSIONS[session_id]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id
        
        # Create new session if needed
        if not session_id or session_id not in SESSIONS:
            session_id = str(uuid.uuid4())
            SESSIONS[session_id] = {
                "id": session_id,
                "title": request.message[:30] + "..." if len(request.message) > 30 else request.message,
                "timestamp": datetime.now().isoformat(),
                "messages": []
            }
        
        # Get history
        session = SESSIONS[session_id]
        
        # Run the LangGraph workflow
        # In a real app, map session['messages'] to LangChain message objects
        result = app_graph.invoke({
            "input": request.message, 
            "chat_history": session["messages"]
        })
        
        response_text = result.get("response", "Sorry, I couldn't generate a response.")
        
        # Update session history
        session["messages"].append({"role": "user", "content": request.message})
        session["messages"].append({"role": "bot", "content": response_text, "grade": result.get("grade"), "subject": result.get("subject")})
        session["timestamp"] = datetime.now().isoformat() # Update timestamp
        
        # Save to file
        save_sessions()
        
        return ChatResponse(
            response=response_text,
            grade_level=result.get("grade", "Unknown"),
            subject=result.get("subject", "Unknown"),
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
