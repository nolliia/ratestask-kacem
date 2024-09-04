import os


class Config:
    POSTGRES_DB_HOST = os.environ.get("POSTGRES_DB_HOST", "localhost")
    POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME", "postgres")
    POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "ratestask")
