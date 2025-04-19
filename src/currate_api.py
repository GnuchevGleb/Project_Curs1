import json
import logging
import os
import pandas as pd
from urllib.request import urlopen
import certifi
import requests
from dotenv import load_dotenv


def currency_exchange() -> list:
    """Функция получения курса валюты с сайта https://www.currate.ru/account"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/currency_exchange.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции currency_exchange")

    """определяем путь к файлу с пользовательскими запросами"""
    logger.info("начало выполнения запроса пути к файлу")
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "..", "data")

    way_ex = os.path.join(data_dir, "user_settings.json")
    logger.info("путь к файлу с данными")
    logger.info(way_ex)
    if os.path.exists(way_ex):
        logger.info("Path exists")
    else:
        logger.info("Path does not exist")

    with open(way_ex, "r") as file:
        content = file.read()
        logger.info("пользовательский запрос")
        logger.info(content)
        content = json.loads(content)
        currency_s = content["user_currencies"]

        currency_1 = currency_s[0]
        currency_11 = currency_s[0] + "RUB"

        currency_2 = currency_s[1]
        currency_22 = currency_s[1] + "RUB"
        logger.info(currency_1)
        logger.info(currency_2)

    load_dotenv()

    """Получение значения переменной API_KEY из .env-файла"""
    kei_api = os.getenv("API_KEY")

    # response_rub_currencys = requests.get(f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={kei_api}")
    response_rub_currencys = requests.get(
        f"https://currate.ru/api/?get=rates&pairs={currency_11},{currency_22}&key={kei_api}"
    )
    logger.info(response_rub_currencys.json())
    logger.info(type(response_rub_currencys.json()))
    currency_rates = []
    currency_rates_usd = {}
    currency_rates_eur = {}
    ################################################################################

    """ результат для проверки функциональности Api возвращает данные вида:
        # response_rub_currencys = {'status': 200, 'message': 'rates',
         'data': {'USDRUB': '64.1824', 'EURRUB': '69.244'}}"""

    #################################################################################
    currency_rates_usd["currency"] = currency_1
    currency_rates_usd["rate"] = (response_rub_currencys.json().get("data")).get(currency_11)
    currency_rates.append(currency_rates_usd)
    currency_rates_eur["currency"] = currency_2
    currency_rates_eur["rate"] = (response_rub_currencys.json().get("data")).get(currency_22)
    currency_rates.append(currency_rates_eur)

    return currency_rates


# print(currency_exchange())
############################################################################################################


def stock_prices():
    """Функция получения стоимости акций компаний с записью в файл example.txt"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/stock_prices.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции stock_prices")

    load_dotenv()

    """Получение значения переменной API_KEY из .env-файла"""
    kei_api = os.getenv("API_KEY_2")
    logger.info(kei_api)
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={kei_api}"
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")

    logger.info(len(data))

    with open("example.txt", "w") as file:
        file.write(data)


# print(stock_prices())


def praise_read() -> list:
    """Функция считывает данные стоимости акций из файла example.txt и выводит стоимость акций компаний указанных в
    пользовательском запросе в файле user_settings.json"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/stock_prices.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции praise_read")
    with open("example.txt", "r") as file:
        content = file.read()
        logger.info("количество компаний в файле")
        logger.info(len(content))

        res_content = json.loads(content)
        df = pd.DataFrame(res_content)
        df = df.rename(columns={"symbol": "stock"})

        """определяем путь к файлу с пользовательскими запросами"""
        logger.info("начало выполнения запроса пути к файлу")
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, "..", "data")

        way_ex = os.path.join(data_dir, "user_settings.json")
        logger.info("путь к файлу с данными")
        logger.info(way_ex)
        if os.path.exists(way_ex):
            logger.info("Path exists")
        else:
            logger.info("Path does not exist")

        with open(way_ex, "r") as file:
            content = file.read()
            logger.info("пользовательский запрос")
            logger.info(content)
            content = json.loads(content)
            stocks = content["user_stocks"]

            stock_prices = []
            for row in stocks:
                df_f = df.loc[(df["stock"] == row)]
                stock_prices.append((df_f[["stock", "price"]]).to_dict(orient="records")[0])

    return stock_prices


# print(praise_read())
