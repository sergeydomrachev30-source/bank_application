import os
from typing import Any, Dict, Hashable, List

import pandas as pd


def read_file(file_path: str) -> List[Dict[Hashable, Any]]:
    """функция для считывания csv и xslx файлов"""
    if file_path.endswith(".csv"):
        data = pd.read_csv(file_path, sep=";")
    elif file_path.endswith(".xlsx"):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Формат файла не поддерживается: " + file_path)

    return data.to_dict(orient="records")


base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "transactions.csv")
excel_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")
csv_data = read_file(csv_path)
excel_data = read_file(excel_path)
print(csv_data)
print(excel_data)
