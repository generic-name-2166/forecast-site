from django.db.models import F, Q
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timezone
import itertools
from typing import Optional
from collections.abc import Iterator

from .models import City
from .api import ApiProxy, ApiResponse, WeatherVariable, Variables


type _CityName = str
type WeatherView = dict[datetime, dict[WeatherVariable, int | float]]
type WeatherViews = dict[_CityName, WeatherView]
type SelectedView = dict[datetime, WeatherView]


def _transpose_response(resp: ApiResponse) -> WeatherView:
    values: Variables = resp["hourly"]  # type: ignore | I know what I'm doing
    times: list[int] = values["time"]  # type: ignore
    temperatures = values["temperature_2m"]
    humidities = values["relative_humidity_2m"]
    apparent_temperatures = values["apparent_temperature"]
    probabilities = values["precipitation_probability"]

    # Trusting that API always returns UTC+00:00 unix timestamps in seconds
    return {
        datetime.fromtimestamp(timestamp, timezone.utc): {
            "temperature_2m": temperatures[i],
            "relative_humidity_2m": humidities[i],
            "apparent_temperature": apparent_temperatures[i],
            "precipitation_probability": probabilities[i],
        }
        for (i, timestamp) in enumerate(times)
    }


def _transpose_responses(cities: dict[_CityName, ApiResponse], exclude: Optional[_CityName] = None) -> WeatherViews:
    views: WeatherViews = {
        city_name: _transpose_response(resp) for (city_name, resp) in cities.items()
    }
    if exclude is not None:
        del views[exclude]
    return views


def _format_day(day: list[tuple[datetime, dict[WeatherVariable, int | float]]]) -> tuple[datetime, dict[datetime, dict[WeatherVariable, int | float]]]:
    # for displaying the date
    hour = day[0][0]
    picked_hours = dict(day[::3])
    return (hour, picked_hours)


def _batch_days(view: WeatherView) -> SelectedView:
    hours = view.items()
    days: Iterator[list[tuple[datetime, dict[WeatherVariable, int | float]]]] = map(list, itertools.batched(hours, 24))
    result = dict(map(_format_day, days))
    return result


def index(request: HttpRequest):
    proxy = ApiProxy()
    cities = City.objects.all()
    responses = {city.name: proxy.get(city.latitude, city.longitude) for city in cities}
    try:
        # idk what other type other than str can it be
        if not isinstance(city_name := request.GET["city"], str): # type: ignore
            raise TypeError 
        city_obj: City = cities.get(name=city_name)
    except (KeyError, City.DoesNotExist):
        context = {"cities": _transpose_responses(responses)}
        return render(request, "weather/index.html", context=context)

    cities = cities.filter(~Q(name=city_name))
    views = _transpose_responses(responses, exclude=city_name)

    city_obj.searches = F("searches") + 1
    city_obj.save()

    selected_city = {
        "name": city_name,
        "days": _batch_days(_transpose_response(responses[city_name])),
    }

    context: dict[str, dict[str, str | SelectedView] | WeatherViews] = {
        "selected_city": selected_city,
        "cities": views,
    }

    return render(request, "weather/index.html", context=context)


def redirect_to_weather(request: HttpRequest):
    city = request.GET.get("city", None)
    print(f"{city=}")
    base: str = reverse("weather:index")
    url = base if city is None else f"{base}?city={city}"
    return HttpResponseRedirect(url)
