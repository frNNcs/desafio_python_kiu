import psycopg

from project.config.base import CONNECTION_STRING

conn = psycopg.connect(CONNECTION_STRING)
