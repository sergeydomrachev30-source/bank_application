import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            generate_description)


@pytest.fixture
def sample_transactions():
    return [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
    ]


@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 1),
        ("EUR", 1),
        ("RUB", 1),
        ("JPY", 0),
    ],
)
def test_filter_by_correct_currency(sample_transactions, currency, expected_count):
    result = list(filter_by_currency(sample_transactions, currency))
    assert len(result) == expected_count


# Фикстура для пустого списка
@pytest.fixture
def empty_transactions():
    return []


# Тест для пустого списка
@pytest.mark.parametrize("currency", ["USD", "EUR", "JPY"])
def test_filter_by_empty_list(currency, empty_transactions):
    result = list(filter_by_currency(empty_transactions, currency))
    assert len(result) == 0


@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        (
            [
                {"description": "Перевод организации"},
                {"description": "Перевод со счета на счет"},
                {"description": "Перевод с карты на карту"},
            ],
            [
                "Перевод организации",
                "Перевод со счета на счет",
                "Перевод с карты на карту",
            ],
        ),
        ([], []),
    ],
)
def test_generate_description(transactions, expected_descriptions):
    result = list(generate_description(transactions))
    assert result == expected_descriptions


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (9999_9999_9999_9999, 9999_9999_9999_9999, ["9999 9999 9999 9999"]),
    ],
)
def test_card_number_generation(start, end, expected):
    generator = card_number_generator(start, end)
    result = list(generator)
    assert result == expected


@pytest.mark.parametrize(
    "number, formatted",
    [
        (1, "0000 0000 0000 0001"),
        (1234_5678_9123_4567, "1234 5678 9123 4567"),
        (9999_9999_9999_9999, "9999 9999 9999 9999"),
    ],
)
def test_card_formatting(number, formatted):
    generator = card_number_generator(number, number)
    result = next(generator)
    assert result == formatted


@pytest.mark.parametrize(
    "start, end", [(0, 0), (9999_9999_9999_9999, 9999_9999_9999_9999)]
)
def test_edge_cases(start, end):
    generator = card_number_generator(start, end)
    result = list(generator)
    assert len(result) == (end - start + 1)
    if start == end:
        formatted_number = f"{start:016d}"
        expected = " ".join(
            [formatted_number[i:i + 4] for i in range(0, len(formatted_number), 4)]
        )
        assert result[0] == expected
