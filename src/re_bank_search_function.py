import csv
import json
import logging
import os
import re
from typing import Any, Dict, Hashable, List

import pandas as pd

logger = logging.getLogger("bank_search")


def read_json(path: str) -> List[Dict[str, Any]]:
    """Функция для считывания файлов в формате JSON."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def read_csv(path: str) -> List[Dict[str, Any]]:
    """Функция для считывания файлов в формате CSV."""
    if not os.path.exists(path):
        return []
    transactions = []
    try:
        with open(path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                transactions.append(row)
            # Если разделитель ; не подошёл и считалась одна колонка, пробуем запятую
            if transactions and len(transactions[0].keys()) <= 1:
                csvfile.seek(0)
                reader = csv.DictReader(csvfile, delimiter=",")
                transactions = [row for row in reader]
    except Exception:
        pass
    return transactions


def read_excel(path: str) -> list[Any] | list[dict[Hashable, Any]]:
    """Функция для считывания файлов в формате Excel."""
    if not os.path.exists(path):
        return []
    try:
        df = pd.read_excel(path)
        # Очищаем ячейки NaN для совместимости
        df_clean = df.where(pd.notnull(df), None)
        return df_clean.to_dict(orient="records")
    except Exception:
        return []


def process_bank_search(
    transactions: List[Dict[str, Any]], search_string: str
) -> List[Dict[str, Any]]:
    """Выполняет регистронезависимый поиск по подстроке в описании или категории."""
    if not search_string or search_string.strip() == "":
        return transactions

    pattern = re.compile(re.escape(search_string.strip()), re.IGNORECASE)
    result = []

    for transaction in transactions:
        description = (
            transaction.get("description") or transaction.get("описание") or ""
        )
        category = (
            transaction.get("category_name")
            or transaction.get("category")
            or transaction.get("категория")
            or ""
        )

        if pattern.search(str(description)) or pattern.search(str(category)):
            result.append(transaction)

    return result
