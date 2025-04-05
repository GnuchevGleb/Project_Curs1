import pandas as pd
import datetime
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter
from typing import Optional


def spending_by_category(transactions: pd.DataFrame, date: Optional[str] = "") -> pd.DataFrame or None:
    """Функция возвращает траты по заданной категории по умолчанию за последние три месяца (от переданной даты)"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/reports", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции spending_by_category")
    logger.info(transactions)
    logger.info(date)

    if date == "":

        date = datetime.now()
        print(type(date))
        print(f"Вы ввели {date} текущую дату ")
    else:
        try:
            # преобразуем строку в объект datetime
            date = datetime.strptime(date, "%d.%m.%Y")

        except ValueError:
            print("дата введена некорректно")
            date = input("введите опциональную дату в формате <<день.месяц.год>> - ")
            i = 0
            while i != 1:
                try:
                    if datetime.strptime(date, "%d.%m.%Y"):
                        print(f"Это правильный ввод. Вы ввели {date} год")
                        i = 1
                except ValueError:
                    date = input("Ошибка ввода. Введите дату в формате <<день.месяц.год>> : ")

            date = datetime.strptime(date, "%d.%m.%Y")

    texts = transactions

    logger.info(date)

    date_start = date
    date_start = pd.to_datetime(date_start, dayfirst=True)

    logger.info(date_start)

    new_date = date - relativedelta(months=3)
    date_finish = new_date.strftime("%d.%m.%Y")
    date_finish = pd.to_datetime(date_finish, dayfirst=True)
    logger.info(date_finish)

    print((date - new_date).days, " количество дней")

    texts = texts.copy()

    filtered_df = texts[
        (pd.to_datetime(texts["Дата платежа"], dayfirst=True) <= date_start)
        & (pd.to_datetime(texts["Дата платежа"], dayfirst=True) >= date_finish)
    ]
    if len(filtered_df) == 0:
        print("за выбранный период транзакции не проводились")
        return None

    filtered_df = filtered_df.map(lambda s: s.lower() if type(s) == str else s)

    print(filtered_df)

    filtered_df_count = Counter(filtered_df["Категория"])
    print(" за выбранный период были выполнены следующие транзакции (категория:количество транзакций):")
    print(dict(filtered_df_count))
    print(f"всего было выполнено {len(filtered_df_count)} транзакции")

    print("по какой категории рассчитать траты?")
    cat = input("введите категорию  ")
    cat = cat.lower()
    cat_lict = []
    for i in filtered_df_count:
        cat_lict.append(i.lower())
    print(cat_lict)
    while cat not in cat_lict:
        cat = input("Вы ввели не верную категорию, повторите ")
        cat = cat.lower()

    filtered_df_cat = filtered_df.loc[filtered_df["Категория"] == cat]

    result = round(float(filtered_df_cat["Сумма операции"].sum(axis=0)), 2)
    print("Траты по выбранной категории составили ", abs(result))
    return filtered_df_cat
