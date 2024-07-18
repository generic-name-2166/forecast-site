from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from unittest import skip

from .models import City


def add_url_city(url: str, city: str) -> str:
    return url + "?" + urlencode({"city": city})


class CityModelTests(TestCase):
    fixtures = ["city.json"]

    def test_getting_city_by_name(self):
        city_name = "Paris"
        print(City.objects.all())
        _city_obj = City.objects.get(name=city_name)


class WeatherViewTests(TestCase):
    fixtures = ["city.json"]

    def test_main_page(self):
        url = reverse("weather:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_specifying_a_city(self):
        city_name = "Paris"
        url = add_url_city(reverse("weather:index"), city_name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(city_name, response.content.decode())

    def test_nonexistent_city(self):
        fictional_city = "Los Santos"
        url = add_url_city(reverse("weather:index"), fictional_city)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(fictional_city, response.content.decode())

    def test_redirect(self):
        url = reverse("root")
        response = self.client.get(url, follow=False)
        self.assertEqual(response.status_code, 301)

    @skip("not implemented")
    def test_redirect_with_city(self):
        city_name = "Paris"
        url = add_url_city(reverse("root"), city_name)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(city_name, response.content.decode())
