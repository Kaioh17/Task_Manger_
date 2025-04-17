from Task_Manger_.src.auth.userSystem import UserSystem
from Task_Manger_.src.db.connection import DataBase
from Task_Manger_.src.db.task_queries import TaskQueries
from Task_Manger_.src.taskmanager.task_manager import TaskManager


class Display:
    def __init__(self):
        task_manager = TaskManager()
        db_connection = DataBase()
        # tasks = TaskQueries()

        user = UserSystem(db_connection.conn, db_connection.cur)
        tasks = TaskQueries(db_connection.conn, db_connection.cur)
        user_name = user.login()
        task_dict = tasks.list_tasks(user_name)

        user_input = "Y"
        while user_input.upper() == "Y":
            navigate_tool = input("Do you want to 'add' a Task, change a 'status','List' all task, or 'delete' a task?: ").strip().lower()
            if navigate_tool.lower() == 'exit': break
            if navigate_tool.lower() == 'add':
                task_name = task_manager.task_info()
                print(tasks.add_task(user_name,task_name))
            elif navigate_tool.lower() == 'status':
                task_id = task_manager.status()
                print(tasks.status(task_id))
            elif navigate_tool.lower() == 'list':
                print(task_manager.list_all(task_dict))
            elif navigate_tool.lower() == 'delete':
                print(task_manager.list_all(task_dict)) #prints the available tasks for user
                task_id = task_manager.del_task()
                print(tasks.delete_task(task_id))
            user_input = input("Do you want to continue?Y|N ").strip().upper()

        db_connection.close_database()


if __name__ == "__main__":
    print_cli = Display()
