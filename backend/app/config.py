import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Auto-Creative Engine"
    PROJECT_VERSION: str = "1.0.0"
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    # IMAGEN_API_KEY: str = os.getenv("IMAGEN_API_KEY", "") # Or Google Cloud credentials path
    
    # Paths
    TEMP_DIR: str = os.path.join(os.getcwd(), "temp_uploads")
    OUTPUT_DIR: str = os.path.join(os.getcwd(), "generated_creatives")

settings = Settings()

# Ensure directories exist
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
