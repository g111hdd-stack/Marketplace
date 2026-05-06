import asyncio
import logging
import nest_asyncio

from datetime import datetime, timezone, timedelta

from sqlalchemy.exc import OperationalError

from wb_sdk.wb_api import WBApi
from database import WBDbConnection
from wb_sdk.errors import ClientError

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

async def get_chats(
        db_conn: WBDbConnection, client_id: str, api_key: str, today: datetime) -> list[tuple[str, str, int]]:
    list_chats = []
    from_timestamp = int(today.timestamp() * 1000)

    skus = db_conn.get_wb_sku_vendor_code(client_id=client_id, new=False)

    mes = ('Здравствуйте. Вы оставили отзыв с низкой оценкой. '
           'Давайте обсудим, что не так с товаром. '
           'Пожалуйста, расскажите подробно: попробую решить проблему')

    api_user = WBApi(api_key=api_key)

    answer_chats = await api_user.get_chats()

    result = answer_chats.result

    if result:
        for row in result:
            if row.lastMessage:
                message = row.lastMessage.text
                timestamp = row.lastMessage.addTimestamp

                if message == mes and timestamp >= from_timestamp:
                    vendor_code = skus.get(str(row.goodCard.nmID))

                    if vendor_code:
                        list_chats.append((row.replySign, vendor_code, timestamp))

    logger.info(f"Количество чатов для ответа: {len(list_chats)}")

    return list_chats


async def post_chats(api_key: str, chats: list[tuple[str, str, int]]) -> None:
    mes = ('Данное сообщение отправлено автоматически. '
           'Пожалуйста, не отвечайте на него. '
           'Если Вы считаете, что получили сообщение по ошибке, просто удалите или проигнорируйте его.')

    api_user = WBApi(api_key=api_key)

    for chat, vendor_code, timestamp in chats:
        msk = timezone(timedelta(hours=3))
        dt = datetime.fromtimestamp(timestamp / 1000, tz=msk)

        logger.info(f"Ответ по отзыву на {vendor_code} за {dt} отправлен")
        answer_chats = await api_user.get_message(reply_sign=chat, message=mes)

        if answer_chats and answer_chats.result:
            logger.info(f"Ответ по отзыву на {vendor_code} за {dt} отправлен")
        elif answer_chats and answer_chats.errors:
            logger.error(f"Ответ не отправлен: {answer_chats.errors}")
        else:
            logger.error(f"Ответ не отправлен: Неизвестная ошибка")


async def main_wb_chats(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="WB")

        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        for client in clients[10:11]:
            negative_client = db_conn.get_wb_negative(client_id=client.client_id)

            if not negative_client or not negative_client.work:
                continue

            negative_api_key = negative_client.api_key

            try:
                logger.info(f"Поиск чатов по негативам для компании: {client.name_company}")

                chats = await get_chats(db_conn=db_conn,
                                        client_id=client.client_id,
                                        api_key=client.api_key,
                                        today=today)

                await post_chats(api_key=negative_api_key, chats=chats)
            except ClientError as e:
                logger.error(f'{e}')
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_chats(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_chats())
    loop.stop()
