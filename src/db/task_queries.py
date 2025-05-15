import random
from datetime import datetime

from anyio import sleep_forever

from Task_Manager_.src.db.connection import DataBase
# from Task_Manager_.auth.userSystem import UserSystem

class TaskQueries:
    def __init__(self,conn, cur):
        self.conn = conn
        self.cur = cur

    # helper function
    def _verify_task_id(self, task_id):
        if not task_id:
            raise ValueError("Cannot be empty...")
        verify_task_id = """SELECT task_id FROM task_table WHERE task_id = %s; """
        self.cur.execute(verify_task_id, (task_id,))
        result = self.cur.fetchone()

        if not result:
             raise ValueError(f"{task_id} does not exist!!!!!")

        return result
    #helper: validates user_id
    def _verify_user_id(self, user_id):
        if not user_id:
            raise ValueError("Cannot be empty.....")
        verify_user_id = """SELECT user FROM task_table WHERE user_id = %s; """
        self.cur.execute(verify_user_id, (user_id,))
        result = self.cur.fetchone()

        if not result:
            raise ValueError(f"{user_id} does not exist!!!!!")

        return result
    def _get_user_id(self,user_name):
        try:
            get_user_id = """
                            SELECT user_id FROM user_table WHERE user_name = %s
                            """
            self.cur.execute(get_user_id, (user_name,))
            # stores one row from result
            result = self.cur.fetchone()
            return result
        except Exception as e:
            return f"Error: {e}"


    """Retrieves task entered and saves to database"""
    def add_task(self, user_name: str, task_name: str, description = "None"):
        try:
            task_id = random.randint(10, 9999)

            # stores one row from result
            result = self._get_user_id(user_name)
            #close if user is not found
            if not result:
                raise ValueError("user not found")
                # return
            user_id = result[0]

            #add task info to table
            add_task_query ="""
                            INSERT INTO task_table (task_id,user_id,task_name,status)
                            VALUES (%s, %s, %s, %s);
                            """

           #execute
            self.cur.execute(add_task_query,(task_id, user_id,task_name,"pending"))
            #commit to database
            self.conn.commit()

            self._description(task_id, description)  ##contains query to set the description if needed

            return task_id

        except Exception as e:
            return  f"Error adding task to table {e}"

    def _description(self, task_id, description):
        #helper function to describe the tasks
        try:
            set_description = '''UPDATE task_table SET description = %s WHERE task_id = %s;'''
            self.cur.execute(set_description, (description, task_id))
            self.conn.commit()


            return description
        except Exception as e:
            return f"error: {e}"




    def list_tasks(self,user_name):
        try:
            #query to access tasks in db
            list_tasks_query= """ 
                                    SELECT t.task_id, t.task_name,t.status  
                                    FROM user_table u 
                                    JOIN task_table t 
                                    ON u.user_id = t.user_id 
                                    WHERE u.user_name = %s ORDER BY t.created_on;
                                """

            self.cur.execute(list_tasks_query, (user_name,))  # execute query

            # get the values retrieved in database
            result = self.cur.fetchall()  # stores content retrieved
            if result:

                all_data = {}
                for data in result:
                    task_id = data[0]
                    all_data[task_id] = {data[1]: data[2]}
            # if result:
            #
            #     all_data = []
            #     for data in result:
            #         task = {
            #             "task_id": data[0],
            #             "task_title": data[1],
            #             "status": data[2]
            #         }
            #         all_data.append(task)

                # print(all_data)
                return all_data

            return []

        except Exception as e:
            return f"Error: {e}"




    """Changes the status of a task and handles cleanup if completed over 20 mins ago."""
    def toggle_task_status(self, task_id):
        try:
            task_id = self._verify_task_id(task_id)[0]

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

                completed_on =self.cur.fetchone()[0]


                # i will be using fast api for this
                # to set a timer to move a task to the archives after being created




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

            return f"Status has been set to '{new_status}'"
        except (Exception, ValueError) as e:
            return f"Error: {e}"
    """Delete_task will send every deleted task sent to the undo table in order for undo function to be active """
    def delete_task(self,task_id):
        try:
            '''Implementing a delete  function that saves the task to delete in an archive'''
            self._verify_task_id(task_id)
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
            self.conn.commit()

            return "Move was a success"

        except Exception as e:
          return f"ERROR: {e}"

    def del_user(self, user_id):
        try:
            self._verify_user_id(user_id)

            self.cur.execute("DELETE FROM user_table WHERE user_id = %s ", (user_id,))

            self.conn.commit()


            return user_id

        except Exception as e:
            return f"Error: {e}"




    def undo_task(self, name):
        try:
            #undo task
            # retrieves last deleted task from the task archive
            # base on user_id matched from login
            return

        except Exception as e:
            return f"Error: {e}"
    #
    #     pass

if __name__ == "__main__":

    db_connection = DataBase()
    test_function =  TaskQueries(db_connection.conn, db_connection.cur)
    test_function.list_tasks('Tosin')
    # test_function.toggle_task_status(3082)


    # test_function.add_task('Tosin',"Set the plane","Check engines" )
    # test_function._description("5503","Get new trucks on the way" )
    # test_function.toggle_task_status("3839")

    # test_function.del_user('3987')