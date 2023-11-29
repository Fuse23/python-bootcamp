from typing import Optional
import uuid
import httpx
from urllib.parse import urlparse
import asyncio
import logging
import argparse

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, HttpUrl
import uvicorn
import aioredis


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
redis: aioredis.Redis = aioredis.from_url("redis://localhost:6379")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
shutdown_even: asyncio.Event = asyncio.Event()
args: argparse.Namespace = argparse.Namespace()


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "time",
        default=60,
        type=int,
        help="time that the cache will be stored",
    )
    return parser.parse_args()


async def clear_cache(interval: int) -> None:
    """Delete all redis keys in timeout (global time variable)
    """
    while not shutdown_even.is_set():
        logging.info("call clear_cache")
        await asyncio.sleep(interval)
        keys: list[bytes] | None = await redis.keys("*")
        if keys is not None:
            for key in keys:
                logging.info(f"delete {key=}")
                await redis.delete(key)


async def make_requests(urls: list[Url], task: Task) -> None:
    """Requests by urls, add result to task

    Args:

        urls (list[Url]): urls for requests

        task (Task): task for add result
    """
    for url in urls:
        url_str: str = url.url.unicode_string()
        cache_status_code: bytes | None = await redis.hget("cache", url_str)
        if cache_status_code is not None:
            status_code: int = int(cache_status_code)
        else:
            status_code = await get_request_code(url_str)
            await redis.hset("cache", url_str, status_code)
        await redis.incr(urlparse(url_str).netloc)
        if task.result is not None:
            task.result.append(Result(url=url_str, status_code=status_code))
        logging.info(f"{url=}, {await redis.get(urlparse(url_str).netloc)}")
    task.status = "ready"
    logging.info(f"{await redis.keys('*')=}")


async def get_request_code(url: str) -> int:
    """Get response status code

    Args:

        url (Url): url for request

    Returns:

        int: response status code
    """
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
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
    background_tasks.add_task(clear_cache, args.time)
    return task


@app.get("/api/v1/tasks/{received_task_id}", response_model=Task)
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
    args = get_args()
    uvicorn.run(app=app, host="localhost", port=8888)
shutdown_even.set()
