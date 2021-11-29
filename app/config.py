from pydantic import BaseSettings

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()