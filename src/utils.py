import json
import logging

import requests

# Настраиваем логгер модуля utils
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("logs/transactions.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
utils_logger.addHandler(handler)


def read_transactions(pathway: str) -> list:
    """
    Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях. Если файл пустой, содержит
    не список или не найден, функция возвращает пустой список.
    """
    transactions_info = []
    try:
        with open(pathway, "r", encoding="utf-8") as file:
            try:
                transactions_info = json.load(file)
                utils_logger.info("Файл успешно прочитан")
            except json.decoder.JSONDecodeError:
                utils_logger.error("Ошибка при чтении файла")
    except FileNotFoundError:
        utils_logger.error("Файл не обнаружен")

    if isinstance(transactions_info, list):
        return transactions_info
    return []


def get_currency_rates(currencies: list) -> list:
    """Получает текущие курсы валют к RUB через внешнее API (requests)."""
    rates = []
    for currency in currencies:
        try:
            url = f"https://er-api.com{currency}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                rub_rate = data.get("rates", {}).get("RUB", 1.0)
                rates.append({"currency": currency, "rate": float(rub_rate)})
            else:
                raise requests.RequestException()
        except Exception as e:
            utils_logger.warning(
                f"Ошибка API валют для {currency}, применен дефолт. Ошибка: {e}"
            )
            rates.append(
                {"currency": currency, "rate": 73.21 if currency == "USD" else 87.08}
            )
    return rates
