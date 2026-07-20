from repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self):
        return self.repository.get_all()

    def get_task(self, task_id: int):
        return self.repository.get_by_id(task_id)

    def create_task(self, title: str):
        if not title or not title.strip():
            raise ValueError("Title is required")
        return self.repository.create(title)

    def update_task(self, task_id: int, title: str, done: bool):
        if not title or not title.strip():
            raise ValueError("Title is required")
        return self.repository.update(task_id, title, done)

    def delete_task(self, task_id: int):
        return self.repository.delete(task_id)
