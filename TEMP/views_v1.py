import datetime

from src.card_processing import card_operations, read_file, top_transactions
from src.reports import spending_by_category
from src.services import profitable_cashbacks


def greeting():
    """функция выводит приветствие пользователя в зависимости от времени,
    по каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    Топ-5 транзакций по сумме платежа.
    Курс валют.
    Стоимость акций из S&P500."""

    current_times = ()
    conclusion = {}
    current_time = int(datetime.datetime.now().strftime(" %H"))
    # print( 'текущее время ', int(current_time), ' часов')
    if 6 <= current_time < 12:
        # print('Доброе утро!')
        current_times = "Доброе утро!"
    elif 12 <= current_time < 18:
        # print('Добрый день!')
        current_times = "Добрый день!"
    elif 18 <= current_time < 24:
        # print("Добрый вечер!")
        current_times = "Добрый вечер!"
    elif 0 <= current_time < 6:
        # print('Доброй ночи!')
        current_times = "Доброй ночи!"

    print(current_times)
    conclusion["greeting"] = current_times
    conclusion["cards"] = card_operations()
    conclusion["top_transactions"] = top_transactions()
    # conclusion["currency_rates"] = currency_exchange()
    # conclusion["stock_prices"] = stock_prices()
    print(conclusion)
    #########################################################################################
    """ анализ выгодности категорий повышенного кеш бэка.
        На вход функции поступают данные для анализа, год и месяц."""

    print("анализ выгодности категорий повышенного кеш бэка")
    yar = input('Введите год поиска категории выгодного кэш бека в формате "****" : ')
    i = 0
    while i != 1:
        try:
            if datetime.datetime.strptime(yar, "%Y"):
                print(f"Это правильный ввод. Вы ввели {yar} год")
                i = 1
        except ValueError:
            yar = input('Ошибка ввода. Введите год в формате "****" : ')

    month = input('Введите месяц поиска категории выгодного кэш бека в формате "**" : ')
    j = 0
    while j != 1:
        try:
            if datetime.datetime.strptime(month, "%m"):
                print(f"Это правильный ввод. Вы ввели {month}  месяц")
                j = 1
        except ValueError:
            month = input('Ошибка ввода. Введите месяц в формате "**" : ')

    print(f"месяц, год поиска: {month}.{yar}")

    print(profitable_cashbacks(int(yar), int(month)))
    #################################################################################################
    print("рассмотрим траты по заданной категории по умолчанию за последние 3 месяца")

    optional_date = input(
        "введите опциональную дату в формате <<день.месяц.год>>, по умолчанию берется текущая дата- "
    )
    texts = read_file()

    print(spending_by_category(texts, optional_date))


if __name__ == "__main__":
    greeting()



#############################################################
import functools

def report_decorator(filepath):
    """
    Декоратор для функций отчетов, который записывает результат работы функции в файл.

    Args:
        filepath (str): Путь к файлу, в который будет записан результат.
    """
    def decorator_report(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обертка для декорируемой функции.
            """
            result = func(*args, **kwargs)  # Вызов оригинальной функции
            try:
                with open(filepath, 'a') as f:  # Открываем файл для добавления (append)
                    f.write(str(result) + '\n')  # Записываем результат в файл
            except Exception as e:
                print(f"Ошибка при записи в файл: {e}")  # Обработка ошибок записи
            return result  # Возвращаем результат работы оригинальной функции
        return wrapper
    return decorator_report

# Пример использования:
@report_decorator('report.txt')
def generate_report(data):
    """
    Функция, генерирующая отчет на основе входных данных.
    """
    report_string = f"Сгенерирован отчет для данных: {data}"
    return report_string

# Вызов функции
report = generate_report({"user_id": 123, "action": "login"})
print(report)  # Вывод отчета в консоль
