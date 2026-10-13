from src.processing import filter_by_state, sort_by_date


def test_sort_by_date_invalid_dates():
    """Тест проверяет, что битые даты не ломают скрипт, а корректно обрабатываются."""
    invalid_data = [
        {"id": 1, "state": "EXECUTED", "date": "not-a-date"},
        {"id": 2, "state": "EXECUTED", "date": "2023-05-10"},
    ]

    # Скрипт не должен выбрасывать ValueError, он должен вернуть отсортированный список
    result = sort_by_date(invalid_data, ascending=True)

    # Транзакция с битой датой получила datetime.min и встала на первое место при возрастании
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_filter_by_state_canceled():
    """Тест фильтрации транзакций по статусу CANCELED."""
    data = [
        {"статус": "CANCELED", "описание": "Отмена"},
        {"статус": "EXECUTED", "описание": "Успех"},
    ]
    result = filter_by_state(data, state="CANCELED")
    assert len(result) == 1
    assert result[0]["описание"] == "Отмена"


def test_sort_by_date_bank_format():
    """Тест точной сортировки дат в банковском формате dd.mm.yyyy."""
    data = [
        {"дата операции": "01.01.2021 12:00:00", "id": 1},
        {"дата операции": "31.12.2021 16:44:00", "id": 2},
    ]
    # Сортируем по убыванию дат (самая свежая должна быть первой)
    result = sort_by_date(data, ascending=False)
    assert result[0]["id"] == 2
