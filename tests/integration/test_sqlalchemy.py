import pytest
from psycopg.errors import InsufficientPrivilege
from sqlalchemy import select, insert, update, delete, DropTable, CreateTable
from sqlalchemy.exc import ProgrammingError
# from sqlalchemy.orm import Session
from models.task import Task
from models.task_group import TaskGroup
from models.users import User
# from models.db import Base


# test that admin user can read and write
@pytest.mark.sqlalchemy
@pytest.mark.integration
def test_admin_can_read_and_write_sqlalchemy(admin_session):
    test_user = User(usr_name="admin_test_user" , pwd_hash="abc123!@#" , email="test@test.com")

    admin_session.add(test_user)
    admin_session.flush()
    print(f'usr_id: {test_user.usr_id}')
    assert test_user.usr_id is not None

# test that readwrite user can actually read and write
@pytest.mark.sqlalchemy
@pytest.mark.integration
def test_readwrite_can_read_and_write_sqlalchemy(readwrite_session):
    test_user = User(usr_name="readwrite_test_user" , pwd_hash="abc123!@#" , email="test@test.com")

    readwrite_session.add(test_user)
    readwrite_session.flush()
    print(f'usr_id: {test_user.usr_id}')
    assert test_user.usr_id is not None


# test that readonly cannot modify users table
@pytest.mark.sqlalchemy
@pytest.mark.integration
def test_readonly_cant_write_sqlalchemy(readonly_session):
    test_user = User(usr_name="readonly_test_user" , pwd_hash="abc123!@#" , email="test@test.com")

    with pytest.raises(ProgrammingError) as exc_info:
        readonly_session.add(test_user)
        readonly_session.flush()

    assert isinstance(exc_info.value.orig, InsufficientPrivilege)

@pytest.mark.sqlalchemy
@pytest.mark.integration
@pytest.mark.usefixtures("seeded_users") # use this instead of passing into function so that it doesn't get marked as "not accessed"
def test_readonly_can_read_sqlalchemy(readonly_session):
    fetched_user1, fetched_user2, fetched_user3 = tuple(readonly_session.query(User).all())

    assert fetched_user1.usr_id is not None
    assert fetched_user1.usr_name == "seeded_username1"
    assert fetched_user1.pwd_hash == "seeded_hash123!@#1"
    assert fetched_user1.email == "seed1@test.com"
    assert fetched_user1.created_at is not None
   
    assert fetched_user2.usr_id is not None
    assert fetched_user2.usr_name == "seeded_username2"
    assert fetched_user2.pwd_hash == "seeded_hash123!@#2"
    assert fetched_user2.email == "seed2@test.com"
    assert fetched_user2.created_at is not None

    assert fetched_user3.usr_id is not None
    assert fetched_user3.usr_name == "seeded_username3"
    assert fetched_user3.pwd_hash == "seeded_hash123!@#3"
    assert fetched_user3.email == "seed3@test.com"
    assert fetched_user3.created_at is not None
