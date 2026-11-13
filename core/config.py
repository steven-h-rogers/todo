"""Loads and validates the environment variables in one accessible location"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

# ! Update this line if the project structure ever changes to reflect where the Base directory actually is relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    admin_username: SecretStr
    admin_password: SecretStr

    read_only_username: SecretStr
    read_only_password: SecretStr

    read_write_username: SecretStr
    read_write_password: SecretStr

    pooled_suffix: SecretStr
    unpooled_suffix: SecretStr

    model_config = SettingsConfigDict(env_file=BASE_DIR /".env", extra="ignore")


    @property
    def admin_url(self) -> str:
        return f"postgresql//:{self.admin_username.get_secret_value()}:{self.admin_password.get_secret_value()}@{self.pooled_suffix.get_secret_value()}"

    @property
    def read_only_url(self) -> str:
        return f"postgresql//:{self.read_only_username.get_secret_value()}:{self.read_only_password.get_secret_value()}@{self.pooled_suffix.get_secret_value()}"

    @property
    def read_write_url(self) -> str:
        return f"postgresql//:{self.read_write_username.get_secret_value()}:{self.read_write_password.get_secret_value()}@{self.pooled_suffix.get_secret_value()}"

config = Config()