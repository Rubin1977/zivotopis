from unittest.mock import patch
from zivotopis.utils import get_price

class Dummy:
    def __init__(self, source_type, url="http://example.com"):
        self.source_type = source_type
        self.url = url

@patch("zivotopis.utils.get_book_price")
def test_get_price_book(mock_book):
    mock_book.return_value = ("Book", 10)
    instance = Dummy("book")
    assert get_price(instance) == ("Book", 10)

@patch("zivotopis.utils.get_flat_price")
def test_get_price_flat(mock_flat):
    mock_flat.return_value = ("Flat", 100000)
    instance = Dummy("flat")
    assert get_price(instance) == ("Flat", 100000)

def test_get_price_unknown():
    instance = Dummy("unknown")
    assert get_price(instance) == ("Neznáma položka", None)
