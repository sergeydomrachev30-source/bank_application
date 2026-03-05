import os

from processing import filter_by_state
from src.re_bank_search_function import (process_bank_search, read_csv,
                                         read_excel, read_json)
from src.re_count_operations import count_operations_by_category
from widget import get_mask_account_card


def main():
    """функция отвечает за основную логику проекта и связывает функциональности между собой."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "data", "transactions.csv")
    excel_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")
    json_path = os.path.join(base_dir, "data", "transactions.json")

    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("Укажите нужную цифру: ")

        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            transactions = read_json(json_path)
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            transactions = read_csv(csv_path)
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            transactions = read_excel(excel_path)
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        status = input(
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING: "
        ).upper()
        if status in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            filtered_transactions = filter_by_state(transactions, status)
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    if not filtered_transactions:
        print(
            "Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        )
        return

    if input("Отсортировать операции по дате? Да/Нет: ").lower() == "да":
        sort_order = input("Отсортировать по возрастанию или по убыванию?: ").lower()
        reverse = sort_order == "по убыванию"
        filtered_transactions.sort(key=lambda x: x["date"], reverse=reverse)

    if input("Выводить только рублевые транзакции? Да/Нет: ").lower() == "да":
        filtered_transactions = [
            t for t in filtered_transactions if t["currency_code"].lower() == "rub"
        ]

    if (
        input(
            "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
        ).lower()
        == "да"
    ):
        keyword = input("Введите слово для фильтрации: ")
        filtered_transactions = process_bank_search(filtered_transactions, keyword)

    categories = [
        "Открытие вклада",
        "Перевод с карты на карту",
        "Перевод организации",
        "Перевод со счета на счет",
    ]
    category_counts = count_operations_by_category(filtered_transactions, categories)
    print("Программа: Подсчет операций по категориям:")
    for category, count in category_counts.items():
        print(f"{category}: {count} операций")

    if filtered_transactions:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        print("Распечатываю итоговый список транзакций...")
        for transaction in filtered_transactions:
            date = transaction.get("date", "Дата не указана")
            description = transaction.get("description", "Описание отсутствует")
            from_account = get_mask_account_card(transaction.get("from", "Не указан"))
            to_account = get_mask_account_card(transaction.get("to", "Не указан"))
            amount = transaction.get("amount", "Нет суммы")
            currency = transaction.get("currency_code", "Нет валюты")

            print(f"{date} {description}")
            print(f"{from_account} -> {to_account}")
            print(f"Сумма: {amount} {currency}")
            print()
    else:
        print(
            "Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        )


if __name__ == "__main__":
    main()
