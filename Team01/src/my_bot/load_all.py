import sqlalchemy as db
import json
from sqlalchemy.orm import declarative_base, Session, relationship
from load_map import Base, engine, insert_data

SCRIPT_JSON = 'load_script/script_game.json'


class Script(Base):
    """
    SQLAlchemy model representing a script in the game.

    Attributes:
        id (int): Primary key for the script.
        text (str): The text content of the script.
    """
    __tablename__ = "script"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, unique=True)


class LineScript(Base):
    """
    SQLAlchemy model representing a line of script in the game.

    Attributes:
        id : int
            Primary key for the line of script.
        text_id : int
            Foreign key referencing the associated Script's id.
        option_a_id : int
            Foreign key referencing the Script id for option A.
        option_b_id : int
            Foreign key referencing the Script id for option B.
        next_dialog_option_a_id : int
            Foreign key referencing the Script id for the next dialog option A.
        next_dialog_option_b_id : int
            Foreign key referencing the Script id for the next dialog option B.
        location_id : int
            Foreign key referencing the location id associated with the line of script.

    Relationships:
        text : relationship
            Relationship with the Script table using the foreign key text_id.
        option_a : relationship
            Relationship with the Script table using the foreign key option_a_id.
        option_b : relationship
            Relationship with the Script table using the foreign key option_b_id.
        next_dialog_option_a : relationship
            Relationship with the Script table using the foreign key next_dialog_option_a_id.
        next_dialog_option_b : relationship
            Relationship with the Script table using the foreign key next_dialog_option_b_id.
        location : relationship
            Relationship with the Locations table using the foreign key location_id.
    """
    __tablename__ = 'line_script'

    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey('script.id'), unique=True)
    option_a_id = db.Column(db.Integer, db.ForeignKey('script.id'))
    option_b_id = db.Column(db.Integer, db.ForeignKey('script.id'))
    next_dialog_option_a_id = db.Column(db.Integer, db.ForeignKey('script.id'))
    next_dialog_option_b_id = db.Column(db.Integer, db.ForeignKey('script.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    text = relationship('Script', foreign_keys=[text_id])
    option_a = relationship('Script', foreign_keys=[option_a_id])
    option_b = relationship('Script', foreign_keys=[option_b_id])
    next_dialog_option_a = relationship(
        'Script', foreign_keys=[next_dialog_option_a_id])
    next_dialog_option_b = relationship(
        'Script', foreign_keys=[next_dialog_option_b_id])
    location = relationship('Locations', foreign_keys=[location_id])


class HealthExperienceDistribution(Base):
    """
    SQLAlchemy model representing health and experience distribution in the game.

    Attributes:
        id : int
            Primary key for health and experience distribution.
        text_id : int
            Foreign key referencing the associated Script's id.
        health : int
            Health value associated with the distribution.
        experience : int
            Experience value associated with the distribution.
        health_enemy : int
            Enemy health value associated with the distribution.

    Relationships:
        text : relationship
            Relationship with the Script table using the foreign key text_id.
    """
    
    __tablename__ = "health_experience_distribution"

    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey('script.id'), unique=True)
    health = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    health_enemy = db.Column(db.Integer)

    text = relationship('Script', foreign_keys=[text_id])


def insert_script():
    """
    Insert script data into the database.
    """
    session = Session(bind=engine)
    with open(SCRIPT_JSON, 'r', encoding='utf-8') as file:
        script_data = json.load(file)
    items_without_ids = [{'text': item['text']}
                         for item in script_data['items']]
    insert_data(session, Script, items_without_ids)
    session.close()


def insert_line_script():
    """
    Insert line script data into the database.
    """
    session = Session(bind=engine)
    line_script_data = [
        {"text_id": 1, "option_a_id": 2, "option_b_id": 4,
            "next_dialog_option_a_id": 3, "next_dialog_option_b_id": 5, "location_id": 1},
        {"text_id": 3, "option_a_id": 60, "option_b_id": None, "next_dialog_option_a_id": 59,
            "next_dialog_option_b_id": None, "location_id": 1},  # конец
        {"text_id": 5, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": 6, "next_dialog_option_b_id": None, "location_id": 1},
        {"text_id": 6, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": 1},
        {"text_id": 7, "option_a_id": 8, "option_b_id": 10,
            "next_dialog_option_a_id": 9, "next_dialog_option_b_id": 11, "location_id": 2},
        {"text_id": 9, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": 12, "next_dialog_option_b_id": None, "location_id": 2},
        {"text_id": 11, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": 12, "next_dialog_option_b_id": None, "location_id": 2},
        {"text_id": 12, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": 2},
        {"text_id": 13, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": 14, "next_dialog_option_b_id": None, "location_id": 3},
        {"text_id": 14, "option_a_id": 15, "option_b_id": 17,
            "next_dialog_option_a_id": 16, "next_dialog_option_b_id": 18, "location_id": 3},
        {"text_id": 16, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": 18, "next_dialog_option_b_id": None, "location_id": 3},
        {"text_id": 18, "option_a_id": 19, "option_b_id": 21,
            "next_dialog_option_a_id": 20, "next_dialog_option_b_id": 22, "location_id": 3},
        {"text_id": 20, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": 3},
        {"text_id": 22, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": 3},
        {"text_id": 23, "option_a_id": 24, "option_b_id": 26,
            "next_dialog_option_a_id": 25, "next_dialog_option_b_id": 27, "location_id": 4},
        {"text_id": 25, "option_a_id": 28, "option_b_id": 30,
            "next_dialog_option_a_id": 29, "next_dialog_option_b_id": 31, "location_id": 4},
        {"text_id": 27, "option_a_id": 28, "option_b_id": 30,
            "next_dialog_option_a_id": 29, "next_dialog_option_b_id": 31, "location_id": 4},
        {"text_id": 29, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": 9},
        {"text_id": 31, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 35, "option_a_id": 37, "option_b_id": 39,
            "next_dialog_option_a_id": 38, "next_dialog_option_b_id": 40, "location_id": 5},
        {"text_id": 38, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 40, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 46, "option_a_id": 47, "option_b_id": 49,
            "next_dialog_option_a_id": 48, "next_dialog_option_b_id": 50, "location_id": 6},
        {"text_id": 48, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 50, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 41, "option_a_id": 42, "option_b_id": 44,
            "next_dialog_option_a_id": 43, "next_dialog_option_b_id": 45, "location_id": 7},
        {"text_id": 43, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 45, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": None},
        {"text_id": 51, "option_a_id": 55, "option_b_id": 57,
            "next_dialog_option_a_id": 56, "next_dialog_option_b_id": 58, "location_id": 8},
        {"text_id": 58, "option_a_id": 60, "option_b_id": None, "next_dialog_option_a_id": 59,
            "next_dialog_option_b_id": None, "location_id": 8},  # конец
        {"text_id": 56, "option_a_id": 60, "option_b_id": None, "next_dialog_option_a_id": 59,
            "next_dialog_option_b_id": None, "location_id": 8},  # конец
        {"text_id": 59, "option_a_id": 60, "option_b_id": None,
            "next_dialog_option_a_id": None, "next_dialog_option_b_id": None, "location_id": 8}
    ]
    insert_data(session, LineScript, line_script_data)
    session.close()


def insert_exp():
    """
    Insert health and experience distribution data into the database.
    """
    session = Session(bind=engine)
    decision_data = [
        {"text_id": 3, "health": 0, "experience": 0, "health_enemy": -1},
        # После разговора вы чувствуйте ухудшение
        {"text_id": 6, "health": -1, "experience": 1, "health_enemy": 1},
        {"text_id": 9, "health": -1, "experience": 1,
            "health_enemy": 0},  # Обратиться к медсестре
        {"text_id": 11, "health": 1, "experience": -1,
            "health_enemy": 0},  # Уверенно пройти мимо
        {"text_id": 16, "health": 1, "experience": -1,
            "health_enemy": -1},  # Отказаться от погружения
        {"text_id": 18, "health": -1, "experience": 1,
            "health_enemy": 1},  # Согласиться на погружение
        {"text_id": 25, "health": -1, "experience": 1,
            "health_enemy": 0},  # Наклониться к Роману
        {"text_id": 27, "health": 0, "experience": 1,
            "health_enemy": 0},  # Оглядеться
        {"text_id": 29, "health": -1, "experience": -1,
            "health_enemy": 1},  # Попытаться вернуться к Роману
        # Рассказать матери о происходящем
        {"text_id": 38, "health": -1, "experience": 1, "health_enemy": 1},
        {"text_id": 40, "health": 1, "experience": 0,
            "health_enemy": -1},  # Ничего не рассказывать
        {"text_id": 43, "health": -1, "experience": 1,
            "health_enemy": 1},  # Отдать сердце
        {"text_id": 45, "health": 1, "experience": -1,
            "health_enemy": -1},  # Оставить сердце
        {"text_id": 48, "health": -1, "experience": 1, "health_enemy": 0},  # Ребенка
        {"text_id": 50, "health": 1, "experience": -1, "health_enemy": 1}   # Девушку
    ]
    insert_data(session, HealthExperienceDistribution, decision_data)
    session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    insert_script()
    insert_line_script()
    insert_exp()
