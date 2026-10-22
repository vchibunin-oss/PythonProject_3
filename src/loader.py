from src.api import get_aircraft_states, get_country_coordinates
from src.database import get_connection

COUNTRIES = [
    "United Arab Emirates",
    "United States",
    "Canada",
    "United Kingdom",
    "France",
    "Germany",
    "Japan",
    "Australia",
    "India",
    "Brazil",
]


def load_countries() -> None:
    """Получает координаты стран и сохраняет их в базу данных."""
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                for country in COUNTRIES:
                    coordinates = get_country_coordinates(country)

                    if coordinates is None:
                        print(f"Не удалось найти страну: {country}")
                        continue

                    cursor.execute(
                        """
                        INSERT INTO countries (name, latitude, longitude)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (name) DO UPDATE SET
                            latitude = EXCLUDED.latitude,
                            longitude = EXCLUDED.longitude;
                        """,
                        (
                            coordinates["country"],
                            coordinates["latitude"],
                            coordinates["longitude"],
                        ),
                    )
                    print(f"Сохранена страна: {country}")
    finally:
        connection.close()


def load_aircraft() -> None:
    """Получает самолёты из OpenSky и сохраняет их в PostgreSQL."""
    connection = get_connection()

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, latitude, longitude FROM countries;"
                )
                countries = cursor.fetchall()

                for country_id, country_name, latitude, longitude in countries:
                    try:
                        aircraft_list = get_aircraft_states(
                            latitude=latitude,
                            longitude=longitude,
                            radius=300.0,
                        )
                    except Exception as error:
                        print(f"Ошибка для {country_name}: {error}")
                        continue

                    for aircraft in aircraft_list:
                        if aircraft["latitude"] is None:
                            continue

                        cursor.execute(
                            """
                            INSERT INTO aircraft (
                                icao24,
                                country_id,
                                callsign,
                                latitude,
                                longitude,
                                velocity,
                                on_ground,
                                last_seen
                            )
                            VALUES (
                            %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                            )
                            ON CONFLICT (icao24) DO UPDATE SET
                                country_id = EXCLUDED.country_id,
                                callsign = EXCLUDED.callsign,
                                latitude = EXCLUDED.latitude,
                                longitude = EXCLUDED.longitude,
                                velocity = EXCLUDED.velocity,
                                on_ground = EXCLUDED.on_ground,
                                last_seen = CURRENT_TIMESTAMP;
                            """,
                            (
                                aircraft["icao24"],
                                country_id,
                                aircraft["callsign"],
                                aircraft["latitude"],
                                aircraft["longitude"],
                                aircraft["velocity"],
                                aircraft["on_ground"],
                            ),
                        )

                    print(
                        f"{country_name}: получено "
                        f"{len(aircraft_list)} записей"
                    )
    finally:
        connection.close()


if __name__ == "__main__":
    load_countries()
    load_aircraft()
