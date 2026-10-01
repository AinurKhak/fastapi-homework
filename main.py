from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Модель данных, которые будут приходить в body
class Task(BaseModel):
    title: str
    description: str
    completed: bool = False


# Временное хранилище вместо базы данных
tasks = {
    1: Task(
        title="Изучить FastAPI",
        description="Разобраться с GET и POST",
        completed=False
    ),
    2: Task(
        title="Сделать домашнее задание",
        description="Написать свой API",
        completed=True
    )
}


# QUERY-параметр
# Пример: GET /tasks?completed=true
@app.get("/tasks")
def get_tasks(completed: bool | None = None):
    if completed is None:
        return tasks

    return {
        task_id: task
        for task_id, task in tasks.items()
        if task.completed == completed
    }


# PATH-параметр
# Пример: GET /tasks/1
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        return {"error": "Задача не найдена"}

    return tasks[task_id]


# BODY-параметр + POST
# Пример: POST /tasks
@app.post("/tasks")
def create_task(task: Task):
    task_id = max(tasks.keys(), default=0) + 1
    tasks[task_id] = task

    return {
        "id": task_id,
        "task": task
    }