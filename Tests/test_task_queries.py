import pytest
from Task_Manger_.src.db.connection_test import TestDB
from Task_Manger_.src.db.task_queries import TaskQueries
import bcrypt
import random


@pytest.fixture
def db():
    """Provides a fresh instance of the database class and cleans up after the test"""
    test_db = TestDB()
    yield test_db
    # clean db after each test
    test_db.cur.execute("DELETE FROM user_table;")
    test_db.cur.execute("DELETE FROM task_table;")
    test_db.conn.commit()
    test_db.close_database()

#helper function for creating dummy users
def _create_test_user(user_id, name, db):
    # convert password to hash
    raw_pw = '12333'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode('utf-8')
    # insert user to the table for testing
    db.cur.execute(
        "INSERT INTO user_table (user_id, user_name,user_password) VALUES (%s, %s , %s);",
        ( user_id, name, hashed_pw_str)
    )
    db.conn.commit()
##helper function to add a test task to the table
def _add_test_task(monkeypatch,db):
    monkeypatch.setattr(random, "randint", lambda a, b: 1010)

    result = TaskQueries(db.conn, db.cur)
    result.add_task("John", "Testing")

def test_add_task(monkeypatch,db):
    #mock inputs

    _create_test_user(1234,"John", db)

    TaskQueries(db.conn,db.cur)
    _add_test_task(monkeypatch, db)

    ## check if task is added
    peek =  "SELECT task_id FROM task_table WHERE task_name = 'Testing';"
    db.cur.execute(peek)
    peeked = db.cur.fetchone()
    db.conn.commit()

    assert peeked[0] == 1010

def test_list_task(monkeypatch, db):
    _create_test_user(1234,"John", db)

    result = TaskQueries(db.conn, db.cur )
    _add_test_task(monkeypatch, db)
    # result.add_task("John" , "Testing")
    list_it = result.list_tasks("John")

    assert list_it == {1010: {'Testing': 'pending'}}  # mock task_id with monkey patch


def test_toggle_task_status(monkeypatch,db):
    _create_test_user(1234,"John", db)

    result = TaskQueries(db.conn, db.cur)
    _add_test_task(monkeypatch, db)
    status = result.toggle_task_status(1010)

    assert status == "done"

def test_delete_task(monkeypatch,db):
    _create_test_user(1234,"John", db)

    result =  TaskQueries(db.conn, db.cur)
    _add_test_task(monkeypatch, db)
    result.delete_task(1010)

    ##check the table to make sure it is empty
    db.cur.execute("SELECT * FROM task_table")
    peek = db.cur.fetchone()
    db.conn.commit()


    assert peek is None, "Expected no rows, but got data"

def test_delete_user(monkeypatch,db):

    _create_test_user(1234,"John", db)


    # perform function
    result = TaskQueries(db.conn, db.cur)
    result.del_user(1234)

    ##check if user exists
    db.cur.execute("SELECT user_id FROM user_table WHERE user_id = '1234'")
    peek = db.cur.fetchone()
    db.conn.commit()

    assert peek is None, "Expected no rows, but got data"



