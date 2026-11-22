import pytest
import psycopg
from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, TaskGroup, Task
# from models.users import User
# from models.task import Task
# from models.task_group import TaskGroup
# from models.db import Base

# ENGINES
@pytest.fixture(scope="session")
def admin_test_engine():
    admin_test_engine = create_engine(config.test_admin_uri, echo=True, pool_pre_ping=True, pool_size=3)
    yield admin_test_engine

@pytest.fixture(scope="session")
def readonly_test_engine():
    readonly_test_engine = create_engine(config.test_read_only_uri, echo=True, pool_pre_ping=True, pool_size=3)
    yield readonly_test_engine

@pytest.fixture(scope="session")
def readwrite_test_engine():
    readwrite_test_engine = create_engine(config.test_read_write_uri, echo=True, pool_pre_ping=True, pool_size=3)
    yield readwrite_test_engine

# SESSIONS
@pytest.fixture(scope="function")
def admin_session(admin_test_engine):
    with Session(admin_test_engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def readonly_session(readonly_test_engine):
    with Session(readonly_test_engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def readwrite_session(readwrite_test_engine):
    with Session(readwrite_test_engine) as session:
        yield session
        session.rollback()

# SEEDS FOR TESTING WHEN USER PRIVILEGE CANNOT CREATE ROWS

# Use when pre-existing data is needed and current role can't create rows itself
@pytest.fixture(scope="function")
def seeded_users(readwrite_session):
    users = [
        User(usr_name="seeded_username1", pwd_hash="seeded_hash123!@#1", email="seed1@test.com"),
        User(usr_name="seeded_username2", pwd_hash="seeded_hash123!@#2", email="seed2@test.com"),
        User(usr_name="seeded_username3", pwd_hash="seeded_hash123!@#3", email="seed3@test.com")
        ]
    readwrite_session.add_all(users)
    readwrite_session.commit()
    for user in users:
        readwrite_session.refresh(user)

    yield users

    for user in users:
        readwrite_session.delete(user)
    readwrite_session.commit()

# users with task_groups
@pytest.fixture(scope="function")
def seeded_users_with_task_groups(readwrite_session):

    users = [
        User(usr_name="seeded_username1", pwd_hash="seeded_hash123!@#1", email="seed1@test.com"),
        User(usr_name="seeded_username2", pwd_hash="seeded_hash123!@#2", email="seed2@test.com"),
        User(usr_name="seeded_username3", pwd_hash="seeded_hash123!@#3", email="seed3@test.com")
        ]

    users[0].task_groups.append(TaskGroup(grp_name="testgroup1", grp_desc="test description"))
    users[0].task_groups.append(TaskGroup(grp_name="testgroup1.2", grp_desc="test description"))

    users[1].task_groups.append(TaskGroup(grp_name="testgroup2", grp_desc="test description"))
    users[2].task_groups.append(TaskGroup(grp_name="testgroup3", grp_desc="test description"))

    readwrite_session.add_all(users)
    readwrite_session.commit()
    for user in users:
        for task_group in user.task_groups:
            readwrite_session.refresh(task_group)
            readwrite_session.refresh(user)

    yield users

    for user in users:
        for task_group in user.task_groups:
            readwrite_session.delete(task_group)
            readwrite_session.delete(user)
    readwrite_session.commit()


# PSYCOPG

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