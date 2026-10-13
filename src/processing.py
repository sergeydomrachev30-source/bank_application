import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

# Настраиваем логгер для модуля обработки данных
logger = logging.getLogger("processing")
logger.setLevel(logging.INFO)


def filter_by_state(
    transactions: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по заданному состоянию (Status / State).
    Поддерживает как английские, так и русские ключи из выгрузок банков.
    """
    filtered_transactions = []
    state_upper = str(state).upper().strip()

    for dictionary in transactions:
        # Извлекаем статус операции, поддерживая форматы JSON и Excel/CSV
        tx_state = (
            dictionary.get("state")
            or dictionary.get("статус")
            or dictionary.get("status")
        )

        if tx_state and str(tx_state).upper().strip() == state_upper:
            filtered_transactions.append(dictionary)

    return filtered_transactions


def _parse_any_date(date_val: Any) -> datetime:
    """Вспомогательная функция для безопасного парсинга дат разных форматов."""
    if not date_val or pd.isna(date_val) if "pd" in globals() else False:
        return datetime.min

    date_str = str(date_val).strip()

    # Пробуем формат ISO (YYYY-MM-DD...)
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass

    # Пробуем банковский формат Excel/CSV (DD.MM.YYYY...)
    for fmt in ("%d.%m.%Y %H:%M:%S", "%d.%m.%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Если формат совсем неизвестен, логируем и возвращаем минимальную дату
    logger.warning(f"Не удалось распознать формат даты: '{date_str}'")
    return datetime.min


def sort_by_date(
    transactions: List[Dict[str, Any]], ascending: bool = False
) -> List[Dict[str, Any]]:
    """
    Сортирует список транзакций по дате (по хронологии, а не по строковому алфавиту).
    Безопасно обрабатывает любые банковские форматы дат (ISO, dd.mm.yyyy).
    """
    # Сортируем список по реальным объектам datetime, полученным из функции фильтрации парсинга
    return sorted(
        transactions,
        key=lambda x: _parse_any_date(
            x.get("date") or x.get("дата операции") or x.get("дата платежа")
        ),
        reverse=not ascending,
    )
