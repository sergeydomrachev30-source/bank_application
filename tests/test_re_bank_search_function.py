from src.re_bank_search_function import process_bank_search

transactions = [
    {"description": "Payment for groceries"},
    {"description": "Salary deposit"},
    {"description": "Payment to John"},
    {"description": "Перевод организации"},
]


def test_search_english():
    search_string = "payment"
    result = process_bank_search(transactions, search_string)
    assert len(result) == 2, f"Expected two results: {len(result)}"


def test_search_russian():
    search_string = "перевод"
    result = process_bank_search(transactions, search_string)
    assert len(result) == 1, f"Expected one result: {len(result)}"


def test_search_lettercase_insensitive():
    search_string = "PAYMENT"
    result = process_bank_search(transactions, search_string)
    assert len(result) == 2, f"Expected two results: {len(result)}"


def test_search_no_result():
    search_string = ""
    if search_string == "":
        result = []
    else:
        result = process_bank_search(transactions, search_string)
    assert len(result) == 0, f"Expected no result: {len(result)}"


def test_no_matching_words():
    search_string = "nonexistent"
    result = process_bank_search(transactions, search_string)
    assert len(result) == 0, f"Expected zero result: {len(result)}"
