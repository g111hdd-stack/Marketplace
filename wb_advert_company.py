import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

from data_classes import DataWBAdvert, DataWBProductCard, DataWBStatisticAdvert, DataWBStatisticCardProduct
from wb_sdk.wb_api import WBApi
from database import WBDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_adverts(db_conn: WBDbConnection, client_id: str, api_key: str, date: datetime) -> None:
    """
        Обновление записей в таблице `wb_adverts_table` за указанную дату.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date (date): Дата, за которую обновилсь данные кампании.
    """

    def format_date(date_format: str) -> datetime.date:
        time_format = "%Y-%m-%d"
        return datetime.strptime(date_format.split('T')[0], time_format).date()

    date = date.date()
    api_user = WBApi(api_key=api_key)
    adverts_list = []
    status_dict = {
        7: 'Кампания завершена',
        9: 'Идут показы',
        11: 'Кампания на паузе',
    }
    type_dict = {
        4: 'Кампания  в каталоге',
        5: 'Кампания в карточке товара',
        6: 'Кампания в поиске',
        7: 'Кампания в рекомендациях на главной странице',
        8: 'Автоматическая кампания',
        9: 'Поиск + каталог'
    }

    for status in status_dict.keys():
        for type_field in type_dict.keys():
            answer_advent = await api_user.get_promotion_adverts(status=status, type_field=type_field)
            if answer_advent:
                for advert in answer_advent.result:
                    create_time = format_date(date_format=advert.createTime)
                    change_time = format_date(date_format=advert.changeTime)
                    start_time = format_date(date_format=advert.startTime)
                    end_time = format_date(date_format=advert.endTime)
                    if change_time >= date:
                        adverts_list.append(DataWBAdvert(id_advert=advert.advertId,
                                                         id_type=advert.type,
                                                         id_status=advert.status,
                                                         name_advert=advert.name,
                                                         create_time=create_time,
                                                         change_time=change_time,
                                                         start_time=start_time,
                                                         end_time=end_time))

    logger.info(f"Обновление информации о рекламных компаний")
    db_conn.add_wb_adverts(client_id=client_id, adverts_list=adverts_list)


async def get_product_card(db_conn: WBDbConnection, client_id: str, api_key: str, offset: int = 0) \
        -> list[DataWBProductCard]:
    """
        Получение карточек товара.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            offset (int, optional): Страница товаров.. Default to 0.

        Returns:
            List[DataWBProductCard]: Список карточек товаров.
    """
    api_user = WBApi(api_key=api_key)
    product_list = []
    answer = await api_user.get_list_goods_filter(limit=1000, offset=offset)
    if answer:
        if answer.data:
            for product in answer.data.listGoods:

                price = round(product.sizes[0].price, 2)
                discount_price = round(product.sizes[0].discountedPrice, 2)
                product_list.append(DataWBProductCard(sku=str(product.nmID),
                                                      vendor_code=product.vendorCode,
                                                      client_id=client_id,
                                                      price=price,
                                                      discount_price=discount_price))
            if len(answer.data.listGoods) >= 1000:
                extend_answer = await get_product_card(db_conn=db_conn,
                                                       client_id=client_id,
                                                       api_key=api_key,
                                                       offset=offset + 1000)
                product_list.extend(extend_answer)

    logger.info(f"Обновление информации о карточках товаров")
    return product_list


async def add_statistic_adverts(db_conn: WBDbConnection, client_id: str, api_key: str, date: datetime) -> \
        list[DataWBStatisticAdvert]:
    """
        Добавление записей в таблицу `wb_statistic_advert` за указанную дату

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date (datetime): Дата, для которой добавляются записи.

        Returns:
                List[DataWBStatisticAdvert]: Список статистики рекламных компаний, удовлетворяющих условию фильтрации.
    """
    company_ids = db_conn.get_wb_adverts_id(client_id=client_id, from_date=date.date())

    if not company_ids:
        logger.info(f"Количество записей: 0")
        return []

    api_user = WBApi(api_key=api_key)
    product_advertising_campaign = []
    app_type = {
        1: 'Сайт',
        32: 'Android',
        64: 'IOS'
    }

    for ids in [company_ids[i:i+100] for i in range(0, len(company_ids), 100)]:
        answer = await api_user.get_fullstats(company_ids=ids, dates=[date.date().isoformat()])
        if answer:
            for advert in answer.result:
                for day in advert.days:
                    for app in day.apps:
                        for position in app.nm:
                            product_advertising_campaign.append(DataWBStatisticAdvert(client_id=client_id,
                                                                                      date=day.date_field,
                                                                                      views=position.views,
                                                                                      clicks=position.clicks,
                                                                                      ctr=round(position.ctr / 100, 2),
                                                                                      cpc=position.cpc,
                                                                                      sum_cost=position.sum,
                                                                                      atbs=position.atbs,
                                                                                      orders_count=position.orders,
                                                                                      shks=position.shks,
                                                                                      sum_price=position.sum_price,
                                                                                      nm_id=str(position.nmId),
                                                                                      advert_id=advert.advertId,
                                                                                      app_type=app_type.get(app.appType, '')))

    logger.info(f"Количество записей: {len(product_advertising_campaign)}")

    db_conn.add_wb_adverts_statistics(client_id=client_id, product_advertising_campaign=product_advertising_campaign)


