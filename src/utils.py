import datetime
import logging
import os
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter


def greeting():
    """функция выводит приветствие пользователя в зависимости от времени суток"""

    current_times = ()
    current_time = int(datetime.now().strftime(" %H"))
    # print( 'текущее время ', int(current_time), ' часов')
    if 6 <= current_time < 12:
        # print('Доброе утро!')
        current_times = "Доброе утро!"
    elif 12 <= current_time < 18:
        # print('Добрый день!')
        current_times = "Добрый день!"
    elif 18 <= current_time < 24:
        # print("Добрый вечер!")
        current_times = "Добрый вечер!"
    elif 0 <= current_time < 6:
        # print('Доброй ночи!')
        current_times = "Доброй ночи!"

    return current_times


###################################################################################################
def read_file(date: str) -> DataFrame:
    """функция считывает файл с транзакциями, удаляет строки с пустыми значениями
    и ошибочными данными в банковских картах, возвращает DataFrame отфильтрованный
    по периоду от 1-го числа месяца до введённой даты"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/read_file.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    """определяем путь к файлу с транзакциями"""
    logger.info("начало выполнения функции read_file")
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "..", "data")

    way_ex = os.path.join(data_dir, "operations.xls")
    logger.info("путь к файлу с данными")
    logger.info(way_ex)

    month = date[:7]

    month_elementary = month + "-01 00:00:00"

    month_elementary = datetime.strptime(month_elementary, "%Y-%m-%d %H:%M:%S")

    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    if os.path.exists(way_ex):
        logger.info("Path exists")
    else:
        logger.info("Path does not exist")

    text = pd.read_excel(way_ex)
    logger.info("считывание файла в переменную text")

    texts = text.loc[:, ["Дата операции", "Номер карты", "Статус", "Сумма операции", "Категория", "Описание"]]

    texts = texts.dropna()  # удаляем строки с пустыми значениями
    mask = texts["Номер карты"].str.contains(r"^\*\d+$", na=False)  # удаляем не корректные данные номеров карт
    texts = texts[mask]
    texts = texts.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill="")

    text_sort = {
        "Дата операции": [],
        "Номер карты": [],
        "Статус": [],
        "Сумма операции": [],
        "Категория": [],
        "Описание": [],
    }
    text_sort = pd.DataFrame(text_sort)
    logger.info("создаём пустой DataFrame text_sort ")
    logger.info(text_sort)
    j = 0
    # filtr = ()
    for index, i in texts.iterrows():

        dat_mod = datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if month_elementary <= dat_mod <= date:
            logger.info("отфильтрованная дата")
            filtr = (dat_mod, i["Номер карты"])
            logger.info(filtr)
            text_sort.loc[j] = (
                dat_mod,
                i["Номер карты"],
                i["Статус"],
                i["Сумма операции"],
                i["Категория"],
                i["Описание"],
            )
            j += 1

    logger.info(text_sort)
    return text_sort


# print(read_file())
############################################################################################################


def read_file_2() -> DataFrame:
    """функция считывает файл с транзакциями, удаляет строки с пустыми значениями
    и ошибочными данными в банковских картах, возвращает DataFrame"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/read_file.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    """определяем путь к файлу с транзакциями"""
    logger.info("начало выполнения функции read_file_2")
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "..", "data")

    way_ex = os.path.join(data_dir, "operations.xls")
    logger.info("путь к файлу с данными")
    logger.info(way_ex)

    if os.path.exists(way_ex):
        logger.info("Path exists")
    else:
        logger.info("Path does not exist")

    text = pd.read_excel(way_ex)

    logger.info("считывание файла в переменную text")

    texts = text.loc[
        :,
        [
            "Дата операции",
            "Дата платежа",
            "Номер карты",
            "Статус",
            "Сумма операции",
            "Валюта операции",
            "Сумма платежа",
            "Валюта платежа",
            "Кэшбэк",
            "Категория",
            "MCC",
            "Описание",
            "Бонусы (включая кэшбэк)",
            "Округление на инвесткопилку",
            "Сумма операции с округлением",
        ],
    ]

    texts = texts.dropna()  # удаляем строки с пустыми значениями

    mask = texts["Номер карты"].str.contains(r"^\*\d+$", na=False)  # удаляем не корректные данные номеров карт
    texts = texts[mask]
    texts = texts.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill="")

    return texts


# print(read_file_2())

#############################################################################################################


def category(date: str) -> dict or None:
    """Функция определяет категории трат по умолчанию за последние три месяца (от переданной даты)"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/reports.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции category")
    logger.info(date)
    print("начало выполнения функции category")

    date = datetime.strptime(date, "%d.%m.%Y")

    texts = read_file_2()

    logger.info(date)

    date_start = date
    date_start = pd.to_datetime(date_start, dayfirst=True)

    logger.info(date_start)

    new_date = date - relativedelta(months=3)
    date_finish = new_date.strftime("%d.%m.%Y")
    date_finish = pd.to_datetime(date_finish, dayfirst=True)
    logger.info(date_finish)

    print((date - new_date).days, " количество дней для поиска транзакций")

    texts = texts.copy()

    filtered_df = texts[
        (pd.to_datetime(texts["Дата платежа"], dayfirst=True) <= date_start)
        & (pd.to_datetime(texts["Дата платежа"], dayfirst=True) >= date_finish)
    ]
    if len(filtered_df) == 0:
        print("за выбранный период транзакции не проводились")
        return None

    filtered_df = filtered_df.map(lambda s: s.lower() if type(s) == str else s)

    logger.info(filtered_df)

    filtered_df_count = Counter(filtered_df["Категория"])
    print(" за выбранный период были выполнены следующие транзакции (категория:количество транзакций):")
    # print(dict(filtered_df_count))
    print(f"всего было выполнено {len(filtered_df_count)} транзакции")
    return dict(filtered_df_count)
