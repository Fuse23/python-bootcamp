from config import DB_NAME, DB_PASS, DB_USER, DB_HOST, DB_PORT

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, connection, cursor


conn: connection = psycopg2.connect(
    dbname='postgres',
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
curs: cursor = conn.cursor()
curs.execute(f'CREATE DATABASE {DB_NAME}')
curs.close()
conn.close()
# conn = psycopg2.connect(
#     dbname='postgres',
#     user=DB_USER,
#     password=DB_PASS,
#     host=DB_HOST,
#     port=DB_PORT
# )
# conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# curs = conn.cursor()
# curs.execute('''
#     CREATE TABLE IF NOT EXISTS ships (
#         id SERIAL NOT NULL,
#         alignment VARCHAR(5) NOT NULL,
#         name VARCHAR(30) NOT NULL,
#         ship_class VARCHAR(30) NOT NULL,
#         length FLOAT NOT NULL,
#         crew_size INTEGER NOT NULL,
#         armed BOOLEAN NOT NULL,
#         PRIMARY KEY (id)
#     )
# ''')
# curs.execute('''
#     CREATE TABLE IF NOT EXISTS officers (
#         id SERIAL NOT NULL,
#         first_name VARCHAR(30) NOT NULL,
#         last_name VARCHAR(30) NOT NULL,
#         rank VARCHAR(30) NOT NULL,
#         ship_id INTEGER NOT NULL,
#         PRIMARY KEY (id),
#         FOREIGN KEY(ship_id) REFERENCES ships (id)
#     )
# ''')
# curs.close()
# conn.close()
