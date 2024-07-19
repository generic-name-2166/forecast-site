from dataclasses import dataclass
import time
import requests
from typing import Any


class Singleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


type Coordinates = tuple[float, float]
type WeatherVariable = str
type UnitsMap = dict[WeatherVariable, str]
type Variables = dict[WeatherVariable, list[int] | list[float]]
type ApiResponse = dict[str, float | str | UnitsMap | Variables]


def get_current_hour() -> int:
    # Surely the machine won't change timezones while active
    seconds = int(time.time())
    remainder = seconds % 3600
    this_hour = seconds - remainder
    return this_hour if remainder < 1800 else this_hour + 3600


API_URL = "https://api.open-meteo.com/v1/forecast"  # ?latitude=52.52&longitude=13.41
VARIABLES = {
    "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability",
    "timeformat": "unixtime",
}


@dataclass(init=False, slots=True)
class ApiProxy(metaclass=Singleton):
    # In-memory cache for the API
    # as a signleton for simplicity
    # The inner dict will only ever have 1 key value pair
    cache: dict[Coordinates, dict[int, ApiResponse]]

    def __init__(self) -> None:
        self.cache = {}

    def _call_api(self, coords: Coordinates) -> ApiResponse:
        params = {
            "latitude": coords[0],
            "longitude": coords[1],
        } | VARIABLES
        return requests.get(API_URL, params=params).json()

    def get(self, latitude: float, longitude: float):
        coords: Coordinates = (latitude, longitude)
        hour = get_current_hour()

        cached = self.cache.get(coords, None)
        if cached is None or cached.get(hour, None) is None:
            resp = self._call_api(coords)
            self.cache[coords] = {hour: resp}
            return resp
        return cached[hour]
