from src.database import get_connection


class DBManager:
    """Выполняет запросы к базе данных о странах и воздушных судах."""

    def get_countries_and_aeroplanes_count(self) -> list[tuple]:
        """Возвращает страны и количество самолётов в каждой стране."""
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        countries.name,
                        COUNT(aircraft.icao24) AS aeroplanes_count
                    FROM countries
                    LEFT JOIN aircraft
                        ON countries.id = aircraft.country_id
                    GROUP BY countries.id, countries.name
                    ORDER BY countries.name;
                    """)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_all_aeroplanes(self) -> list[tuple]:
        """Возвращает список всех воздушных судов."""
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        icao24,
                        callsign,
                        latitude,
                        longitude,
                        velocity,
                        on_ground,
                        country_id,
                        last_seen
                    FROM aircraft
                    ORDER BY icao24;
                    """)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_avg_speed(self) -> float | None:
        """Возвращает среднюю скорость воздушных судов в м/с."""
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT AVG(velocity)
                    FROM aircraft
                    WHERE velocity IS NOT NULL;
                    """)
                result = cursor.fetchone()
                return float(result[0]) if result[0] is not None else None
        finally:
            connection.close()

    def get_aeroplanes_with_higher_speed(self) -> list[tuple]:
        """Возвращает воздушные суда со скоростью выше средней."""
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        icao24,
                        callsign,
                        latitude,
                        longitude,
                        velocity,
                        on_ground,
                        country_id,
                        last_seen
                    FROM aircraft
                    WHERE velocity > (
                        SELECT AVG(velocity)
                        FROM aircraft
                        WHERE velocity IS NOT NULL
                    )
                    ORDER BY velocity DESC;
                    """)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_aeroplanes_with_keyword(
        self,
        keyword: str,
    ) -> list[tuple]:
        """Ищет воздушные суда по части позывного без учёта регистра."""
        if not keyword or not keyword.strip():
            raise ValueError("Поисковое слово не должно быть пустым.")

        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        icao24,
                        callsign,
                        latitude,
                        longitude,
                        velocity,
                        on_ground,
                        country_id,
                        last_seen
                    FROM aircraft
                    WHERE callsign ILIKE %s
                    ORDER BY callsign;
                    """,
                    (f"%{keyword.strip()}%",),
                )
                return cursor.fetchall()
        finally:
            connection.close()


if __name__ == "__main__":
    manager = DBManager()

    print("Самолёты по странам:")
    for country, count in manager.get_countries_and_aeroplanes_count():
        print(f"{country}: {count}")

    print(f"\nВсего воздушных судов: {len(manager.get_all_aeroplanes())}")
    print("Средняя скорость:", manager.get_avg_speed(), "м/с")

    faster_aircraft = manager.get_aeroplanes_with_higher_speed()
    print("Быстрее средней скорости:", len(faster_aircraft))

    keyword = "ACA"
    matching_aircraft = manager.get_aeroplanes_with_keyword(keyword)
    print(f"\nСамолёты с позывным, содержащим {keyword}:")
    print(f"Найдено: {len(matching_aircraft)}")

    for plane in matching_aircraft[:10]:
        print(plane)
