class TaskManager:
    def __init__(self, db):
        self.db = db

    def view_tasks(self):
        return self.db.fetch_tasks()

    def view_history(self):
        return self.db.fetch_completed_tasks()

    def add_task(self, task):
        self.db.add_task(task)

    def complete_task(self, task_id):
        self.db.complete_task(task_id)

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
