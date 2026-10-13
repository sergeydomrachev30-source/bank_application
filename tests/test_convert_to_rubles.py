from unittest.mock import patch

import requests

from src.external_api import convert_to_rubles


def test_convert_with_bad_status_code():
    with patch("external_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 404

        transaction = {
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        amount_in_rubles = convert_to_rubles(transaction)
        assert amount_in_rubles == 0.0


def test_convert_with_request_exception():
    with patch("external_api.requests.get", side_effect=requests.RequestException):
        transaction = {
            "operationAmount": {
                "amount": "1.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        amount_in_rubles = convert_to_rubles(transaction)
        assert amount_in_rubles == 0.0


def test_convert_rub_currency():
    """Тест: если валюта операции RUB, функция сразу возвращает сумму без запросов к API."""
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"name": "RUB", "code": "RUB"},
        }
    }
    assert convert_to_rubles(transaction) == 1500.50


def test_convert_invalid_structure():
    """Тест устойчивости: если структура транзакции повреждена
    (KeyError/TypeError), возвращается 0.0."""
    # Передаем пустой словарь без нужных ключей
    assert convert_to_rubles({}) == 0.0
    # Передаем некорректный тип данных суммы
    bad_transaction = {"operationAmount": {"amount": None, "currency": {"name": "USD"}}}
    assert convert_to_rubles(bad_transaction) == 0.0
