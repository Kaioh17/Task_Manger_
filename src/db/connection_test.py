import psycopg2

class TestDB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                user="postgres",
                password="1308",
                database="test_task_manager",
                port="5432",
                host="localhost",
            )

            self.cur = self.conn.cursor()
        except(Exception,psycopg2.Error) as e:
            print(f"Error connecting to test-db: {e}")

    def close_database(self):
        self.cur.close()
        self.conn.close()
        print("Test Connection Closed!!")