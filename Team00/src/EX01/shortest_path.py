import argparse
import json
import os

from neo4j import GraphDatabase, RoutingControl
from dotenv import load_dotenv


FROM_DEFAULT = 'Welsh Corgi'
TO_DEFAULT = 'Received Pronunciation'

URI = 'neo4j://localhost:7687'
AUTH = ('neo4j', 'password')


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--from',
        default=FROM_DEFAULT,
        type=str,
        help=f'Start page for pathfinding (default: {FROM_DEFAULT})',
        dest='_from',
    )
    parser.add_argument(
        '-t',
        '--to',
        default=TO_DEFAULT,
        type=str,
        help=f'End page for pathfinding (default: {TO_DEFAULT})',
        dest='to',
    )
    parser.add_argument(
        '-n',
        '--non-directed',
        action='store_true',
        default=False,
        help='Removes the direction from the edges of the graph',
        dest='non_directed',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Removes the direction from the edges of the graph',
        dest='verbose',
    )
    return parser.parse_args()


def get_path_from_neo4j(uri: str,
                        auth: tuple[str | None, str | None],
                        start: str = FROM_DEFAULT,
                        end: str = TO_DEFAULT) -> dict:
    result: dict = {}
    with GraphDatabase.driver(uri=uri, auth=auth) as driver:
        records, _, _ = driver.execute_query(
            'MATCH (s:Page{title:$s_title}), '
            '(e:Page{title:$e_title}), '
            'p = shortestPath((s)-[*]-(e)) '
            'RETURN p',
            s_title=start, e_title=end,
            database_='neo4j', routing_=RoutingControl.READ
        )
        if len(records):
            path: list[str] = []
            for node in records[0].get('p').nodes:
                path.append(node.get('title'))
            result['path'] = prettify_path(path)
            result['length'] = len(records[0].get('p'))
    return result


def get_non_derected_graph(graph: dict) -> dict:
    new_graph: dict = graph.copy()
    for vertex in graph:
        for mention in graph[vertex]:
            if mention not in graph:
                new_graph[mention] = [vertex]
            elif vertex not in graph[mention]:
                new_graph[mention].append(vertex)
    return new_graph


def get_graph(directed: bool = False) -> dict:
    path: str | None = os.environ.get('WIKI_FILE')
    if not path:
        print('Database not found')
        exit(-1)
    path = os.path.dirname(__file__) + path
    if not os.path.exists(path):
        print('Database not found', path)
        exit(-1)
    with open(path, 'r') as file:
        graph: dict = json.load(file)
    return graph if not directed else get_non_derected_graph(graph)


def get_path(graph: dict,
             start: str = FROM_DEFAULT,
             end: str = TO_DEFAULT) -> list[str]:
    if start not in graph:
        return []
    paths: dict = {page: [start] for page in graph[start]}
    while end not in paths:
        new_paths: dict = {}
        for page in paths:
            if page in graph:
                for next in graph[page]:
                    if next not in paths[page]:
                        new_paths[next] = paths[page] + [page]
        paths.update(new_paths)
        if all(page not in graph for page in paths):
            break
    return paths[end] + [end] if end in paths else []


def prettify_path(path: list[str]) -> str:
    s_path: str = ''
    for i in range(len(path) - 1):
        s_path += path[i] + ' -> '
    return s_path + path[-1]


def load_env() -> None:
    env_path: str = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(env_path):
        print(
            '.env file not found\n'
            + 'Check README_src.md file for more information'
        )
        exit(-1)
    load_dotenv(env_path)


if __name__ == '__main__':
    load_env()
    args: argparse.Namespace = get_args()
    graph: dict = get_graph(args.non_directed)
    path: list[str] = get_path(graph, args._from, args.to)
    if not len(path):
        print('Path not found =(')
    else:
        if args.verbose:
            print(prettify_path(path))
        print(len(path) - 1)
    uri: str | None = os.environ.get('URI')
    auth: tuple[str | None, str | None] = (
        os.environ.get('USER_NAME'),
        os.environ.get('PASSWORD'),
    )
    if uri and any(_ for _ in auth):
        bd_path: dict = get_path_from_neo4j(
            uri,
            auth,
            args._from,
            args.to,
        )
        print('Found path use neo4j (always non directed):', bd_path)
