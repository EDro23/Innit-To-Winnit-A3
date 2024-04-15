# Importing other two files
from Q3task_manager import TaskManager
from Q3database import Database

def main():
    db = Database('task_list_db.sqlite') #connecting to given Database
    task_manager = TaskManager(db)

    print("task list\n")
    print("COMMAND MENU")
    print("view\t - View pending tasks")
    print("history\t - view completed tasks")
    print("add\t\t - Add a task")
    print("complete - Complete a task")
    print("delete\t - Delete a task")
    print("exit\t - Exit program")

    while True:
        choice = input("\nCommand: ")
        if choice.lower() == 'view': #Method for viewing tasks (uncompleted)
            tasks = task_manager.view_tasks()
            if tasks:
                for i, task in enumerate(tasks, 1):
                    task_description = task[1]
                    print(f"{i}. {task_description}")
            else:
                print("No tasks.")

        elif choice.lower() == 'history': #Method for viewing tasks (completed)
            history = task_manager.view_history()
            if history:
                for i, task in enumerate(history, 1):
                    task_description = task[1]
                    status = "DONE!" if task[2] == 1 else ""
                    print(f"{i}. {task_description}  ({status})")
            else:
                print("No history.")

        elif choice.lower() == 'add': #Method for adding a task to database
            task_description = input("Enter task description: ")
            task_manager.add_task(task_description)
            print("Task added.")

        elif choice.lower() == 'complete': #Method for completing a task
            task_id = input("Enter task ID to mark as completed: ")
            task_manager.complete_task(task_id)
            print("Task marked as completed.")

        elif choice.lower() == 'delete': #Method to delete a task
            task_id = input("Enter task ID to delete: ")
            task_manager.delete_task(task_id)
            print("Task deleted.")

        elif choice.lower() == 'exit': #Exit method
            print('Bye!')
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
