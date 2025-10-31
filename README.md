# Random Name Generator

This project provides both a command-line interface and a small Flask web app for generating random full names. It draws from a dataset of more than 5,000 first names (male and female) and 6,000 last names sourced from multiple Faker locales.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# CLI usage
python random_name_generator.py --count 20 --gender female --seed 123

# Web app
flask --app app run
```

Open http://127.0.0.1:5000/ in your browser to access the web interface.

## API Endpoint

The web service also exposes a JSON API:

```
GET /api/names?count=25&gender=male&seed=99
```

Response:

```json
[
  {
    "first_name": "Carlos",
    "last_name": "Hernandez",
    "full_name": "Carlos Hernandez"
  }
]
```

## Dataset

The dataset is stored at `data/name_pools.json`. If you want to regenerate it, install the optional dependency `Faker` and run the helper script:

```bash
python scripts/build_dataset.py
```

This will rebuild the JSON file using the latest Faker locale providers.
