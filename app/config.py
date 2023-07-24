from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    DATABASE_PORT: int

    CLIENT_ORIGIN: str

    class Config:
        env_file = 'database.env'


settings = Settings()