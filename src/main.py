from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from src.financial_operations_reader import read_csv_file
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions


def _to_float(value: Any) -> Optional[float]:
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
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    s = f"{value:.2f}"
    s = s.rstrip("0").rstrip(".")
    return s


def currency_label(code: str, name: str) -> str:
    c = (code or "").strip().upper()
    n = (name or "").strip()

    if c == "RUB":
        return "руб."
    if c:
        return c
    if n:
        return n
    return "N/A"


def mask_account_card(info_str: str) -> str:
    if not isinstance(info_str, str) or not info_str.strip():
        return "None"

    s = info_str.strip()
    first_digit_idx = None
    for i, ch in enumerate(s):
        if ch.isdigit():
            first_digit_idx = i
            break
    if first_digit_idx is None:
        return "None"

    type_part_raw = s[:first_digit_idx].strip()
    number_part = s[first_digit_idx:]
    cleaned_number = "".join(filter(str.isdigit, number_part))

    if not cleaned_number:
        return "None"

    type_part_norm = type_part_raw.lower().strip().replace("ё", "е")
    is_account = (
        ("счет" in type_part_norm)
        or ("счёт" in type_part_norm)
        or (len(cleaned_number) == 20)
    )

    if is_account:
        if len(cleaned_number) < 4:
            return "None"
        return "Счет **" + cleaned_number[-4:]

    if len(cleaned_number) == 16:
        masked = (
            f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
        )
        if type_part_raw:
            return f"{type_part_raw} {masked}"
        return masked

    if len(cleaned_number) >= 4:
        return "Счет **" + cleaned_number[-4:]

    return "None"


def get_date(date_str: str) -> str:
    if not isinstance(date_str, str) or not date_str.strip():
        return ""

    s = date_str.strip()
    try:
        dt_obj = datetime.fromisoformat(s)
        return dt_obj.strftime("%d.%m.%Y")
    except Exception:
        pass

    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y.%m.%d"):
        try:
            dt_obj = datetime.strptime(s, fmt)
            return dt_obj.strftime("%d.%m.%Y")
        except Exception:
            continue

    return s


def read_excel_file(file_path: Path) -> List[Dict[str, Any]]:
    df = pd.read_excel(file_path)
    records = df.to_dict(orient="records")
    return [{str(k): v for k, v in record.items()} for record in records]


