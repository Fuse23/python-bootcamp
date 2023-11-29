import argparse
import asyncio

import aiohttp


URL = "http://localhost:8888/api/v1/tasks/"


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "method",
        choices=["post", "get"],
        help="""Select request method
            (post use with list urls, get with task's uuid)""",
    )
    parser.add_argument(
        "data",
        type=str,
        nargs="+",
        help="List of urls if method post and task's uuid if methos get",
    )
    return parser.parse_args()


def create_data(urls: list[str]) -> list[dict[str, str]]:
    return [{"url": url} for url in urls]


async def main(method: str, data: list[str]) -> None:
    async with aiohttp.ClientSession() as session:
        if method == "post":
            async with session.post(
                url=URL,
                json=create_data(data)
            ) as response:
                if response.status == 201:
                    print(await response.json())
        else:
            response = await session.get(
                URL + f"received_task_id?received_tasK_id={data[0]}"
            )
            if response.status == 200:
                res_data: dict = await response.json()
                print(res_data)
            else:
                print("ERROR:", await response.json())


if __name__ == "__main__":
    args: argparse.Namespace = get_args()
    asyncio.run(main(args.method, args.data))
