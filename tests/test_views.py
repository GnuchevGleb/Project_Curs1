import unittest
from unittest.mock import patch
from pandas import Timestamp

from src import views


class TestWebPages(unittest.TestCase):

    # Mock-функции для внешних зависимостей, чтобы изолировать тест
    @patch('src.views.read_file')
    @patch('src.views.stock_prices')
    @patch('src.views.greeting')
    @patch('src.views.card_operations')
    @patch('src.views.top_transactions')
    @patch('src.views.currency_exchange')
    @patch('src.views.praise_read')

    def test_web_pages_returns_dict_with_correct_keys(
        self,
            mock_praise_read,
            mock_currency_exchange,
            mock_top_transactions,
            mock_card_operations,
            mock_greeting,
            mock_stock_prices,
            mock_read_file
    ):
        # Настраиваем возвращаемые значения mock-функций
        mock_read_file.return_value = "some_text_filters"
        mock_stock_prices.return_value = [{'stock': 'AAPL', 'price': 209.28}, {'stock': 'AMZN', 'price': 188.99},
                  {'stock': 'GOOGL', 'price': 161.96}, {'stock': 'MSFT', 'price': 391.85},
                  {'stock': 'TSLA', 'price': 284.95}]
        mock_greeting.return_value = 'Доброе утро!'
        mock_card_operations.return_value = [{'last_digits': 7197, 'total_spent': 22320.45, 'cashback': 22.32},
                                        {'last_digits': 4556, 'total_spent': 64681.8, 'cashback': 64.68}]
        mock_top_transactions.return_value = [{'date': Timestamp('2018-01-22 19:23:40'), 'amount': '30000.0', 'category': 'Наличные',
                       'description': 'Снятие в банкомате Райффайзенбанк'},
                      {'date': Timestamp('2018-01-22 19:24:45'), 'amount': '22500.0', 'category': 'Наличные',
                       'description': 'Снятие в банкомате Райффайзенбанк'},
                      {'date': Timestamp('2018-01-15 14:21:02'), 'amount': '7196.8', 'category': 'Наличные',
                       'description': 'Операция в других кредитных организациях RCONNECT C2C MCMS MOSCOW RUS'},
                      {'date': Timestamp('2018-01-24 22:53:54'), 'amount': '5748.0', 'category': 'Авиабилеты',
                       'description': 'Aviacassa'},
                      {'date': Timestamp('2018-01-22 21:10:31'), 'amount': '3500.0', 'category': 'Переводы',
                       'description': 'Аренда'}]
        mock_currency_exchange.return_value = [{'currency': 'USD', 'rate': '64.1824'}, {'currency': 'EUR', 'rate': '69.244'}]
        mock_praise_read.return_value = {"stock1": 100.0}


        # Вызываем тестируемую функцию
        result = views.web_pages("2018-01-31 15:44:39")


        # Проверяем, что функция вернула словарь с ожидаемыми ключами
        expected_keys = {"greeting", "cards", "top_transactions", "currency_rates", "stock_prices"}
        self.assertEqual(set(result.keys()), expected_keys)

        # Проверяем, что mock-функции были вызваны
        mock_read_file.assert_called_once_with("2018-01-31 15:44:39")
        mock_stock_prices.assert_called_once()
        mock_greeting.assert_called_once()
        mock_card_operations.assert_called_once_with("some_text_filters")
        mock_top_transactions.assert_called_once_with("some_text_filters")
        mock_currency_exchange.assert_called_once()
        mock_praise_read.assert_called_once()

if __name__ == '__main__':
    unittest.main()
