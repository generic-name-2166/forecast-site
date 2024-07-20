# Forecast webiste

Website to show weather forecasts from [Open-Meteo API](https://open-meteo.com/)

# Additional features

- [x] Tests
- [x] Dockerized
- [ ] Autocomplete
- [x] Previously visited city suggestion
- [ ] Search history
    - [ ] Show search count per city

# Notice

This project uses the following packages
- `Django` as back end framework
- `requests` to communicate with Open Meteo API
- `uvicorn` as a production server
- `whitenoise` for static file middleware

# How to build and run

```bash
docker compose build
docker compose up
```

and go to http://localhost:8000

## Development

```bash
python -m venv venv
venv\Scripts\Activate.ps1  # venv/bin/activate
pip install -e ".[formatting]"
cd src/forecast_site
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > secret.txt
python manage.py migrate
python manage.py loaddata city.json
python manage.py runserver
```

To deploy

```bash
python manage.py collectstatic
python -m uvicorn forecast_site.asgi:application
```
