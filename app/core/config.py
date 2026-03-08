from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    HANA_DB_HOST: str = "localhost"
    HANA_DB_PORT: int = 30015
    HANA_DB_USER: str = "SYSTEM"
    HANA_DB_PASSWORD: str = "password"
    HANA_DB_SCHEMA: Optional[str] = "CRIMSON_APP"

    @property
    def HANA_URL(self) -> str:
        # Use the sqlalchemy-hana dialect
        # Format: hana://user:password@host:port
        return f"hana://{self.HANA_DB_USER}:{self.HANA_DB_PASSWORD}@{self.HANA_DB_HOST}:{self.HANA_DB_PORT}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
