from collections import Counter
from typing import Any, Dict, List


def count_operations_by_category(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Принимает список словарей с данными о банковских операциях и список искомых категорий.
    Возвращает точное количество успешных операций в каждой категории.
    """
    if not categories:
        return {}

    # Приводим искомые категории к нижнему регистру для точного сравнения
    categories_lower = [str(cat).lower().strip() for cat in categories]
    category_mapping = {str(cat).lower().strip(): cat for cat in categories}

    categories_counter: Counter[str] = Counter()

    for transaction in transactions:
        # УЧИТЫВАЕМ РЕАЛЬНЫЙ КЛЮЧ ИЗ ТВОЕГО ФАЙЛА EXCEL: 'category_name'
        tx_category = (
            transaction.get("category_name")
            or transaction.get("category")
            or transaction.get("категория")
            or ""
        )

        # Игнорируем пустые ячейки (NaN / None)
        if (
            tx_category is None
            or str(tx_category).lower() == "nan"
            or str(tx_category).strip() == ""
        ):
            continue

        tx_category_str = str(tx_category).lower().strip()

        # Ищем совпадение категории
        for cat_low in categories_lower:
            if cat_low == tx_category_str or cat_low in tx_category_str:
                orig_name = category_mapping[cat_low]
                categories_counter[orig_name] += 1

    return dict(categories_counter)
