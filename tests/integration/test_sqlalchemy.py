import pytest
from psycopg.errors import InsufficientPrivilege
from sqlalchemy import select, insert, update, delete, DropTable, CreateTable
from sqlalchemy.exc import ProgrammingError
from models.task import Task
from models.task_group import TaskGroup
from models.users import User


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


# tests that multiple users can be add and read from the database
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


@pytest.mark.integration
@pytest.mark.sqlalchemy
@pytest.mark.usefixtures("seeded_users_with_task_groups")
def test_readonly_can_read_task_groups_from_user(readonly_session):
    stmt1 = select(TaskGroup).join(TaskGroup.user).where(User.usr_name == "seeded_username1")
    stmt2 = select(TaskGroup).join(TaskGroup.user).where(User.usr_name == "seeded_username2")
    stmt3 = select(TaskGroup).join(TaskGroup.user).where(User.usr_name == "seeded_username3")

    user1_task_groups = readonly_session.scalars(stmt1).all()
    user1_task_group1 = user1_task_groups[0]
    user1_task_group2 = user1_task_groups[1]
    user2_task_group = readonly_session.scalar(stmt2)
    user3_task_group = readonly_session.scalar(stmt3)

    # check first user's taskgroups
    assert user1_task_group1.grp_id is not None
    assert user1_task_group1.usr_id is not None
    assert user1_task_group1.user is not None
    assert user1_task_group1.grp_name == "testgroup1"
    assert user1_task_group1.grp_desc == "test description"
    assert user1_task_group1.grp_due_date is None

    assert user1_task_group2.grp_id is not None
    assert user1_task_group2.usr_id is not None
    assert user1_task_group2.user is not None
    assert user1_task_group2.grp_name == "testgroup1.2"
    assert user1_task_group2.grp_desc == "test description"
    assert user1_task_group2.grp_due_date is None

    assert user1_task_group1.usr_id == user1_task_group2.usr_id # make sure both test groups refer to the same user owner
    assert user1_task_group1.user == user1_task_group2.user # make sure both test groups refer to the same user owner

    # check second user's taskgroup
    assert user2_task_group.grp_id is not None
    assert user2_task_group.usr_id is not None
    assert user2_task_group.user is not None
    assert user2_task_group.grp_name == "testgroup2"
    assert user2_task_group.grp_desc == "test description"
    assert user2_task_group.grp_due_date is None

    # check third user's taskgroup
    assert user3_task_group.grp_id is not None
    assert user3_task_group.usr_id is not None
    assert user3_task_group.user is not None
    assert user3_task_group.grp_name == "testgroup3"
    assert user3_task_group.grp_desc == "test description"
    assert user3_task_group.grp_due_date is None

    @pytest.mark.integration
    @pytest.mark.sqlalchemy
    @pytest.mark.usefixtures("seeded_users_with_task_groups_with_tasks")
    def test_readonly_can_read_task_from_task_group(readonly_session):
        stmt1 = select(Task).join(Task.task_group).join(TaskGroup.user).where(User.usr_name == "seeded_username1")
        stmt2 = select(Task).join(Task.task_group).join(TaskGroup.user).where(User.usr_name == "seeded_username2")
        stmt3 = select(Task).join(Task.task_group).join(TaskGroup.user).where(User.usr_name == "seeded_username3")

        user1_tasks = readonly_session.scalars(stmt1).all()
        user2_tasks = readonly_session.scalars(stmt2).all() # doing it this way to see if behavior of scalars and all change how it is returned
        user3_tasks = readonly_session.scalar(stmt3)

        assert user1_tasks[0].tsk_id is not None
        assert user1_tasks[0].grp_id is not None
        assert user1_tasks[0].tsk_name == "test1.0"
        assert user1_tasks[0].tsk_desc == "test1.0 description"
        assert user1_tasks[0].priority_lvl == 2
        assert user1_tasks[0].is_complete == False

        assert user1_tasks[1].tsk_id is not None
        assert user1_tasks[1].grp_id is not None
        assert user1_tasks[1].tsk_name == "test1.1"
        assert user1_tasks[1].tsk_desc == "test1.1 description"
        assert user1_tasks[1].priority_lvl == 3
        assert user1_tasks[1].is_complete == False

        assert user1_tasks[2].tsk_id is not None
        assert user1_tasks[2].grp_id is not None
        assert user1_tasks[2].tsk_name == "test1.2"
        assert user1_tasks[2].tsk_desc == "test1.2 description"
        assert user1_tasks[2].priority_lvl == 2
        assert user1_tasks[2].is_complete == False

        assert user1_tasks[0].task_group == user1_tasks[1].task_group
        assert user1_tasks[0].task_group != user1_tasks[2].task_group

        assert user2_tasks[0].tsk_id is not None
        assert user2_tasks[0].grp_id is not None
        assert user2_tasks[0].tsk_name == "test2"
        assert user2_tasks[0].tsk_desc == "test2 description"
        assert user2_tasks[0].priority_lvl == 3
        assert user2_tasks[0].is_complete == True

        assert user3_tasks.tsk_id is not None
        assert user3_tasks.grp_id is not None
        assert user3_tasks.tsk_name == "test3"
        assert user3_tasks.tsk_desc == "test3 description"
        assert user3_tasks.priority_lvl == 5
        assert user3_tasks.is_complete == True




    




