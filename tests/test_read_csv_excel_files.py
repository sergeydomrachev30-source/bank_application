from unittest.mock import mock_open, patch

import pandas as pd

from src.read_transactions_from_excel_and_csv import read_file


@patch("pandas.read_excel")
def test_read_excel_file(mock_read_excel):
    mock_data = pd.DataFrame(
        {
            "id": [650703],
            "state": ["EXECUTED"],
            "date": ["2023-09-05T11:30:32Z"],
            "amount": [16210],
            "currency_name": ["Sol"],
            "currency_code": ["SOL"],
            "from": ["Alice"],
            "to": ["Bob"],
            "description": ["Перевод организации"],
        }
    )
    mock_read_excel.return_value = mock_data

    expected_result = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "SOL",
            "from": "Alice",
            "to": "Bob",
            "description": "Перевод организации",
        }
    ]
    result = read_file("transactions_excel.xlsx")
    assert result == expected_result


# Тест для чтения CSV файла
@patch(
    "builtins.open",
    mock_open(
        read_data="id;state;date;amount;currency_name;currency_code;"
        "from;to;description\n650703;EXECUTED;"
        "2023-09-05T11:30:32Z;16210;Sol;SOL;Alice;"
        "Bob;Перевод организации"
    ),
)
def test_read_csv_file():
    expected_result = [
        {
            "id": 650703,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "SOL",
            "from": "Alice",
            "to": "Bob",
            "description": "Перевод организации",
        }
    ]
    result = read_file("transactions.csv")
    assert result == expected_result
