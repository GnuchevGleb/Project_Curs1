import logging
import pandas as pd


def profitable_cashbacks(data: list, yars: str, months: str) -> dict:
    """Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кеш бэк а.
    На выходе — JSON с анализом, сколько на каждой категории можно заработать
     кешбэка в указанном месяце года."""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/services.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции profitable_cashbacks")

    texts = data

    logger.info(texts)
    logger.info(yars)
    logger.info(months)

    texts = pd.DataFrame(data)
    logger.info(texts)

    texts["Дата платежа"] = pd.to_datetime(texts["Дата платежа"], format="%d.%m.%Y")
    filtered_data = texts.loc[
        (texts["Дата платежа"].dt.month == int(months)) & (texts["Дата платежа"].dt.year == int(yars))
    ]

    category_s = filtered_data.loc[:, ["Категория", "Сумма платежа"]]

    category_s_group = category_s.groupby("Категория")["Сумма платежа"].min()

    category_s_group_n = category_s_group.apply(lambda x: round(abs(x / 1000), 2) if x < 0 else None)
    logger.info(category_s_group_n)

    return category_s_group_n.to_json()


# print(profitable_cashbacks(2018,12))
