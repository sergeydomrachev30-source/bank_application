from unittest.mock import mock_open, patch

import pandas as pd

from src.re_bank_search_function import (
    process_bank_search,
    read_csv,
    read_excel,
    read_json,
)


def test_process_bank_search_success():
    """Тест базового поиска по описанию и категории."""
    transactions = [
        {"description": "Покупка в Магните", "category_name": "Supermarkets"},
        {"description": "Перевод другу", "category_name": "Transfer"},
    ]
    result = process_bank_search(transactions, "магнит")
    assert len(result) == 1


@patch("os.path.exists")
def test_read_json_file_not_found(mock_exists):
    mock_exists.return_value = False
    assert read_json("ghost.json") == []


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
def test_read_json_success(mock_file, mock_exists):
    mock_exists.return_value = True
    assert read_json("real.json") == [{"id": 1}]


@patch("os.path.exists")
def test_read_csv_file_not_found(mock_exists):
    mock_exists.return_value = False
    assert read_csv("ghost.csv") == []


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="id;state\n1;OK")
def test_read_csv_success(mock_file, mock_exists):
    mock_exists.return_value = True
    assert len(read_csv("real.csv")) == 1


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_read_excel_success(mock_read_excel, mock_exists):
    mock_exists.return_value = True
    mock_read_excel.return_value = pd.DataFrame([{"id": 1}])
    result = read_excel("real.xlsx")
    assert len(result) == 1


@patch("os.path.exists")
@patch("pandas.read_excel", side_effect=Exception("Excel error"))
def test_read_excel_exception(mock_read_excel, mock_exists):
    mock_exists.return_value = True
    assert read_excel("corrupted.xlsx") == []
