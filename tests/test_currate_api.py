import os

from src.currate_api import currency_exchange, stock_prices


def test_currency_exchange():
    assert type(currency_exchange()) == list
    assert len(currency_exchange()) != 0


def test_stock_prices():
    stock_prices()
    file_path = os.path.join(os.path.dirname(__file__), 'example.txt')
    assert os.path.exists(file_path) == True, f"Файл '{file_path}' не существует"
