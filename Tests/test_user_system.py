import pytest
from Task_Manger_.src.db.connection_test import TestDB
from Task_Manger_.src.auth.userSystem import UserSystem
import bcrypt

@pytest.fixture
def db():
    """Provides a fresh instance of the database class and cleans up after the test"""
    test_db = TestDB()
    yield  test_db
    #clean db after each test
    test_db.cur.execute("DELETE FROM user_table;")
    test_db.conn.commit()
    test_db.close_database()

def test_login(monkeypatch,db):
    #convert password to hash
    raw_pw = '12333'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str= hashed_pw.decode('utf-8')
    #insert user to the table for testing
    db.cur.execute(
        "INSERT INTO user_table (user_name,user_password) VALUES (%s , %s);" ,
                   ('John', hashed_pw_str)
        )
    db.conn.commit()

    # simulate login
    inputs = iter(["y","John", "12333"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # run the login and check the returned user_name
    system = UserSystem(db.conn, db.cur)
    result =  system.login()

    assert result == 'John'

def test_login_user_not_found_retry_success(monkeypatch,db):
    raw_pw = '12345'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode('utf_8')
    #insert user to the table for testing
    db.cur.execute("INSERT INTO user_table (user_name,user_password) VALUES (%s , %s);", ('John', hashed_pw_str))
    db.conn.commit()

    #Simulate login
    inputs = iter(["Y", "Jane", "R"]) #input incorrect name
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    inputs = iter(["Y","John","12345"]) #input correct password
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    system = UserSystem(db.conn, db.cur)
    result = system.login()
    assert result == "John"


def test_login_user_not_found_create_user(monkeypatch, db):
    raw_pw = '12345'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode('utf-8')

    # insert user to the table for testing
    db.cur.execute("INSERT INTO user_table (user_name,user_password) VALUES (%s , %s);", ('John', hashed_pw_str))
    db.conn.commit()

    #simulate login
    inputs = iter(["Y", "Jane", "N","Jane", "12345", "12345"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    system = UserSystem(db.conn, db.cur)
    result = system.login()

    assert result == "Jane"
def test_login_wrong_password_then_exit(db):
    raise NotImplemented
def test_login_wrong_password_then_retry_success(monkeypatch,db):
    # convert password to hash
    raw_pw = '1233'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode('utf-8')
    # insert user to the table for testing
    db.cur.execute(
        "INSERT INTO user_table (user_name,user_password) VALUES (%s , %s);",
        ('Mubaraq', hashed_pw_str)
    )
    db.conn.commit()

    # simulate login
    inputs = iter(["y", "Mubaraq", "2324","y"])  #wrong password
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    inputs = iter(["y", "Mubaraq", "1233", "y"])  # correct password
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # run the login and check the returned user_name
    system = UserSystem(db.conn, db.cur)
    result = system.login()

    assert result == 'Mubaraq'
def test_login_no_account_redirect(db):
    #enter "n"
    #should trigger create_user()
    raise NotImplemented

"""Test create password"""
def test_create_user_success(db):
    raise NotImplemented
def test_create_user_passwords_do_not_match(db):
    raise NotImplemented
def test_create_user_password_too_short(db):
    raise NotImplemented



