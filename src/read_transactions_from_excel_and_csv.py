# src/read_transactions_from_excel_and_csv.py
import os

import pandas as pd


def read_file(file_path: str) -> list:
    """Функция для считывания csv и xlsx файлов с очисткой названий колонок."""
    if not os.path.exists(file_path):
        return []

    if file_path.endswith(".csv"):
        try:
            data = pd.read_csv(file_path, sep=",")
            if len(data.columns) <= 1:
                data = pd.read_csv(file_path, sep=";")
        except Exception:
            data = pd.read_csv(file_path, sep=";")
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Формат файла не поддерживается")

    # Переводим колонки в нижний регистр и очищаем от скрытых пробелов
    data.columns = [str(col).strip().lower() for col in data.columns]

    # Заменяем NaN на None для безопасной работы с JSON/циклами
    data_clean = data.where(pd.notnull(data), None)
    return data_clean.to_dict(orient="records")
