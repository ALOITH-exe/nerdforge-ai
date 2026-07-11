# backend/app/config.py
import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    # Railway (and most managed Postgres providers) hand out DATABASE_URL with a
    # "postgres://" scheme, but SQLAlchemy 2.0's psycopg2 driver requires
    # "postgresql://". We normalize it here so both local SQLite and Railway
    # Postgres work without code changes.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nerdforge.db")

    # AI Models
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    # Model Selection Strategy - actual order used by LLMService (Groq first,
    # Gemini as fallback). Kept here for reference/visibility, not branching logic.
    PRIMARY_MODEL: str = "groq"
    FALLBACK_MODEL: str = "gemini"

    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # CORS - comma-separated list of allowed origins. Defaults cover local dev;
    # set CORS_ORIGINS in Railway to your deployed frontend URL(s).
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    )

    # Server
    PORT: int = int(os.getenv("PORT", "8000"))

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def normalized_database_url(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
