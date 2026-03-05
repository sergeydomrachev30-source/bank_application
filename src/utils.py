import json
import logging
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("logs/transactions.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
utils_logger.addHandler(handler)


def read_transactions(pathway):
    """функция принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых
    транзакциях. Если файл пустой, содержит не список
    или не найден, функция возвращает пустой список"""
    transactions_info = []
    try:
        with open(pathway, "r", encoding="utf-8") as file:
            try:
                transactions_info = json.load(file)
                utils_logger.info("Файл успешно прочитан")
            except json.decoder.JSONDecodeError:
                utils_logger.error("Ошибка при чтении файла")
                print("Ошибка при чтении файла")
    except FileNotFoundError:
        utils_logger.error("Файл не обнаружен")
    if isinstance(transactions_info, list):
        return transactions_info
    return []


base_dir = os.path.dirname(os.path.dirname(__file__))  # Поднимаемся на уровень выше
path = os.path.join(base_dir, "data", "operations.json")

transactions = read_transactions(path)
print(transactions)
