from datetime import datetime
from typing import Dict, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список транзакций по заданному состоянию"""
    filtered_transactions = []
    for dictionary in transactions:
        if dictionary["state"] == state:
            filtered_transactions.append(dictionary)
    return filtered_transactions


def sort_by_date(transactions: List[Dict], ascending: bool = False) -> List[Dict]:
    """Сортирует список транзакций по дате"""
    for dictionary in transactions:
        try:
            datetime.fromisoformat(dictionary["date"])
        except ValueError:
            raise ValueError(f"Некорректный формат даты: '{dictionary['date']}'")
    return sorted(transactions, key=lambda x: x["date"], reverse=not ascending)
