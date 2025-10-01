import requests
from bs4 import BeautifulSoup
import re

def get_reality_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "sk",
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return None, None

    soup = BeautifulSoup(r.text, "lxml")

    name_element = soup.select_one("h1")
    if name_element is None:
        print("Name element not found")
        return None, None
    name = name_element.getText().strip()

    price_elements = soup.select('p[data-test-id="text"]')
    price = None

    for el in price_elements:
        text = el.get_text(strip=True)
        digits = re.sub(r'[^\d]', '', text)
        if digits and len(digits) >= 5:  # napr. 169000
            price = int(digits)
            print(f"Nájdená cena: {price}")
            break

    if price is None:
        print("Žiadna platná cena sa nenašla")
        return name, None


    price = int(digits)

    # 💬 Tu vlož svoje výpisy:
    print(f"Nájdený názov: {name}")
    print(f"Nájdená cena: {price}")

    return name, price
