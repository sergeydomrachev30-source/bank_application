from unittest.mock import mock_open, patch

from src.csv_to_json import csv_to_json


@patch("os.path.exists")
def test_csv_to_json_file_not_found(mock_exists):
    """Проверяем, что функция корректно завершается, если исходный файл отсутствует."""
    mock_exists.return_value = False
    # Функция не должна падать, она просто залогирует ошибку и выйдет
    assert csv_to_json("nonexistent.csv", "output.json") is None


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="id,state,amount\n1,OK,100")
@patch("json.dump")
def test_csv_to_json_success(mock_json_dump, mock_file, mock_exists):
    """Проверяем успешную конвертацию валидного CSV в формат JSON."""
    mock_exists.return_value = True

    csv_to_json("data/transactions.csv", "data/transactions.json")

    # Проверяем, что файлы открывались и на чтение, и на запись
    mock_file.assert_any_call("data/transactions.csv", newline="", encoding="utf-8")
    mock_file.assert_any_call("data/transactions.json", mode="w", encoding="utf-8")

    # Проверяем, что json.dump был вызван для записи данных
    mock_json_dump.assert_called_once()
