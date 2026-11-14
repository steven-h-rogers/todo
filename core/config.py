"""Loads and validates the environment variables in one accessible location"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path

# ! Update this line if the project structure ever changes to reflect where the Base directory actually is relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent

# ! Do not create an instance of this class, instead import config instance
class Config(BaseSettings):
    admin_username: SecretStr
    admin_password: SecretStr

    read_only_username: SecretStr
    read_only_password: SecretStr

    read_write_username: SecretStr
    read_write_password: SecretStr

    prod_pooled_suffix: SecretStr
    prod_unpooled_suffix: SecretStr

    test_pooled_suffix: SecretStr
    test_unpooled_suffix: SecretStr

    model_config = SettingsConfigDict(env_file=BASE_DIR /".env", extra="ignore")

    # use prod and test to connect to production or test database respectively
    @property
    def prod_admin_uri(self) -> str:
        return f"postgresql//:{self.admin_username.get_secret_value()}:{self.admin_password.get_secret_value()}@{self.prod_pooled_suffix.get_secret_value()}"

    @property
    def prod_read_only_uri(self) -> str:
        return f"postgresql//:{self.read_only_username.get_secret_value()}:{self.read_only_password.get_secret_value()}@{self.prod_pooled_suffix.get_secret_value()}"

    @property
    def prod_read_write_uri(self) -> str:
        return f"postgresql//:{self.read_write_username.get_secret_value()}:{self.read_write_password.get_secret_value()}@{self.prod_pooled_suffix.get_secret_value()}"

    @property
    def test_admin_uri(self):
            return f"postgresql//:{self.admin_username.get_secret_value()}:{self.admin_password.get_secret_value()}@{self.test_pooled_suffix.get_secret_value()}"

    @property
    def test_read_only_uri(self):
            return f"postgresql//:{self.admin_username.get_secret_value()}:{self.admin_password.get_secret_value()}@{self.test_pooled_suffix.get_secret_value()}"

    @property
    def test_read_write_uri(self):
            return f"postgresql//:{self.admin_username.get_secret_value()}:{self.admin_password.get_secret_value()}@{self.test_pooled_suffix.get_secret_value()}"
    


# ! To use this class, import this instance
config = Config() 