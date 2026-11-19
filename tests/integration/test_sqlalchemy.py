import pytest
# from sqlalchemy.orm import Session
# from models.task import Task
# from models.task_group import TaskGroup
from models.users import Users
# from models.db import Base

@pytest.mark.sqlalchemy
def test_admin_sql_alchemy(admin_session):
    test_user = Users(usr_name="steven" , pwd_hash="abc123!@#" , email="test@test.com")

    admin_session.add(test_user)
    admin_session.flush()
    print(f'usr_id: {test_user.usr_id}')
    assert test_user.usr_id is not None