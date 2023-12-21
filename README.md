# ScraperBS4 FastAPI App

Welcome to the ScraperBS4 FastAPI app! This application allows you to scrape web pages and retrieve URLs from a given domain using the BeautifulSoup library.

## Features

- **Get Unique Domain URLs**: The `/urls` endpoint allows you to provide a URL, and the app will retrieve unique domain URLs from the provided URL.

- **Scrape URLs**: The `/scrape` endpoint enables you to scrape and retrieve data from a list of URLs.

## Getting Started

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI app:

   ```bash
   uvicorn scraper_app:app --host 0.0.0.0 --port 3000 --reload
   ```

   The app will be running at [http://localhost:3000](http://localhost:3000).

## API Endpoints

### 1. Get Unique Domain URLs

- **Endpoint**: `/urls`
- **Method**: GET
- **Parameters**:
  - `url` (query parameter): The URL for which you want to retrieve unique domain URLs.

#### Example:

```bash
curl -X 'GET' \
  'http://localhost:3000/urls?url=https://example.com' \
  -H 'accept: application/json'
```

### 2. Scrape URLs

- **Endpoint**: `/scrape`
- **Method**: POST
- **Parameters**:
  - `data` (request body): List of URLs to scrape.

#### Example:

```bash
curl -X 'POST' \
  'http://localhost:3000/scrape' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "urls": ["https://example.com/page1", "https://example.com/page2"]
}'
```

## Contact

For any questions or issues, feel free to contact us:

- **Name**: LumaticAI
- **Email**: contact@lumaticai.com

Thank you for using the ScraperBS4 FastAPI app! Happy scraping!!
