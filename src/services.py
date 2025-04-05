import pandas as pd

from src.card_processing import card_operations, read_file
import logging


def profitable_cashbacks(yars: int, months: int) -> dict:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кеш бэк а."""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/services", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции profitable_cashbacks")

    texts = read_file()

    logger.info(texts)
    logger.info(yars)
    logger.info(months)

    texts["Дата платежа"] = pd.to_datetime(texts["Дата платежа"], format="%d.%m.%Y")
    filtered_data = texts.loc[
        (texts["Дата платежа"].dt.month == int(months)) & (texts["Дата платежа"].dt.year == int(yars))
    ]

    category_s = filtered_data.loc[:, ["Категория", "Сумма операции"]]

    category_s_group = category_s.groupby("Категория")["Сумма операции"].min()

    category_s_group_n = category_s_group.apply(lambda x: round(abs(x / 1000), 2) if x < 0 else None)

    return category_s_group_n.dropna().to_dict()


# print(profitable_cashbacks(2018,12))
