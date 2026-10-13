from unittest.mock import mock_open, patch

import pandas as pd

from src.read_transactions_from_excel_and_csv import read_file


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_read_excel_file(mock_read_excel, mock_exists):
    """Тест успешного чтения Excel-файла через подмену DataFrame."""
    mock_exists.return_value = True

    # Передаем данные списком словарей, обходя любые фильтры разметки чата
    mock_records = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 1.0,
            "currency_name": "Sol",
            "currency_code": "SOL",
            "from": "Alice",
            "to": "Bob",
            "description": "Перевод организации",
        }
    ]
    mock_read_excel.return_value = pd.DataFrame.from_records(mock_records)

    result = read_file("transactions_excel.xlsx")
    assert result == mock_records


@patch("os.path.exists")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=(
        "id,state,date,amount,currency_name,currency_code,from,to,description\n"
        "1,EXECUTED,2023-09-05T11:30:32Z,1.0,Sol,SOL,Alice,Bob,Перевод организации"
    ),
)
def test_read_csv_file(mock_file, mock_exists):
    """Тест успешного чтения CSV-файла через mock_open."""
    mock_exists.return_value = True

    expected_result = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 1.0,
            "currency_name": "Sol",
            "currency_code": "SOL",
            "from": "Alice",
            "to": "Bob",
            "description": "Перевод организации",
        }
    ]

    result = read_file("transactions.csv")
    assert result == expected_result
