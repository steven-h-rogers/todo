"""Loads and validates the environment variables in one accessible location"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    admin_username: str
    admin_password: str

    read_only_username: str
    read_only_password: str

    read_write_username: str
    read_write_password: str

    pooled_suffix: str
    unpooled_suffix: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def admin_url(self) -> str:
        return f"postgresql//:{self.admin_username}:{self.admin_password}@{self.pooled_suffix}"

    @property
    def read_only_url(self) -> str:
        return f"postgresql//:{self.read_only_username}:{self.read_only_password}@{self.pooled_suffix}"

    @property
    def read_write_url(self) -> str:
        return f"postgresql//:{self.read_write_username}:{self.read_write_password}@{self.pooled_suffix}"