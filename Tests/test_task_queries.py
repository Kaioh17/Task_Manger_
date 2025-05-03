import pytest
from Task_Manger_.src.db.connection_test import TestDB
from Task_Manger_.src.db.task_queries import TaskQueries
import bcrypt


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
def _create_test_user(name, db):
    # convert password to hash
    raw_pw = '12333'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode('utf-8')
    # insert user to the table for testing
    db.cur.execute(
        "INSERT INTO user_table (user_id, user_name,user_password) VALUES (%s,%s , %s);",
        ('1234', name, hashed_pw_str)
    )
    db.conn.commit()

def test_add_task(monkeypatch,db):
    #mock inputs
    # monkeypatch.setattr(random, "randint", lambda a, b: 1010)
    _create_test_user("John", db)
    #
    #
    result = TaskQueries(db.conn,db.cur)
    result.add_task("John", "Testing")

    #
    peek =  "SELECT user_id FROM task_table WHERE task_name = 'Testing';"
    db.cur.execute(peek)
    peeked = db.cur.fetchone()
    db.conn.commit()

    assert peeked[0] == 1234

def test_list_task(monkeypatch, db):
    pass

def test_toggle_task_status(monkeypatch,db):
    pass

def test_delete_task(monkeypatch,db):
    pass

def test_delete_user(monkeypatch,db):
    pass


