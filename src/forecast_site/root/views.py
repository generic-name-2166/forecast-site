from django.http import HttpResponse
from typing import Any


def index(_request: Any):
    return HttpResponse("Hello, world. You're at the polls index.")
