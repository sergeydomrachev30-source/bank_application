import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rubles(transaction: Dict) -> float:
    """функция для возврата суммы транзакции в рублях, тип данных —
    float. Если транзакция была в USD или EUR, происходит обращение к внешнему
    API для получения текущего курса валют и конвертации суммы операции в рубли."""
    currency_name = transaction["operationAmount"]["currency"]["name"]
    amount = float(transaction["operationAmount"]["amount"])

    if currency_name == "RUB":
        return amount

    elif currency_name == "EUR" or currency_name == "USD":
        api_key = os.getenv("API_KEY")
        url = "https://api.apilayer.com/exchangerates_data/convert"

        params = {
            "amount": amount,
            "from": currency_name,
            "to": "RUB",
            "apikey": api_key,
        }

        # Запрос к API для получения курса валют
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return round(float(data["result"]), 2)
                else:
                    print("Ошибка при конвертации валюты")
                    return 0.0
            else:
                print(f"Ошибка API: {response.status_code}")
                return 0.0
        except requests.RequestException as e:
            print(f"Произошла ошибка при запросе: {e}")
            return 0.0
    return 0.0
