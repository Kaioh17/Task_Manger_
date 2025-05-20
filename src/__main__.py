from Task_Manager_.src.auth.userSystem import UserSystem
from Task_Manager_.src.db.connection import DataBase
from Task_Manager_.src.db.task_queries import TaskQueries
from Task_Manager_.src.taskmanager.task_manager import TaskManager


class Display:
    def __init__(self):
        task_manager = TaskManager()
        db = DataBase()
        # tasks = TaskQueries()

        user = UserSystem(db.conn, db.cur)
        tasks = TaskQueries(db.conn, db.cur)

        print("\n=====TASK MANAGER LOGIN======")
        user_name = user.login()

        user_input = "Y"
        while user_input.upper() == "Y":
            task_dict = tasks.list_tasks(user_name)

            print("\n================")
            print("  TASK MANAGER  ")
            print("================\n")
            print("[1] Add task")
            print("[2] Status task")
            print("[3] List task")
            print("[4] 🗑️Delete task")
            print("[5] Undo task")
            print("exit program(exit)")

            response = input("\nChoose an option: ").strip().lower()

            if response == 'exit': break
            if response == 'add' or response == '1':
                task_name = task_manager.task_info()
                description = task_manager.add_description()
                print(tasks.add_task(user_name,task_name, description))
            elif response == 'status' or response == '2':
                print(task_manager.list_all(task_dict))
                task_id = task_manager.status()
                print(tasks.toggle_task_status(task_id))
            elif response== 'list' or response == '3':
                print(task_manager.list_all(task_dict))
            elif response == 'delete' or response == '4':

                print(task_manager.list_all(task_dict))
                while True:
                    task_id = task_manager.del_task()
                    tasks.delete_task(task_id)

                    delete_more = input("Do you want to delete another task?(Y|N): ").upper().strip()

                    if delete_more != "Y":
                        break

            elif response == 'undo' or response == '5':
                print(tasks.undo_task(user_name))

            user_input = input("Do you want to continue?Y|N ").strip().upper()

        db.close_database()


if __name__ == "__main__":
    print_cli = Display()
