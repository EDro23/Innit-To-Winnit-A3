import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def fetch_tasks(self):
        self.cursor.execute("SELECT * FROM task WHERE completed = 0")
        return self.cursor.fetchall()

    def add_task(self, task):
        self.cursor.execute("INSERT INTO task (description, completed) VALUES (?, ?)", (task, 0))
        self.conn.commit()

    def complete_task(self, task_id):
        self.cursor.execute("UPDATE task SET completed = 1 WHERE taskID = ?", (task_id,))
        self.conn.commit()

    def fetch_completed_tasks(self):
        self.cursor.execute("SELECT * FROM task WHERE completed = 1")
        return self.cursor.fetchall()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM task WHERE taskID = ?", (task_id,))
        self.conn.commit()
