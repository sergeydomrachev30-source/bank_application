import csv
import json
import os
import re

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


def process_bank_search(transactions: list[dict], search_string: str) -> list[dict]:
    """ функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка."""
    pattern = re.compile(search_string, re.IGNORECASE)
    result = [
        transaction
        for transaction in transactions
        if pattern.search(str(transaction.get("description", "")))
    ]

    return result


base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "transactions.csv")
csv_data = read_csv(csv_path)
excel_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")
excel_data = read_excel(excel_path)
json_path = os.path.join(base_dir, "data", "transactions.json")
json_data = read_json(json_path)
