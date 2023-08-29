from pydantic import BaseSettings


class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_pw: str
    db_name: str
    db_userName: str
    secret_key: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
