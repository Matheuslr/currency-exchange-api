import urllib

from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings"""

    host: str
    port: int

    service_name: str = "sbf-challenge"
    workers_count: int

    reload: bool

    currency_api_url: str

    mongo_host: str
    mongo_port: int

    mongo_user: str
    mongo_password: str
    mongo_database_name: str

    mongo_max_connections_count: int
    mongo_min_connections_count: int

    currency_collection_name = "currencies"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "SBF_CHALLENGE_"

    def mongo_url(self) -> str:

        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/{self.mongo_database_name}?authSource=admin"  # noqa


settings = Settings()
