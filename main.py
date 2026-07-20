from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repository import PostgresTaskRepository
from service import TaskService

app = FastAPI()

repository = PostgresTaskRepository()  # was: InMemoryTaskRepository()
service = TaskService(repository)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


@app.get("/", summary="API info")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


@app.get("/hello", summary="Greeting")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return service.list_tasks()


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int):
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a task")
def create_task(task: TaskCreate):
    try:
        return service.create_task(task.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, update: TaskUpdate):
    try:
        task = service.update_task(task_id, update.title, update.done)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
