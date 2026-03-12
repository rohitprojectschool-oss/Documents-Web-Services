from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # PostgreSQL Configuration (New Default)
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/postgres"

    # SAP HANA Configuration (Kept for legacy/optional use)
    HANA_DB_HOST: Optional[str] = None
    HANA_DB_PORT: Optional[int] = 443
    HANA_DB_USER: Optional[str] = None
    HANA_DB_PASSWORD: Optional[str] = None
    HANA_DB_SCHEMA: Optional[str] = "CRIMSON_APP"

    @property
    def HANA_URL(self) -> str:
        return f"hana://{self.HANA_DB_USER}:{self.HANA_DB_PASSWORD}@{self.HANA_DB_HOST}:{self.HANA_DB_PORT}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
