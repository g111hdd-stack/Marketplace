import logging
import warnings
import pandas as pd
import tkinter as tk

from tkinter import filedialog

from database import DbConnection
from data_classes import DataOverseasPurchase

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=UserWarning)


def select_files():
    db_conn = DbConnection()
    db_conn.start_db()

    file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx *.xls")])

    if file_paths:
        for file_path in file_paths:
            list_purchase = process_file(file_path)
            db_conn.add_overseas_purchases(list_purchase=list_purchase)


def process_file(path_file: str):
    headers = {'accrual_date': None,
               'vendor_code': None,
               'quantity': None,
               'ptice_￥': None,
               'logistics_cost_$': None,
               'add_logistics_ru': None}

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

                accrual_date = row_data.get('accrual_date')
                if accrual_date:
                    try:
                        accrual_date = accrual_date.date()
                    except Exception as e:
                        print(accrual_date, e)
                        continue
                else:
                    print('Not date')
                    continue

                vendor_code = row_data.get('vendor_code')
                if vendor_code:
                    vendor_code = vendor_code.strip().lower()
                else:
                    print('Not vendor_code')
                    continue

                quantities = row_data.get('quantity')
                if isinstance(quantities, (float, int)):
                    quantities = int(quantities)
                else:
                    print('Not quantities')
                    continue

                price = row_data.get('ptice_￥')
                if isinstance(price, (float, int)):
                    price = round(float(price), 2)
                else:
                    print('Not price')
                    continue

                log_cost = row_data.get('logistics_cost_$')
                if isinstance(log_cost, (float, int)):
                    log_cost = round(float(log_cost), 2)
                else:
                    print('Not logistics_cost')
                    continue

                log_add_cost = row_data.get('add_logistics_ru')
                if isinstance(log_add_cost, (float, int)):
                    log_add_cost = round(float(log_add_cost), 2)
                else:
                    log_add_cost = 0.00

                result_data.append(DataOverseasPurchase(accrual_date=accrual_date,
                                                        vendor_code=vendor_code,
                                                        quantities=quantities,
                                                        price=price,
                                                        log_cost=log_cost,
                                                        log_add_cost=log_add_cost))
            except Exception as e:
                print(e)
                continue

        print(len(result_data))
        # Агрегирование данных
        aggregate = {}
        for data in result_data:
            key = (data.accrual_date, data.vendor_code)
            if key in aggregate:
                aggregate[key].append((data.quantities, data.price, data.log_cost, data.log_add_cost))
            else:
                aggregate[key] = [(data.quantities, data.price, data.log_cost, data.log_add_cost)]
        result_data = []
        for key, value in aggregate.items():
            accrual_date, vendor_code = key
            quantities = sum([val[0] for val in value])
            price = max([val[1] for val in value])
            log_cost = sum([val[2] for val in value])
            log_add_cost = sum([val[3] for val in value])

            result_data.append(DataOverseasPurchase(accrual_date=accrual_date,
                                                    vendor_code=vendor_code,
                                                    quantities=quantities,
                                                    price=price,
                                                    log_cost=log_cost,
                                                    log_add_cost=log_add_cost))
        print(len(result_data))
        return result_data
    except Exception as e:
        logger.error(f'Ошибка при чтении файла {path_file}: {e}')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Выберите Excel файлы для обработки:")
    select_files()
