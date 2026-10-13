import os

from processing import filter_by_state, sort_by_date
from re_bank_search_function import process_bank_search, read_csv, read_excel, read_json
from re_count_operations import count_operations_by_category
from widget import get_mask_account_card


def main():
    """Функция отвечает за основную логику проекта и связывает функциональности между собой."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(base_dir, "data", "transactions.csv")
    excel_path = os.path.join(base_dir, "data", "transactions_excel.xlsx")
    json_path = os.path.join(base_dir, "data", "transactions.json")

    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("Укажите нужную цифру: ").strip()

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
        status = (
            input("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING: ")
            .strip()
            .upper()
        )
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

    if input("Отсортировать операции по дате? Да/Нет: ").strip().lower() == "да":
        sort_order = (
            input("Отсортировать по возрастанию или по убыванию?: ").strip().lower()
        )
        ascending_choice = sort_order == "по возрастанию"
        # Используем твою функцию из модуля processing
        filtered_transactions = sort_by_date(
            filtered_transactions, ascending=ascending_choice
        )

    if input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower() == "да":
        filtered_transactions = [
            t
            for t in filtered_transactions
            if str(t.get("currency_code", t.get("currency", ""))).lower() == "rub"
        ]

    if (
        input(
            "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
        )
        .strip()
        .lower()
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
            date = (
                transaction.get("date")
                or transaction.get("дата операции")
                or "Дата не указана"
            )
            description = (
                transaction.get("description")
                or transaction.get("описание")
                or "Описание отсутствует"
            )
            from_account = get_mask_account_card(
                transaction.get("from") or transaction.get("номер карты") or "Не указан"
            )
            to_account = get_mask_account_card(
                transaction.get("to") or transaction.get("счет") or "Не указан"
            )
            amount = (
                transaction.get("amount")
                or transaction.get("сумма операции")
                or "Нет суммы"
            )
            currency = (
                transaction.get("currency_code")
                or transaction.get("currency")
                or "Нет валюты"
            )

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
