import asyncio
import logging

import nest_asyncio

from datetime import timedelta, date

from sqlalchemy.exc import OperationalError

from database import OzDbConnection
from ozon_sdk.ozon_api import OzonApi
from data_classes import DataOzBonus
from ozon_sdk.errors import ClientError

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_oz_bonus(db_conn: OzDbConnection, client_id: str, api_key: str) -> None:
    """
        Добавление записей в таблицу `oz_bonus` за прошлый месяц.

        Args:
            db_conn (OzDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """

    from_date = date.today().replace(day=1) - timedelta(days=1)
    month = from_date.month
    year = from_date.year

    logger.info(f"За {month} месяц {year}")

    list_bonus = []
    dict_sku = db_conn.get_oz_sku_vendor_code(client_id=client_id)

    # Инициализация API-клиента Ozon
    api_user = OzonApi(client_id=client_id, api_key=api_key)
    # Получение списка отчёта о реализации
    answer = await api_user.get_finance_realization(month=month, year=year)

    # Обработка полученных результатов
    for row in answer.result.rows:
        vendor_code = row.item.offer_id

        sku = str(row.item.sku)
        if sku not in dict_sku:
            answer_info = await api_user.get_product_info_discounted(discounted_skus=[sku])
            for info in answer_info.items:
                if sku == str(info.discounted_sku):
                    sku = str(info.sku)
                    break
        if sku not in dict_sku:
            answer_info = await api_user.get_product_related_sku_get(skus=[sku])
            for info in answer_info.items:
                if str(info.sku) in dict_sku:
                    sku = str(info.sku)
                    break

        bonus = 0
        amount = 0
        bank_coinvestment = 0

        if row.delivery_commission:
            bonus += row.delivery_commission.bonus
            amount += row.delivery_commission.amount
            bank_coinvestment += row.delivery_commission.bank_coinvestment or 0
        if row.return_commission:
            bonus -= row.return_commission.bonus
            amount -= row.return_commission.amount
            bank_coinvestment -= row.return_commission.bank_coinvestment or 0

        list_bonus.append(DataOzBonus(date=from_date,
                                      client_id=client_id,
                                      sku=sku,
                                      vendor_code=vendor_code,
                                      bonus=bonus,
                                      amount=amount,
                                      bank_coinvestment=bank_coinvestment))

    # Агрегирование данных
    aggregate = {}
    for row in list_bonus:
        key = (
            row.date,
            row.client_id,
            row.sku,
            row.vendor_code,
        )
        if key in aggregate:
            aggregate[key].append((row.bonus, row.amount, row.bank_coinvestment))
        else:
            aggregate[key] = [(row.bonus, row.amount, row.bank_coinvestment)]
    list_bonus = []
    for key, value in aggregate.items():
        field_date, client_id, sku, vendor_code = key
        bonus = round(sum([val[0] for val in value]), 2)
        amount = round(sum([val[1] for val in value]), 2)
        bank_coinvestment = round(sum([val[2] for val in value]), 2)

        list_bonus.append(DataOzBonus(date=field_date,
                                      client_id=client_id,
                                      sku=sku,
                                      vendor_code=vendor_code,
                                      bonus=bonus,
                                      amount=amount,
                                      bank_coinvestment=bank_coinvestment))

    logger.info(f'Количество записей: {len(list_bonus)}')
    db_conn.add_oz_bonus_entry(list_bonus=list_bonus)


async def main_oz_bonus(retries: int = 6) -> None:
    try:
        db_conn = OzDbConnection()

        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="Ozon")

        for client in clients:
            try:
                logger.info(f"Добавление в базу данных компании '{client.name_company}'")
                await add_oz_bonus(db_conn=db_conn,
                                   client_id=client.client_id,
                                   api_key=client.api_key)
            except ClientError as e:
                logger.error(f'{e}')
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_oz_bonus(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_oz_bonus())
    loop.stop()
