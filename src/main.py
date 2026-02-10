import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.financial_operations_reader import read_csv_file, read_excel_file
from src.process_bank import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card

JSON_PATH = Path(
    r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\operations.json"
)
CSV_PATH = Path(
    r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\transactions.csv"
)
XLSX_PATH = Path(
    r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\transactions_excel.xlsx"
)

logging.disable(logging.INFO)


def to_float(value: Any) -> Optional[float]:
    """Преобразовать значение в float.

    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if not s:
        return None
    s = s.replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def format_amount(value: float) -> str:
    """Форматирует сумму для печати.

    """
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    s = f"{value:.2f}"
    s = s.rstrip("0").rstrip(".")
    return s


def format_currency(code: str, name: str) -> str:
    """Возвращает короткую подпись валюты для вывода пользователю.

    """
    c = (code or "").strip().upper()
    n = (name or "").strip()
    if c == "RUB":
        return "руб."
    if c:
        return c
    if n:
        return n
    return "N/A"


def normalize_transaction(tx: Dict[str, Any]) -> Dict[str, Any]:
    """Приводит одну транзакцию к единому формату, чтобы main работал одинаково для JSON/CSV/XLSX.

    """
    if not isinstance(tx, dict) or not tx:
        return {}
    if "operationAmount" in tx and isinstance(tx["operationAmount"], dict):
        op = tx["operationAmount"]
        amt = to_float(op.get("amount"))
        if amt is not None:
            op["amount"] = amt
        tx["operationAmount"] = op
        return tx
    if "operationAmount" in tx and isinstance(tx["operationAmount"], (int, float, str)):
        amt = to_float(tx["operationAmount"])
        if amt is not None:
            tx["operationAmount"] = {
                "amount": amt,
                "currency": {"code": "RUB", "name": "руб."},
            }
        else:
            tx["operationAmount"] = None
        return tx
    if "operationAmount" not in tx and "amount" in tx:
        amt = to_float(tx.get("amount"))
        if amt is None:
            tx["operationAmount"] = None
            return tx
        code = str(tx.get("currency_code", "")).strip()
        name = str(tx.get("currency_name", "")).strip()
        tx["operationAmount"] = {
            "amount": amt,
            "currency": {"code": code, "name": name},
        }
        return tx
    tx["operationAmount"] = None
    return tx


def normalize_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Нормализует список транзакций, отбрасывая пустые/некорректные записи."""
    result: List[Dict[str, Any]] = []
    for tx in transactions:
        ntx = normalize_transaction(tx)
        if ntx:
            result.append(ntx)
    return result


def safe_get_date(date_str: str) -> str:
    """Безопасно форматирует дату в ДД.ММ.ГГГГ, переиспользуя src.widget.get_date.

    """
    if not isinstance(date_str, str):
        return ""
    s = date_str.strip()
    if not s:
        return ""
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return get_date(s)
    except Exception:
        return ""


def format_party(info_str: str) -> str:
    """Форматирует поле ‘from’ или ‘to’ для вывода.

    """
    if not isinstance(info_str, str) or not info_str.strip():
        return "None"
    masked = mask_account_card(info_str)
    if masked in ("None", ""):
        return "None"
    s = info_str.strip()
    first_digit_pos = None
    for i, ch in enumerate(s):
        if ch.isdigit():
            first_digit_pos = i
            break
    if first_digit_pos is None:
        return "None"
    type_part = s[:first_digit_pos].strip()
    type_part_lower = type_part.lower()
    if type_part_lower in ("счет", "счёт"):
        return "Счет " + masked
    if "visa" in type_part_lower or "mastercard" in type_part_lower:
        return type_part + " " + masked
    return masked


def extract_amount_and_currency(tx: Dict[str, Any]) -> Tuple[Optional[float], str]:
    """Достаёт сумму и подпись валюты из нормализованной транзакции.

    """
    op = tx.get("operationAmount")
    if not isinstance(op, dict):
        return None, "N/A"
    amount = to_float(op.get("amount"))
    cur = op.get("currency") or {}
    code = str(cur.get("code", "")).strip()
    name = str(cur.get("name", "")).strip()
    return amount, format_currency(code, name)


def ask_state() -> str:
    """Запрашивает у пользователя статус операции и валидирует ввод."""
    valid_states = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        state_raw = input(
            "\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
            "Пользователь: "
        ).strip()
        state = state_raw.upper()
        if state in valid_states:
            return state
        print(f'\nПрограмма: Статус операции "{state_raw}" недоступен.')


