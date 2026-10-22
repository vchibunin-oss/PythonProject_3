from unittest.mock import patch

from src import loader


@patch("src.loader.get_connection")
@patch("src.loader.get_country_coordinates")
def test_load_countries_success(mock_get_coordinates, mock_get_connection):
    mock_get_coordinates.return_value = {
        "country": "Japan",
        "latitude": 35.0,
        "longitude": 139.0,
    }

    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value

    loader.load_countries()

    assert mock_get_coordinates.call_count == len(loader.COUNTRIES)
    assert cursor.execute.call_count == len(loader.COUNTRIES)
    connection.close.assert_called_once()


@patch("src.loader.get_connection")
@patch("src.loader.get_country_coordinates")
def test_load_countries_skips_missing_country(
    mock_get_coordinates, mock_get_connection
):
    mock_get_coordinates.return_value = None

    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value

    loader.load_countries()

    cursor.execute.assert_not_called()
    connection.close.assert_called_once()


@patch("src.loader.get_connection")
@patch("src.loader.get_aircraft_states")
def test_load_aircraft_success(mock_get_aircraft, mock_get_connection):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        (1, "Japan", 35.0, 139.0),
    ]

    mock_get_aircraft.return_value = [
        {
            "icao24": "abc123",
            "callsign": "JAL123",
            "latitude": 35.1,
            "longitude": 139.1,
            "velocity": 220.0,
            "on_ground": False,
        }
    ]

    loader.load_aircraft()

    mock_get_aircraft.assert_called_once_with(
        latitude=35.0,
        longitude=139.0,
        radius=300.0,
    )
    assert cursor.execute.call_count == 2
    connection.close.assert_called_once()


@patch("src.loader.get_connection")
@patch("src.loader.get_aircraft_states")
def test_load_aircraft_skips_missing_latitude(
    mock_get_aircraft, mock_get_connection
):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        (1, "Japan", 35.0, 139.0),
    ]

    mock_get_aircraft.return_value = [
        {
            "icao24": "abc123",
            "callsign": "JAL123",
            "latitude": None,
            "longitude": 139.1,
            "velocity": 220.0,
            "on_ground": False,
        }
    ]

    loader.load_aircraft()

    assert cursor.execute.call_count == 1
    connection.close.assert_called_once()


@patch("src.loader.get_connection")
@patch("src.loader.get_aircraft_states")
def test_load_aircraft_handles_api_error(
    mock_get_aircraft, mock_get_connection
):
    connection = mock_get_connection.return_value
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        (1, "Japan", 35.0, 139.0),
    ]

    mock_get_aircraft.side_effect = RuntimeError("API unavailable")

    loader.load_aircraft()

    assert cursor.execute.call_count == 1
    connection.close.assert_called_once()
