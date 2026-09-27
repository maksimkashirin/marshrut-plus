from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    mini_app_url: str | None = None

    max_bot_token: str | None = None

    max_api_url: str = (
        "https://platform-api2.max.ru"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()