def normalize_transaction(tx: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(tx, dict) or not tx:
        return {}

    op = tx.get("operationAmount")
    if isinstance(op, dict):
        amt = _to_float(op.get("amount"))
        if amt is not None:
            op["amount"] = amt
            tx["operationAmount"] = op
        return tx

    if op is not None and op != "":
        amt = _to_float(op)
        tx["operationAmount"] = amt if amt is not None else None
        return tx

    if "operationAmount" not in tx and "amount" in tx:
        amt = _to_float(tx.get("amount"))
        if amt is None:
            tx["operationAmount"] = None
            return tx

        code = str(tx.get("currency_code", "")).strip()
        name = str(tx.get("currency_name", "")).strip()
        tx["operationAmount"] = {
            "amount": amt,
            "currency": {"name": name, "code": code},
        }
        return tx

    return tx


def normalize_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for tx in transactions:
        ntx = normalize_transaction(tx)
        if ntx:
            result.append(ntx)
    return result


def process_transaction_safe(tx: Dict[str, Any]) -> Optional[float]:
    op = tx.get("operationAmount")

    if isinstance(op, dict):
        return _to_float(op.get("amount"))
    return _to_float(op)


def filter_by_description_keyword(
    transactions: List[Dict[str, Any]], keyword: str
) -> List[Dict[str, Any]]:
    kw = (keyword or "").strip().lower()
    if not kw:
        return transactions

    result: List[Dict[str, Any]] = []
    for tx in transactions:
        desc = str(tx.get("description", "")).lower()
        if kw in desc:
            result.append(tx)
    return result


def ask_sort_reverse() -> bool:
    while True:
        choice = (
            input(
                "\nПрограмма: Выберите порядок сортировки:\n"
                "1 - по возрастанию (сначала старые)\n"
                "2 - по убыванию (сначала новые)\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )

        if choice in ("1", "по возрастанию", "возрастанию", "asc", "a"):
            return False
        if choice in ("2", "по убыванию", "убыванию", "desc", "d"):
            return True
        print("\nПрограмма: Некорректный выбор. Введите 1 или 2.")


def main() -> None:
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
            file_path = Path(
                r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\operations.json"
            )
            if not file_path.exists():
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = load_transactions(str(file_path))
            print("\nПрограмма: Для обработки выбран JSON-файл.")

        elif choice == "2":
            file_path = Path(
                r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\transactions.csv"
            )
            if not file_path.exists():
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = read_csv_file(str(file_path))
            print("\nПрограмма: Для обработки выбран CSV-файл.")

        elif choice == "3":
            file_path = Path(
                r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\transactions_excel.xlsx"
            )
            if not file_path.exists():
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = read_excel_file(file_path)
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
        else:
            print("\nПрограмма: Неверный выбор формата файла")
            return

        if not transactions:
            print("\nПрограмма: Ошибка загрузки данных или файл пуст")
            return

        transactions = normalize_transactions(transactions)

        valid_states = {"EXECUTED", "CANCELED", "PENDING"}
        state = ""
        while state not in valid_states:
            state = (
                input(
                    "\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                    "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
                    "Пользователь: "
                )
                .strip()
                .upper()
            )
            if state not in valid_states:
                print(f"\nПрограмма: Статус операции {state} недоступен.")

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
                if (
                    isinstance(tx.get("operationAmount"), dict)
                    and str(
                        tx.get("operationAmount", {})
                        .get("currency", {})
                        .get("code", "")
                    ).upper()
                    == "RUB"
                )
                or (isinstance(tx.get("operationAmount"), (int, float)))
            ]

        search_choice = (
            input(
                "\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )
        if search_choice in ("да", "yes"):
            keyword = input(
                "\nПрограмма: Введите слово для поиска в описании\nПользователь: "
            ).strip()
            filtered_transactions = filter_by_description_keyword(
                filtered_transactions, keyword
            )

        print("\nПрограмма: Распечатываю итоговый список транзакций...")
        if not filtered_transactions:
            print(
                "\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации."
            )
            return

        print(
            f"\nПрограмма: Всего банковских операций в выборке: {len(filtered_transactions)}"
        )
        for tx in filtered_transactions:
            try:
                date_str = tx.get("date", "")
                if not date_str:
                    continue
                date = get_date(date_str)
                description = tx.get("description", "Не указано")
                from_masked = mask_account_card(tx.get("from", ""))
                to_masked = mask_account_card(tx.get("to", ""))
                op = tx.get("operationAmount")
                amount = process_transaction_safe(tx)

                print(f"\n{date} {description}")
                if from_masked != "None" and to_masked != "None":
                    print(f"{from_masked} -> {to_masked}")
                elif from_masked != "None":
                    print(from_masked)
                elif to_masked != "None":
                    print(to_masked)

                if op is None or op == "" or amount is None:
                    print("Сумма: данные отсутствуют")
                    continue

                if isinstance(op, dict):
                    cur = op.get("currency") or {}
                    code = str(cur.get("code", "")).strip()
                    name = str(cur.get("name", "")).strip()
                    cur_text = currency_label(code, name)
                else:
                    cur_text = "руб."

                print(f"Сумма: {format_amount(amount)} {cur_text}")

            except Exception as e:
                print(f"\nОшибка при обработке транзакции: {str(e)}")

    except KeyboardInterrupt:
        print("\nПрограмма: Работа прервана пользователем.")
    except Exception as e:
        print(f"\nПрограмма: Произошла ошибка: {str(e)}")
    finally:
        print("\nПрограмма: Работа завершена.")


if __name__ == "__main__":
    main()
