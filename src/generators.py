from typing import Dict, Iterator, List


def filter_by_currency(transactions_list: List[Dict], currency: str) -> Iterator:
    """Функция возвращает итератор с транзакциями, соответствующими указанной валюте."""
    found = False
    for transaction in transactions_list:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            found = True
            yield transaction
    if not found:
        print("Валюта не найдена")


def generate_description(transactions_list: List[Dict]) -> Iterator[str]:
    """Функция возвращает итератор, который выдаёт описание каждой транзакции."""
    for transaction in transactions_list:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Функция генерирует номера карт в формате "XXXX XXXX XXXX XXXX" для чисел в заданном диапазоне."""
    for number in range(start, end + 1):
        card_number = f"{number:016d}"
        formatted_card_number = " ".join(
            [card_number[i:i + 4] for i in range(0, len(card_number), 4)]
        )
        yield formatted_card_number
