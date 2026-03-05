from src.re_count_operations import count_operations_by_category

transactions = [
    {"description": "Payment for groceries"},
    {"description": "Salary deposit"},
    {"description": "Payment to John"},
    {"description": "Перевод организации"},
]

categories = ["Открытие вклада", "Перевод с карты на карту", "Перевод организации"]


def test_count_operations_by_category_english():
    result = count_operations_by_category(transactions, ["payment"])
    assert result.get("payment", 0) == 2, (
        f"Expected 2, but " f"got {result.get('payment', 0)}"
    )


def test_count_operations_by_category_russian():
    result = count_operations_by_category(transactions, ["перевод"])
    assert result.get("перевод", 0) == 1, (
        f"Expected 1, but " f"got {result.get("перевод", 0)}"
    )


def test_count_operations_no_match():
    result = count_operations_by_category(transactions, ["nonexistent"])
    assert result.get("nonexistent", 0) == 0, (
        f"Expected 1, but " f"got {result.get("nonexistent", 0)}"
    )
