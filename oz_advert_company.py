import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, date
from sqlalchemy.exc import OperationalError
from pyodbc import Error

from data_classes import DataOzProductCard, DataOzStatisticCardProduct, DataOzAdvert, DataOzStatisticAdvert
from ozon_sdk.ozon_api import OzonApi, OzonPerformanceAPI
from database import OzDbConnection, Client

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_adverts(db_conn: OzDbConnection, client_id: str, performance_id: str, client_secret: str,
                      from_date: date) -> None:
    """
        Обновление записей в таблице `oz_adverts_table` за указанную дату.

        Args:
            db_conn (OzDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            performance_id (str): ID рекламного кабинета.
            client_secret (str): SECRET KEY рекламного кабинета.
            from_date (date): Дата, за которую обновилсь данные кампании.
    """
    time_format = "%Y-%m-%d"
    adverts_list = []
    adverts_daily_budget = dict()
    api_user = OzonPerformanceAPI(client_id=performance_id, client_secret=client_secret)
    answer = await api_user.get_client_campaign()
    if answer:
        for advert in answer.list_field:
            if float(advert.dailyBudget) and advert.advObjectType == 'SKU':
                adverts_daily_budget[advert.id_field] = round(float(advert.dailyBudget) / 1000000, 2)
            create_time = advert.createdAt.date()
            change_time = advert.updatedAt.date()
            start_time = None
            end_time = None
            if advert.fromDate:
                start_time = datetime.strptime(advert.fromDate, time_format).date()
            if advert.toDate:
                end_time = datetime.strptime(advert.toDate, time_format).date()
            if change_time >= from_date:
                adverts_list.append(DataOzAdvert(id_advert=int(advert.id_field),
                                                 field_type=advert.advObjectType,
                                                 field_status=advert.state,
                                                 name_advert=advert.title,
                                                 create_time=create_time,
                                                 change_time=change_time,
                                                 start_time=start_time,
                                                 end_time=end_time))

    logger.info(f"Обновление информации о рекламных компаний")
    db_conn.add_oz_adverts(client_id=client_id, adverts_list=adverts_list)
    company_ids = db_conn.get_oz_adverts_id(client_id=client_id, date=from_date)
    daily_budget = {advert_id: budget for advert_id, budget in adverts_daily_budget.items() if advert_id in company_ids}
    db_conn.add_oz_advert_daily_budget(date=from_date, adverts_daily_budget=daily_budget)


async def get_products_ids(client_id: str, api_key: str) -> list[int]:
    """
        Получения списка ID товаров.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.

        Returns:
            List[int]: Список ID товаров.
    """
    list_product_ids = []
    api_user = OzonApi(client_id=client_id, api_key=api_key)
    last_id = None
    total = 1000
    while total >= 1000:
        answer = await api_user.get_product_list(limit=1000, last_id=last_id)
        if answer:
            if answer.result:
                for item in answer.result.items:
                    list_product_ids.append(item.product_id)
                total = answer.result.total
                last_id = answer.result.last_id
    return list_product_ids


async def add_card_products(db_conn: OzDbConnection, client_id: str, api_key: str) -> None:
    """
        Обновление записей в таблице `oz_card_product` за указанную дату.

        Args:
            db_conn (OzDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """
    list_card_product = []
    list_product_ids = await get_products_ids(client_id=client_id, api_key=api_key)

    api_user = OzonApi(client_id=client_id, api_key=api_key)
    for ids in [list_product_ids[i:i + 100] for i in range(0, len(list_product_ids), 100)]:
        answer = await api_user.get_product_info_list(product_id=ids)
        attributes = await api_user.get_products_info_attributes(product_id=[str(product) for product in ids],
                                                                 limit=1000)
        if answer:
            if answer.result:
                for item in answer.result.items:
                    vendor_code = item.offer_id
                    brand = None
                    category = None
                    if attributes:
                        if attributes.result:
                            for product in attributes.result:
                                if product.id_field == item.id_field:
                                    for attribute in product.attributes:
                                        if attribute.attribute_id == 8229:
                                            category = attribute.values[0].value
                                        elif attribute.attribute_id == 85:
                                            brand = attribute.values[0].value
                    price = round(float(item.old_price), 2)
                    discount_price = round(float(item.price), 2)
                    for sku in [item.sku, item.fbo_sku, item.fbs_sku]:
                        if sku:
                            link = f"https://www.ozon.ru/product/{sku}"
                            list_card_product.append(DataOzProductCard(sku=str(sku),
                                                                       client_id=client_id,
                                                                       vendor_code=vendor_code,
                                                                       brand=brand,
                                                                       category=category,
                                                                       link=link,
                                                                       price=price,
                                                                       discount_price=discount_price))
    logger.info(f"Обновление информации о карточках товаров")

    db_conn.add_oz_cards_products(client_id=client_id, list_card_product=list_card_product)


