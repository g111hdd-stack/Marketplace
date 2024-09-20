import logging
import tkinter as tk
import warnings
import pandas as pd

from datetime import datetime
from tkinter import filedialog

from data_classes import DataOzStorage
from database import OzDbConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=UserWarning)


def select_files():
    db_conn = OzDbConnection()
    db_conn.start_db()

    file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx *.xls")])

    if file_paths:
        for file_path in file_paths:
            list_storage = process_file(file_path)
            db_conn.add_storage_entry(list_storage=list_storage)


def process_file(path_file):
    headers = {'Дата': None,
               'SKU': None,
               'Начисленная стоимость размещения': None}

    try:
        df = pd.read_excel(path_file)
        df = df.fillna('')
        logger.info(f'Файл {path_file} прочитан успешно.')

        result_data = []

        for idx, row in df.iterrows():
            try:
                row_data = {}
                for header in headers:
                    if header in df.columns:
                        row_data[header] = row[header]

                accrual_date = row_data.get('Дата', None)
                sku = row_data.get('SKU', None)
                cost = row_data.get('Начисленная стоимость размещения', None)
                if sku:
                    sku = str(sku)
                if accrual_date is not None:
                    accrual_date = datetime.strptime(str(accrual_date), '%Y-%m-%d %H:%M:%S').date()
                if cost is not None:
                    cost = round(float(cost), 2)
                    if cost:
                        result_data.append(DataOzStorage(date=accrual_date,
                                                         sku=sku,
                                                         cost=cost))
            except Exception:
                continue

        # Агрегирование данных
        aggregate = {}
        for data in result_data:
            key = (
                data.date,
                data.sku
            )
            if key in aggregate:
                aggregate[key] += data.cost
            else:
                aggregate[key] = data.cost
        result_data = []
        for key, cost in aggregate.items():
            date, sku = key
            result_data.append(DataOzStorage(date=date,
                                             sku=sku,
                                             cost=cost))
        return result_data
    except Exception as e:
        logger.error(f'Ошибка при чтении файла {path_file}: {e}')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Выберите Excel файлы для обработки:")
    select_files()
