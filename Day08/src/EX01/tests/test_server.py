import asyncio
from typing import Any
from unittest.mock import AsyncMock
import uuid
from httpx import Response
import pytest
from pydantic import HttpUrl
from fastapi.testclient import TestClient
import time

import server


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, status_code",
    [
        ("http://www.google.com", 200),
        ("http://www.yahoo.com", 301),
        ("http://www.ya.ru", 301),
        ("http://www.example.com", 200),
        ("https://github.com/Fuse23/java", 404)
    ]
)
async def test_get_request_code(url: str, status_code: int):
    assert await server.get_request_code(
        server.Url(url=HttpUrl(url))
    ) == status_code


@pytest.fixture
def client() -> TestClient:
    return TestClient(server.app)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "urls",
    [
        ([{"url": "http://www.yahoo.com"}]),
        ([{"url": "http://www.google.com"}, {"url": "http://www.ya.ru"}]),
    ]
)
async def test_create_task(
    urls: list[dict[str, str]],
    client: TestClient
) -> None:
    response: Response = client.post("/api/v1/tasks", json=urls)
    assert response.status_code == 201
    data: dict = response.json()
    assert data
    assert "id" in data
    assert "status" in data
    assert (
        (data.get("status") == "running" and len(data.get("result")) == 0)
        or (data.get("status") == "ready" and len(data.get("result")) > 0)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "urls, result",
    [
        (
            [server.Url(url=HttpUrl("http://www.yahoo.com/"))],
            [server.Result(url="http://www.yahoo.com/", status_code=301)],
        ),
        (
            [
                server.Url(url=HttpUrl("http://www.google.com")),
                server.Url(url=HttpUrl("http://www.ya.ru")),
            ],
            [
                server.Result(url="http://www.google.com/", status_code=200),
                server.Result(url="http://www.ya.ru/", status_code=302),
            ]
        )
    ]
)
async def test_make_request(
    urls: list[server.Url],
    result: list[server.Result],
    monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(asyncio, "run", AsyncMock())
    task = server.Task(id=uuid.uuid4(), status="running")
    await server.make_requests(urls, task)
    assert task.status == "ready"
    assert task.result == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "urls",
    [
        (
            [{"url": "http://www.yahoo.com/"}]
        ),
        (
            [{"url": "http://www.google.com"}, {"url": "http://www.ya.ru"}]
        ),
    ]
)
async def test_get_task(
    urls: list[dict[str, str]],
    client: TestClient
) -> None:
    response_create: Response = client.post("/api/v1/tasks", json=urls)
    task_data: dict = response_create.json()
    task_id: str = task_data["id"]
    response_get: Response = client.get(
        f"/api/v1/tasks/received_task_id?received_tasK_id={task_id}"
    )
    assert response_get.status_code == 200
    retrieved_task = response_get.json()
    assert retrieved_task["id"] == task_id
