from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get(
    "/", summary="API info", description="Returns basic information about this API."
)
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": False},
    {"id": 3, "title": "Read a book", "done": True},
]


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@app.get(
    "/health",
    summary="Health check",
    description="Returns server status — used to verify the API is alive.",
)
def health():
    return {"status": "ok"}


@app.get("/hello", summary="Greeting", description="Returns a friendly hello message.")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}


@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns every task in the in-memory list.",
)
def get_tasks():
    return tasks


@app.get(
    "/tasks/{task_id}",
    summary="Get one task",
    description="Returns a single task by id, or 404 if it doesn't exist.",
)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a task",
    description="Creates a new task. Requires a non-empty title.",
)
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put(
    "/tasks/{task_id}",
    summary="Update a task",
    description="Replaces a task's title and done status. 404 if the id doesn't exist.",
)
def update_task(task_id: int, update: TaskUpdate):
    if not update.title or not update.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = update.title
            task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete a task",
    description="Removes a task by id. 404 if it doesn't exist.",
)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
