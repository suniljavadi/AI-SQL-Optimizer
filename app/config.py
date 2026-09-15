from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./optimizer.db"
    llm_mode: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    max_rows: int = 1000
    query_timeout_seconds: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