def ask_sort_reverse() -> bool:
    """Запрашивает направление сортировки и возвращает reverse для sort_by_date.

    reverse=False -> по возрастанию (сначала старые)
    reverse=True  -> по убыванию (сначала новые)
    """
    while True:
        choice = (
            input(
                "\nПрограмма: Отсортировать по возрастанию или по убыванию?\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )
        if choice in ("по возрастанию", "возрастанию"):
            return False
        if choice in ("по убыванию", "убыванию"):
            return True
        print(
            '\nПрограмма: Некорректный выбор. Введите "по возрастанию" или "по убыванию".'
        )


def main() -> None:
    """Основная функция программы: связывает чтение данных, фильтрацию, сортировку и вывод."""
    try:
        print(
            "\nПрограмма: Привет! Добро пожаловать в программу работы с банковскими транзакциями."
        )
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("\nПользователь: ").strip()
        transactions: List[Dict[str, Any]] = []

        if choice == "1":
            if not JSON_PATH.exists():
                print(f"\nПрограмма: Файл не найден: {JSON_PATH}")
                return
            transactions = load_transactions(str(JSON_PATH))
            print("\nПрограмма: Для обработки выбран JSON-файл.")
        elif choice == "2":
            if not CSV_PATH.exists():
                print(f"\nПрограмма: Файл не найден: {CSV_PATH}")
                return
            transactions = read_csv_file(str(CSV_PATH))
            print("\nПрограмма: Для обработки выбран CSV-файл.")
        elif choice == "3":
            if not XLSX_PATH.exists():
                print(f"\nПрограмма: Файл не найден: {XLSX_PATH}")
                return
            transactions = read_excel_file(str(XLSX_PATH))
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
        else:
            print("\nПрограмма: Неверный выбор формата файла")
            return

        if not transactions:
            print("\nПрограмма: Ошибка загрузки данных или файл пуст")
            return

        transactions = normalize_transactions(transactions)
        state = ask_state()
        filtered_transactions = filter_by_state(transactions, state)
        print(f'\nПрограмма: Операции отфильтрованы по статусу "{state}"')

        sort_choice = (
            input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ")
            .strip()
            .lower()
        )
        if sort_choice in ("да", "yes"):
            reverse = ask_sort_reverse()
            filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

        rub_choice = (
            input(
                "\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: "
            )
            .strip()
            .lower()
        )
        if rub_choice in ("да", "yes"):
            filtered_transactions = [
                tx
                for tx in filtered_transactions
                if isinstance(tx.get("operationAmount"), dict)
                and str(
                    tx.get("operationAmount", {}).get("currency", {}).get("code", "")
                ).upper()
                == "RUB"
            ]

        search_choice = (
            input(
                "\nПрограмма: Отфильтровать список транзакций по определенному слову \n"
                "в описании? Да/Нет\n\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )
        if search_choice in ("да", "yes"):
            keyword = input(
                "\nПрограмма: Введите слово для поиска\nПользователь: "
            ).strip()
            filtered_transactions = process_bank_search(filtered_transactions, keyword)

        print("\nПрограмма: Распечатываю итоговый список транзакций...")
        if not filtered_transactions:
            print(
                "\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши\nусловия фильтрации."
            )
            return

        print(
            f"\nПрограмма:\nВсего банковских операций в выборке: {len(filtered_transactions)}"
        )
        for tx in filtered_transactions:
            date_str = tx.get("date", "")
            date = safe_get_date(date_str)
            if not date:
                continue
            description = tx.get("description", "Не указано")
            from_text = format_party(tx.get("from", ""))
            to_text = format_party(tx.get("to", ""))
            amount, cur_text = extract_amount_and_currency(tx)

            print(f"\n{date} {description}")
            if from_text != "None" and to_text != "None":
                print(f"{from_text} -> {to_text}")
            elif from_text != "None":
                print(from_text)
            elif to_text != "None":
                print(to_text)

            if amount is None:
                print("Сумма: данные отсутствуют")
            else:
                print(f"Сумма: {format_amount(amount)} {cur_text}")

    except KeyboardInterrupt:
        print("\nПрограмма: Работа прервана пользователем.")
    except Exception as e:
        print(f"\nПрограмма: Произошла ошибка: {str(e)}")
    finally:
        print("\nПрограмма: Работа завершена.")


if __name__ == "__main__":
    main()
