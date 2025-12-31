from zivotopis.utils import detect_source_type

def test_detect_source_type_empty():
    assert detect_source_type("") == "flat"

def test_detect_source_type_books():
    assert detect_source_type("https://books.toscrape.com/catalogue/") == "book"

def test_detect_source_type_flat_keywords():
    assert detect_source_type("https://www.nehnutelnosti.sk/byt-2-izbovy/") == "flat"

def test_detect_source_type_unknown():
    assert detect_source_type("https://example.com") == "flat"
