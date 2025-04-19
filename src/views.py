import logging

# import datetime

from src.card_processing import card_operations, top_transactions
from src.currate_api import stock_prices, praise_read, currency_exchange
from src.utils import greeting, read_file


def web_pages(date: str) -> dict:
    """функция анализа и вывода на веб-страницах — это данные с начала месяца,
    на который выпадает входящая дата, по входящую дату"""

    logger = logging.getLogger("views.py")
    file_handler = logging.FileHandler("../logs/views.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции web_pages")
    logger.info(date)

    # web_pages_dikt = {}

    text_filtrs = read_file(date)
    stock_prices()

    web_pages_dikt = {
        "greeting": greeting(),
        "cards": card_operations(text_filtrs),
        "top_transactions": top_transactions(text_filtrs),
        "currency_rates": currency_exchange(),
        "stock_prices": praise_read(),
    }
    print("#######################################################################################################")
    return web_pages_dikt
