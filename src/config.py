import datetime
import enum
import logging
import os
import pathlib
import typing

from pydantic_settings import BaseSettings

PROJECT_NAME = "yass-wpp-service"
API_VERSION = "1"
API_PREFIX = f"/api/v{API_VERSION}"

ROOT_PROJECT_DIR = pathlib.Path(__file__).parent.parent
ENV_FILE_PATH = os.path.join(ROOT_PROJECT_DIR, ".env")

origins = ["*"]


class Environment(str, enum.Enum):
    PROD = "PROD"
    DEV = "DEV"
    STAGING = "STAGE"
    CICD = "CICD"

    @staticmethod
    def from_str(label: typing.Optional[str]) -> "Environment":
        if label is not None:
            if label.upper() in ("PROD", "PRODUCTIVE"):
                return Environment.PROD
            elif label.upper() in ("STG", "STAGING"):
                return Environment.STAGING
            elif label.upper() in ("CICD"):
                return Environment.CICD
        return Environment.DEV

    @staticmethod
    def get_log_level(environment: "Environment") -> int:
        if environment == Environment.DEV:
            return logging._nameToLevel["DEBUG"]
        return logging._nameToLevel["INFO"]


class AppConfig(BaseSettings):
    app_name: str = "YASS-NEWS"
    # base_url: str

    db_url: str
    db_schema: str

    slack_webhook_url: str

    @property
    def environment(self) -> Environment:
        return Environment.from_str(os.environ.get("ENVIRONMENT"))

    @property
    def logger_level(self) -> int:
        return Environment.get_log_level(self.environment)

    class Config:
        extra = "allow"


settings = AppConfig(_env_file=ENV_FILE_PATH, _env_file_encoding="utf-8")  # type: ignore
