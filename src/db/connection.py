import psycopg2

class DataBase:
    def __init__(self):
        try:

            self.conn = psycopg2.connect(
                user="postgres",
                password="1308",
                database="to_do_list",
                port="5432",
                host="localhost",
            )
            # cursor to perform database operations
            self.cur = self.conn.cursor()
            print("Connected to database successfully")

        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close_database(self):

        self.cur.close()
        self.conn.close()
        print("Connection Closed!!")