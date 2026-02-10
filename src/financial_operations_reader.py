from pathlib import Path

import pandas as pd


def read_csv_file(file_path: str) -> list:
    """Читает CSV и возвращает список словарей."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path.absolute()}")

    df = pd.read_csv(path, sep=";", encoding="utf-8")
    return df.to_dict("records")


def read_excel_file(file_path: str) -> list:
    """Читает Excel и возвращает список словарей."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path.absolute()}")

    df = pd.read_excel(path, engine="openpyxl")
    return df.to_dict("records")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    csv_path = project_root / "data" / "transactions.csv"
    excel_path = project_root / "data" / "transactions_excel.xlsx"

    try:
        csv_data = read_csv_file(str(csv_path))
        excel_data = read_excel_file(str(excel_path))

        print("Первые 2 записи из CSV:", csv_data[:2])
        print("Первые 2 записи из Excel:", excel_data[:2])

    except Exception as e:
        print(f"Ошибка: {e}")
