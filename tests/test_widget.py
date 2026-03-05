import pytest

from src.widget import get_date, get_mask_account_card


# тесты для функции get_mask_account_card
# параметризованный тест для проверки корректного распознавания и маскировки
@pytest.mark.parametrize(
    "info, expected_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_get_mask_account_card(info, expected_result):
    result = get_mask_account_card(info)
    assert result == expected_result


# Тестирование на некорректные данные
@pytest.mark.parametrize(
    "info",
    [
        "Invalid Format",
        "111223534667587990",
        "some random string",
    ],
)
def test_get_mask_account_card_invalid(info):
    with pytest.raises(ValueError):
        get_mask_account_card(info)


# тесты для функции get_date
@pytest.mark.parametrize(
    "iso_date,expected_result",
    [
        ("2023-12-31", "31.12.2023"),
        ("2020-02-29", "29.02.2020"),
    ],
)
def test_get_date_standard(iso_date, expected_result):
    result = get_date(iso_date)
    assert result == expected_result


@pytest.mark.parametrize(
    "iso_date,expected_result",
    [("0001-01-01", "01.01.0001"), ("9999-12-31", "31.12.9999")],
)
def test_get_date_edge_cases(iso_date, expected_result):
    result = get_date(iso_date)
    assert result == expected_result


# Тесты для некорректных входных данных
@pytest.mark.parametrize("iso_date", ["", "not-a-date"])
def test_get_date_invalid(iso_date):
    with pytest.raises(ValueError):
        get_date(iso_date)
