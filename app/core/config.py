from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="app_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    host: str
    port: int
    log_level: str


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="db_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    user: str
    password: str
    host: str
    port: int
    name: str

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="auth_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    repeat: int
    secret: str
    algorithm: str
    salt: str
    salt_len: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
