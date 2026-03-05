from unittest.mock import patch

from src.external_api import convert_to_rubles


# Тест конвертации USD в рубли
def test_convert_usd_to_rubles():
    mock_response = {"success": True, "result": 74.0}

    with patch("src.external_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200  # Добавляем успешный статус код
        mock_get.return_value.json.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        amount_in_rubles = convert_to_rubles(transaction)
        assert amount_in_rubles == 74.0, "Test failed: Expected 74.0 for USD conversion"


# Тест конвертации рублей в рубли
def test_convert_rub_to_rubles():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "RUB", "code": "RUB"},
        }
    }

    amount_in_rubles = convert_to_rubles(transaction)
    assert amount_in_rubles == 100.0, "Test failed: Expected 100.0 for RUB conversion"


# Тест для неуспешного статус кода
def test_convert_with_bad_status_code():
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 404  # Неуспешный статус код
        mock_get.return_value.json.return_value = {"success": False}

        transaction = {
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        amount_in_rubles = convert_to_rubles(transaction)
        assert amount_in_rubles == 0.0, "Test failed: Expected 0.0 for bad status code"


# Тест для обработки исключения
def test_convert_with_request_exception():
    import requests

    with patch("src.external_api.requests.get", side_effect=requests.RequestException):
        transaction = {
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        amount_in_rubles = convert_to_rubles(transaction)
        assert (
            amount_in_rubles == 0.0
        ), "Test failed: Expected 0.0 for request exception"


# Тест для неподдерживаемой валюты
def test_convert_with_unsupported_currency():
    transaction = {
        "operationAmount": {
            "amount": "1.00",
            "currency": {"name": "XYZ", "code": "XYZ"},  # Неподдерживаемая валюта
        }
    }

    amount_in_rubles = convert_to_rubles(transaction)
    assert amount_in_rubles == 0.0, "Test failed: Expected 0.0 for unsupported currency"
