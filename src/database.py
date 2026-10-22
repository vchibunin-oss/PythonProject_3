import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Создаёт подключение к базе данных PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "aircraft_tracker"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )


def create_tables() -> None:
    """Создаёт таблицы стран и воздушных судов."""
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS countries (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        latitude DOUBLE PRECISION NOT NULL,
                        longitude DOUBLE PRECISION NOT NULL
                    );
                    """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS aircraft (
                        icao24 VARCHAR(6) PRIMARY KEY,
                        country_id INTEGER REFERENCES countries(id),
                        callsign VARCHAR(20),
                        latitude DOUBLE PRECISION,
                        longitude DOUBLE PRECISION,
                        velocity DOUBLE PRECISION,
                        on_ground BOOLEAN,
                        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """)

        print("Таблицы countries и aircraft созданы или уже существуют.")
    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
