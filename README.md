# Forecast webiste

Website to show weather forecasts from [Open-Meteo API](https://open-meteo.com/)

# Additional features

- [ ] Tests
- [ ] Dockerized
- [ ] Autocomplete
- [ ] Previously visited city suggestion
- [ ] Search history
    - [ ] Show search count per city

# How to build and run

## Development

```bash
python -m venv venv
venv\Scripts\Activate.ps1  # venv/bin/activate
pip install -e ".[formatting]"
python src/forecast_site/manage.py migrate
python src/forecast_site/manage.py runserver
```
