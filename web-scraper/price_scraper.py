import requests
from bs4 import BeautifulSoup

def get_price(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    product = soup.find("span", {"class": "price"})
    return product.text.strip() if product else "Price not found"

if __name__ == "__main__":
    print(get_price("https://example.com/product"))