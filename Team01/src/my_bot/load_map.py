import sqlalchemy as db
from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy.exc import IntegrityError

DATABASE = "database/game.db"

Base = declarative_base()
engine = db.create_engine(f"sqlite:///{DATABASE}", echo=False)


class Locations(Base):
    """
    SQLAlchemy model representing locations in the game.

    Attributes:
        id : int
            Primary key for the location.
        name : str
            The name of the location.
        description : str
            The description of the location.
        connections : relationship
            Relationship with the Connection table, representing connections to other locations.
    """
    
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    connections = relationship(
        "Connection",
        primaryjoin="or_(Locations.id==Connection.location_id, Locations.id==Connection.target_location_id)",
        back_populates="location"
    )


class Connection(Base):
    """
    SQLAlchemy model representing connections between locations in the game.

    Attributes:
        id : int
            Primary key for the connection.
        location_id : int
            Foreign key referencing the source location's id.
        target_location_id : int
            Foreign key referencing the target location's id.
        direction : str
            The direction of the connection.

    Relationships:
        location : relationship
            Relationship with the Locations table using the foreign key location_id.
    """
    
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    target_location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    direction = db.Column(db.String)

    location = relationship(
        "Locations", back_populates="connections", foreign_keys=[location_id])


def insert_data(session, model, data):
    """
    Insert data into the specified table.

    Parameters
    ----------
    session : Session
        SQLAlchemy session.
    model : DeclarativeBase
        SQLAlchemy model representing the table.
    data : list
        List of dictionaries containing data to be inserted.
    """
    for entry in data:
        obj = model(**entry)
        session.add(obj)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


def insert_locations():
    """
    Insert location data into the database.
    """
    session = Session(bind=engine)
    locations_data = [
        {"name": "Дом", "description": "Вы находитесь в своем доме."},
        {"name": "Больница", "description": "Вы находитесь в больнице."},
        {"name": "Палата", "description": "Вы находитесь в палате реанимации Романа."},
        {"name": "Сознание Романа", "description": "Вы погрузились в сознание Романа."},
        {"name": "Ступеньки", "description": "Вы находитесь в сознании Романа, рядом со ступеньками, где сидит маленькая девочка."},
        {"name": "Окно", "description": "Вы находитесь в сознании Романа, рядом с окном, где стоит высокий мужчина с массивными плечами"},
        {"name": "Проход между скамеек",
            "description": "Вы находитесь в сознании Романа, в проходе между скамейками рядом с двумя девушками."},
        {"name": "Финал", "description": "Вы находитесь рядом с Романом, в его сознании"},
        {"name": "Центр", "description": "Вы находитесь в центре помещения"}
    ]
    insert_data(session, Locations, locations_data)
    session.close()


def insert_connections():
    """
    Insert connection data into the database.
    """
    session = Session(bind=engine)
    connections_data = [
        {"location_id": 1, "direction": "вперед", "target_location_id": 2},
        {"location_id": 2, "direction": "вперед", "target_location_id": 3},
        {"location_id": 3, "direction": "вперед", "target_location_id": 4},
        {"location_id": 4, "direction": "вперед", "target_location_id": 9},
        {"location_id": 5, "direction": "налево", "target_location_id": 7},
        {"location_id": 5, "direction": "вперед", "target_location_id": 6},
        {"location_id": 5, "direction": "направо", "target_location_id": 8},
        {"location_id": 6, "direction": "налево", "target_location_id": 8},
        {"location_id": 6, "direction": "вперед", "target_location_id": 5},
        {"location_id": 6, "direction": "направо", "target_location_id": 7},
        {"location_id": 7, "direction": "налево", "target_location_id": 6},
        {"location_id": 7, "direction": "вперед", "target_location_id": 8},
        {"location_id": 7, "direction": "направо", "target_location_id": 5},
        {"location_id": 9, "direction": "налево", "target_location_id": 5},
        {"location_id": 9, "direction": "вперед", "target_location_id": 7},
        {"location_id": 9, "direction": "направо", "target_location_id": 6},
    ]
    for entry in connections_data:
        existing_entry = (
            session.query(Connection)
            .filter_by(
                location_id=entry["location_id"],
                direction=entry["direction"]
            )
            .first()
        )
        if not existing_entry:
            insert_data(session, Connection, [entry])
    session.close()


if __name__ == "__main__":

    Base.metadata.create_all(engine)
    insert_locations()
    insert_connections()
