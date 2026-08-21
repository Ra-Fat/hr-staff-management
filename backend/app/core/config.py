from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_BASE_URL: str
    FERNET_KEY: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7   # 1 week
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ENVIRONMENT: str  # "development" or "production" (production disables /docs)

    # Explicit list of browser origins; empty means no cross-origin access.
    ALLOWED_ORIGINS: list[str] = []

    # --- Outbound email (registration verification codes) ------------------
    # When SMTP_HOST is empty the email service runs in "dev" mode: it logs the
    # code and writes the rendered email to disk instead of sending it.
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    # Connection security: "ssl" (implicit TLS, e.g. port 465),
    # "starttls" (upgrade on a plain connection, e.g. port 587) or "none".
    SMTP_SECURITY: str = "starttls"
    EMAIL_FROM: str = "no-reply@hrsystem.local"
    EMAIL_FROM_NAME: str = "HR System"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
