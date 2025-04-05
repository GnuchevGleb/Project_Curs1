import logging
import os
import requests
from dotenv import load_dotenv


def currency_exchange() -> list:
    """Функция получения курса валюты с сайта https://www.currate.ru/account"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/currency_exchange", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции currency_exchange")
    load_dotenv()

    """Получение значения переменной API_KEY из .env-файла"""
    kei_api = os.getenv("API_KEY")

    response_rub_currencys = requests.get(f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={kei_api}")
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

    currency_rates_usd["currency"] = "USD"
    currency_rates_usd["rate"] = (response_rub_currencys.json().get("data")).get("USDRUB")
    currency_rates.append(currency_rates_usd)
    currency_rates_eur["currency"] = "EUR"
    currency_rates_eur["rate"] = (response_rub_currencys.json().get("data")).get("EURRUB")
    currency_rates.append(currency_rates_eur)
    return currency_rates


# print(currency_exchange())


def stock_prices() -> list:
    """Функция получения стоимости акций компаний"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/stock_prices", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции stock_prices")

    load_dotenv()
    stock_price = []
    """Получение значения переменной API_KEY из .env-файла"""
    kei_api = os.getenv("API_KEY_2")
    logger.info(kei_api)

    response = requests.get(f"https://financialmodelingprep.com/stable/company-screener?apikey={kei_api}")
    logger.info(response)
    company_screener = response.json()
    company_name = ()
    for row in company_screener:

        for key, value in row.items():
            if key == "companyName":
                company_name = value

            if key == "price":

                stock_price.append({f'"company_name": "{company_name}", "price": {value}'})

        #################################################################################
    return stock_price


# print(stock_prices())
