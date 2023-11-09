import argparse
import os
from typing import Any

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


URL = 'http://localhost:8888/'


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['upload', 'list'],
        help='Action to perform \
            ("upload": local file or "list": show uploaded files)'
    )
    parser.add_argument(
        'path',
        nargs='?',
        help='Path to the file to upload (only for "upload" action)'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args: argparse.Namespace = get_args()
    if args.action == 'list':
        response: requests.Response = requests.get(URL)
        if response.status_code != 200:
            print('Server not started!')
            exit(-1)
        soup: BeautifulSoup = BeautifulSoup(response.text, 'lxml')
        source: Tag | Any
        for source in soup.find_all('source'):
            if isinstance(source, Tag) and \
                    isinstance(source['src'], str):
                print(source['src'].split('/')[-1])
    elif not os.path.exists(args.path):
        print('Unvalid path')
    else:
        with open(args.path, 'rb') as file:
            response = requests.post(URL, files={'file': file})
            print(response)
