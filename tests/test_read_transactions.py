from unittest.mock import mock_open, patch

from src.utils import get_currency_rates, read_transactions


def test_read_transactions_success():
    """Тест успешного чтения транзакций."""
    mock_data = '[{"id": 1, "amount": "100.00", "currency": "USD"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        transactions = read_transactions("dummy_path.json")
        assert len(transactions) == 1
        assert transactions[0]["id"] == 1


def test_read_transactions_file_not_found():
    """Тест на случай, когда файл не найден."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        transactions = read_transactions("dummy_path.json")
        assert transactions == []


@patch("utils.requests.get")
def test_get_currency_rates_success(mock_get):
    """Тест успешного получения курсов валют через API."""
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.50}}

    result = get_currency_rates(["USD"])
    assert result == [{"currency": "USD", "rate": 75.50}]


@patch("utils.requests.get")
def test_get_currency_rates_error(mock_get):
    """Тест устойчивости: возврат дефолта при ошибке API валют."""
    mock_get.return_value.status_code = 500

    result = get_currency_rates(["USD"])
    assert result == [{"currency": "USD", "rate": 73.21}]
