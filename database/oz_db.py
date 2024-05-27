import logging
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.sql import select

from .db import DbConnection
from classes import DataOperation, DataOzProductCard, DataOzAdvert, DataOzStatisticCardProduct, DataOzStatisticAdvert
from .models import Client, OzMain, OzCardProduct, OzAdverts, OzPerformance, OzStatisticCardProduct, OzStatisticAdvert

logger = logging.getLogger(__name__)


class OzDbConnection(DbConnection):
    def add_oz_operation(self, client_id: str, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами

            Args:
                client_id (str): ID кабинета.
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = OzMain(client_id=operation.client_id,
                                       accrual_date=operation.accrual_date,
                                       type_of_transaction=operation.type_of_transaction,
                                       vendor_code=operation.vendor_code,
                                       posting_number=operation.posting_number,
                                       delivery_schema=operation.delivery_schema,
                                       sku=operation.sku,
                                       sale=operation.sale,
                                       quantities=operation.quantities)
                self.session.add(new_operation)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def get_oz_performance(self, client_id: str) -> OzPerformance:
        """
            Получает данные реклаиного кабинета по ID кабинета Ozon.

            Args:
                client_id (str): ID кабинета Ozon.

            Returns:
                OzPerformance: Данные рекламного кабинета, удовлетворяющих условию фильтрации.
        """
        with self.session.begin_nested():
            result = self.session.execute(select(OzPerformance).filter(OzPerformance.client_id == client_id)).first()
        return result[0]

    def add_oz_adverts(self, client_id: str, adverts_list: list[DataOzAdvert]) -> None:
        """
            Обновление информации о рекламных компаниях.

            Args:
                client_id (str): ID кабинета.
                adverts_list (list[DataOzAdvert]): Список данных о рекламных компаниях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for advert in adverts_list:
                new_advert = OzAdverts(id_advert=advert.id_advert,
                                       client_id=client_id,
                                       field_type=advert.field_type,
                                       field_status=advert.field_status,
                                       name_advert=advert.name_advert,
                                       create_time=advert.create_time,
                                       change_time=advert.change_time,
                                       start_time=advert.start_time,
                                       end_time=advert.end_time)
                self.session.merge(new_advert)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def add_oz_cards_products(self, client_id: str, list_card_product: list[DataOzProductCard]) -> None:
        """
            Обновление информации о карточках товаров.

            Args:
                client_id (str): ID кабинета.
                list_card_product (list[DataOzProductCard]): Список данных о карточках товаров.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for card in list_card_product:
                new_card = OzCardProduct(sku=card.sku,
                                         client_id=client_id,
                                         vendor_code=card.vendor_code,
                                         category=card.category,
                                         brand=card.brand,
                                         link=card.link,
                                         price=card.price,
                                         discount_price=card.discount_price)

                self.session.merge(new_card)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def add_oz_cards_products_statistics(self, client_id: str, list_card_product: list[DataOzStatisticCardProduct]) \
            -> None:
        """
            Добавление в базу данных записи статистики карточек товаров.

            Args:
                client_id (str): ID кабинета.
                list_card_product (list[DataOzStatisticCardProduct]): Список данных статистики карточек товаров.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for card in list_card_product:
                card_product = self.session.query(OzCardProduct).filter_by(sku=card.sku).first()
                new_statistic_card_product = OzStatisticCardProduct(sku=card.sku,
                                                                    date=card.date,
                                                                    view_search=card.view_search,
                                                                    view_card=card.view_card,
                                                                    add_to_cart_from_search_count=card.add_to_cart_from_search_count,
                                                                    add_to_cart_from_card_count=card.add_to_cart_from_card_count,
                                                                    orders_count=card.orders_count,
                                                                    add_to_cart_from_card_percent=card.add_to_cart_from_card_percent,
                                                                    add_to_cart_from_search_percent=card.add_to_cart_from_search_percent,
                                                                    price=card_product.price,
                                                                    discount_price=card_product.discount_price)
                self.session.add(new_statistic_card_product)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def get_oz_adverts_id(self, client_id: str, date: datetime.date) -> list[str]:
        """
            Получает список рекламных компаний, отфильтрованных по кабинету и дате активности.

            Args:
                client_id (str): ID кабинета.
                date (date): Дата активности.

            Returns:
                List[str]: Список рекламных компаний, удовлетворяющих условию фильтрации.
        """
        with self.session.begin_nested():
            result = self.session.execute(select(OzAdverts).filter(and_(OzAdverts.client_id == client_id,
                                                                        or_(OzAdverts.field_status == 'CAMPAIGN_STATE_RUNNING',
                                                                            OzAdverts.change_time >= date)))).fetchall()
        return [str(advert[0].id_advert) for advert in result]

    def add_oz_adverts_statistics(self, client_id: str, list_statistics_advert: list[DataOzStatisticAdvert]) \
            -> None:
        """
            Добавление в базу данных записи статистики рекламных компаний.

            Args:
                client_id (str): ID кабинета.
                list_statistics_advert (list[DataOzStatisticAdvert]): Список данных статистики рекламных компаний.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for stat in list_statistics_advert:
                new_stat = OzStatisticAdvert(sku=stat.sku,
                                             advert_id=stat.advert_id,
                                             date=stat.date,
                                             views=stat.views,
                                             clicks=stat.clicks,
                                             cpc=stat.cpc,
                                             orders_count=stat.orders_count,
                                             sum_price=stat.sum_price,
                                             sum_cost=stat.sum_cost)
                self.session.add(new_stat)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def get_oz_sku_card_product(self, client_id: str) -> list[str]:
        """
            Получает список SKU товаров, отфильтрованных по кабинету.

            Args:
                client_id (str): ID кабинета.

            Returns:
                List[str]: Список SKU товаров, удовлетворяющих условию фильтрации.
        """
        with self.session.begin_nested():
            result = self.session.execute(select(OzCardProduct).filter(OzCardProduct.client_id == client_id)).fetchall()
        return [card_product[0].sku for card_product in result]
