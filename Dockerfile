FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /home/forecast_site

RUN pip install /home/forecast_site

WORKDIR /home/forecast_site/src/forecast_site

RUN python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > secret.txt
RUN python manage.py migrate
RUN python manage.py loaddata city.json
# RUN python manage.py collectstatic

EXPOSE 8000

ENTRYPOINT [ "python", "-m", "uvicorn", "forecast_site.asgi:application" ]
