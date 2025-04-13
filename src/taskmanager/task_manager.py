"""To do task save in dictionary"""
import pandas as pd
# from helper import val_task_info


class TaskManager:
    def __init__(self):

        # self.tm_dict = {}
        self.db_tasks  = []

    def task_info(self):
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


    def status(self):

        # get task user wants to change status of
        while True:
            try:
                task = input("Enter task: ").strip().capitalize()
                if not task: raise IndexError("Cannot accept no value") #check if task empty
                if task not in  self.tm_dict: raise KeyError("Task not in memory") #make sure task in dictionary


                status = input("--Change status (pending/done): ").strip().capitalize()
                #makes sure user enters valid status
                if status.lower() not in "pending""done":
                    raise IndexError("Invalid status! User can only enter(pending/done)")
                self.tm_dict[task] = status

                """Set a condition so that when status is set to done its delete from db and cache """


                return print(self.tm_dict)

            except (KeyError,IndexError) as e:
                print(f"Error: {e}")
                #ask user if they want to retry
                retry = input("Do you want to try again: ").strip()
                if retry.lower() != 'y':
                    for _ in range(50):
                        print('-',end ="")
                    print("closed")
                    break
    def __delete__(self):
        """What do you wish to delete?
        """
        pass

if __name__ == "__main__":
    from Task_Manger_.src.auth.userSystem import UserSystem
    from Task_Manger_.src.db.connection import DataBase
    from Task_Manger_.src.db.task_queries import TaskQueries

    task_manager = TaskManager()
    db_connection = DataBase()
    # tasks = TaskQueries()
    user = UserSystem(db_connection.conn, db_connection.cur)
    tasks = TaskQueries(db_connection.conn, db_connection.cur)
    user_name = "Mubaraq"
    # tasks = TaskQueries(db_connection.conn, db_connection.cur)
    task_dict = tasks.list_tasks(user_name)
    print(task_manager.list_all(task_dict))

