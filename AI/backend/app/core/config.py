import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    PROJECT_NAME: str = "EduChat AI"
    VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    VECTOR_DB_PATH: str = os.path.join(BASE_DIR, "data", "chroma_db")

settings = Settings()
