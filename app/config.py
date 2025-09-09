from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ambiente
    APP_ENV: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Banco de dados
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # URL de conexão completa (opcional, mas prática)
    DATABASE_URL: str

    # Configurações do Pydantic para ler o .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instância global que você importa no projeto
settings = Settings()
