import os

from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
HOSTNAME = os.getenv("HOSTNAME")

CONNECTION_STRING = f"""
    dbname={POSTGRES_DB}
    user={POSTGRES_USER}
    password={POSTGRES_PASSWORD}
    host={HOSTNAME}
    port={POSTGRES_PORT}
"""
