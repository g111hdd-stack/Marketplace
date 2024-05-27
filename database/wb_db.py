import asyncio
import logging
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.sql import select

from .db import DbConnection
from classes import DataOperation, DataWBStatisticCardProduct, DataWBStatisticAdvert, DataWBProductCard, DataWBAdvert
from .models import Client, WBMain, WBAdverts, WBStatisticCardProduct, WBCardProduct, WBStatisticAdvert
from wb_sdk.wb_api import WBApi

logger = logging.getLogger(__name__)


class WBDbConnection(DbConnection):
    def add_wb_operation(self, client_id: str, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                client_id (str): ID кабинета.
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = WBMain(client_id=operation.client_id,
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

    def add_wb_adverts(self, client_id: str, adverts_list: list[DataWBAdvert]) -> None:
        """
            Обновление информации о рекламных компаниях.

            Args:
                client_id (str): ID кабинета.
                adverts_list (list[DataWBAdvert]): Список данных о рекламных компаниях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for advert in adverts_list:

                new_advert = WBAdverts(id_advert=advert.id_advert,
                                       client_id=client_id,
                                       id_type=advert.id_type,
                                       id_status=advert.id_status,
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

    def add_wb_cards_products(self, client_id: str, list_card_product: list[DataWBProductCard]) -> None:
        """
            Обновление информации о карточках товаров.

            Args:
                client_id (str): ID кабинета.
                list_card_product (list[DataWBProductCard]): Список данных о карточках товаров.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for card in list_card_product:
                new_card = WBCardProduct(sku=card.sku,
                                         client_id=client_id,
                                         vendor_code=card.vendor_code,
                                         price=card.price,
                                         discount_price=card.discount_price)

                self.session.merge(new_card)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def add_wb_adverts_statistics(self, client_id: str, product_advertising_campaign: list[DataWBStatisticAdvert]) \
            -> None:
        """
            Добавление в базу данных записи статистики рекламных компаний.

            Args:
                client_id (str): ID кабинета.
                product_advertising_campaign (list[DataWBStatisticAdvert]): Список данных статистики рекламных компаний.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for stat in product_advertising_campaign:
                existing_card = self.session.query(WBCardProduct).filter_by(sku=stat.nm_id).first()
                if existing_card:
                    new_stat = WBStatisticAdvert(sku=stat.nm_id,
                                                 advert_id=stat.advert_id,
                                                 date=stat.date,
                                                 views=stat.views,
                                                 clicks=stat.clicks,
                                                 ctr=stat.ctr,
                                                 cpc=stat.cpc,
                                                 atbs=stat.atbs,
                                                 orders_count=stat.orders_count,
                                                 shks=stat.shks,
                                                 sum_price=stat.sum_price,
                                                 sum_cost=stat.sum_cost,
                                                 appType=stat.app_type)
                    self.session.add(new_stat)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def add_wb_cards_products_statistics(self, client_id: str, list_card_product: list[DataWBStatisticCardProduct]) \
            -> None:
        """
            Добавление в базу данных записи статистики карточек товаров.

            Args:
                client_id (str): ID кабинета.
                list_card_product (list[DataWBStatisticCardProduct]): Список данных статистики карточек товаров.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for card in list_card_product:
                card_product = self.session.query(WBCardProduct).filter_by(sku=card.sku).first()
                if card_product is None:
                    api_user = WBApi(api_key=existing_client.api_key)
                    product = asyncio.run(api_user.get_list_goods_filter(filter_nm_id=int(card.sku)))
                    price = product.data.listGoods[0].sizes[0].price
                    discount_price = product.data.listGoods[0].sizes[0].discountedPrice
                    new_card = WBCardProduct(sku=card.sku,
                                             vendor_code=card.vendor_code,
                                             client_id=client_id,
                                             category=card.category,
                                             brand=card.brand,
                                             link=card.link,
                                             price=price,
                                             discount_price=discount_price)
                    self.session.merge(new_card)
                else:
                    price = card_product.price
                    discount_price = card_product.discount_price
                    if card_product.link is None:
                        new_card = WBCardProduct(sku=card.sku,
                                                 vendor_code=card.vendor_code,
                                                 client_id=client_id,
                                                 category=card.category,
                                                 brand=card.brand,
                                                 link=card.link)
                        self.session.merge(new_card)

                new_statistic_card_product = WBStatisticCardProduct(sku=card.sku,
                                                                    date=card.date,
                                                                    open_card_count=card.open_card_count,
                                                                    add_to_cart_count=card.add_to_cart_count,
                                                                    orders_count=card.orders_count,
                                                                    add_to_cart_percent=card.add_to_cart_percent,
                                                                    cart_to_order_percent=card.cart_to_order_percent,
                                                                    price=price,
                                                                    discount_price=discount_price)

                self.session.add(new_statistic_card_product)
            try:
                self.session.commit()
                logger.info(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def get_wb_adverts_id(self, client_id: str, date: datetime.date) -> list[WBAdverts]:
        """
            Получает список рекламных компаний, отфильтрованных по кабинету и дате активности.

            Args:
                client_id (str): ID кабинета.
                date (date): Дата активности.

            Returns:
                List[WBAdverts]: Список рекламных компаний, удовлетворяющих условию фильтрации.
        """
        with self.session.begin_nested():
            result = self.session.execute(select(WBAdverts).filter(and_(WBAdverts.client_id == client_id,
                                                                        or_(WBAdverts.id_status == 9,
                                                                            WBAdverts.change_time >= date)))).fetchall()
        return [advert[0].id_advert for advert in result]
