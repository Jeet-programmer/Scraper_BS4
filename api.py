import httpx
import logging
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from typing import List
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware
from bypass.uagent import get_random_user_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UrlsInput(BaseModel):
    urls: List[str]

class ScrapedData(BaseModel):
    url: str
    title: str
    text_content: str

def get_random_proxy():
    with open("proxies.txt", "r") as working_proxy_n:
        available_proxies = working_proxy_n.read().splitlines()  
        
    if not available_proxies: 
        raise Exception("No proxies available") 
    else:
        random_p = random.choice(available_proxies)
        return random_p
    
# Function to check robots.txt before scraping
async def check_robots_txt(url: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get(urljoin(url, "/robots.txt"))
    if response:
        return "User-agent: *" in response.text

# Introduce delays between requests
async def delay_request(delay: int):
    await asyncio.sleep(delay)

async def get_unique_domain_urls(url: str) -> List[str]:
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

    proxy = get_random_proxy()
    proxies = {f'http://': f'http://{proxy}'}
    headers = {"User-Agent": get_random_user_agent()}

    async with httpx.AsyncClient(timeout=30, proxies=proxies, headers=headers) as client:
        logger.info("Attempting to connect to URL: %s using proxy: %s using header: %s", url, proxy, headers)
        response = await client.get(url)

    # Check if the response has a "Via" header indicating proxy usage
    via_header = response.headers.get("Via")
    if via_header:
        logger.info("Via header: %s", via_header)
    else:
        logger.info("Proxy was not used.")

    logger.info("Connection successful")

    
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            if full_url not in urls and urlparse(full_url).netloc == urlparse(url).netloc:
                urls.append(full_url)

    logger.info(f"Generated unique domain URLs for {url}")
    return urls

async def scrape_page(url: str) -> ScrapedData:
    try:
        proxy = get_random_proxy()
        proxies = {f'http://': f'http://{proxy}'}
        headers = {"User-Agent": get_random_user_agent()}

        async with httpx.AsyncClient(timeout=30, proxies=proxies, headers=headers) as client:
            logger.info("Attempting to connect to URL: %s using proxy: %s using header: %s", url, proxy, headers)
            response = await client.get(url)

        # Check if the response has a "Via" header indicating proxy usage
        via_header = response.headers
        if via_header:
            logger.info("Proxy was used. Via header: %s", via_header)
        else:
            logger.info("Proxy was not used.")

        logger.info("Connection successful")

        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title.string if soup.title else ""
            text_content = soup.get_text()
            cleaned_text_content = " ".join(text_content.split())

            return ScrapedData(url=url, title=title, text_content=cleaned_text_content)
        else:
            raise HTTPException(status_code=response.status_code, detail="Error Fetching URL")

    except Exception as e:
        logger.error("Error scraping %s: %s", url, str(e))
        err = str(e)
        return ScrapedData(url=url, title="", text_content="Error scraping {url}: {err}".format(url=url, err=err))

@app.get("/")
async def root():
    return {
        "message": "Welcome to the LumaticAI Web Scraper API",
        "description": "This API allows you to scrape web pages and retrieve URLs from a given domain.",
        "endpoints": [
            {
                "path": "/urls",
                "description": "Get unique domain URLs from a provided URL."
            },
            {
                "path": "/scrape",
                "description": "Scrape and retrieve data from a list of URLs."
            }
        ],
        "documentation": "/docs",
        "contact": {
            "name": "LumaticAI",
            "email": "contact@lumaticai.com"
        }
    }

@app.get("/urls")
async def get_urls(url: str = Depends(get_unique_domain_urls)):
    try:
        if not url:
            logger.warning("Invalid URL or no URLs found")
            raise HTTPException(status_code=400, detail="Invalid URL or no URLs found")
        
        return {"urls": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
async def scrape_urls(data: UrlsInput, background_tasks: BackgroundTasks):
    try: 
        if not data.urls:
            raise HTTPException(status_code=400, detail="No URLs provided for scraping")
    
        tasks = [scrape_page(url) for url in data.urls]
        scraped_data = await asyncio.gather(*tasks)
        
        background_tasks.add_task(log_scraped_data, scraped_data)  
        
        return {"message": "Scraping completed", "data": scraped_data}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def log_scraped_data(data: List[ScrapedData]):
    for entry in data:
        logger.info(f"Scraped: {entry.url}")

if __name__ == "__main__":
    print("Server is running at port 3000")
    uvicorn.run(app, host="0.0.0.0", port="3000")


