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

    def list_tasks(self,user_name):
        try:
            #query to access tasks in db
            list_tasks_query= """ SELECT t.task_id, t.task_name,t.status  
                                    FROM user_table u 
                                    JOIN task_table t 
                                    ON u.user_id = t.user_id 
                                    WHERE u.user_name = %s ORDER BY t.created_on;
                                """

            self.cur.execute(list_tasks_query, (user_name,))  # execute query

            # get the values retrieved in database
            result = self.cur.fetchall()  # stores content retrieved
            if result:
                # print(result)
                all_data = {}
                for data in result:
                    task_id = data[0]
                    all_data[task_id] = {data[1]: data[2]}
                return all_data

            return {}

        except Exception as e:
            print(f"Error: {e}")
            return {}

    """Changes status of task"""
    def status(self,user_name):
        """
           use list all function to access the tasks
           get task_id for tasks that need to be changed
                check if task exists in the dictionary
                    if it does:
                        ask user for new status
                        send to database
        """

    """Delete_task will send every deleted task sent to the undo table in order for undo function to be active """
    def delete_task(self):
        pass

    def undo_task(self):
        pass
db_connection = DataBase()
test_function =  TaskQueries(db_connection.conn, db_connection.cur)

test_function.list_tasks('Mubaraq')