# scrape_amazon_product

Python Version: 3.8+

## Install Python Packages
```bash
pip install -r requirements.txt
```

## Install Pre-Commit hooks
```bash
pre-commit install
```

## Run server
```bash
python manage.py runserver
```

## Test API

### Using curl
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/scrape-products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "keyword": "laptop"
}'
```

### Using Swagger
- open swagger in browser http://127.0.0.1:8000/api/swagger/
- run `/scrape-products/`
