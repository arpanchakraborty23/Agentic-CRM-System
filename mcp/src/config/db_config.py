from pydantic_settings import BaseSettings, SettingsConfigDict

class DBConfig(BaseSettings):
    DATABASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

db = DBConfig()