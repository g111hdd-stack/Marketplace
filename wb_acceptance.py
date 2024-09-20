import asyncio
import logging

import nest_asyncio

from datetime import datetime, timedelta

from sqlalchemy.exc import OperationalError

from wb_sdk.wb_api import WBApi
from database import WBDbConnection
from data_classes import DataWBAcceptance

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_acceptance(db_conn: WBDbConnection, client_id: str, api_key: str, from_date: str, to_date: str) -> None:
    """
        Получает список расходов по приёмке товара для указанного клиента за определенный период времени.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            from_date (str): Начальная дата периода (В формате строки).
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.
            to_date (str): Конечная дата периода (В формате строки).
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.
    """

    list_acceptance = []

    # Инициализация API-клиента WB
    api_user = WBApi(api_key=api_key)

    # Получение отчёта по приёмке товара
    answer = await api_user.get_analytics_acceptance_report(date_from=from_date, date_to=to_date)

    # Обработка полученных результатов
    for acceptance in answer.report:
        list_acceptance.append(DataWBAcceptance(client_id=client_id,
                                                date=acceptance.shkCreateDate,
                                                sku=str(acceptance.nmID),
                                                cost=round(acceptance.total, 2)))

    # Агрегирование данных
    aggregate = {}
    for row in list_acceptance:
        key = (
            row.client_id,
            row.date,
            row.sku
        )
        if key in aggregate:
            aggregate[key] += row.cost
        else:
            aggregate[key] = row.cost
    list_acceptance = []
    for key, cost in aggregate.items():
        client_id, date, sku = key
        list_acceptance.append(DataWBAcceptance(client_id=client_id,
                                                date=date,
                                                sku=sku,
                                                cost=cost))

    logger.info(f"Количсетво строк: {len(list_acceptance)}")
    db_conn.add_wb_acceptance_entry(client_id=client_id, list_acceptance=list_acceptance)


async def main_wb_acceptance(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()

        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="WB")

        date_now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_date = date_now - timedelta(days=1)
        to_date = date_now - timedelta(microseconds=1)

        for client in clients:
            logger.info(f'Сбор информации о приёмке товара маназина {client.name_company} '
                        f'за дату {from_date.date().isoformat()}')
            await add_acceptance(db_conn=db_conn,
                                 client_id=client.client_id,
                                 api_key=client.api_key,
                                 from_date=from_date.isoformat(),
                                 to_date=to_date.isoformat())
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_acceptance(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_acceptance())
    loop.stop()
