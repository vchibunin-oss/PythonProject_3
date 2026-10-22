from unittest.mock import Mock, patch

from src.api import get_aircraft_states, get_country_coordinates


@patch("src.api.requests.get")
def test_get_country_coordinates_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"lat": "25.276987", "lon": "55.296249"}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_country_coordinates("United Arab Emirates")

    assert result == {
        "country": "United Arab Emirates",
        "latitude": 25.276987,
        "longitude": 55.296249,
    }
    mock_get.assert_called_once()


@patch("src.api.requests.get")
def test_get_country_coordinates_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_country_coordinates("Unknown Country")

    assert result is None


@patch("src.api.requests.get")
def test_get_aircraft_states_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "states": [
            [
                "abc123",
                " ACA123  ",
                None,
                None,
                None,
                55.296249,
                25.276987,
                None,
                False,
                200.5,
            ]
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_aircraft_states(25.276987, 55.296249)

    assert result == [
        {
            "icao24": "abc123",
            "callsign": "ACA123",
            "longitude": 55.296249,
            "latitude": 25.276987,
            "velocity": 200.5,
            "on_ground": False,
        }
    ]


@patch("src.api.requests.get")
def test_get_aircraft_states_without_data(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"states": None}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_aircraft_states(25.276987, 55.296249)

    assert result == []
