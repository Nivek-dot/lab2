from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory task database
task_db = [{"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}]

# Task model for creating and updating tasks
class Task(BaseModel):
    task_title: str
    task_desc: Optional[str] = None
    is_finished: bool = False

# Helper function to find task by ID
def find_task_by_id(task_id: int):
    return next((task for task in task_db if task["task_id"] == task_id), None)

@app.get("/traject/{task_id}")
def get_task(task_id: int):
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="not found")
    return task

@app.post("/traject")
def create_task(task: Task):
    new_task_id = len(task_db) + 1
    new_task = {"task_id": new_task_id, **task.dict()}
    task_db.append(new_task)
    return new_task

@app.patch("/traject/{task_id}")
def update_task(task_id: int, task: Task):
    existing_task = find_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="not found")

    # Update only provided fields
    updated_task = task.dict(exclude_unset=True)
    existing_task.update(updated_task)
    return existing_task

@app.delete("/traject/{task_id}")
def delete_task(task_id: int):
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="not found")
    task_db.remove(task)
    return {"message": "deleted successfully"}

@app.put("/traject/{task_id}")
def replace_task(task_id: int, task: Task):
    task_to_replace = find_task_by_id(task_id)
    if not task_to_replace:
        raise HTTPException(status_code=404, detail="not found")

    task_db.remove(task_to_replace)
    updated_task = {"task_id": task_id, **task.dict()}  
    task_db.append(updated_task) 

    return updated_task

