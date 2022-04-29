from pydantic import BaseConfig

class Settings(BaseConfig):
    """App settings"""
    host: str
    port: int

    service_name: str = "sbf-challenge"
    workers_count: int

    reload=bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "SBF_CHALLENGE_"

settings = Settings()
