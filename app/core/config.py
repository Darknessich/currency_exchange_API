from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="app_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    host: str
    port: int
    log_level: str


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="auth_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    pass


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app: AppSettings = AppSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
