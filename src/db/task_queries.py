import random
from Task_Manger_.src.db.connection import DataBase
# from Task_Manger_.auth.userSystem import UserSystem

class TaskQueries:
    def __init__(self,conn, cur):
        self.conn = conn
        self.cur = cur

    """Retrieves task entered and saves to database"""
    def add_task(self, user_name, task_name):
        try:
            task_id = random.randint(10, 9999)

            #get user-id from username
            get_user_id = """
                            SELECT user_id FROM user_table WHERE user_name = %s
                            """
            #execute query
            self.cur.execute(get_user_id,(user_name,))
            # stores one row from result
            result = self.cur.fetchone()
            #close if user is not found
            if not result:
                print("user not found")
                return
            user_id = result[0]

            #add task info to table
            add_task_query = """
                            INSERT INTO task_table (task_id,user_id,task_name,status)
                            VALUES (%s, %s, %s, %s);
                            """
            #execute
            self.cur.execute(add_task_query,(task_id, user_id,task_name,"pending"))
            #commit to database
            self.conn.commit()

        except Exception as e:
            print(f"Error adding task to table {e}")

    """Delete_task will send every deleted task sent to the undo table in order for undo function to be active """
    def delete_task(self):
        pass

    def undo_task(self):
        pass
db_connection = DataBase()