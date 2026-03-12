from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # PostgreSQL Configuration
    # Defaults to production URL if not provided by environment
    DATABASE_URL: str = "postgresql://documents_web_db_user:9VV8ybPm54i17j2XcVyV4P5CTKewMO41@dpg-d6oq89s50q8c739u8ddg-a.oregon-postgres.render.com/documents_web_db"

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
