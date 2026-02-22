from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def get_mask_account_card(info: str) -> str:
    """Функция маскирует номер карты или счета"""
    info_list = info.split()
    if info_list[0].lower() == "счет":
        return get_mask_account(info)
    else:
        return get_mask_card_number(info)


def get_date(iso_date: str) -> str:
    """Функция преобразует даты из формата ISO 8601 в формат ДД.ММ.ГГГГ"""
    try:
        date_obj = datetime.fromisoformat(iso_date)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError(f"Некорректный формат даты: '{iso_date}'")
