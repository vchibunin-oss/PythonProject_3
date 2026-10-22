from src.database import create_tables
from src.db_manager import DBManager
from src.loader import load_aircraft, load_countries


def main() -> None:
    """Запускает сбор данных и вывод результатов."""
    create_tables()

    print("\nЗагрузка координат стран...")
    load_countries()

    print("\nЗагрузка данных о воздушных судах...")
    load_aircraft()

    manager = DBManager()

    print("\nСамолёты по странам:")
    for country, count in manager.get_countries_and_aeroplanes_count():
        print(f"{country}: {count}")

    print(f"\nВсего воздушных судов: {len(manager.get_all_aeroplanes())}")
    print("Средняя скорость:", manager.get_avg_speed(), "м/с")


if __name__ == "__main__":
    main()
