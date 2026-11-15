from core.config import config
import psycopg
from psycopg import errors
import pytest

# have a parametrized list of all of the database uri's and test if they work on one function
@pytest.mark.integration
@pytest.mark.parametrize(
    "config_db_uri",
    [config.test_admin_uri, config.test_read_only_uri, config.test_read_write_uri]
)
def test_valid_db_connection(config_db_uri):
    with psycopg.connect(config_db_uri) as conn:
        try:
            row = conn.execute("SELECT 1, current_user").fetchone()
            print(row)
            assert row[0] == 1
        finally:
            conn.rollback()


