def get_mask_card_number(card_number: str) -> str:
    """Функция выводит номер кредитной карты в замаскированном виде"""
    if card_number.strip() == "":
        return ""
    index_of_first_digit = -1
    index = 0
    for char in card_number:
        if char.isdigit():
            index_of_first_digit = index  # Используем текущий индекс
            break
        index += 1
    if index_of_first_digit == -1:
        raise ValueError("Неизвестный формат: строка не содержит чисел")
    # Проверка длины числовой части
    numeric_part = card_number[index_of_first_digit:].replace(" ", "")
    if len(numeric_part) != 16:
        raise ValueError("Некорректная длина числовой части")
    masked_number = (
        f"{card_number[:index_of_first_digit]}"
        f"{card_number[index_of_first_digit:index_of_first_digit + 4]} "
        f"{card_number[index_of_first_digit + 4:index_of_first_digit + 6]}** **** "
        f"{card_number[-4:]}"
    )

    return masked_number


def get_mask_account(account_number: str) -> str:
    """Функция выводит счет в замаскированном виде, включая слово Счет"""
    if account_number.strip() == "":
        return ""
    index_of_first_digit = -1
    for char in account_number:
        if char.isdigit():
            index_of_first_digit = account_number.index(char)
            break
    if index_of_first_digit == -1:
        raise ValueError("Неизвестный формат: строка не содержит чисел")
    numeric_part = account_number[index_of_first_digit:].replace(" ", "")
    if len(numeric_part) != 20:
        raise ValueError("Некорректная длина числовой части")
    return f"{account_number[:index_of_first_digit - 1]} **{account_number[-4:]}"
