from app.services.vector_store import vector_store_service

def ingest_data():
    print("Ingesting dummy educational content...")
    
    texts = [
        "Newton's First Law: An object will remain at rest or in uniform motion unless acted upon by an external force. This is also called the law of inertia.",
        "Newton's Second Law: Force equals mass times acceleration (F=ma).",
        "Newton's Third Law: For every action, there is an equal and opposite reaction.",
        "Photosynthesis is the process used by plants to convert light energy into chemical energy.",
        "The quadratic formula is x = (-b ± sqrt(b² - 4ac)) / 2a.",
        "In Python, a list is a mutable sequence of elements.",
        "Ohm's Law states that V = IR, where V is voltage, I is current, and R is resistance."
    ]
    
    metadatas = [
        {"subject": "Physics", "grade": "Class 9"},
        {"subject": "Physics", "grade": "Class 9"},
        {"subject": "Physics", "grade": "Class 9"},
        {"subject": "Biology", "grade": "Class 10"},
        {"subject": "Math", "grade": "Class 10"},
        {"subject": "Computer Science", "grade": "B.Tech"},
        {"subject": "Physics", "grade": "Class 12"}
    ]
    
    if vector_store_service.vectordb:
        vector_store_service.add_texts(texts, metadatas)
        print("Ingestion complete.")
    else:
        print("Vector DB validation failed (API Key might be missing). Skipping ingestion.")

if __name__ == "__main__":
    ingest_data()
