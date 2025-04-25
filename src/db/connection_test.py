import psycopg2
import os
from dotenv import load_dotenv

class TestDB:
    def __init__(self):
        try:
            load_dotenv()

            _user = os.getenv("DB_user")
            _db_name = os.getenv("DB_test_name")
            _password = os.getenv("DB_password")
            _port = os.getenv("DB_port")
            _host = os.getenv("DB_host")

            self.conn = psycopg2.connect(
                user=_user,
                database=_db_name,
                password=_password,
                port=_port,
                host=_host
            )

            self.cur = self.conn.cursor()
        except(Exception,psycopg2.Error) as e:
            print(f"Error connecting to test-db: {e}")

    def close_database(self):
        self.cur.close()
        self.conn.close()
        print("Test Connection Closed!!")