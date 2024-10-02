from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn  # Import uvicorn to run the app programmatically
import json     # Import json module to read and write JSON files

# File path for storing the tasks
TASK_FILE = "tasks.json"

# Initialize FastAPI app
app = FastAPI()

# Function to read tasks from the file
def read_tasks_from_file():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If file does not exist, return an empty list
        return []

# Function to write tasks to the file
def write_tasks_to_file(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file)

# Load tasks from the file into a global variable
tasks: List[str] = read_tasks_from_file()

# Task model for request body validation
class Task(BaseModel):
    task: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI To-Do List App!"}

@app.get("/tasks", response_model=List[str])
def get_tasks():
    return tasks

@app.post("/tasks", status_code=201)
def add_task(task: Task):
    tasks.append(task.task)
    write_tasks_to_file(tasks)  # Write the updated task list to the file
    return {"message": f"Task '{task.task}' added successfully!"}

@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        removed_task = tasks.pop(task_id)
        write_tasks_to_file(tasks)  # Write the updated task list to the file
        return {"message": f"Task '{removed_task}' removed successfully!"}
    raise HTTPException(status_code=404, detail="Task not found")

# This block will run only if the script is executed directly
if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn on the specified host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
