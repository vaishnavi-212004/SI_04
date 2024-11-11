import json
import os
from datetime import datetime

# Task class represents a task in the system
class Task:
    def __init__(self, task_id, title, description, assignee, deadline, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.assignee = assignee
        self.deadline = deadline
        self.status = status

    def __repr__(self):
        return f"Task(ID: {self.task_id}, Title: {self.title}, Assignee: {self.assignee}, Deadline: {self.deadline}, Status: {self.status})"

    def to_dict(self):
        """Convert Task object to a dictionary for JSON storage."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "deadline": self.deadline,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """Create Task object from a dictionary."""
        return Task(data["task_id"], data["title"], data["description"], data["assignee"], data["deadline"], data["status"])

# TaskManager class to manage tasks
class TaskManager:
    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_data()

    def load_data(self):
        """Load task data from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                return [Task.from_dict(data) for data in json.load(file)]
        return []

    def save_data(self):
        """Save all tasks to the JSON file."""
        with open(self.data_file, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, title, description, assignee, deadline):
        """Add a new task."""
        task_id = len(self.tasks) + 1  # Generate a new task ID
        new_task = Task(task_id, title, description, assignee, deadline)
        self.tasks.append(new_task)
        self.save_data()
        print(f"Task '{title}' assigned to {assignee} successfully.")

    def view_tasks(self):
        """View all tasks."""
        if not self.tasks:
            print("No tasks in the system.")
        else:
            for task in self.tasks:
                print(task)

    def update_task(self, task_id, title=None, description=None, assignee=None, deadline=None, status=None):
        """Update an existing task."""
        task = self.get_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if assignee:
                task.assignee = assignee
            if deadline:
                task.deadline = deadline
            if status:
                task.status = status
            self.save_data()
            print(f"Task ID {task_id} updated successfully.")
        else:
            print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        """Delete a task by ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_data()
            print(f"Task ID {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")

    def search_task(self, search_term):
        """Search for tasks by title or status."""
        found_tasks = [task for task in self.tasks if search_term.lower() in task.title.lower() or search_term.lower() in task.status.lower()]
        if found_tasks:
            for task in found_tasks:
                print(task)
        else:
            print(f"No tasks found for '{search_term}'.")

    def get_task_by_id(self, task_id):
        """Get a task by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

# Main program to test Task Assignment and Tracking System
def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Assignment and Tracking System")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Search Task")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            assignee = input("Enter assignee name: ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            task_manager.add_task(title, description, assignee, deadline)

        elif choice == '2':
            task_manager.view_tasks()

        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (leave blank to keep current): ")
            description = input("Enter new description (leave blank to keep current): ")
            assignee = input("Enter new assignee (leave blank to keep current): ")
            deadline = input("Enter new deadline (leave blank to keep current): ")
            status = input("Enter new status (leave blank to keep current): ")
            task_manager.update_task(
                task_id,
                title or None,
                description or None,
                assignee or None,
                deadline or None,
                status or None
            )

        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            task_manager.delete_task(task_id)

        elif choice == '5':
            search_term = input("Enter title or status to search: ")
            task_manager.search_task(search_term)

        elif choice == '6':
            print("Exiting Task Management System.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
