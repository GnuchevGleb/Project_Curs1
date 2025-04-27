import os

from src.currate_api import currency_exchange, stock_prices, praise_read


def test_currency_exchange():
    """Проверяет, существует ли файл с пользовательскими запросами по указанному пути."""
    file_path =  os.path.join(os.path.dirname(__file__), '..', 'data', 'user_settings.json')
    assert os.path.exists(file_path) == True, f"Файл '{file_path}' не существует"


def test_currency_exchange_2():
    """Проверяет, существует ли файл с API_KEY по указанному пути."""
    file_path =  os.path.join(os.path.dirname(__file__), '..',  '.env')
    assert os.path.exists(file_path) == True, f"Файл '{file_path}' не существует"

def test_currency_exchange_3():
    """Проверяет результат работы функции - возвращает строку."""
    assert type(currency_exchange()) == list

def test_stock_prices():
    """Проверяет, создаётся ли файл с акциями компаний после выполнения функции"""
    stock_prices()

    file_path =  os.path.join(os.path.dirname(__file__), 'example.txt')
    assert os.path.exists(file_path) == True, f"Файл '{file_path}' не существует"

def test_praise_read():
    """Проверяет результат работы функции - возвращает строку."""
    assert type(praise_read()) == list