from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """
    bot_token: SecretStr

    # Tell Pydantic to read from a .env file if it exists, ignoring extra fields
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Instantiate the settings so they can be imported elsewhere
settings = Settings()
