from datetime import datetime

from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(info_str: str) -> str:
    """Реализованна функция, которая обрабатывает входящую строку и вызывает функцию маскировки"""
    first_digit_pos = next(
        (i for i, symbol in enumerate(info_str) if symbol.isdigit()), None
    )
    if first_digit_pos is None:
        return "None"

    type_part = info_str[:first_digit_pos].strip()
    number_part = info_str[first_digit_pos:]

    if not number_part.isdigit():
        return "None"

    if any(
        keyword in type_part.lower()
        for keyword in [
            "visa",
            "mastercard",
        ]
    ):
        return get_mask_card_number(number_part)
    elif type_part.lower() == "счет":
        return get_mask_account(number_part)
    else:
        return "None"


def get_date(date_str: str) -> str:
    """Функция которая принимает строку с датой в формате ISO8601 и возвращает строку с датой в формате ДД.ММ.ГГГГ"""

    dt_obj = datetime.fromisoformat(date_str)
    formatted_date = dt_obj.strftime("%d.%m.%Y")
    return formatted_date


input_date = "2024-03-11T02:26:18.671407"
output_date = get_date(input_date)

if __name__ == "__main__":  # pragma: no cover
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(output_date)
