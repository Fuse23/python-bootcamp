from EX00.reporting_client import get_ships
from EX01.reporting_client_v2 import is_valid_ship
from config import DB_PASS, DB_HOST, DB_NAME, DB_PORT, DB_USER

import argparse
import json
from typing import Annotated

import grpc
from sqlalchemy import (
    create_engine,
    Engine,
    String,
    ForeignKey,
    URL,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)


url: URL = URL.create(
    drivername='postgresql+psycopg2',
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
engine: Engine = create_engine(url)
Session = sessionmaker(bind=engine)

pk = Annotated[int, mapped_column(primary_key=True)]
str_5 = Annotated[str, 5]
str_30 = Annotated[str, 30]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_5: String(5),
        str_30: String(30),
    }


class Officers(Base):
    __tablename__ = 'officers'
    id: Mapped[pk]
    first_name: Mapped[str_30]
    last_name: Mapped[str_30]
    rank: Mapped[str_30]
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))


class Ships(Base):
    __tablename__ = 'ships'
    id: Mapped[pk]
    alignment: Mapped[str_5]
    name: Mapped[str_30]
    ship_class: Mapped[str_30]
    length: Mapped[float]
    crew_size: Mapped[int]
    armed: Mapped[bool]


# Drop all table and create new
# def create_tables() -> None:
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)


def get_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        'cmd',
        choices=['scan', 'list_traitors'],
        help='Select command: scan, list_traitors'
    )
    parser.add_argument('coords', nargs='*', type=float)
    return parser.parse_args()


def is_duplicate(data: dict) -> bool:
    with Session() as session:
        ships: list[Ships] = session.query(Ships).filter(
            Ships.name == data['name']
        ).all()
        if len(ships) == 0:
            return False
        for ship in ships:
            officers: list[Officers] = session.query(Officers).filter(
                Officers.ship_id == ship.id
            ).all()
            if len(officers) != len(data['officers']):
                return False
            for officer in officers:
                officer_d: dict = {
                    'first_name': officer.first_name,
                    'last_name': officer.last_name,
                    'rank': officer.rank,
                }
                if officer_d not in data['officers']:
                    return False
    return True


def add_to_table(ship: str) -> None:
    data: dict = json.loads(ship)
    if is_duplicate(data):
        print('lol')
        return
    with Session() as session:
        new_ship: Ships = Ships(
            alignment=data['alignment'],
            name=data['name'],
            ship_class=data['class'],
            length=data['length'],
            crew_size=data['crew_size'],
            armed=data['armed'],
        )
        session.add(new_ship)
        session.commit()
        session.refresh(new_ship)
        for officer in data['officers']:
            new_officers: Officers = Officers(
                first_name=officer['first_name'],
                last_name=officer['last_name'],
                rank=officer['rank'],
                ship_id=new_ship.id
            )
            session.add(new_officers)
        session.commit()


def get_officers(alignmet: str) -> list:
    with Session() as session:
        return session.query(
            Officers.first_name,
            Officers.last_name,
            Officers.rank,
            Ships.alignment,
        ).join(Ships).filter(
            Ships.alignment == alignmet
        ).all()


def get_traitors() -> list[dict]:
    ally_officers: list[dict] = [
        {
            "first_name": officer.first_name,
            "last_name": officer.last_name,
            "rank": officer.rank
        } for officer in get_officers('Ally')
    ]
    enemy_officers: list[dict] = [
        {
            "first_name": officer.first_name,
            "last_name": officer.last_name,
            "rank": officer.rank
        } for officer in get_officers('Enemy')
    ]
    traitors: list[dict] = []
    for i in range(min(len(ally_officers), len(enemy_officers))):
        if ally_officers[i] in enemy_officers \
                and ally_officers[i] not in traitors:
            traitors.append(ally_officers[i])
    return traitors


if __name__ == '__main__':
    args: argparse.Namespace = get_args()
    if args.cmd == 'scan':
        if len(args.coords) == 0:
            print('Bad coords!')
            exit(-1)
        # create_tables()
        with grpc.insecure_channel('localhost:50051') as channel:
            for ship in get_ships(channel, args.coords):
                if is_valid_ship(ship):
                    print(ship)
                    add_to_table(ship)
    else:
        traitors: list[dict] = get_traitors()
        if len(traitors) == 0:
            print("There aren't traitors!", traitors)
        else:
            for traitor in traitors:
                print(traitor)
