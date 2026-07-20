from abc import ABC, abstractmethod


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self): ...

    @abstractmethod
    def get_by_id(self, task_id: int): ...

    @abstractmethod
    def create(self, title: str): ...

    @abstractmethod
    def update(self, task_id: int, title: str, done: bool): ...

    @abstractmethod
    def delete(self, task_id: int): ...


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks = [
            {"id": 1, "title": "Buy milk", "done": False},
            {"id": 2, "title": "Walk the dog", "done": False},
            {"id": 3, "title": "Read a book", "done": True},
        ]

    def get_all(self):
        return self.tasks

    def get_by_id(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def create(self, title: str):
        new_id = max((t["id"] for t in self.tasks), default=0) + 1
        new_task = {"id": new_id, "title": title, "done": False}
        self.tasks.append(new_task)
        return new_task

    def update(self, task_id: int, title: str, done: bool):
        task = self.get_by_id(task_id)
        if task is None:
            return None
        task["title"] = title
        task["done"] = done
        return task

    def delete(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                return True
        return False
