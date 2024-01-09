import psycopg2

from project.config.base import CONNECTION_STRING

conn = psycopg2.connect(CONNECTION_STRING)
