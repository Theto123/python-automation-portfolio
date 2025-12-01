import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

HEADERS = {"User-Agent": "Mozilla/5.0"}
RETRIES = 3
PRODUCT_URLS = [
    "https://example.com/product1",
    "https://example.com/product2",
    "https://example.com/product3"
]

def get_price(url):
    """Fetches the product price from a given URL with retry logic."""
    for attempt in range(1, RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product = soup.find("span", {"class": "price"})
            return product.text.strip() if product else "Price not found"
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed for {url}: {e}")
            sleep(1)
    return "Failed after retries"

def scrape_products(urls):
    """Scrapes prices for a list of product URLs and returns structured data."""
    results = []
    for url in urls:
        price = get_price(url)
        results.append({"url": url, "price": price})
    return results

def save_to_csv(data, filename="products.csv"):
    """Saves the scraped data to a CSV file."""
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    products = scrape_products(PRODUCT_URLS)
    for p in products:
        print(f"{p['url']} -> {p['price']}")
    save_to_csv(products)
