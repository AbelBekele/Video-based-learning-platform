import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings, Field

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent # app/
    templates_dir = Path = Path(__file__).resolve().parent / "templates"
    keyspace: str = Field(..., env='ASTRADB_KEYSPACE')
    db_client_id: str = Field(..., env='ASTRADB_CLIENT_ID')
    db_client_secret: str = Field(..., env='ASTRADB_CLIENT_SECRET')
    secret_key: str = Field(..., env='SECRET_KEY')
    jwt_algorithm: str = Field(default = "HS256")
    session_duration: int = Field(default=86400, env="SESSION_DURATION")
    
    class Config:
        env_file= '.env'

def get_settings():
    return Settings()