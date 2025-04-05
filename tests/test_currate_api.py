
from src.currate_api import currency_exchange, stock_prices


def test_currency_exchange():
    assert type(currency_exchange()) == list
    assert len(currency_exchange()) != 0


def test_stock_prices():
    assert type(stock_prices()) == list
    assert len(stock_prices()) != 0
