from django.db.models import F
from django.shortcuts import render
from django.http import HttpRequest

from .models import City


def index(request: HttpRequest):
    try:
        # idk what other type other than str can it be
        city_name: str = request.GET["city"]  # type: ignore
        city_obj: City = City.objects.get(name=city_name)
    except (KeyError, City.DoesNotExist):
        return render(request, "root/index.html")

    city_obj.searches = F("searches") + 1
    city_obj.save()

    context: dict[str, str] = {"city_name": city_name}

    return render(request, "root/index.html", context=context)
