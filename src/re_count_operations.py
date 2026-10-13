import csv
import json
import os
from collections import Counter

import pandas as pd


def read_json(path: str) -> list[dict]:
    """функция для считывания файлов в формате json"""
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data


def read_csv(path: str) -> list[dict]:
    """функция для считывания файлов в формате csv"""
    transactions = []
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            transactions.append(row)
    return transactions


def read_excel(path: str) -> list[dict]:
    """функция для считывания файлов в формате excel"""
    df = pd.read_excel(path)
    return df.to_dict(orient="records")


def count_operations_by_category(
    transactions: list[dict], categories: list[str]
) -> dict[str, int]:
    """функция принимает список словарей с данными о банковских операциях
    и список категорий операций, а возвращает словарь, в котором ключи —
    это названия категорий, а значения — это количество операций в каждой категории."""
    categories_counter: Counter[str] = Counter()
    for transaction in transactions:
        description = str(transaction.get("description")).lower()
        for category in categories:
            if category.lower() in description:
                categories_counter[category] += 1
    return dict(categories_counter)


base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "transactions.csv")
csv_data = read_csv(csv_path)
excel_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")
excel_data = read_excel(excel_path)
json_path = os.path.join(base_dir, "data", "transactions.json")
json_data = read_json(json_path)
