"""To do task save in dictionary"""
import pandas as pd
# from helper import val_task_info
from Task_Manger_.src.db.task_queries import TaskQueries


class TaskManager:
    def __init__(self):

        # self.tm_dict = {}
        self.db_tasks  = []
    @staticmethod
    def task_info():
        """User adds task to memory """
        while True:
            try:
                #User inputs
                task = str(input("Task name: ").strip().capitalize())
                # val_task_info(task)
                if not task:
                    raise ValueError("Task cannot be empty!!")

                """Ask if user wants to enter in more task"""

                print(f"{task} successfully added")
                return task

            except (Exception,ValueError) as e:
                print(f"Error: {e} ")

                retry = input("Do you want to try again?(Y|N) ").strip(). capitalize()

                if retry.lower()!= "y":
                    for _ in range(50):
                        print("-", end = "")
                    print("Exited:(")
                    break

    # @staticmethod
    def list_all(self, task_dict):
        """display all task for current user in the database as a table"""
        while True:
            try:
                self.db_tasks = task_dict
                data = []
                for task_id, value in self.db_tasks.items():
                    task_name = list(value.keys())[0]
                    status = value[task_name]
                    data.append([task_id, task_name, status])
                df_list = pd.DataFrame(data, columns=[' task_id', ' task_name', ' status' ])

                print ("Table from list of lists:")
                print(f"-" * 50)
                return  df_list
            except Exception as e:
                print(f"Error in task_manager: {e}")

                retry= input("Do you want to try again(Y|N): ").strip().capitalize()

                if retry.lower() != 'y':
                    break

    @staticmethod
    def status():

        # get task user wants to change status of
        while True:
            try:
                task_id = input("Enter taskid: ").strip()

                return task_id
                # task2 = TaskQueries(db_connection.conn, db_connection.cur)
                # task2.status(task_id)

            except (KeyError,IndexError) as e:
                print(f"Error: {e}")
                #ask user if they want to retry
                retry = input("Do you want to try again: ").strip()
                if retry.lower() != 'y':
                    for _ in range(50):
                        print('-',end ="")
                    print("closed")
                    return

    @staticmethod
    def del_task():
        """What do you wish to delete?
        """
        try:
            task_id = input("Enter task id of task to delete: ")
            if not task_id:
                raise ValueError("Task cannot be empty")


            return task_id
        except Exception as e:
            return f"Error {e}"


if __name__ == "__main__":
    from Task_Manger_.src.auth.userSystem import UserSystem
    from Task_Manger_.src.db.connection import DataBase


    task_manager = TaskManager()
    db_connection = DataBase()
    # tasks = TaskQueries()
    user = UserSystem(db_connection.conn, db_connection.cur)
    tasks = TaskQueries(db_connection.conn, db_connection.cur)
    user_name = "Tosin"
    # tasks = TaskQueries(db_connection.conn, db_connection.cur)
    task_dict = tasks.list_tasks(user_name)
    print(task_manager.list_all(task_dict))

    task_manager.del_task()


