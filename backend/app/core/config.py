from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_name: str = "Ecommerce API"
    ENV: str = "development"


    DATABASE_URl: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASS: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()