async def get_statistics_card_products(db_conn: OzDbConnection, client_id: str, api_key: str, date_from: date,
                                       offset: int = 0) -> list[DataOzStatisticCardProduct]:
    """
        Получение списка статистики карточек товара за указанную дату.

        Args:
            db_conn (OzDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date_from (datetime): Дата, за которую собираются данные.
            offset (int, optional): Количество элементов, которое будет пропущено в ответе.

        Returns:
                List[DataWBStatisticCardProduct]: Список статистики карточек товара, удовлетворяющих условию фильтрации.
    """
    list_statistics_card_products = []
    metrics = [
        'ordered_units',
        'revenue',
        'hits_tocart_search',
        'hits_tocart_pdp',
        'session_view_search',
        'session_view_pdp',
        'conv_tocart_search',
        'conv_tocart_pdp',
    ]
    api_user = OzonApi(client_id=client_id, api_key=api_key)
    answer = await api_user.get_analytics_data(date_from=date_from.isoformat(),
                                               date_to=date_from.isoformat(),
                                               dimension=['sku'],
                                               limit=1000,
                                               metrics=metrics,
                                               offset=offset)
    if answer:
        if answer.result:
            list_sku = db_conn.get_oz_sku_card_product(client_id=client_id)
            for product in answer.result.data:
                sku = str(product.dimensions[0].id_field)
                if sku not in list_sku:
                    continue
                metrics_round = [round(metric, 2) for metric in product.metrics]
                if len(metrics_round) < len(metrics):
                    logger.error(f"Статистика не доступна из-за отсутсвия Премиума")
                    break
                if not sum(metrics_round):
                    continue
                data = dict(zip(metrics, metrics_round))
                list_statistics_card_products.append(DataOzStatisticCardProduct(sku=sku,
                                                                                date=date_from,
                                                                                orders_count=int(data.get('ordered_units')),
                                                                                add_to_cart_from_search_count=int(data.get('hits_tocart_search')),
                                                                                add_to_cart_from_card_count=int(data.get('hits_tocart_pdp')),
                                                                                view_search=int(data.get('session_view_search')),
                                                                                view_card=int(data.get('session_view_pdp')),
                                                                                add_to_cart_from_search_percent=data.get('conv_tocart_search'),
                                                                                add_to_cart_from_card_percent=data.get('conv_tocart_pdp')))
            if len(answer.result.data) >= 1000:
                extend_statistics_card_products = await get_statistics_card_products(db_conn=db_conn,
                                                                                     client_id=client_id,
                                                                                     api_key=api_key,
                                                                                     date_from=date_from,
                                                                                     offset=offset + 1000)
                list_statistics_card_products.extend(extend_statistics_card_products)

    logger.info(f"Количество записей: {len(list_statistics_card_products)}")
    return list_statistics_card_products


