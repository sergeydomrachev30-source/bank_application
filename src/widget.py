from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def get_mask_account_card(info: str) -> str:
    """
    Функция маскирует номер карты или счета, сохраняя текстовое описание.
    Пример: 'Visa Platinum 7000792289606361' -> 'Visa Platinum 7000 79** **** 6361'
    """
    if not info or str(info).strip() == "":
        return "Пустая строка"

    if not isinstance(info, str):
        info = str(info)

    info_list = info.split()
    # Регистронезависимо проверяем первый элемент
    if info_list and info_list[0].lower() == "счет":
        return get_mask_account(info)
    else:
        try:
            return get_mask_card_number(info)
        except ValueError as e:
            # Возвращаем понятную строку-заглушку, чтобы бэкенд не падал при генерации JSON
            print(f"Ошибка маскирования: {e}. Данные: {info}")
            return "Некорректный формат"


def get_date(iso_date: str) -> str:
    """
    Преобразует даты из формата ISO 8601 (например, '2024-03-11T02:26:18')
    в строковый формат 'ДД.ММ.ГГГГ' по требованиям ТЗ.
    """
    if not iso_date or str(iso_date).strip() == "" or str(iso_date).lower() == "nan":
        return "Нет даты"

    # Шаг 1: Берем строго первый элемент списка строк после разделения по "T"
    try:
        clean_date = str(iso_date).split("T")[0]
        date_obj = datetime.strptime(clean_date, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except Exception:
        pass

    # Шаг 2: Если не вышло, пробуем встроенный fromisoformat в полном try-except
    try:
        date_obj = datetime.fromisoformat(str(iso_date))
        return date_obj.strftime("%d.%m.%Y")
    except Exception:
        # Полная защита: возвращаем строку вместо падения всего бэкенда и raise
        return "Некорректная дата"