async def get_statistic_product_card(client_id: str,
                                     api_key: str,
                                     date_from: datetime,
                                     buyouts_percent: dict,
                                     page: int = 1) -> list[DataWBStatisticCardProduct]:
    """
        Получение списка статистики карточек товара за указанную дату.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date_from (datetime): Дата, за которую собираются данные.
            buyouts_percent (dict): Словарь sku с процентом выкупа за последнии 30 дней.
            page (int, optional): Номер страницы запроса.. Default to 1.

        Returns:
                List[DataWBStatisticCardProduct]: Список статистики карточек товара, удовлетворяющих условию фильтрации.
    """
    api_user = WBApi(api_key=api_key)
    list_card_product = []
    date_from = date_from.replace(hour=0, minute=0, second=0, microsecond=0)
    date_to = (date_from + timedelta(days=1)) - timedelta(microseconds=1)
    answer = await api_user.get_nm_report_detail(date_from=date_from.isoformat(sep=" "),
                                                 date_to=date_to.isoformat(sep=" "),
                                                 page=page)
    if answer:
        if answer.data:
            for card in answer.data.cards:
                stat = card.statistics.selectedPeriod
                stocks = (card.stocks.stocksMp + card.stocks.stocksWb) < 10
                open_card_count = int(stat.openCardCount)
                add_to_cart_count = int(stat.addToCartCount)
                orders_count = int(stat.ordersCount)
                add_to_cart_percent = round(stat.conversions.addToCartPercent / 100, 2)
                cart_to_order_percent = round(stat.conversions.cartToOrderPercent / 100, 2)
                buyouts_count = int(stat.buyoutsCount)

                if not open_card_count and not add_to_cart_count and not orders_count and stocks:
                    continue
                list_card_product.append(DataWBStatisticCardProduct(sku=str(card.nmID),
                                                                    vendor_code=card.vendorCode,
                                                                    client_id=client_id,
                                                                    category=card.object.name,
                                                                    brand=card.brandName,
                                                                    link=f"https://www.wildberries.ru/catalog/{card.nmID}/detail.aspx",
                                                                    date=date_from.date(),
                                                                    open_card_count=open_card_count,
                                                                    add_to_cart_count=add_to_cart_count,
                                                                    orders_count=orders_count,
                                                                    add_to_cart_percent=add_to_cart_percent,
                                                                    cart_to_order_percent=cart_to_order_percent,
                                                                    buyouts_count=buyouts_count,
                                                                    buyouts_last_30days_percent=buyouts_percent.get(card.nmID, None)))
            if answer.data.isNextPage:
                extend_card_product = await get_statistic_product_card(client_id=client_id,
                                                                       api_key=api_key,
                                                                       date_from=date_from,
                                                                       buyouts_percent=buyouts_percent,
                                                                       page=page + 1)
                list_card_product.extend(extend_card_product)

    logger.info(f"Количество записей: {len(list_card_product)}")
    return list_card_product


async def get_buyouts_percent(client_id: str, api_key: str, date_from: datetime, page: int = 1) -> dict:
    """
        Получение словаря sku с процентом выкупа за последнии 30 дней.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date_from (datetime): Дата, за которую собираются данные.
            page (int, optional): Номер страницы запроса.. Default to 1.

        Returns:
                dict: Словарь sku с процентом выкупа за последнии 30 дней.
    """
    api_user = WBApi(api_key=api_key)
    buyouts_percent = dict()
    date_from = date_from.replace(hour=0, minute=0, second=0, microsecond=0)
    date_from_30days = date_from - timedelta(days=29)
    date_to = (date_from + timedelta(days=1)) - timedelta(microseconds=1)

    answer_last_30days = await api_user.get_nm_report_detail(date_from=date_from_30days.isoformat(sep=" "),
                                                             date_to=date_to.isoformat(sep=" "),
                                                             page=page)
    if answer_last_30days:
        if answer_last_30days.data:
            for card in answer_last_30days.data.cards:
                buyouts_percent[card.nmID] = round(card.statistics.selectedPeriod.conversions.buyoutsPercent / 100, 2)
            if answer_last_30days.data.isNextPage:
                update_dict = await get_buyouts_percent(client_id=client_id,
                                                        api_key=api_key,
                                                        date_from=date_from,
                                                        page=page + 1)
                buyouts_percent.update(update_dict)
    return buyouts_percent


async def main_wb_advert(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="WB")
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date_yesterday = date - timedelta(days=1)

        for client in clients:
            logger.info(f"Сбор карточек товаров {client.name_company}")
            card_products_list = await get_product_card(db_conn=db_conn,
                                                        client_id=client.client_id,
                                                        api_key=client.api_key)
            db_conn.add_wb_cards_products(client_id=client.client_id, list_card_product=card_products_list)

            logger.info(f"Сбор рекламных компаний {client.name_company}")
            await add_adverts(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key, date=date_yesterday)

            logger.info(f"Статистика карточек товара {client.name_company} за {date_yesterday.date().isoformat()}")
            buyouts_percent = await get_buyouts_percent(client_id=client.client_id,
                                                        api_key=client.api_key,
                                                        date_from=date_yesterday)
            list_card_product = await get_statistic_product_card(client_id=client.client_id,
                                                                 api_key=client.api_key,
                                                                 date_from=date_yesterday,
                                                                 buyouts_percent=buyouts_percent)
            db_conn.add_wb_cards_products_statistics(client_id=client.client_id, list_card_product=list_card_product)

            logger.info(f"Статистика рекламы {client.name_company} за {date_yesterday.date().isoformat()}")
            await add_statistic_adverts(db_conn=db_conn,
                                        client_id=client.client_id,
                                        api_key=client.api_key,
                                        date=date_yesterday)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_advert(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_advert())
    loop.stop()
