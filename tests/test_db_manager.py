from unittest.mock import patch

import pytest

from src.db_manager import DBManager


@patch("src.db_manager.get_connection")
def test_get_countries_and_aeroplanes_count(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [("Japan", 10), ("France", 5)]

    result = DBManager().get_countries_and_aeroplanes_count()

    assert result == [("Japan", 10), ("France", 5)]
    cursor.execute.assert_called_once()
    connection.close.assert_called_once()


@patch("src.db_manager.get_connection")
def test_get_all_aeroplanes(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        ("abc123", "ABC123", 25.0, 55.0, 200.0, False, 1, None)
    ]

    result = DBManager().get_all_aeroplanes()

    assert len(result) == 1
    assert result[0][0] == "abc123"
    connection.close.assert_called_once()


@patch("src.db_manager.get_connection")
def test_get_avg_speed(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (200.0,)

    result = DBManager().get_avg_speed()

    assert result == 200.0
    connection.close.assert_called_once()


@patch("src.db_manager.get_connection")
def test_get_avg_speed_without_data(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (None,)

    result = DBManager().get_avg_speed()

    assert result is None
    connection.close.assert_called_once()


@patch("src.db_manager.get_connection")
def test_get_aeroplanes_with_higher_speed(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        ("abc123", "ABC123", 25.0, 55.0, 250.0, False, 1, None)
    ]

    result = DBManager().get_aeroplanes_with_higher_speed()

    assert len(result) == 1
    assert result[0][4] == 250.0
    connection.close.assert_called_once()


@patch("src.db_manager.get_connection")
def test_get_aeroplanes_with_keyword(mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        ("abc123", "ACA123", 25.0, 55.0, 200.0, False, 1, None)
    ]

    result = DBManager().get_aeroplanes_with_keyword("ACA")

    assert len(result) == 1
    assert result[0][1] == "ACA123"
    cursor.execute.assert_called_once()
    connection.close.assert_called_once()


def test_get_aeroplanes_with_empty_keyword():
    with pytest.raises(ValueError):
        DBManager().get_aeroplanes_with_keyword("   ")
