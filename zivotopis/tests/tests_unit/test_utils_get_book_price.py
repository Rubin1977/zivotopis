from unittest.mock import patch, Mock
from zivotopis.utils import get_book_price

@patch("zivotopis.utils.requests.get")
def test_get_book_price_success(mock_get):
    html = """
    <div class="product_main">
        <h1>Test Book</h1>
        <p class="price_color">£10.00</p>
    </div>
    """
    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    name, price = get_book_price("http://example.com")
    assert name == "Test Book"
    assert isinstance(price, int)

@patch("zivotopis.utils.requests.get")
def test_get_book_price_error(mock_get):
    mock_get.side_effect = Exception("Network error")
    name, price = get_book_price("http://example.com")
    assert name == "Neznáma položka"
    assert price is None
