import datetime
import logging
from collections import Counter
from datetime import datetime
from typing import Optional
from functools import wraps
import json
import pandas as pd
from dateutil.relativedelta import relativedelta


def report_to_json(filename="my_report.json"):
    """
    Декоратор для записи результатов функции отчета в JSON файл. (filename) (str): Имя файла для сохранения"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обертка для выполнения функции и записи результата в файл.
            """
            result = func(*args, **kwargs)  # Вызываем функцию

            try:
                with open(filename, "w") as f:
                    if isinstance(result, pd.DataFrame):
                        json.dump(result.to_json(), f)
                    else:
                        json.dump(result, f)  # Записываем результат в JSON

            except TypeError as e:
                print(f"Ошибка записи в JSON: {e}")
            return result

        return wrapper

    return decorator


@report_to_json()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = "") -> pd.DataFrame or None:
    """Функция возвращает траты по заданной категории по умолчанию за последние три месяца (от переданной даты)"""

    logger = logging.getLogger("sort_list.py")
    file_handler = logging.FileHandler("../logs/reports.log", "w")
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    logger.info("начало выполнения функции spending_by_category")
    logger.info(transactions)
    logger.info(date)
    logger.info(category)
    logger.info(transactions)

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
    logger.info(" количество дней")
    logger.info((date - new_date).days)
    #
    texts = texts.copy()

    filtered_df = texts[
        (pd.to_datetime(texts["Дата платежа"], dayfirst=True) <= date_start)
        & (pd.to_datetime(texts["Дата платежа"], dayfirst=True) >= date_finish)
    ]
    if len(filtered_df) == 0:
        logger.info("за выбранный период транзакции не проводились")
        return None

    filtered_df = filtered_df.map(lambda s: s.lower() if type(s) == str else s)

    logger.info(filtered_df)

    filtered_df_count = Counter(filtered_df["Категория"])
    logger.info(" за выбранный период были выполнены следующие транзакции (категория:количество транзакций):")
    logger.info(dict(filtered_df_count))
    logger.info(f"всего было выполнено {len(filtered_df_count)} транзакции")

    cat = category
    filtered_df_cat = filtered_df.loc[filtered_df["Категория"] == cat]

    result = round(float(filtered_df_cat["Сумма операции"].sum(axis=0)), 2)

    logger.info("Траты по выбранной категории составили ")
    logger.info(abs(result))
    return filtered_df_cat
