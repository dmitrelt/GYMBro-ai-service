from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str

    GEMINI_MODEL: str

    JWT_SECRET: str

    JWT_ALGORITHM: str

    class Config:
        env_file = '.env'
        extra = 'ignore'

settings = Settings()