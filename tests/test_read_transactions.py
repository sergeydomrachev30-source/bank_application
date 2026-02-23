from unittest.mock import mock_open, patch

from src.utils import read_transactions


# Тест успешного чтения транзакций
def test_read_transactions_success():
    mock_data = '[{"id": 1, "amount": "100.00", "currency": "USD"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        transactions = read_transactions("dummy_path.json")
        assert len(transactions) == 1, "Тест не пройден: ожидается 1 транзакция"
        assert (
            transactions[0]["id"] == 1
        ), "Тест не пройден: ожидается, что ID транзакции будет 1"


# Тест на случай, когда файл не найден
def test_read_transactions_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        transactions = read_transactions("dummy_path.json")
        assert (
            transactions == []
        ), "Test failed: Expected empty list when file not found"


# Тест на случай неправильного JSON
def test_read_transactions_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        transactions = read_transactions("dummy_path.json")
        assert transactions == [], "Test failed: Expected empty list for invalid JSON"
