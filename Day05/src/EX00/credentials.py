from wsgiref.simple_server import make_server, WSGIServer
from urllib.parse import parse_qs
import json
from typing import Callable


species: dict[str, str] = {
    'Cyberman': 'John Lumic',
    'Dalek': 'Davros',
    'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
    'Human': 'Leonardo da Vinci',
    'Ood': 'Klineman Halpen',
    'Silence': 'Tasha Lem',
    'Slitheen': 'Coca-Cola salesman',
    'Sontaran': 'General Staal',
    'Time Lord': 'Rassilon',
    'Weeping Angel': 'The Division Representative',
    'Zygon': 'Broton',
}


def application(environ: dict, start_response: Callable) -> list[bytes]:
    query: dict = parse_qs(environ['QUERY_STRING'])
    if (not query or 'species' not in query
            or query['species'][0] not in species):
        status: str = '404 NOT FOUND'
        response_body: bytes = json.dumps({"credentials": "Unknown"}).encode()
    else:
        status = '200 OK'
        response_body = json.dumps({
            'credentials': species[query['species'][0]]
        }).encode()
    response_headers: list[tuple[str, str]] = [
        ('Content-Type', 'application/json'),
        ('Content-Encoding', 'utf-8')
    ]
    start_response(status, response_headers)
    return [response_body]


httpd: WSGIServer = make_server('localhost', 8888, application)
httpd.serve_forever()
