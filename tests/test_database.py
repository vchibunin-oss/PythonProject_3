from unittest.mock import ANY, MagicMock, patch

from src.database import create_tables, get_connection


@patch("src.database.psycopg2.connect")
def test_get_connection(mock_connect):
    get_connection()

    mock_connect.assert_called_once_with(
        host="localhost",
        port="5432",
        database="aircraft_tracker",
        user="postgres",
        password=ANY,
    )


@patch("src.database.get_connection")
def test_create_tables(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor

    create_tables()

    assert cursor.execute.call_count == 2
    connection.close.assert_called_once()
