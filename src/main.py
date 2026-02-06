import csv
import json
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, List

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


def load_json_transactions(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список транзакций")
        return data


def load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загрузка транзакций из CSV-файла."""
    transactions = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(row)
    return transactions


def _normalize_cell_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, date) or isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, time):
        return value.strftime("%H:%M:%S")
    elif isinstance(value, timedelta):
        return str(value)
    elif hasattr(value, "text"):
        return str(value.text)
    return value


def load_xlsx_transactions(filepath: str) -> List[Dict[str, Any]]:
    wb = load_workbook(filepath)
    sheet = wb.active

    if sheet is None:
        raise ValueError("Активный лист не найден")
    if not isinstance(sheet, Worksheet):
        raise TypeError(f"Лист имеет тип {type(sheet)}, а не Worksheet")

    headers = [str(cell.value) if cell.value is not None else "" for cell in sheet[1]]

    transactions: List[Dict[str, Any]] = []

    for row in sheet.iter_rows(min_row=2):
        transaction: Dict[str, Any] = {}
        for idx, cell in enumerate(row):
            if idx < len(headers):
                key = headers[idx]
                raw_value = cell.value
                normalized_value = _normalize_cell_value(raw_value)
                transaction[key] = normalized_value
        transactions.append(transaction)

    return transactions


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по статусу (с приведением к верхнему регистру)."""
    return [t for t in transactions if t.get("state", "").upper() == status.upper()]


def sort_transactions(
    transactions: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """Сортировка транзакций по дате."""
    return sorted(
        transactions,
        key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"),
        reverse=not ascending,
    )


def filter_ruble_transactions(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Фильтрация транзакций только в рублях."""
    ruble_variants = ["руб", "rub", "rur"]  # Поддерживаем разные написания
    return [
        t
        for t in transactions
        if (
            t.get("operationAmount", {}).get("currency", {}).get("name", "").lower()
            in ruble_variants
        )
    ]


def search_by_keyword(
    transactions: List[Dict[str, Any]], keyword: str
) -> List[Dict[str, Any]]:
    """Поиск транзакций по ключевому слову в описании."""
    return [
        t
        for t in transactions
        if keyword.lower() in str(t.get("description", "")).lower()
    ]


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Вывод транзакций в консоль."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        date = t.get("date", "")
        description = t.get("description", "")
        from_acc = t.get("from", "")
        to_acc = t.get("to", "")

        # Получаем сумму и валюту
        op_amount = t.get("operationAmount", {})
        amount = op_amount.get("amount", "")
        currency = op_amount.get("currency", {}).get("name", "")

        print(f"{date} {description}")

        if from_acc:
            print(f"{from_acc} -> {to_acc}")
        else:
            # Маскируем последние 4 цифры счёта ВСЕГДА (даже если короткий)
            to_str = str(to_acc) if to_acc else ""
            if len(to_str) >= 4:
                print(f"Счет **{to_str[-4:]}")
            else:
                # Если меньше 4 цифр — выводим как есть, но с префиксом "Счет **"
                print(f"Счет **{to_str}")

        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("> ")

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_json_transactions(file_path)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = load_csv_transactions(file_path)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = load_xlsx_transactions(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    status = ""
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input("> ").strip()
        if status.upper() in valid_statuses:
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    print(f'Операции отфильтрованы по статусу "{status.upper()}"')
    filtered_transactions = filter_by_status(transactions, status)

    sort_choice = input("Отсортировать операции по дате? Да/Нет\n> ").strip().lower()
    if sort_choice == "да":
        order = (
            input("Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        )
        ascending = order == "по возрастанию"
        filtered_transactions = sort_transactions(filtered_transactions, ascending)

    ruble_choice = (
        input("Выводить только рублёвые транзакции? Да/Нет\n> ").strip().lower()
    )
    if ruble_choice == "да":
        filtered_transactions = filter_ruble_transactions(filtered_transactions)

    keyword_choice = (
        input(
            "Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n> "
        )
        .strip()
        .lower()
    )
    if keyword_choice == "да":
        keyword = input("Введите ключевое слово: ").strip()
        filtered_transactions = search_by_keyword(filtered_transactions, keyword)

    print("Распечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":
    main()
