import logging
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Настраиваем логирование модуля
logger = logging.getLogger("external_api")
logger.setLevel(logging.DEBUG)

# Локальный кэш для хранения результатов конвертации (чтобы не стучаться в API для одинаковых сумм)
_conversion_cache: Dict[str, float] = {}


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Функция для возврата суммы транзакции в рублях, тип данных — float.
    Если транзакция была в USD или EUR, происходит обращение к внешнему
    API для получения текущего курса валют и конвертации суммы операции в рубли.
    Полный URL эндпоинта: https://apilayer.com
    """
    try:
        # Безопасное извлечение данных из вложенной структуры JSON банковской транзакции
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})

        currency_name = currency_info.get("name", "RUB")
        amount = float(operation_amount.get("amount", 0.0))
    except (KeyError, ValueError, TypeError):
        logger.error("Неверная или поврежденная структура транзакции при конвертации")
        return 0.0

    if currency_name == "RUB":
        return amount

    if currency_name in ["EUR", "USD"]:
        # Создаем уникальный ключ для кэша на основе валюты и суммы (например, "USD_150.0")
        cache_key = f"{currency_name}_{amount}"
        if cache_key in _conversion_cache:
            return _conversion_cache[cache_key]

        api_key = os.getenv("API_KEY")
        url = "https://api.apilayer.com/exchangerates_data/convert"

        params = {
            "amount": amount,
            "from": currency_name,
            "to": "RUB",
            "apikey": api_key,
        }

        try:
            # Делаем запрос к API exchangerates_data
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = round(float(data["result"]), 2)
                    # Сохраняем результат в кэш
                    _conversion_cache[cache_key] = result
                    logger.info(
                        f"Успешная конвертация {amount} {currency_name} ➔ "
                        f"{result} RUB через API"
                    )
                    return result
                else:
                    logger.error(
                        f"Флаг success=False от API при конвертации {currency_name}"
                    )
                    return 0.0
            else:
                logger.error(
                    f"Ошибка API exchangerates_data. Статус-код: {response.status_code}"
                )
                return 0.0
        except requests.RequestException as e:
            logger.error(f"Произошла сетевая ошибка при запросе к APILayer: {e}")
            return 0.0

    return 0.0
