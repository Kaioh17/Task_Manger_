"""To do task save in dictionary"""
from Task_Manger_.src.auth.userSystem import user


class TaskManager:
    def __init__(self):
        #using nested dictionaries
        self.to_do_dict = {}

    def task_info(self,user_name):
        """User adds task to memory """
        while True:
            try:
                #User inputs
                task = input("Task name: ").strip().capitalize()
                # check if task already exists
                if task in self.to_do_dict: raise ValueError("Task already exists")
                #checks if task is empty
                if not task: raise ValueError("Task cannot be empty")

                """Ask if user wants to enter in more task"""

                """check if user doesn't exist create new slot for the user"""
                if user_name not in self.to_do_dict:
                    self.to_do_dict[user_name] = {}

                print("Found user name")
                self.to_do_dict[user_name][task] = "Pending"
                    # add task with default status "pending"
                print(f"{task} successfully entered to user: {user_name}")
                return task

            except ValueError as e:
                print(f"Error: {e} ")

                retry = input("Do you want to try again?(Y|N) ").strip(). capitalize()

                if retry.lower()!= "y":
                    for _ in range(50):
                        print("-", end = "")
                    print("Exited:(")
                    break
    def list_all(self):
        """display dictionary using list """
        while True:
            try:
                #request username before giving the list
                user_name = input("Enter user name: ")

                #handle when user not in dict
                if user_name not in self.to_do_dict:
                    raise KeyError("User is not  in memory")

                result = {user_name: list(self.to_do_dict[user_name].items())}

                return result
            except KeyError as e:
                print(f"Error: {e}")

                retry= input("Do you want to try again(Y|N): ").strip().capitalize()

                if retry.lower() != 'y':
                    break





    def status(self):

        # get task user wants to change status of
        while True:
            try:
                task = input("Enter task: ").strip().capitalize()
                if not task: raise IndexError("Cannot accept no value") #check if task empty
                if task not in  self.to_do_dict: raise KeyError("Task not in memory") #make sure task in dictionary


                status = input("--Change status (pending/done): ").strip().capitalize()
                #makes sure user enters valid status
                if status.lower() not in "pending""done":
                    raise IndexError("Invalid status! User can only enter(pending/done)")
                self.to_do_dict[task] = status

                """Set a condition so that when status is set to done its delete from db and cache """



                return print(self.to_do_dict)

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




