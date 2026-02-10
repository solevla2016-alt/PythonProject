import logging
import os

# Настройка логгера (ДОЛЖНО БЫТЬ В НАЧАЛЕ ФАЙЛА)
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# FileHandler
file_handler = logging.FileHandler("logs/masks.log", mode="w")
file_formatter = logging.Formatter(
    "%(asctime)s [%(name)s] [%(levelname)s]: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# StreamHandler (консоль)
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter(
    "%(asctime)s [%(name)s] [%(levelname)s]: %(message)s"
)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты (16 цифр)."""
    logger.debug(f"Получен номер карты: {card_number}")

    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(
            f"Переданный номер карты некорректен: {card_number}. Длина должна быть ровно 16 символов."
        )
        return ""

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info(f"Маскировка номера карты выполнена успешно: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта (минимум 4 цифры) → последние 2 цифры."""
    logger.debug(f"Получен номер счёта: {account_number}")

    if len(account_number) < 4 or not account_number.isdigit():
        logger.error(
            f"Переданный номер счёта некорректен: {account_number}. Длина должна быть минимум 4 символа."
        )
        return ""

    # ВАЖНО: берём только последние 2 цифры!
    masked = f"**{account_number[-4:]}"
    logger.info(f"Маскировка номера счёта выполнена успешно: {masked}")
    return masked
