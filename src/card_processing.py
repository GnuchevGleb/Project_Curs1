import logging

from collections import Counter
from pandas.core.interchange.dataframe_protocol import DataFrame


def card_operations(texts) -> list or DataFrame:
    """функция считывает файл с транзакциями и выдаёт номера банковских карт, сумму операций и кэшбэк"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/card_operations.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    # texts = read_file()
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

    # dict_cart_cum_nn = {}
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


def top_transactions(texts) -> list:
    """Функция находит Топ-5 транзакций по сумме платежа"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/top_transactions.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    top_transaction = []
    top_dict = {}
    logger.info("начало выполнения функции top_transactions")

    logger.info(texts)

    # print((texts.sort_values(by = 'Сумма операции')))
    logger.info(texts.sort_values(by="Сумма операции"))
    i = 0
    top_transaction_faive = []
    for index, row in texts.sort_values(by="Сумма операции").iterrows():

        if i <= 4:

            top_dict["date"] = row["Дата операции"]
            top_dict["amount"] = str(abs(row["Сумма операции"]))

            top_dict["category"] = row["Категория"]
            top_dict["description"] = row["Описание"]
            top_transaction.append(top_dict)

            top_transaction_faive.append(dict(top_dict))

            i += 1

    return top_transaction_faive


# print(top_transactions())
# ##############################################################################################
