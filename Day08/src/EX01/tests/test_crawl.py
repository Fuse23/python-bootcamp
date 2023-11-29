from typing import Any, Callable, Coroutine
import pytest
import asyncio

import aiohttp

import crawl


@pytest.mark.parametrize(
        "urls, expected",
        [
            (
                ["url 1", "url 2", "url 3"],
                [{"url": "url 1"}, {"url": "url 2"}, {"url": "url 3"}],
            ),
            (
                ["some url"],
                [{"url": "some url"}],
            ),
        ]
)
def test_create_data(urls: list[str], expected: list[dict[str, str]]) -> None:
    assert crawl.create_data(urls) == expected


class MockResponse:
    def __init__(self, status: int, json_data: dict) -> None:
        self._status: int = status
        self._json_data: dict = json_data

    async def __aenter__(self) -> 'MockResponse':
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    async def json(self) -> dict:
        return self._json_data

    @property
    def status(self) -> int:
        return self._status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method, data, status, response, expected",
    [
        (
            "post",
            [
                "https://www.google.com",
                "https://www.yahoo.com",
                "https://www.ya.ru"
            ],
            201,
            {"id": "some_id", "status": "running", "result": []},
            "{'id': 'some_id', 'status': 'running', 'result': []}\n",
        ),
        (
            "get",
            ["some_data"],
            200,
            {"id": "some_id", "status": "ready", "result": []},
            "{'id': 'some_id', 'status': 'ready', 'result': []}\n",
        ),
    ]
)
async def test_main(
    method: str,
    data: list[str],
    status: int,
    response: dict[str, str | list[Any]],
    expected: str,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch
) -> None:
    def mock_post(*args, **kwargs) -> MockResponse:
        return MockResponse(status, response)

    async def mock_post_async(*args, **kwargs) -> MockResponse:
        return MockResponse(status, response)

    if method == "post":
        mock: Callable[..., MockResponse | Coroutine] = mock_post
    else:
        mock = mock_post_async
    monkeypatch.setattr(aiohttp.ClientSession, method, mock)
    await crawl.main(method, data)
    captured = capsys.readouterr()
    assert captured.out == expected
