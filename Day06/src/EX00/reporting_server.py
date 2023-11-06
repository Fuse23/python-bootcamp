import sys
import os

# Get the absolute path to the directory containing client.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the 'src' directory to the Python path
src_dir = os.path.join(current_dir, '..')
sys.path.append(src_dir)

from constants.constants import NAMES, FIRST_NAMES, LAST_NAMES, RANKS
import proto.galaxy_pb2 as pb2
import proto.galaxy_pb2_grpc as pb2_grpc

from typing import Generator
import random
from concurrent import futures

import grpc


class Galaxy(pb2_grpc.GalaxyService):
    def get_ships(self,
                  request: pb2.GalacticCoordinates,
                  context: grpc.ServicerContext) -> Generator:
        print(f'Coords: {request.coords}')
        for _ in range(random.randint(1, 10)):
            ship: pb2.Ship = pb2.Ship(
                alignment=random.choice(0, 1),
                name=random.choice(NAMES),
                length=random.uniform(80, 20_000),
                ship_class=random.randint(0, 5),
                crew_size=random.randint(4, 500),
                armed=random.choice([True, False]),
            )
            min_officers: int = 0 if ship.alignment == 'Enemy' else 1
            for _ in range(random.randint(min_officers, 10)):
                officer: pb2.Ship.Officer = ship.officers.add()
                officer.first_name = random.choice(FIRST_NAMES)
                officer.last_name = random.choice(LAST_NAMES)
                officer.rank = random.choice(RANKS)
            yield ship


def server() -> None:
    server: grpc.Server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    pb2_grpc.add_GalaxyServiceServicer_to_server(Galaxy(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()
