from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    db_hostname: str
    db_port: str
    db_password: str
    db_database: str
    db_userName: str
    token_secret: str
    access_token_exp_minutes: int
    algorithm: str

    class Config:
        env_file = ".env"


settings = Settings()
