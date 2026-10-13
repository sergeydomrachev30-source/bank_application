import pytest

from src.masks import get_mask_account, get_mask_card_number


# тесты для функции get_mask_card_number
@pytest.fixture()
def single_card_number():
    return "Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"


def test_get_mask_card_number_with_fixture(single_card_number):
    card_number, expected_result = single_card_number
    result = get_mask_card_number(card_number)
    assert result == expected_result


# Параметризованный тест с другими наборами данных
@pytest.mark.parametrize(
    "card_number, expected_result",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("", ""),
    ],
)
def test_get_mask_card_number_with_parametrize(card_number, expected_result):
    result = get_mask_card_number(card_number)
    assert result == expected_result


@pytest.mark.parametrize("card_number", ["Invalid Format"])
def test_get_mask_card_number_invalid(card_number):
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "card_number",
    [
        "Short 123",  # Нестандартная короткая длина номера
        "Extra Long 12345678901234567890",  # Нестандартная длинная длина номера
    ],
)
def test_get_mask_card_number_non_standard_lengths(card_number):
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


# тесты для функции get_mask_account


@pytest.mark.parametrize(
    "account_number, expected_result",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("", ""),
    ],
)
def test_get_mask_account(account_number, expected_result):
    result = get_mask_account(account_number)
    assert result == expected_result


@pytest.mark.parametrize("account_number", ["Invalid Format"])
def test_get_mask_account_invalid(account_number):
    with pytest.raises(ValueError):
        get_mask_account(account_number)


@pytest.mark.parametrize(
    "account_number",
    [
        "Short 123",  # Нестандартная короткая длина номера
        "Extra Long 123456789012345678905678",  # Нестандартная длинная длина номера
    ],
)
def test_get_mask_account_non_standard_lengths(account_number):
    with pytest.raises(ValueError):
        get_mask_account(account_number)
