from typing import TypedDict, Annotated, Literal
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm_factory import get_llm
from app.services.vector_store import vector_store_service

class AgentState(TypedDict):
    input: str
    chat_history: list
    grade: str
    subject: str
    context: str
    response: str

llm = get_llm()

def classify_input(state: AgentState):
    """Detects grade and subject from the input."""
    question = state["input"]
    # Simple heuristic/mock for now if LLM fails or is missing
    # In a real app, use LLM with structured output or a classification chain
    if not llm:
        return {"grade": "General", "subject": "General"}
    
    prompt = f"""Analyze the following question and determine the target student Grade (e.g., Class 8, B.Tech) and Subject.
    Question: {question}
    Return only 'Grade: <grade>, Subject: <subject>' format."""
    
    try:
        result = llm.invoke([HumanMessage(content=prompt)]).content
        # Basic parsing (robust implementations would use JSON output)
        parts = result.split(",")
        grade = parts[0].split(":")[1].strip() if ":" in parts[0] else "General"
        subject = parts[1].split(":")[1].strip() if len(parts) > 1 and ":" in parts[1] else "General"
    except:
        grade = "General"
        subject = "General"
        
    return {"grade": grade, "subject": subject}

def retrieve_context(state: AgentState):
    """Retrieves relevant docs from vector store."""
    query = state["input"]
    docs = vector_store_service.similarity_search(query)
    context = "\n\n".join([d.page_content for d in docs])
    return {"context": context}

def generate_response(state: AgentState):
    """Generates the final answer."""
    grade = state.get("grade", "General")
    subject = state.get("subject", "General")
    context = state.get("context", "")
    question = state["input"]
    
    if not llm:
        return {"response": "I am unable to process your request because the LLM is not configured."}

    system_prompt = f"""You are an educational AI assistant for {grade} students studying {subject}.
    Explain things clearly and simply. Use examples.
    If context is provided, use it.
    
    Context:
    {context}
    """
    
    messages = [SystemMessage(content=system_prompt)]
    
    # Add chat history
    history = state.get("chat_history", [])
    for msg in history:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg.get("content", "")))
        elif msg.get("role") == "bot":
            from langchain_core.messages import AIMessage
            messages.append(AIMessage(content=msg.get("content", "")))
            
    messages.append(HumanMessage(content=question))

    try:
        response = llm.invoke(messages)
        return {"response": response.content}
    except Exception as e:
        print(f"Error generating response: {e}")
        return {"response": "I am unable to generate a response at the moment due to an AI service error."}

# Graph Definition
workflow = StateGraph(AgentState)

workflow.add_node("classify", classify_input)
workflow.add_node("retrieve", retrieve_context)
workflow.add_node("generate", generate_response)

workflow.set_entry_point("classify")

# Conditional edge: For now, we always retrieve, but we could skip it for simple greetings
workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()
