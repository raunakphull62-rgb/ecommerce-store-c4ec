from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    STRIPE_API_KEY: str = os.getenv("STRIPE_API_KEY")
    STRIPE_API_SECRET: str = os.getenv("STRIPE_API_SECRET")
    PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID")
    PAYPAL_CLIENT_SECRET: str = os.getenv("PAYPAL_CLIENT_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

def get_database_url() -> str:
    return settings.DATABASE_URL

def get_supabase_url() -> str:
    return settings.SUPABASE_URL

def get_supabase_key() -> str:
    return settings.SUPABASE_KEY

def get_jwt_secret_key() -> str:
    return settings.JWT_SECRET_KEY

def get_jwt_algorithm() -> str:
    return settings.JWT_ALGORITHM

def get_access_token_expire_minutes() -> int:
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES

def get_smtp_server() -> str:
    return settings.SMTP_SERVER

def get_smtp_port() -> int:
    return settings.SMTP_PORT

def get_smtp_username() -> str:
    return settings.SMTP_USERNAME

def get_smtp_password() -> str:
    return settings.SMTP_PASSWORD

def get_stripe_api_key() -> str:
    return settings.STRIPE_API_KEY

def get_stripe_api_secret() -> str:
    return settings.STRIPE_API_SECRET

def get_paypal_client_id() -> str:
    return settings.PAYPAL_CLIENT_ID

def get_paypal_client_secret() -> str:
    return settings.PAYPAL_CLIENT_SECRET