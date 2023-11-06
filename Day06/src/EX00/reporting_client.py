import sys
import os

# Get the absolute path to the directory containing client.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the 'src' directory to the Python path
src_dir = os.path.join(current_dir, '..')
sys.path.append(src_dir)

from proto import galaxy_pb2 as pb2
from proto import galaxy_pb2_grpc as pb2_grpc

import argparse
import json
from typing import Generator

import grpc


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('coords', nargs='*', type=float)
    return parser.parse_args()


def get_ships(channel: grpc.Channel, coords: list[float]) -> Generator:
    stub: pb2_grpc.GalaxyServiceStub = pb2_grpc.GalaxyServiceStub(channel)
    ship: pb2.Ship
    for ship in stub.get_ships(pb2.GalacticCoordinates(coords=coords)):
        yield json.dumps({
            'alignment': pb2.Ship.AlignmentType.Name(ship.alignment),
            'name': ship.name,
            'class': pb2.Ship.ShipType.Name(ship.ship_class),
            'length': ship.length,
            'crew_size': ship.crew_size,
            'armed': ship.armed,
            'officers': [{
                'first_name': officer.first_name,
                'last_name': officer.last_name,
                'rank': officer.rank,
            } for officer in ship.officers]
        }, indent=4)


if __name__ == '__main__':
    args: argparse.Namespace = get_args()
    if len(args.coords) == 0:
        print('Bad coords!')
        exit(-1)
    with grpc.insecure_channel('localhost:50051') as channel:
        for ship in get_ships(channel, args.coords):
            print(ship)
