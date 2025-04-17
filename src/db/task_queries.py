import random
from datetime import datetime

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
                raise ValueError("user not found")
                # return
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
                print(all_data)
                return all_data

            return {}

        except Exception as e:
            print(f"Error: {e}")
            return {}

    #heelper function
    def _verify_task_id(self,task_id):
        if not task_id:
                raise ValueError("Cannot be empty...")
        verify_task_id = """SELECT task_id FROM task_table WHERE task_id = %s; """
        self.cur.execute(verify_task_id, (task_id,))
        result = self.cur.fetchone()
        if not result:
            print(f"{task_id} does not exist!!!!!")

    """Changes the status of a task and handles cleanup if completed over 20 mins ago."""
    def status(self,task_id):
        try:
            self._verify_task_id(task_id)

            # Get current status
            self.cur.execute("""SELECT status FROM task_table WHERE task_id = %s""", (task_id,))
            current_status = self.cur.fetchone()[0]

            ## toggle between "pending" and "done"
            new_status = "pending" if current_status == "done" else  "done"
            ## status
            if new_status == "done":
                #mark tasks as completed
                self.cur.execute("""UPDATE task_table 
                                    SET completed_on = CURRENT_TIMESTAMP
                                    WHERE task_id = %s;""", (task_id,))
                self.cur.execute("""SELECT completed_on FROM task_table WHERE task_id = %s; """, (task_id,))

                created_on =self.cur.fetchone()[0]
                # print("Time: ",created_on)

                # Compare current time and completed time
                now = datetime.now().replace(tzinfo=None)
                created_on = created_on.replace(tzinfo=None)
                # print("Time now: ",now)
                diff = now - created_on

                if diff.total_seconds() >= 1200:
                    self.delete_task(task_id)

                # self.conn.commit()
            else:
                # Reset completion time when status is changed back to pending
                self.cur.execute("""UPDATE task_table 
                                    SET completed_on = NULL
                                    WHERE task_id = %s;""", (task_id,))
            #update status column
            update_status_query = """
                                    UPDATE task_table 
                                    SET status = %s
                                    WHERE task_id = %s;        
                                    """

            self.cur.execute(update_status_query, (new_status,task_id,))
            self.conn.commit()
        except (Exception, ValueError) as e:
            print(f"Error: {e}")
    """Delete_task will send every deleted task sent to the undo table in order for undo function to be active """
    def delete_task(self,task_id):
        try:
            '''Implementing a delete  function that saves the task to delete in an archive'''

            # this stores deleted task to archive for 24hrs before archive refreshes
            save_task = """
                            INSERT INTO task_archive (task_id, user_id, task_name, status)
                            SELECT task_id,user_id, task_name, status
                            FROM task_table
                            WHERE task_id = %s;
                        """
            self.cur.execute(save_task, (task_id,))

            #deletes task from the task_table
            delete_task = """DELETE FROM task_table WHERE task_id = %s;"""
            self.cur.execute(delete_task, (task_id,))

            #clear archive after 24 hours
            clear_archive = """DELETE FROM task_archive WHERE deleted_on < now() -INTERVAL '3 HOURS';"""
            self.cur.execute(clear_archive)

            print("move was success")
            self.conn.commit()
        except Exception as e:
            print(f"ERROR: {e}")




    def undo_task(self):
        pass

if __name__ == "__main__":

    db_connection = DataBase()
    test_function =  TaskQueries(db_connection.conn, db_connection.cur)
    # test_function.list_tasks('Mubaraq')
    test_function.list_tasks('Tosin')
    test_function.status("3839")

