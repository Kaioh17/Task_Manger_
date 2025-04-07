import random
from Task_Manger_.src.db.connection import DataBase


"""Handles User login"""
class UserSystem:
    def __init__(self,conn, cur):
        self.conn = conn
        self.cur = cur
    def login(self):

        try:
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
                print(f"{user_name} found in database")
                password = input("password: ").strip().capitalize()
                if password == result[0]:
                    print("Connected successfully you may begin!!!")
                    return user_name

                else:
                    #user is prompted to try again if username is incorrect
                    retry = input("password incorrect would you like to try again?(Y|N)").strip().capitalize()
                    if retry.lower() == "y":
                        return self.login() #restarts login
                    else:
                        return #exit


            else:
                print("user not found. Please create an account.")
                return self.create_user()

        except Exception as e:
            print("There was an error", e)

    def create_user(self):

        try:
            # get user id then eventually add hashing foe user id
            user_id = random.randint(1, 9900)

            #ask user for name
            user_name = input("Choose a user name: ").strip().capitalize()
            user_password = input("Choose a password: ").strip().capitalize()

            #create user sql query
            create_user_query = """
                                INSERT INTO user_table (user_id, user_name, user_password) VALUES (%s, %s, %s);
                                """
            #execute query
            self.cur.execute(create_user_query, (user_id,user_name,user_password))

            #commit transaction
            self.conn.commit()

            print(f"{user_name} successfully created as {user_id}")
            return user_name

        except Exception as e:
            print(f"ERROR: {e}")


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
                                        status VARCHAR(25) NOT NULL,
                                        created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (user_id) REFERENCES user_table(user_id)ON DELETE CASCADE
                                        );"""
            self.cur.execute(create_table_query_2)

            print("successfully created table ")
            self.conn.commit()

        except Exception as e:
            print(f"error creating table: {e}")


db_connection = DataBase()
user = UserSystem(db_connection.conn, db_connection.cur)
user.create_table()
db_connection.close_database()