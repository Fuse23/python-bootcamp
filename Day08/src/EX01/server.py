from typing import Optional
import uuid
import httpx
import asyncio

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, HttpUrl
import uvicorn


class Url(BaseModel):
    url: HttpUrl


class Result(BaseModel):
    url: str
    status_code: int


class Task(BaseModel):
    id: uuid.UUID
    status: str
    result: Optional[list[Result]] = []


app: FastAPI = FastAPI()
tasks: list[Task] = []


async def make_requests(urls: list[Url], task: Task) -> None:
    """Requests by urls, add result to task

    Args:

        urls (list[Url]): urls for requests

        task (Task): task for add result
    """
    for url in urls:
        status_code: int = await get_request_code(url)
        if task.result is not None:
            task.result.append(Result(
                url=url.url.unicode_string(),
                status_code=status_code
            ))
    task.status = "ready"


async def get_request_code(url: Url) -> int:
    """Get response status code

    Args:

        url (Url): url for request

    Returns:

        int: response status code
    """
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url.url.unicode_string())
        return response.status_code


@app.post("/api/v1/tasks", response_model=Task, status_code=201)
async def create_task(
    urls: list[Url],
    background_tasks: BackgroundTasks
) -> Task:
    """Create task, add to tasks list and bachground_tasks

    Args:

        urls (list[Url]):
            list of urls to which requests will be sent

        background_tasks (BackgroundTask):
            FastAPI class for start task after client's request

    Returns:

        Task: created task
    """
    task: Task = Task(id=uuid.uuid4(), status="running")
    tasks.append(task)
    background_tasks.add_task(make_requests, urls, task)
    return task


@app.get("/api/v1/tasks/{received_task_id}")
async def get_task(received_tasK_id: uuid.UUID) -> Task | None:
    """Search task with args id

    Args:

        received_tasK_id (UUID):
            id for search task
    """
    if len(tasks) == 0:
        return None
    for task in tasks:
        if task.id == received_tasK_id:
            return task


if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8888)
