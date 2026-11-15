import pytest
import psycopg
from core.config import config

@pytest.fixture
def admin_db_connection():
    with psycopg.connect(config.test_admin_uri) as conn:
        try:
            yield conn
        finally:
            conn.rollback()

@pytest.fixture
def read_only_db_connection():
    with psycopg.connect(config.test_read_only_uri) as conn:
        try:
            yield conn
        finally:
            conn.rollback()

@pytest.fixture
def read_write_db_connection():
    with psycopg.connect(config.test_read_write_uri) as conn:
        try:
            yield conn
        finally:
            conn.rollback()