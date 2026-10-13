import pytest

from src.processing import filter_by_state, sort_by_date


# тестирование функции filter_by_state
# Фикстура для тестовых данных
@pytest.fixture
def dictionary_data():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Тестирование фильтрации по статусу
@pytest.mark.parametrize(
    "state, expected_result",
    [
        (
            "EXECUTED",
            [
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                },
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                },
            ],
        ),
        (
            "CANCELED",
            [
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                },
                {
                    "id": 615064591,
                    "state": "CANCELED",
                    "date": "2018-10-14T08:21:33.419441",
                },
            ],
        ),
        ("PENDING", []),  # Статус, которого нет в списке
    ],
)
def test_filter_by_state(dictionary_data, state, expected_result):
    result = filter_by_state(dictionary_data, state)
    assert result == expected_result


# тестирование функции sort_by_state
# Фикстура для тестовых данных
@pytest.fixture
def dictionary_data2():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Тестирование сортировки по датам
@pytest.mark.parametrize(
    "ascending, expected_result",
    [
        (
            True,
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                },
                {
                    "id": 615064591,
                    "state": "CANCELED",
                    "date": "2018-10-14T08:21:33.419441",
                },
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                },
            ],
        ),
        (
            False,
            [
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                },
                {
                    "id": 615064591,
                    "state": "CANCELED",
                    "date": "2018-10-14T08:21:33.419441",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                },
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                },
            ],
        ),
    ],
)
def test_sort_by_date(dictionary_data2, ascending, expected_result):
    result = sort_by_date(dictionary_data2, ascending)
    assert result == expected_result


# Фикстура для тестовых данных с одинаковыми датами
@pytest.fixture
def dictionary_data_same_date():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 3, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.mark.parametrize(
    "ascending, expected_result",
    [
        (
            True,
            [
                {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 3, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
        (
            False,
            [
                {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 2, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 3, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
    ],
)
def test_sort_by_date_same_dates(dictionary_data_same_date, ascending, expected_result):
    result = sort_by_date(dictionary_data_same_date, ascending)
    assert result == expected_result


# Тестирование сортировки с некорректными датами
@pytest.mark.parametrize(
    "invalid_data",
    [
        [{"id": 1, "state": "EXECUTED", "date": "not-a-date"}],
        [{"id": 2, "state": "CANCELED", "date": "1234-56-78"}],
    ],
)
def test_sort_by_date_invalid_dates(invalid_data):
    with pytest.raises(ValueError):
        sort_by_date(invalid_data, True)
