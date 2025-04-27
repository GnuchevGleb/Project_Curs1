import os

from unittest.mock import patch
from src import utils
from datetime import datetime
from src.utils import category


def test_greeting_morning():
    # Тест для утреннего приветствия
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 9, 0, 0)
        assert utils.greeting() == "Доброе утро!"


def test_greeting_dey():
    # Тест для дневного приветствия
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 15, 0, 0)
        assert utils.greeting() ==  "Добрый день!"

def test_greeting_evening():
    # Тест для дневного приветствия
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 19, 0, 0)
        assert utils.greeting() ==  "Добрый вечер!"

def test_greeting_night():
    # Тест для дневного приветствия
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 2, 0, 0)
        assert utils.greeting() ==  "Доброй ночи!"

def test_greeting_dey2():
    # Тест для граничного условия
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        assert utils.greeting() == "Добрый день!"

def test_greeting_dey3():
    # Тест для граничного условия
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        assert type(utils.greeting()) == str





def test_file_exists():
    """Проверяет, существует ли файл по указанному пути."""
    file_path =  os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.xls')
    assert os.path.exists(file_path) == True, f"Файл '{file_path}' не существует"

def test_category():
    """Проверяет результат работы функции при несуществующих данных"""
    assert category('01.02.2025') is None


def test_category_2():
    """Проверяет результат работы функции при известных данных"""
    assert category('01.03.2021') == {'аптеки': 4, 'ж/д билеты': 3, 'транспорт': 6}