async def add_statistic_adverts(db_conn: OzDbConnection, client_id: str, performance_id: str, client_secret: str,
                                from_date: date) -> None:
    """
        Добавление статистики карточек товара за указанную дату.

        Args:
            db_conn (OzDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            performance_id (str): ID рекламного кабинета.
            client_secret (str): SECRET KEY рекламного кабинета кабинета.
            from_date (date): Дата, за которую собираются данные.
    """
    list_statistics_advert = []
    company_ids = db_conn.get_oz_adverts_id(client_id=client_id, date=from_date)
    if not company_ids:
        return
    list_sku = db_conn.get_oz_sku_card_product(client_id=client_id)
    api_user = OzonPerformanceAPI(client_id=performance_id, client_secret=client_secret)
    for ids in [company_ids[i:i + 10] for i in range(0, len(company_ids), 10)]:
        answer = await api_user.get_client_statistics_json(campaigns=ids,
                                                           date_from=from_date.isoformat(),
                                                           date_to=from_date.isoformat(),
                                                           group_by='DATE')
        uuid = answer.UUID

        link = None
        while link is None:
            await asyncio.sleep(5)
            answer_uuid = await api_user.get_client_statistics_uuid(uuid=uuid)
            link = answer_uuid.link

        answer_report = await api_user.get_client_statistics_report(uuid=uuid)
        if answer_report:
            if answer_report.result:
                for advert in answer_report.result:
                    advert_id = advert.field_id
                    for row in advert.statistic.report.rows:
                        sku = row.sku
                        if sku not in list_sku:
                            continue
                        field_date = datetime.strptime(row.date, '%d.%m.%Y').date()
                        cpc = round(float(row.avgBid.replace(',', '.')), 2)
                        sum_cost = round(float(row.moneySpent.replace(',', '.')), 2)
                        sum_price = round(float(row.ordersMoney.replace(',', '.')), 2)
                        list_statistics_advert.append(DataOzStatisticAdvert(client_id=client_id,
                                                                            date=field_date,
                                                                            advert_id=int(advert_id),
                                                                            sku=sku,
                                                                            views=int(row.views),
                                                                            clicks=int(row.clicks),
                                                                            cpc=cpc,
                                                                            sum_cost=sum_cost,
                                                                            orders_count=int(row.orders),
                                                                            sum_price=sum_price))

    logger.info(f"Количество записей: {len(list_statistics_advert)}")
    db_conn.add_oz_adverts_statistics(client_id=client_id, list_statistics_advert=list_statistics_advert)

readiness_check = {}
check_func = {'cards': True, 'adverts': True, 'stat_cards': True, 'stat_adverts': False}


async def statistic(db_conn: OzDbConnection, client: Client, date_yesterday: datetime.date):
    print(readiness_check[client.name_company])
    performance = db_conn.get_oz_performance(client_id=client.client_id)

    if not readiness_check[client.name_company]['cards']:
        await add_card_products(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key)
        readiness_check[client.name_company]['cards'] = True
        logger.info(f"{client.name_company} Сбор карточек товаров {client.name_company}")

    if not readiness_check[client.name_company]['adverts']:
        await add_adverts(db_conn=db_conn,
                          client_id=client.client_id,
                          performance_id=performance.performance_id,
                          client_secret=performance.client_secret,
                          from_date=date_yesterday)
        readiness_check[client.name_company]['adverts'] = True
        logger.info(f"{client.name_company} Сбор рекламных компаний")

    if not readiness_check[client.name_company]['stat_cards']:
        list_statistics_card_products = await get_statistics_card_products(db_conn=db_conn,
                                                                           client_id=client.client_id,
                                                                           api_key=client.api_key,
                                                                           date_from=date_yesterday)
        db_conn.add_oz_cards_products_statistics(client_id=client.client_id,
                                                 list_card_product=list_statistics_card_products)
        readiness_check[client.name_company]['stat_cards'] = True
        logger.info(f"{client.name_company} Статистика карточек товара за {date_yesterday.isoformat()}")

    if not readiness_check[client.name_company]['stat_adverts']:
        await add_statistic_adverts(db_conn=db_conn,
                                    client_id=client.client_id,
                                    performance_id=performance.performance_id,
                                    client_secret=performance.client_secret,
                                    from_date=date_yesterday)
        readiness_check[client.name_company]['stat_adverts'] = True
        logger.info(f"{client.name_company} Статистика рекламы за {date_yesterday.isoformat()}")

    if all(readiness_check[client.name_company].values()):
        readiness_check.pop(client.name_company)


async def main_oz_advert(retries: int = 6) -> None:
    try:
        db_conn = OzDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="Ozon")
        if not readiness_check:
            for client in clients:
                if client.name_company in ['Vayor']:
                    continue
                readiness_check[client.name_company] = check_func.copy()

        date_yesterday = (datetime.now() - timedelta(days=1)).date()
        tasks = []

        for client in clients:
            if client.name_company not in readiness_check.keys():
                continue
            tasks.append(statistic(db_conn=db_conn, client=client, date_yesterday=date_yesterday))
        await asyncio.gather(*tasks)

    except (OperationalError, Error):
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_oz_advert(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_oz_advert(retries=retries - 1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_oz_advert())
    loop.stop()
