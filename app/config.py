from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "flash"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://flash:flash@localhost:5432/flash"
    redis_url: str = "redis://localhost:6379/0"
    whatsapp_verify_token: str = ""
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    llm_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
