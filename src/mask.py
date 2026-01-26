import logging
import os


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

    # Создаём директорию для логов, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Настраиваем логер для модуля masks
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # FileHandler с индивидуальным форматером
    file_handler = logging.FileHandler("logs/masks.log", mode="w")
    file_formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s]: %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # StreamHandler (консоль)
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s]: %(message)s"
    )
    stream_handler.setFormatter(stream_formatter)

    # Добавляем обработчики к логеру
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    def get_mask_card_number(card_number: str) -> str:
        """
        Функция маскирует номер банковской карты, оставляя первые шесть цифр и последние четыре цифры открытыми.
        """
        logger.debug(f"Получен номер карты: {card_number}")

        if len(card_number) != 16 or not card_number.isdigit():
            logger.error(
                f"Переданный номер карты некорректен: {card_number}. Длина должна быть ровно 16 символов."
            )
            return ""

        try:
            masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
            logger.info(f"Маскировка номера карты выполнена успешно: {masked}")
            return masked
        except Exception as e:
            logger.exception(f"Ошибка при обработке номера карты: {e}")
            return ""

    def get_mask_account(account_number: str) -> str:
        """
        Функция маскирует банковский счёт, показывая только последние четыре символа.
        """
        logger.debug(f"Получен номер счёта: {account_number}")

        if len(account_number) < 4 or not account_number.isdigit():
            logger.error(
                f"Переданный номер счёта некорректен: {account_number}. Длина должна быть минимум 4 символа."
            )
            return ""

        try:
            masked = f"**{account_number[-4:]}"
            logger.info(f"Маскировка номера счёта выполнена успешно: {masked}")
            return masked
        except Exception as e:
            logger.exception(f"Ошибка при обработке номера счёта: {e}")
            return ""

    if __name__ == "__main__":
        print(get_mask_card_number("1234567890123456"))
        print(get_mask_account("1234567890123456"))
