import math

import requests


def get_country_coordinates(country: str) -> dict | None:
    """Получает географические координаты страны через Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "country": country,
        "format": "jsonv2",
        "limit": 1,
    }
    headers = {"User-Agent": "PythonProject3Student/1.0 (educational project)"}

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15,
    )
    response.raise_for_status()

    results = response.json()
    if not results:
        return None

    return {
        "country": country,
        "latitude": float(results[0]["lat"]),
        "longitude": float(results[0]["lon"]),
    }


def get_aircraft_states(
    latitude: float,
    longitude: float,
    radius: float = 300.0,
) -> list[dict]:
    """Получает самолёты в небольшой области вокруг координат."""
    lat_delta = radius / 111
    cos_latitude = abs(math.cos(math.radians(latitude)))
    lon_delta = radius / (111 * max(cos_latitude, 0.01))

    params = {
        "lamin": latitude - lat_delta,
        "lamax": latitude + lat_delta,
        "lomin": longitude - lon_delta,
        "lomax": longitude + lon_delta,
    }

    url = "https://opensky-network.org/api/states/all"
    response = requests.get(
        url,
        params=params,
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    states = data.get("states") or []

    aircraft = []
    for state in states:
        aircraft.append(
            {
                "icao24": state[0],
                "callsign": (state[1] or "").strip(),
                "longitude": state[5],
                "latitude": state[6],
                "velocity": state[9],
                "on_ground": state[8],
            }
        )

    return aircraft


if __name__ == "__main__":
    coordinates = get_country_coordinates("United Arab Emirates")

    if coordinates is None:
        print("Не удалось получить координаты страны.")
    else:
        print("Координаты страны:", coordinates)

        try:
            aircraft = get_aircraft_states(
                latitude=coordinates["latitude"],
                longitude=coordinates["longitude"],
            )
            print("Количество найденных самолётов:", len(aircraft))
            print(
                "Пример самолёта:",
                aircraft[0] if aircraft else "Самолётов нет",
            )
        except requests.RequestException as error:
            print(f"Ошибка при запросе к OpenSky: {error}")
