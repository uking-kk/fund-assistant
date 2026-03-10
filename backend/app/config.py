from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    ARK_API_KEY: str = ""
    ARK_BASE_URL: str = "https://ark.cn-beijing.volces.com/api/v3"
    ARK_MODEL: str = "doubao-seed-2-0-pro-260215"
    
    EMBEDDING_MODEL: str = "BAAI/bge-small-zh-v1.5"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
