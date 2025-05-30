from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = ""

    class ConfigDict:
        env_file = ".env"
        env_file_encoding = "utf-8"
