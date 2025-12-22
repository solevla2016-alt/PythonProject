def get_mask_card_number(card_number: str) -> str:
    """Реализована функция, которая принимает номер карты и возвращает ее маску."""
    if len(card_number) != 16 or not card_number.isdigit():

        return ""


    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked


if __name__ == "__main__":
    print(get_mask_card_number("card"))


def get_mask_account(account_number: str) -> str:
    """Реализована функция, которая принимает номер счета и возвращает его маску ."""
    if len(account_number) < 4 or not account_number.isdigit():

        return ""


    masked = f"**{account_number[-4:]}"
    return masked


if __name__ == "__main__":
    print(get_mask_account("account"))
