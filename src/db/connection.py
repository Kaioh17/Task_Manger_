import psycopg2

class DataBase:
    def __init__(self):
        try:

            self.conn = psycopg2.connect(
                        user="postgres",
                        password="1308",
                        database="task_manager",
                        port="5432",
                        host="localhost",
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