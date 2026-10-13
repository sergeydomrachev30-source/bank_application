import csv
import json
import os


def csv_to_json(csv_file_path, json_file_path):
    """функция для преобразования файла в формате csv в файл формата json"""
    with open(csv_file_path, newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        data = [row for row in csv_reader]

    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


base_dir = os.path.dirname(os.path.dirname(__file__))
csv_path = os.path.join(base_dir, "data", "transactions.csv")
json_path = os.path.join(base_dir, "data", "transactions.json")

csv_to_json(csv_path, json_path)
