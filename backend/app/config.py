from pathlib import Path
from urllib.parse import urlsplit

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parents[1]
MAX_RESULT_ROWS = 20


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", env_file_encoding="utf-8", extra="ignore")

    # DATABASE_URL takes precedence when supplied. Otherwise the MYSQL_* fields
    # below are used; there are no credential-bearing fallback defaults.
    database_url: str | None = None
    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str | None = None
    mysql_password: SecretStr = SecretStr("")
    mysql_database: str = "s_demo"
    sql_dialect: str = "mysql"
    business_timezone: str = ""

    ollama_host: str = "http://127.0.0.1:11434"
    ollama_api_key: SecretStr = SecretStr("")
    ollama_embed_host: str | None = None
    ollama_embed_api_key: SecretStr = SecretStr("")
    ollama_timeout_seconds: float = 120
    ollama_llm_model: str = "qwen2.5-coder:7b"
    ollama_embed_model: str = "nomic-embed-text"
    chroma_path: str = str(ROOT / "chroma_db")
    admin_schemas_path: str = str(ROOT / "admin" / "admin_schemas")
    top_tables: int = 3
    top_columns: int = 14
    top_examples: int = 4
    sql_candidates: int = 3
    max_repair_attempts: int = 2
    default_row_limit: int = MAX_RESULT_ROWS
    max_row_limit: int = MAX_RESULT_ROWS
    db_timeout_seconds: int = 8
    enable_data_sampling: bool = True
    enable_entity_resolution: bool = True
    entity_resolution_columns_limit: int = 300
    entity_resolution_matches_per_column: int = 4
    return_debug: bool = True
    session_secret: str = ""

    @field_validator("default_row_limit", "max_row_limit")
    @classmethod
    def cap_row_limit(cls, value: int) -> int:
        return max(1, min(value, MAX_RESULT_ROWS))

    @field_validator("chroma_path", "admin_schemas_path")
    @classmethod
    def resolve_storage_path(cls, value: str) -> str:
        path = Path(value).expanduser()
        return str((path if path.is_absolute() else ROOT / path).resolve())

    @property
    def database_connection_url(self) -> str | URL:
        if self.database_url:
            return self.database_url
        if not self.mysql_user:
            raise ValueError("Database credentials are missing: set DATABASE_URL or MYSQL_USER in .env")
        return URL.create(
            "mysql+pymysql",
            username=self.mysql_user,
            password=self.mysql_password.get_secret_value(),
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
        )

    @property
    def ollama_native_host(self) -> str:
        return self.ollama_host.rstrip("/").removesuffix("/v1")

    @property
    def ollama_direct_cloud(self) -> bool:
        return urlsplit(self.ollama_native_host).hostname == "ollama.com"

    @property
    def ollama_chat_model(self) -> str:
        model = self.ollama_llm_model
        if self.ollama_direct_cloud:
            return model.removesuffix(":cloud").removesuffix("-cloud")
        return model

    @property
    def embedding_host(self) -> str:
        if self.ollama_embed_host:
            return self.ollama_embed_host.rstrip("/").removesuffix("/v1")
        return "http://127.0.0.1:11434" if self.ollama_direct_cloud else self.ollama_native_host

    @property
    def domain_dir(self) -> Path:
        return ROOT / "domain"


settings = Settings()
