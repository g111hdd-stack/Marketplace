import logging
import tkinter as tk
import warnings
import pandas as pd

from tkinter import filedialog

from data_classes import DataCostPrice
from database import DbConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=UserWarning)


def select_files():
    db_conn = DbConnection()
    db_conn.start_db()
    file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_paths:
        for file_path in file_paths:
            list_cost_price = process_file(file_path)
            db_conn.add_cost_price(list_cost_price=list_cost_price)


def process_file(path_file):
    headers = {'Месяц': None,
               'Год': None,
               'Артикул': None,
               'Себес': None}

    try:
        df = pd.read_excel(path_file)
        df = df.fillna('')
        logger.info(f'Файл {path_file} прочитан успешно.')

        result_data = []
        data = {}

        for idx, row in df.iterrows():
            try:
                row_data = {}
                for header in headers:
                    if header in df.columns:
                        row_data[header] = row[header]

                month_date = row_data.get('Месяц', None)
                year_date = row_data.get('Год', None)
                vendor_code = row_data.get('Артикул', None)
                cost = row_data.get('Себес', None)
                if month_date:
                    month_date = int(month_date)
                if year_date:
                    year_date = int(year_date)
                if cost:
                    cost = round(float(cost), 2)
                if vendor_code:
                    vendor_code = vendor_code.lower()
                    for size in ['/xs', '/s', '/m', '/м', '/l', '/xl', '/2xl']:
                        if vendor_code.endswith(size):
                            vendor_code = '/'.join(vendor_code.split('/')[:-1])
                            break
                key = (month_date, year_date, vendor_code)
                if key not in data.keys():
                    data[key] = cost
            except Exception:
                continue
        for row, cost in data.items():
            result_data.append(DataCostPrice(month_date=row[0],
                                             year_date=row[1],
                                             vendor_code=row[2],
                                             cost=cost))
        return result_data
    except Exception as e:
        logger.error(f'Ошибка при чтении файла {path_file}: {e}')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Выберите Excel файлы для обработки:")
    select_files()
