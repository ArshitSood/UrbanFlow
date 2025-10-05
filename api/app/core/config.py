from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    urbanflow_env: str = "dev"
    gcp_project_id: str = "local-fixture"
    bigquery_dataset: str = "urbanflow_dev"
    agent_write_actions_enabled: bool = False
    api_auth_mode: str = "development"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:4173"

    @property
    def allowed_cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
