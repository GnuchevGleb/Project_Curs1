import logging
import os
from collections import Counter
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame


def read_file() -> DataFrame:
    """функция считывает файл с транзакциями, удаляет строки с пустыми значениями
    и ошибочными данными в банковских картах"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/read_file", "w")
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

    if os.path.exists(way_ex):
        logger.info("Path exists")
    else:
        logger.info("Path does not exist")

    text = pd.read_excel(way_ex)
    logger.info("считывание файла в переменную text")

    texts = text.loc[:, ["Дата платежа", "Номер карты", "Статус", "Сумма операции", "Категория", "Описание"]]

    texts = texts.dropna()  # удаляем строки с пустыми значениями
    mask = texts["Номер карты"].str.contains(r"^\*\d+$", na=False)  # удаляем не корректные данные номеров карт
    texts = texts[mask]
    texts = texts.reset_index(level=None, drop=True, inplace=False, col_level=0, col_fill="")

    return texts


# print(read_file())
############################################################################################################


def card_operations() -> list or DataFrame:
    """функция считывает файл с транзакциями и выдаёт номера банковских карт, сумму операций и кэшбэк"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/card_operations", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    texts = read_file()
    logger.info(texts.head())

    card_numbers = Counter(texts["Номер карты"])
    logger.info(
        "все номера карт в транзакции в том числе ошибочные",
    )
    logger.info(dict(card_numbers))

    card_numbers_lict = []

    for row in card_numbers:
        card_numbers_lict.append((str(row)))

    logger.info("номера карт в транзакции")
    logger.info(card_numbers_lict)

    dict_cart_cum_nn = {}
    result = []

    for j in card_numbers_lict:

        summ_c = 0
        for i in range(0, int(texts.shape[0])):

            if j == texts.at[i, "Номер карты"]:

                summ_c = round((summ_c + texts.at[i, "Сумма операции"]), 2)

        dict_cart_cum_nn = dict(
            last_digits=int(j[-4:]), total_spent=abs(float(summ_c)), cashback=abs(round(float(summ_c / 1000), 2))
        )
        result.append(dict_cart_cum_nn)

    return result


# print(card_operations())
###################################################################################################


def top_transactions() -> list:
    """Функция находит Топ-5 транзакций по сумме платежа"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/top_transactions", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    top_transaction = []
    top_dict = {}
    logger.info("начало выполнения функции top_transactions")

    texts = read_file()
    logger.info(texts.head())

    # print((texts.sort_values(by = 'Сумма операции')))
    logger.info(texts.sort_values(by="Сумма операции"))
    i = 0
    top_transaction_faive = []
    for index, row in texts.sort_values(by="Сумма операции").iterrows():

        if i <= 4:

            top_dict["date"] = row["Дата платежа"]
            top_dict["amount"] = str(abs(row["Сумма операции"]))

            top_dict["category"] = row["Категория"]
            top_dict["description"] = row["Описание"]
            top_transaction.append(top_dict)

            top_transaction_faive.append(dict(top_dict))

            i += 1

    return top_transaction_faive


# print(top_transactions())
##############################################################################################
