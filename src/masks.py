import logging

# Настраиваем логгер для модуля маскирования
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("logs/masks.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
masks_logger.addHandler(handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция выводит номер кредитной карты в замаскированном виде."""
    if not card_number or card_number.strip() == "":
        masks_logger.warning("Пустая строка передана в get_mask_card_number")
        return ""

    index_of_first_digit = -1
    index = 0
    for char in card_number:
        if char.isdigit():
            index_of_first_digit = index
            break
        index += 1

    if index_of_first_digit == -1:
        masks_logger.error("Неизвестный формат: строка не содержит чисел")
        raise ValueError("Неизвестный формат: строка не содержит чисел")

    # Проверка длины числовой части
    numeric_part = card_number[index_of_first_digit:].replace(" ", "")
    if len(numeric_part) != 16:
        masks_logger.error("Некорректная длина числовой части карты")
        raise ValueError("Некорректная длина числовой части карты")

    masked_number = (
        f"{card_number[:index_of_first_digit]}"
        f"{card_number[index_of_first_digit:index_of_first_digit + 4]} "
        f"{card_number[index_of_first_digit + 4:index_of_first_digit + 6]}** **** "
        f"{card_number[-4:]}"
    )
    masks_logger.info("Карта успешно замаскирована")
    return masked_number


def get_mask_account(account_number: str) -> str:
    """Функция выводит счет в замаскированном виде, включая префикс типа 'Счет'."""
    if not account_number or account_number.strip() == "":
        masks_logger.warning("Пустая строка передана в get_mask_account")
        return ""

    index_of_first_digit = -1
    index = 0
    for char in account_number:
        if char.isdigit():
            index_of_first_digit = index
            break
        index += 1

    if index_of_first_digit == -1:
        masks_logger.error("Неизвестный формат: строка не содержит чисел")
        raise ValueError("Неизвестный формат: строка не содержит чисел")

    numeric_part = account_number[index_of_first_digit:].replace(" ", "")
    if len(numeric_part) != 20:
        masks_logger.error("Некорректная длина числовой части счета")
        raise ValueError("Некорректная длина числовой части счета")

    # Безопасно извлекаем префикс. Если чисел в начале нет, префикс пустой
    prefix = account_number[:index_of_first_digit].strip()
    prefix_str = f"{prefix} " if prefix else ""

    masked_account = f"{prefix_str}**{account_number[-4:]}"
    masks_logger.info("Счет успешно замаскирован")
    return masked_account
