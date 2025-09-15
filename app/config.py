from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    app_secret: str = "change_me"
    app_env: str = "dev"
    base_url: str = "http://127.0.0.1:8000"

    db_url: str = "sqlite:///./clearpoint.db"

    stripe_public_key: str | None = None
    stripe_secret_key: str | None = None
    stripe_price_id_growth: str | None = None
    stripe_price_id_starter: str | None = None
    stripe_webhook_secret: str | None = None

    s3_bucket: str | None = None
    s3_region: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    email_verify_provider: str | None = None
    email_verify_api_key: str | None = None

    scheduler_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

settings = Settings()
