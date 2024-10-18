import logging
import warnings
import pandas as pd
import tkinter as tk

from tkinter import filedialog

from database import DbConnection
from data_classes import DataSelfPurchase

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=UserWarning)


def select_files():
    db_conn = DbConnection()
    db_conn.start_db()

    file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx *.xls")])

    if file_paths:
        for file_path in file_paths:
            list_self_purchase = process_file(db_conn, file_path)
            db_conn.add_self_purchase(list_self_purchase=list_self_purchase)


def process_file(db_conn: DbConnection, path_file: str):
    headers = {'Дата Заказа: ': None,
               'Дата забора:': None,
               'ИП': None,
               'Артикул': None,
               'К-во товара': None,
               'Цена': None,
               'МП': None}

    try:
        df = pd.read_excel(path_file)
        df = df.fillna('')
        logger.info(f'Файл {path_file} прочитан успешно.')

        clients = db_conn.get_clients()
        clients_ids = {
            (client.entrepreneur.lower(), client.marketplace.lower()): client.client_id for client in clients
        }

        result_data = []

        for idx, row in df.iterrows():
            try:
                row_data = {}
                for header in headers:
                    if header in df.columns:
                        row_data[header] = row[header]

                entrepreneur = row_data.get('ИП')
                marketplace = row_data.get('МП')
                if entrepreneur and marketplace:
                    client_id = clients_ids.get((entrepreneur.strip().lower(), marketplace.strip().lower()))
                    if not client_id:
                        print('Not client_id')
                        continue
                else:
                    print('Not client')
                    continue

                order_date = row_data.get('Дата Заказа: ')
                accrual_date = row_data.get('Дата забора:')
                if order_date and accrual_date:
                    try:
                        order_date = order_date.date()
                        accrual_date = accrual_date.date()
                    except Exception as e:
                        print(order_date, accrual_date, e)
                        continue
                else:
                    print('Not date')
                    continue

                vendor_code = row_data.get('Артикул')
                if vendor_code:
                    vendor_code = vendor_code.strip().lower()
                else:
                    print('Not vendor_code')
                    continue

                quantities = row_data.get('К-во товара')
                if isinstance(quantities, (float, int)):
                    quantities = int(quantities)
                else:
                    print('Not quantities')
                    continue

                price = row_data.get('Цена')
                if isinstance(price, (float, int)):
                    price = round(float(price), 2)
                else:
                    print('Not price')
                    continue
                result_data.append(DataSelfPurchase(client_id=client_id,
                                                    order_date=order_date,
                                                    accrual_date=accrual_date,
                                                    vendor_code=vendor_code,
                                                    quantities=quantities,
                                                    price=price))
            except Exception as e:
                print(e)
                continue

        print(len(result_data))
        # Агрегирование данных
        aggregate = {}
        for data in result_data:
            key = (
                data.client_id,
                data.order_date,
                data.accrual_date,
                data.vendor_code,
                data.price
            )
            if key in aggregate:
                aggregate[key] += data.quantities
            else:
                aggregate[key] = data.quantities
        result_data = []
        for key, quantities in aggregate.items():
            client_id, order_date, accrual_date, vendor_code, price = key
            result_data.append(DataSelfPurchase(client_id=client_id,
                                                order_date=order_date,
                                                accrual_date=accrual_date,
                                                vendor_code=vendor_code,
                                                quantities=quantities,
                                                price=price))
        print(len(result_data))
        return result_data
    except Exception as e:
        logger.error(f'Ошибка при чтении файла {path_file}: {e}')


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    print("Выберите Excel файлы для обработки:")
    select_files()
