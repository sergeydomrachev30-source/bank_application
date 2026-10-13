from src.re_count_operations import count_operations_by_category

transactions = [
    {"category_name": "Supermarkets", "description": "Groceries purchase"},
    {"category_name": "Supermarkets", "description": "Shop weekly buy"},
    {"category_name": "Transfer", "description": "Payment to John"},
    {"category_name": "Перевод организации", "description": "Оплата счета"},
]


def test_count_operations_by_category_english():
    """Тест: подсчет англоязычных категорий расходов по подстроке."""
    result = count_operations_by_category(transactions, ["Supermarkets"])
    assert (
        result.get("Supermarkets", 0) == 2
    ), f"Expected 2, but got {result.get('Supermarkets', 0)}"


def test_count_operations_by_category_russian():
    """Тест: подсчет кириллических категорий расходов."""
    result = count_operations_by_category(transactions, ["Перевод организации"])
    assert (
        result.get("Перевод организации", 0) == 1
    ), f"Expected 1, but got {result.get('Перевод организации', 0)}"


def test_count_operations_no_match():
    """Тест: поведение счетчика при отсутствии совпадений категорий."""
    result = count_operations_by_category(transactions, ["NonexistentCategory"])
    # Метод count_operations_by_category возвращает словарь, где отсутствующие ключи не создаются
    assert "NonexistentCategory" not in result
    assert result.get("NonexistentCategory", 0) == 0
