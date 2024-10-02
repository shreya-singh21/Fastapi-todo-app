from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn  # Import uvicorn to run the app programmatically

# Initialize FastAPI app
app = FastAPI()

# In-memory task list
tasks: List[str] = []

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
    return {"message": f"Task '{task.task}' added successfully!"}

@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        removed_task = tasks.pop(task_id)
        return {"message": f"Task '{removed_task}' removed successfully!"}
    raise HTTPException(status_code=404, detail="Task not found")


# This block will run only if the script is executed directly
if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn on the specified host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
