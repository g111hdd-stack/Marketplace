import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

from data_classes import DataWBStorage
from wb_sdk.wb_api import WBApi
from database import WBDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_storage(client_id: str, api_key: str, from_date: str, to_date: str):
    def format_date(date_format: str) -> datetime.date:
        time_format = "%Y-%m-%d"
        return datetime.strptime(date_format.split('T')[0], time_format).date()

    list_storage = []
    api_user = WBApi(api_key=api_key)
    answer = await api_user.get_paid_storage(date_from=from_date, date_to=to_date)
    if answer:
        task_id = answer.data.taskId

        while True:
            await asyncio.sleep(5)
            answer_status = await api_user.get_paid_storage_status(task_id=task_id)
            if answer_status:
                if answer_status.data.status == 'done':
                    break
                elif answer_status.data.status == 'canceled':
                    logger.info(f"Отчет отменен")
                    return list_storage

        answer_download = await api_user.get_paid_storage_download(task_id=task_id)
        if answer_download:
            for storage in answer_download.result:
                list_storage.append(DataWBStorage(client_id=client_id,
                                                  date=format_date(storage.date),
                                                  vendor_code=storage.vendorCode,
                                                  sku=str(storage.nmId),
                                                  calc_type=storage.calcType,
                                                  cost=round(float(storage.warehousePrice), 2)))
        else:
            logger.error(f"Ошибка ответа или пустой отчет {answer_download}")
    logger.info(f"Количсетво строк: {len(list_storage)}")
    return list_storage


async def main_wb_storage(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="WB")
        from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        to_date = from_date + timedelta(days=1) - timedelta(microseconds=1)
        for client in clients:
            logger.info(f'Сбор информации о хранении маназина {client.name_company} за дату {from_date.date().isoformat()}')
            list_storage = await get_storage(client_id=client.client_id,
                                             api_key=client.api_key,
                                             from_date=from_date.isoformat(),
                                             to_date=to_date.isoformat())
            db_conn.add_wb_storage_entry(client_id=client.client_id, list_storage=list_storage)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_storage(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_storage())
    loop.stop()
