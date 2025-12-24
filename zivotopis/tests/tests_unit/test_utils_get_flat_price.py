from unittest.mock import patch, Mock
from zivotopis.utils import get_flat_price

@patch("zivotopis.utils.requests.get")
def test_get_flat_price_success(mock_get):
    html = """
    <h1 data-test-id="text">2-izbový byt</h1>
    <div data-test-id="text">150000 EUR</div>
    """
    mock_response = Mock()
    mock_response.text = html
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    name, price = get_flat_price("http://example.com")
    assert "byt" in name.lower()
    assert price == 150000

@patch("zivotopis.utils.requests.get")
def test_get_flat_price_error(mock_get):
    mock_get.side_effect = Exception("Network error")
    name, price = get_flat_price("http://example.com")
    assert name == "Neznámy byt"
    assert price is None
