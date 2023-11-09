from proto import galaxy_pb2 as pb2
from EX00.reporting_client import get_args, get_ships

import grpc
from pydantic import BaseModel, model_validator, ValidationError, Field

import argparse


class Officer(BaseModel):
    first_name: str
    last_name: str
    rank: str


class Ship(BaseModel):
    alignment: str
    name: str
    length: float
    ship_class: str = Field(alias='class')
    crew_size: int
    armed: bool
    officers: list[Officer]

    @model_validator(mode='after')
    def check_model(self) -> 'Ship':
        if not ((
                 self.ship_class == 'Corvette' and 80 <= self.length <= 250
                 and 4 <= self.crew_size <= 10 and self.armed
                 ) or (
                 self.ship_class == 'Frigate' and 300 <= self.length <= 600
                 and 10 <= self.crew_size <= 15 and self.armed
                 and self.alignment == 'Ally'
                 ) or (
                 self.ship_class == 'Cruiser' and 500 <= self.length <= 1000
                 and 15 <= self.crew_size <= 30 and self.armed
                 ) or (
                 self.ship_class == 'Destroyer' and 800 <= self.length <= 2000
                 and 50 <= self.crew_size <= 80 and self.armed
                 and self.alignment == 'Ally'
                 ) or (
                 self.ship_class == 'Carrier' and 1000 <= self.length <= 4000
                 and 120 <= self.crew_size <= 250 and not self.armed
                 ) or (
                 self.ship_class == 'Dreadnought'
                 and 5000 <= self.length <= 20000
                 and 300 <= self.crew_size <= 500 and self.armed
                )
                and not (self.name == 'Unknown' and self.alignment == 'Ally')
                ):
            raise ValueError()
        return self


def is_valid_ship(ship: pb2.Ship) -> bool:
    try:
        Ship.model_validate_json(ship)
        return True
    except ValidationError:
        return False


if __name__ == '__main__':
    args: argparse.Namespace = get_args()
    if len(args.coords) == 0:
        print('Bad coords!')
        exit(-1)
    with grpc.insecure_channel('localhost:50051') as channel:
        for ship in get_ships(channel, args.coords):
            if is_valid_ship(ship):
                print(ship)
