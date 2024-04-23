from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    database_url: SecretStr
    logger_level: str
    ai_api_key: SecretStr
    ai_base_url: str

    class Config:
        env_file = "../.env"
        env_file_encode = "utf-8"


cfg = Settings()
