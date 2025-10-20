import re
import random
import requests
from bs4 import BeautifulSoup



# ==============================
# 🧩 Pomocné funkcie pre model Post
# ==============================

def save_post_with_images(form, user, image_files):
    """
    Uloží Post a všetky nahraté obrázky.
    """
    from .models import Image  # ak pracuješ s obrázkami v save_post_with_images
    post = form.save(commit=False)
    post.author = user
    post.save()
    for image_file in image_files:
        Image.objects.create(post=post, image=image_file)
    return post


# ==============================
# 💰 Pomocné funkcie pre model Ceny
# ==============================

def save_ceny_instance(form, get_price, detect_source_type):
    """
    Uloží položku Ceny vrátane detekcie typu zdroja a načítania aktuálnej ceny.
    """
    instance = form.save(commit=False)

    if not instance.url:
        return None, "⚠️ URL je prázdna"

    instance.source_type = detect_source_type(instance.url)
    name, price = get_price(instance)

    if name is None:
        name = "Neznáma položka"
    if price is None:
        price = 0

    instance.name = name
    instance.now_price = price
    instance.old_price = price
    instance.differ_price = 0
    instance.save()

    return instance, None  # (objekt, chyba)


# ==============================
# 🔍 Detekcia zdroja podľa URL
# ==============================

def detect_source_type(url: str) -> str:
    if not url:
        print("⚠️ URL je prázdna, nastavujem 'flat'")
        return "flat"

    url = url.lower()
    if "books.toscrape.com" in url:
        print("🔍 Rozpoznaný typ: book")
        return "book"
    elif "nehnutelnosti" in url or "reality" in url or "byt" in url:
        print("🔍 Rozpoznaný typ: flat")

    print("⚠️ URL neobsahuje známe kľúčové slová, fallback na 'flat'")
    return "flat"


# ==============================
# 🔁 Výber funkcie podľa typu zdroja
# ==============================

def get_price(instance):
    print(f"🔁 Prepínam podľa typu: {instance.source_type}")
    if instance.source_type == "book":
        return get_book_price(instance.url)
    elif instance.source_type == "flat":
        return get_flat_price(instance.url)
    return "Neznáma položka", None


# ==============================
# 📚 Získanie ceny z Books to Scrape
# ==============================

def get_book_price(url):
    """
    Načítanie názvu a ceny knihy zo stránky Books to Scrape.
    """
    if not url:
        return "Neznáma položka", None

    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Chyba pri načítaní stránky: {e}")
        return "Neznáma položka", None

    soup = BeautifulSoup(response.text, "html.parser")

    # názov knihy
    name_tag = soup.select_one(".product_main h1")
    name = name_tag.text.strip() if name_tag else "Neznáma kniha"

    # cena knihy
    price_tag = soup.select_one(".product_main .price_color")
    if price_tag:
        price_text = price_tag.text.strip()
        try:
            price = float(price_text.replace("£", "").strip())
            GBP_TO_EUR = 1.1483612
            price = int(price * GBP_TO_EUR)
            price += random.choice([-5, 0, 5])
        except ValueError:
            print(f"⚠️ Nepodarilo sa spracovať cenu: {price_text}")
            price = None
    else:
        print("⚠️ Nenájdený element .price_color")
        price = None

    return name, price


# ==============================
# 🏠 Získanie ceny bytu z reality portálu
# ==============================

def get_flat_price(url):
    """
    Načítanie názvu a ceny bytu z reality stránky (napr. nehnutelnosti.sk).
    """
    if not url:
        return "Neznáma položka", None

    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Chyba pri načítaní stránky: {e}")
        return "Neznámy byt", None

    soup = BeautifulSoup(response.text, "html.parser")

    # názov bytu
    name = "Neznámy byt"
    name_tags = soup.select('h1[data-test-id="text"], h2[data-test-id="text"]')
    for tag in name_tags:
        text = tag.text.strip()
        if "byt" in text.lower() or "izbový" in text.lower():
            name = text
            break
    if name == "Neznámy byt":
        title_tag = soup.select_one("title")
        if title_tag:
            name = title_tag.text.strip()

    # cena bytu
    price = None
    price_tag = soup.select_one('[data-test-id="text"]')
    if price_tag:
        try:
            price_text = price_tag.text.strip().split(" ")[0]
            price_text = price_text.replace(".", "").replace(" ", "")
            price = int(price_text)
        except ValueError:
            print(f"⚠️ Nepodarilo sa spracovať cenu: {price_tag.text}")

    # fallback – hľadanie cez text
    if price is None:
        full_text = soup.get_text()
        match = re.search(r"(\d{1,3}(?:[.\s]?\d{3})*)\s*EUR", full_text)
        if match:
            try:
                price_text = match.group(1).replace(".", "").replace(" ", "")
                price = int(price_text)
                print(f"✅ Našiel som cenu cez text: {price} €")
            except ValueError:
                print(f"⚠️ Nepodarilo sa spracovať cenu: {match.group(0)}")
        else:
            print("⚠️ Cena sa nepodarila nájsť ani cez text")

    return name, price
