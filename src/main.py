import logging
import json

from datetime import datetime
from src.reports import spending_by_category
from src.services import profitable_cashbacks
from src.utils import read_file_2, category
from src.views import web_pages

""" main.py модуль, где вызывается последовательно функция веб страницы,
 функция сервиса и функцию отчёта друг за другом"""

logger = logging.getLogger("main.py")
file_handler = logging.FileHandler("../logs/main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.info("начало выполнения функции main")

dates = input("Введите входящую дату и время в формате YYYY-MM-DD HH:MM:SS :  ")

i = 0
while i != 1:
    try:
        if datetime.strptime(dates, "%Y-%m-%d %H:%M:%S"):
            print(f"Это правильный ввод. Вы ввели {dates} дату и время")
            i = 1
    except ValueError:
        dates = input("Ошибка ввода. Введите дату и время в формате YYYY-MM-DD HH:MM:SS : ")

logger.info("введённая дата")
logger.info(dates)


print(web_pages(dates))

############################################################################################################

logger.info("Определяем Выгодные категории повышенного кешбэка")
print("Определяем Выгодные категории повышенного кешбэка")
year = input("Введите год, за который проводится анализ в формате YYYY:  ")
i = 0
while i != 1:
    try:
        if datetime.strptime(year, "%Y"):
            print(f"Это правильный ввод. Вы ввели {year} год")
            i = 1
    except ValueError:
        year = input("Ошибка ввода. Введите год в формате YYYY : ")
logger.info("введённый год ")

month = input("Введите месяц, за который проводится анализ в формате MM:  ")
i = 0
while i != 1:
    try:
        if datetime.strptime(month, "%m"):
            print(f"Это правильный ввод. Вы ввели {month} месяц")
            i = 1
    except ValueError:
        month = input("Ошибка ввода. Введите месяц в формате MM : ")
logger.info("введённый месяц ")

all_transactions = read_file_2()
transactions_for_service = all_transactions.loc[:, ["Дата платежа", "Сумма платежа", "Категория"]]
logger.info(transactions_for_service)

transactions_for_service = transactions_for_service.to_dict(orient="records")

print(json.loads(profitable_cashbacks(transactions_for_service, year, month)))

##############################################################################################################

logger.info("Определяем Траты по категории")
print("Определяем Траты по категориям")

dates = input("Введите опциональную дату  в формате YYYY-MM-DD  или нажмите Enter для ввода текущей даты :  ")

if dates == "":
    date = str(datetime.now().date())
    # print(type(date))
    print(date)
    dates = datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")
    print(f"Вы ввели {date} текущую дату ")

else:
    i = 0
    while i != 1:
        try:
            if datetime.strptime(dates, "%Y-%m-%d"):
                print(f"Это правильный ввод. Вы ввели {dates} дату ")
                i = 1
        except ValueError:
            dates = input("Ошибка ввода. Введите опциональную дату в формате YYYY-MM-DD  : ")

    logger.info("введённая дата")
    logger.info(dates)

    dates = datetime.strptime(dates, "%Y-%m-%d").strftime("%d.%m.%Y")

filtered_df_count = category(dates)
print(filtered_df_count)
if filtered_df_count is not None:
    print("по какой категории рассчитать траты?")
    cat = input("введите категорию  ")
    print(cat)
    cat = cat.lower()
    cat_lict = []
    for i in filtered_df_count:
        cat_lict.append(i.lower())
    # print(cat_lict)
    while cat not in cat_lict:
        cat = input("Вы ввели не верную категорию, повторите ")
        cat = cat.lower()

    print(f"Определяем Траты по категории {cat}:")

    print(spending_by_category(read_file_2(), cat, dates))


# 2018-01-31 15:44:39
