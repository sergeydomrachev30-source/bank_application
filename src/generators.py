import logging
from typing import Any, Dict, Iterator, List

# Настраиваем логгер для модуля генераторов
logger = logging.getLogger("generators")
logger.setLevel(logging.INFO)


def filter_by_currency(
        transactions_list: List[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """
    Функция возвращает память-сберегающий итератор с транзакциями, соответствующими указанной валюте.
    Поддерживает как структуру JSON (operationAmount -> currency -> code),
    так и выгрузку Excel (Валюта операции).
    """
    currency_upper = str(currency).upper().strip()
    found = False

    for transaction in transactions_list:
        # 1. Проверяем формат JSON структуры
        op_amount = transaction.get("operationAmount")
        if isinstance(op_amount, dict):
            currency_info = op_amount.get("currency", {})
            tx_currency = currency_info.get("code") or currency_info.get("name")
        else:
            # 2. Если формат плоский (CSV/Excel), ищем русские и английские ключи
            tx_currency = (
                    transaction.get("валюта операции")
                    or transaction.get("валюта платежа")
                    or transaction.get("currency")
            )

        # Сравниваем валюту в верхнем регистре
        if tx_currency and str(tx_currency).upper().strip() == currency_upper:
            found = True
            yield transaction

    if not found:
        logger.warning(
            f"Транзакции с валютой {currency_upper} не найдены в предоставленном списке."
        )


def generate_description(transactions_list: List[Dict[str, Any]]) -> Iterator[str]:
    """Функция возвращает итератор, который безопасно выдаёт описание каждой транзакции (JSON/Excel)."""
    for transaction in transactions_list:
        # Поддерживаем оба языка для ключей описания
        description = (
                transaction.get("description")
                or transaction.get("описание")
                or "Без описания"
        )

        # Защита от NaN ячеек Pandas
        if description is None or str(description).lower() == "nan":
            description = "Без описания"

        yield str(description)


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Функция генерирует номера карт в формате 'XXXX XXXX XXXX XXXX' для чисел в заданном диапазоне."""
    for number in range(start, end + 1):
        # Добиваем число нулями слева до 16 знаков
        card_number = f"{number:016d}"
        # Нарезаем по 4 символа и склеиваем через пробел
        formatted_card_number = " ".join(
            [card_number[i: i + 4] for i in range(0, len(card_number), 4)]
        )
        yield formatted_card_number
