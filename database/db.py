import os
from pathlib import Path

import psycopg

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def get_connection():

    return psycopg.connect(

        host=os.getenv("DB_HOST"),

        port=os.getenv("DB_PORT"),

        dbname=os.getenv("DB_NAME"),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD"),

    )


def initialize_database():

    schema_file = (
        BASE_DIR / "database" / "schema.sql"
    )

    schema = schema_file.read_text(
        encoding="utf-8"
    )

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(schema)

    print("Database initialized successfully.")


def test_connection():

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute("SELECT version();")

            result = cursor.fetchone()

            print("PostgreSQL connected!")

            print(result[0])