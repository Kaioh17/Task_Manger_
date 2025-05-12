from Task_Manager_.src.auth.userSystem import UserSystem
from Task_Manager_.src.db.connection import DataBase
from Task_Manager_.src.db.task_queries import TaskQueries
from Task_Manager_.src.taskmanager.task_manager import TaskManager


class Display:
    def __init__(self):
        task_manager = TaskManager()
        db_connection = DataBase()
        # tasks = TaskQueries()

        user = UserSystem(db_connection.conn, db_connection.cur)
        tasks = TaskQueries(db_connection.conn, db_connection.cur)
        user_name = user.login()

        user_input = "Y"
        while user_input.upper() == "Y":
            task_dict = tasks.list_tasks(user_name)

            navigate_tool = input("Do you want to 'add' a Task, change a 'status','List' all task, or 'delete' a task?: ").strip().lower()

            if navigate_tool == 'exit': break
            if navigate_tool == 'add':
                task_name = task_manager.task_info()
                description = task_manager.add_description()
                print(tasks.add_task(user_name,task_name, description))
            elif navigate_tool == 'status':
                task_id = task_manager.status()
                print(tasks.toggle_task_status(task_id))
            elif navigate_tool== 'list':
                print(task_manager.list_all(task_dict))
            elif navigate_tool == 'delete':
                print(task_manager.list_all(task_dict)) #prints the available tasks for user to delete

                while True:
                    task_id = task_manager.del_task()
                    tasks.delete_task(task_id)

                    delete_more = input("Do you want to delete another task?(Y|N): ").upper().strip()

                    if delete_more != "Y":
                        break
            user_input = input("Do you want to continue?Y|N ").strip().upper()

        db_connection.close_database()


if __name__ == "__main__":
    print_cli = Display()
