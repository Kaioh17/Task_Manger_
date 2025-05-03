from os import system

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

#helper function for creating dummy users
def _create_test_user(name, db):
    # convert password to hash
    raw_pw = '12345'
    hashed_pw = bcrypt.hashpw(raw_pw.encode('utf-8'), bcrypt.gensalt())
    hashed_pw_str = hashed_pw.decode('utf-8')
    # insert user to the table for testing
    db.cur.execute(
        "INSERT INTO user_table (user_id, user_name,user_password) VALUES (%s,%s , %s);",
        ('1234', name, hashed_pw_str)
    )
    db.conn.commit()

def test_login(monkeypatch,db):
    #convert password to hash
    _create_test_user("John", db)

    # simulate login
    inputs = iter(["y","John", "12345"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # run the login and check the returned user_name
    system = UserSystem(db.conn, db.cur)
    result =  system.login()

    assert result == 'John'


def test_login_user_not_found_retry_success(monkeypatch,db):
    _create_test_user("John", db)
    #Simulate login
    inputs = iter(["Y", "Jane", "R"]) #input incorrect name
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    inputs = iter(["Y","John","12345"]) #input correct password
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    system = UserSystem(db.conn, db.cur)
    result = system.login()
    assert result == "John"
def test_login_user_not_found_create_user(monkeypatch, db):
    _create_test_user("John", db)

    #simulate login
    inputs = iter(["Y", "Jane", "N","Jane", "12345", "12345"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    login = UserSystem(db.conn, db.cur)
    result = login.login()

    assert result == "Jane"



def test_login_wrong_password_then_exit(monkeypatch,db):
    _create_test_user("John", db)

    # simulate inputs
    inputs = iter(["y", "John", "11234", "N"])
    monkeypatch.setattr("builtins.input",lambda _: next(inputs))

    system = UserSystem(db.conn, db.cur)


    with pytest.raises(SystemExit): # checks if  this input has a
        system.login()
def test_login_wrong_password_then_retry_success(monkeypatch,db):
    _create_test_user("John", db)

    # simulate login
    inputs = iter(["y", "John", "12323","y"])  #wrong password
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    inputs = iter(["y", "John", "12345", "y"])  # correct password
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # run the login and check the returned user_name
    system = UserSystem(db.conn, db.cur)
    result = system.login()

    assert result == 'John'

def test_login_wrong_password_retry_limit(monkeypatch, db):
    _create_test_user("John", db)

    #simulate login
    inputs = iter(['y','John','1233','y'])
    monkeypatch.setattr("builtins.inputs", lambda _:next(inputs))

    #start function
    login = UserSystem(db.conn,db.cur)

    with pytest.raises(SystemExit):
        login.login()


"""Test create user"""
def test_create_user_success(monkeypatch,db):

    #simulate user inputs
    inputs = iter(['John', '12345', '12345'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    #call function
    create = UserSystem(db.conn, db.cur)
    result = create.create_user()

    assert result == 'John'
def test_create_user_passwords_do_not_match(monkeypatch, db):
    #simulate input

    inputs = iter(['John', '12345', '12343'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    inputs = iter(['John', '12345', '12345'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    #call function
    create = UserSystem(db.conn,db.cur)
    result =  create.create_user()

    assert result == 'John'

def test_create_user_password_too_short(monkeypatch, db):
    inputs = iter(['John', '1234', '1234'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    inputs = iter(['John', '12345', '12345'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # call function
    create = UserSystem(db.conn, db.cur)
    result = create.create_user()

    assert result == 'John'

def test_create_user_password_retries_limit(monkeypatch,db):


    inputs = iter(['John', '1234','John', '1344' ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    create = UserSystem(db.conn, db.cur)
    with pytest.raises(SystemExit):
        create.create_user()




