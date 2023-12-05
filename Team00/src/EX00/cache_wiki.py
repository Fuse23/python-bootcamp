import argparse
import requests
import json
import logging
from typing import Any
import os
from dotenv import load_dotenv
from urllib.parse import quote

from bs4 import BeautifulSoup, Tag, ResultSet
from neo4j import GraphDatabase, Driver


DEFAULT_PAGE = 'Welsh Corgi'
DEPTH = 3
LINK_PREFIX = 'https://en.wikipedia.org'

logging.basicConfig(level=logging.INFO)

graph: dict = dict()
page_count: int = 1000
visited_pages: set[str] = set()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--page',
        default=DEFAULT_PAGE,
        type=str,
        help=f'Start page title (default: {DEFAULT_PAGE})',
        dest='page',
    )
    parser.add_argument(
        '-d',
        '--depth',
        default=DEPTH,
        type=int,
        help=f'Depth of search (default: {DEPTH})',
        dest='depth',
    )
    return parser.parse_args()


def check_link(link: str) -> bool:
    if (link.startswith('/wiki/')
            and not link.startswith('/wiki/File:')
            and not link.startswith('/wiki/Portal:')):
        return True
    return False


def get_links(title: str) -> list[dict]:
    links: list[dict] = []
    links_titles: set[str] = set()
    response: requests.Response = requests.get(
        f'{LINK_PREFIX}/wiki/' + quote(title)
    )
    logging.info(
        f'Visited page: {LINK_PREFIX}/wiki/'
        + f'{title.replace(" ", "_")} with title: {title}'
    )
    if response.status_code != 200:
        return links
    soup: BeautifulSoup = BeautifulSoup(response.text, 'lxml')
    content_text: Tag | Any = soup.find('div', {'id': 'mw-content-text'})
    if content_text:
        paragraphs: ResultSet[Tag | Any] = content_text.find_all('p')
    if paragraphs:
        for paragraph in paragraphs:
            for link in paragraph.find_all('a', href=True):
                link_href: str = link['href'].split('#', 1)[0]
                if check_link(link_href) and link_href not in links_titles:
                    links_titles.add(link_href)
                    links.append({
                        'title': link_href[6:].replace('_', ' '),
                        'link': LINK_PREFIX + link_href,
                    })
    see_also_section: Tag | Any = soup.find('span', {'id': 'See_also'})
    if see_also_section:
        for link in see_also_section.find_all('a', href=True):
            link_href = link['href'].split('#', 1)[0]
            if check_link(link_href) and link_href not in links_titles:
                links_titles.add(link_href)
                links.append({
                        'title': link_href[6:].replace('_', ' '),
                        'link': LINK_PREFIX + link_href,
                })
    return links


def add_graph(driver: Driver, graph: list[dict]) -> None:
    driver.execute_query(
        'UNWIND $data AS entry '
        'MERGE (p1:Page{title: entry.title}) '
        'ON CREATE SET p1.link = entry.link '
        'WITH p1, entry.mentions AS mentions '
        'UNWIND mentions AS mention '
        'MERGE (p2:Page{title: mention.title}) '
        'ON CREATE SET p2.link = mention.link '
        'MERGE (p1)-[:MENTIONS]->(p2)',
        data=graph, database_='neo4j',
    )


def create_graph(title: str,
                 depth: int = 3,
                 driver: Driver | None = None) -> None:
    global page_count
    title = title.replace('_', ' ')
    if (title not in graph and page_count > 0
            and depth != 0 and title not in visited_pages):
        visited_pages.add(title)
        mentions: list[dict] = get_links(title)
        graph_neo4j: list[dict] = []
        if page_count < len(mentions):
            graph[title] = [
                mention['title'] for mention in mentions[:page_count]
            ]
            graph_neo4j.append({
                'title': title,
                'link': LINK_PREFIX + '/wiki/' + title.replace(' ', '_'),
                'mentions': mentions[:page_count],
            })
        elif page_count > 0:
            graph[title] = [mention['title'] for mention in mentions]
            graph_neo4j.append({
                'title': title,
                'link': LINK_PREFIX + 'wiki/' + title.replace(' ', '_'),
                'mentions': mentions,
            })
        if driver:
            add_graph(driver, graph_neo4j)
        page_count -= len(mentions)
        for vertex in graph[title]:
            create_graph(vertex, depth - 1, driver)


def load_env() -> None:
    env_path: str = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(env_path):
        print(
            '.env file not found\n'
            + 'Check README_src.md file for more information'
        )
    load_dotenv(env_path)


if __name__ == '__main__':
    load_env()
    args: argparse.Namespace = get_args()
    uri: str | None = os.environ.get('URI')
    auth: tuple[str | None, str | None] = (
        os.environ.get('USER_NAME'),
        os.environ.get('PASSWORD'),
    )
    driver: Driver | None = None
    if uri and any(_ for _ in auth):
        driver = GraphDatabase.driver(uri=uri, auth=auth)
    create_graph(args.page, args.depth, driver)
    with open(os.path.dirname(__file__) + '/../wiki.json', 'w') as file:
        json.dump(graph, file, indent=4)
