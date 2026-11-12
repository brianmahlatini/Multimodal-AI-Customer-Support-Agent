from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multimodal AI Customer Support Agent"
    environment: str = "development"
    database_url: str = "sqlite:///./support_agent.db"
    redis_url: str = "redis://localhost:6379/0"
    cors_allow_origins: str = "http://localhost:5173"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_transcription_model: str = "gpt-4o-mini-transcribe"
    llm_provider: str = "mock"
    jwt_secret: str = "change-me"
    access_token_expire_minutes: int = 60
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region: str = "us-east-1"
    s3_bucket: str = "support-artifacts"
    s3_endpoint_url: str | None = None
    local_object_store: str = "data/local_s3"
    max_upload_mb: int = 25
    human_handover_sentiment_threshold: float = -0.55

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_allow_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
