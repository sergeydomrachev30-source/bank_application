import json


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
            except json.decoder.JSONDecodeError:
                print("Ошибка при чтении файла")
    except FileNotFoundError:
        print("Файл не обнаружен")
    if isinstance(transactions_info, list):
        return transactions_info
    return []


path = r"C:\Users\serik\PycharmProjects\FunctionsToMaskBankTransactions\data\operations.json"
transactions = read_transactions(path)
print(transactions)
