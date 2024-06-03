import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../.env")


class Settings(BaseSettings):
    bot_token: SecretStr
    database_url: SecretStr
    logger_level: str
    ai_api_key: SecretStr
    ai_base_url: str
    yoomoney_base_url: str
    yoomoney_redirect_url: str
    yoomoney_client_id: SecretStr
    yoomoney_client_secret: SecretStr

    class Config:
        env_file = DOTENV_PATH
        env_file_encode = "utf-8"


cfg = Settings()
