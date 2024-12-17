from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Web Scraper System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Proxy settings
    PROXY_CHECK_INTERVAL: int = 300  # 5 minutes
    MAX_PROXY_FAILURES: int = 3
    
    # Task settings
    DEFAULT_TASK_TIMEOUT: int = 300  # 5 minutes
    MAX_RETRIES: int = 3
    CONCURRENT_TASKS: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
