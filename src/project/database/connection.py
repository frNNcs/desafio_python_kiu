import psycopg2

from project.config.base import CONNECTION_STRING
from project.database.init_db import init_db

conn = psycopg2.connect(CONNECTION_STRING)

init_db()
