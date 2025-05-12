import random
import re
import sys
from operator import length_hint

from psycopg2.errorcodes import INVALID_PASSWORD

from Task_Manager_.src.db.connection import DataBase

import bcrypt



"""Handles User login"""

#helper function
def _shutdown(message):
    # self.conn.close()
    # self.cur.close()
    sys.exit(message)


class UserSystem:
    def __init__(self,conn, cur):
        self.conn = conn
        self.cur = cur


    def login(self):
        retry_count = 0
        while retry_count < 3:
            try:
                retry_count += 1
                #ask user to login or signup
                request_login = input("Do you have an account(Y|N): ").strip().lower()

                if request_login.lower() != "y":
                   return self.create_user()

                user_name = input("User name: ").strip().capitalize()

                #check if user exists
                check_username = """
                                SELECT user_password FROM user_table WHERE user_name = %s;
                                """

                #execute query
                self.cur.execute(check_username, (user_name,))
                # stores one row from result
                result = self.cur.fetchone() #stores what password in tuple
                if result:
                    logged_pw = result[0]
                    print(f"welcome {user_name} ")
                    password = input("password: ").strip()
                    if bcrypt.checkpw(password.encode('utf-8'),logged_pw.encode('utf-8')):
                        print("Connected successfully you may begin!!!")
                        return user_name

                    else:
                        #user is prompted to try again if username is incorrect
                        retry = input("password incorrect would you like to try again?(Y|N)").strip().lower()

                        if retry.lower() == "y":
                        # password = input("Password: ").strip()
                            return self.login()   # restarts login
                        else:
                            return _shutdown("Exiting program...")#exit



                else:
                    while True:
                        retry = input("user not found. Would you like to create an account(New) or retry(R).").strip()
                        if retry.lower() != ('r','n'):
                            break
                        if retry.lower() == "r":
                            raise ValueError("Retry...")
                        elif retry.lower() == "n" or "new":
                            return self.create_user()
                        else:
                            return _shutdown("Exiting program...")

            except Exception as e:
                print("There was an error", e)

        return _shutdown("Retry limit reached...")

    def create_user(self):

        try:

            #helper function
            def _check_password(pw):
                if not re.match(r'^.{5,}$',pw):  # create test case for this (i.e when user enters less than 52)
                    raise ValueError("Password entered is to low... try again")
            # get user id then eventually add hashing foe user id
            user_id = random.randint(1, 9900)

            #ask user for name
            user_name = input("Choose a user name: ").strip().capitalize()

            if not re.match(r'^[A-Za-z0-9]+$', user_name):   #create test case for this
                raise ValueError("Password entered is to low... try again")

            print("Password must be at least 5 characters long...")
            user_password = str(input("Choose a password: ")).strip()
            _check_password(user_password) #checks password before

            confirm_password = str(input("confirm the password: ")).strip() #prompt user to confirm password
            _check_password(confirm_password) #handle any edge case
            #check if passwords are the same
            if user_password != confirm_password:
                raise ValueError("Passwords do not match....try again")
            #check if password is correct length

            # hash password to protect password in database
            hashed_pw = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt())#protect password in database
            hashed_pw_str = hashed_pw.decode('utf-8')
            # print(hashed_pw)

            #create user sql query

            create_user_query = """
                                INSERT INTO user_table (user_id, user_name, user_password) VALUES (%s, %s, %s);
                                """
            #execute query
            self.cur.execute(create_user_query, (user_id,user_name,hashed_pw_str))

            #commit transaction
            self.conn.commit()

            print(f"{user_name} successfully created as {user_id}")
            return user_name

        except Exception as e:
            return f"ERROR: {e}"



        # function to create tables
    def create_table(self):

        try:
            # create user table
            create_table_query = """CREATE TABLE IF NOT EXISTS user_table(
                                        user_id SERIAL PRIMARY KEY,
                                        user_name VARCHAR(225) NOT NULL,
                                        user_password TEXT NOT NULL
                                        );"""
            self.cur.execute(create_table_query)

            # create tasks table
            create_table_query_2 = """CREATE TABLE IF NOT EXISTS task_table(
                                        task_id SERIAL PRIMARY KEY,
                                        user_id INT NOT NULL, 
                                        task_name VARCHAR(225) NOT NULL,
                                        description VARCHAR(225),
                                        status VARCHAR(25) NOT NULL,
                                        created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        completed_on TIMESTAMP, 
                                        FOREIGN KEY (user_id) REFERENCES user_table(user_id)ON DELETE CASCADE
                                        );"""
            self.cur.execute(create_table_query_2)
            #create task archive
            create_table_query_3 = """CREATE TABLE IF NOT EXISTS task_archive(
                                           archive_id SERIAL PRIMARY KEY,
                                           task_id INT NOT NULL,
                                           user_id INT NOT NULL, 
                                           task_name VARCHAR(225) NOT NULL,
                                           status VARCHAR(25) NOT NULL,
                                           deleted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                           FOREIGN KEY (user_id) REFERENCES user_table(user_id)ON DELETE CASCADE
                                           );"""
            self.cur.execute(create_table_query_3)

            print("successfully created table ")
            self.conn.commit()

        except Exception as e:
            print(f"error creating table: {e}")


if __name__ == "__main__":

    db_connection = DataBase()
    user = UserSystem(db_connection.conn, db_connection.cur)
    # user.login()
    user.create_table()


