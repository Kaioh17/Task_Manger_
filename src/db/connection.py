import psycopg2
import os
from dotenv import load_dotenv


####using pool to for easier connection

class DataBase:
    def __init__(self):
        try:
            load_dotenv()

            _user = os.getenv("DB_user")
            _db_name = os.getenv("DB_name")
            _password = os.getenv("DB_password")
            _port = os.getenv("DB_port")
            _host = os.getenv("DB_host")

            self.conn = psycopg2.connect(
                        user=_user,
                        password=_password,
                        database=_db_name,
                        port=_port,
                        host=_host,
                        )
            # cursor to perform database operations
            self.cur = self.conn.cursor()
            print("Connected to database successfully")

        except (Exception,psycopg2.Error) as e:
            print(f"Error connecting to database: {e}")

    def close_database(self):

        self.cur.close()
        self.conn.close()
        print("Connection Closed!!")

# connect_to = DataBase()
# connect_to.close_database()