"""
URL configuration for forecast_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.urls import reverse
from django.http import HttpRequest, HttpResponsePermanentRedirect


def redirect_to_weather(request: HttpRequest):
    city = request.GET.get("city", None)
    base: str = reverse("weather:index")
    url = base if city is None else f"{base}?city={city}"
    return HttpResponsePermanentRedirect(url)


urlpatterns = [
    path("", redirect_to_weather, name="root"),
    path("weather/", include("weather.urls")),
    path("admin/", admin.site.urls),
]
