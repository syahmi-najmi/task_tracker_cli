import argparse   # Handles command-line arguments
import json       # Handles reading and writing JSON files
import os         # Checks if the JSON file exists
from datetime import datetime  # Handles timestamps


# This function reads the JSON file and returns the tasks as a list.
def read_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
    return []

# This function saves tasks back to the tasks.json file.
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

# Function to add a task
def add_task(params):
    if not params:
        print("Please provide a task description.")
        return

    description = " ".join(params)
    tasks = read_tasks()
    task_id = len(tasks) + 1  # Assign a unique task ID
    created_at = updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": created_at,
        "updatedAt": updated_at
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {task_id})")

# Function to list tasks
def list_tasks(params):
    tasks = read_tasks()

    if not tasks:
        print("No tasks available.")
        return

    if params:
        status = params[0]
        tasks = [task for task in tasks if task["status"] == status]

    if tasks:
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created: {task['createdAt']}")
    else:
        print(f"No tasks found with status '{status}'.")

# Function to update a task
def update_task(params):
    if len(params) < 2:
        print("Please provide task ID and new description.")
        return

    task_id = int(params[0])
    new_description = " ".join(params[1:])
    tasks = read_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return

    print(f"Task {task_id} not found.")

# Function to delete a task
def delete_task(params):
    if not params:
        print("Please provide a task ID.")
        return

    task_id = int(params[0])
    tasks = read_tasks()

    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)

    print(f"Task {task_id} deleted successfully.")

# Function to mark a task as "in-progress"
def mark_in_progress(params):
    if not params:
        print("Please provide a task ID.")
        return

    task_id = int(params[0])
    tasks = read_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} marked as in-progress.")
            return

    print(f"Task {task_id} not found.")

# Function to mark a task as "done"
def mark_done(params):
    if not params:
        print("Please provide a task ID.")
        return

    task_id = int(params[0])
    tasks = read_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} marked as done.")
            return

    print(f"Task {task_id} not found.")

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Task tracker CLI")
    
    # Define available commands and arguments
    parser.add_argument("command", choices=["add", "list", "update", "delete", "mark-in-progress", "mark-done"], help="Command to run")
    parser.add_argument("params", nargs="*", help="Additional parameters for the command")
    
    return parser.parse_args()

# Main function to handle user commands
def main():
    args = parse_args()
    
    if args.command == "add":
        add_task(args.params)
    elif args.command == "list":
        list_tasks(args.params)
    elif args.command == "update":
        update_task(args.params)
    elif args.command == "delete":
        delete_task(args.params)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.params)
    elif args.command == "mark-done":
        mark_done(args.params)

# Run the script
if __name__ == "__main__":
    main()
