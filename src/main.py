import os
from datetime import datetime
from typing import Any, Dict, List

from src.external_api import \
    process_transaction  # process_transaction лежит здесь!
from src.financial_operations_reader import read_csv_file, read_excel_file
from src.process_bank import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions


def get_mask_card_number(card_number: str) -> str:
    if len(card_number) != 16 or not card_number.isdigit():
        return ""
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    if len(account_number) < 4 or not account_number.isdigit():
        return ""
    return f"**{account_number[-4:]}"


def mask_account_card(info_str: str) -> str:
    """Маскирует номер карты или счёта в зависимости от типа."""
    if not isinstance(info_str, str) or not info_str.strip():
        return "None"

    # Находим первую цифру (начало номера)
    first_digit_idx = None
    for i, char in enumerate(info_str):
        if char.isdigit():
            first_digit_idx = i
            break

    if first_digit_idx is None:
        return "None"  # Нет цифр в строке

    # Выделяем тип (всё до первой цифры) и номер (от первой цифры до конца)
    type_part = info_str[:first_digit_idx].strip()
    number_part = info_str[first_digit_idx:]

    # Очищаем номер от всех нецифровых символов
    cleaned_number = "".join(filter(str.isdigit, number_part))

    if len(cleaned_number) == 0:
        return "None"

    # Нормализуем тип (нижний регистр, без лишних пробелов)
    normalized_type = type_part.lower().strip()  # ← Здесь было: normalizedtype (без _)

    # Проверяем тип и длину
    if normalized_type in ("visa", "mastercard"):  # ← Исправлено: normalized_type (с _)
        if len(cleaned_number) == 16:
            return f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
        else:
            return "None"
    elif normalized_type == "счет":  # ← Исправлено: normalized_type (с _)
        if len(cleaned_number) >= 4:
            return f"**{cleaned_number[-4:]}"
        else:
            return "None"
    else:
        return "None"  # Неизвестный тип


def get_date(date_str: str) -> str:
    """Преобразует ISO-дату в формат ДД.ММ.ГГГГ."""
    dt_obj = datetime.fromisoformat(date_str)
    return dt_obj.strftime("%d.%m.%Y")


def main() -> None:
    """Основная функция программы."""
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
            file_path = input("Введите путь к JSON-файлу: ").strip()
            if not os.path.exists(file_path):
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = load_transactions(file_path)
            print("\nПрограмма: Для обработки выбран JSON-файл.")

        elif choice == "2":
            file_path = input("Введите путь к CSV-файлу: ").strip()
            if not os.path.exists(file_path):
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = read_csv_file(file_path)
            print("\nПрограмма: Для обработки выбран CSV-файл.")

        elif choice == "3":
            file_path = input("Введите путь к XLSX-файлу: ").strip()
            if not os.path.exists(file_path):
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
            input(
                "\nПрограмма: Отсортировать операции по дате? Да/Нет\n" "Пользователь: "
            )
            .strip()
            .lower()
        )

        if sort_choice in ("да", "yes"):
            reverse_choice = (
                input(
                    "\nПрограмма: Отсортировать по возрастанию или по убыванию?\n"
                    "Пользователь: "
                )
                .strip()
                .lower()
            )
            reverse = reverse_choice == "по убыванию"
            filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

        rub_choice = (
            input(
                "\nПрограмма: Выводить только рублевые транзакции? Да/Нет\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )

        if rub_choice in ("да", "yes"):
            filtered_transactions = [
                tx
                for tx in filtered_transactions
                if tx.get("operationAmount", {}).get("currency", {}).get("code")
                == "RUB"
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
            query = input("Введите слово для поиска: ").strip()
            filtered_transactions = process_bank_search(filtered_transactions, query)

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
                    print("\nОшибка: поле 'date' отсутствует в транзакции")
                    continue
                date = get_date(date_str)

                description = tx.get("description", "Не указано")
                from_info = mask_account_card(tx.get("from", ""))
                to_info = mask_account_card(tx.get("to", ""))

                amount = process_transaction(tx)
                currency_code = tx["operationAmount"]["currency"]["code"]
                currency_name = tx["operationAmount"]["currency"].get(
                    "name", currency_code
                )

                print(f"\n{date} {description}")
                if from_info != "None" and to_info != "None":
                    print(f"{from_info} -> {to_info}")
                elif from_info != "None":
                    print(f"Счёт: {from_info}")
                elif to_info != "None":
                    print(f"Счёт: {to_info}")

                print(f"Сумма: {round(amount, 2)} {currency_name}")

            except KeyError as e:
                print(f"\nОшибка: отсутствует поле {e} в транзакции")
            except Exception as e:
                print(f"\nОшибка при обработке транзакции: {str(e)}")

    except KeyboardInterrupt:
        print("\nПрограмма: Работа прервана пользователем.")
    except Exception as e:
        print(f"\nПрограмма: Произошла ошибка: {str(e)}")
    finally:
        print("\nПрограмма: Работа завершена.")

