import logging

from sqlalchemy.dialects.postgresql import insert

from .models import *
from data_classes import *
from .db import DbConnection, retry_on_exception

logger = logging.getLogger(__name__)


class YaDbConnection(DbConnection):

    @retry_on_exception()
    def add_ya_campaigns(self, list_campaigns: list[DataYaCampaigns]) -> None:
        for campaign in list_campaigns:
            existing_client = self.session.query(Client).filter_by(client_id=campaign.client_id).first()
            if existing_client:
                new_campaign = YaCampaigns(campaign_id=campaign.campaign_id,
                                           client_id=campaign.client_id,
                                           name=campaign.name,
                                           placement_type=campaign.placement_type)
                self.session.merge(new_campaign)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_operation(self, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        for row in list_operations:
            stmt = insert(YaMain).values(
                client_id=row.client_id,
                accrual_date=row.accrual_date,
                type_of_transaction=row.type_of_transaction,
                vendor_code=row.vendor_code,
                posting_number=row.posting_number,
                delivery_schema=row.delivery_schema,
                sku=row.sku,
                sale=row.sale,
                quantities=row.quantities,
                bonus=row.bonus
            ).on_conflict_do_update(
                index_elements=['accrual_date', 'client_id', 'type_of_transaction', 'posting_number', 'sku'],
                set_={'sale': row.sale,
                      'quantities': row.quantities,
                      'bonus': row.bonus}
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_report(self, list_reports: list[DataYaReport]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                list_reports (list[DataYaReport]): Список данных об операциях.
        """
        type_services = set(self.session.query(YaTypeReport.operation_type,
                                               YaTypeReport.service).all())
        for row in list_reports:
            if (row.operation_type, row.service or '') not in type_services:
                new_type = YaTypeReport(operation_type=row.operation_type,
                                        service=row.service or '',
                                        type_name='new')
                self.session.add(new_type)
                type_services.add((row.operation_type, row.service or ''))
            stmt = insert(YaReport).values(
                client_id=row.client_id,
                campaign_id=row.campaign_id,
                posting_number=row.posting_number or '',
                operation_type=row.operation_type,
                vendor_code=row.vendor_code or '',
                service=row.service or '',
                date=row.date,
                cost=row.cost
            ).on_conflict_do_update(
                index_elements=['client_id',
                                'campaign_id',
                                'date',
                                'posting_number',
                                'vendor_code',
                                'operation_type',
                                'service'],
                set_={'cost': row.cost}
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_report_shows(self, list_reports: list[DataYaReportShows]) -> None:
        """
            Добавление в базу данных записи по бусту показов.

            Args:
                list_reports (list[DataYaReportShows]): Список данных об операциях.
        """
        for row in list_reports:
            stmt = insert(YaReportShows).values(
                client_id=row.client_id,
                date=row.date,
                vendor_code=row.vendor_code,
                name_product=row.name_product,
                shows=row.shows,
                clicks=row.clicks,
                add_to_card=row.add_to_card,
                orders_count=row.orders_count,
                cpm=row.cpm,
                cost=row.cost,
                orders_sum=row.orders_sum,
                advert_id=row.advert_id,
                name_advert=row.name_advert
            ).on_conflict_do_update(
                index_elements=['client_id',
                                'date',
                                'vendor_code',
                                'advert_id'
                                ],
                set_={'name_product': row.name_product,
                      'shows': row.shows,
                      'clicks': row.clicks,
                      'add_to_card': row.add_to_card,
                      'orders_count': row.orders_count,
                      'cpm': row.cpm,
                      'cost': row.cost,
                      'orders_sum': row.orders_sum,
                      'name_advert': row.name_advert}
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_report_consolidated(self, list_reports: list[DataYaReportConsolidated]) -> None:
        """
            Добавление в базу данных записи по бусту продаж.

            Args:
                list_reports (list[DataYaReportСonsolidated]): Список данных об операциях.
        """
        for row in list_reports:
            stmt = insert(YaReportConsolidated).values(
                client_id=row.client_id,
                date=row.date,
                vendor_code=row.vendor_code,
                name_product=row.name_product,
                boost_shows=row.boost_shows,
                total_shows=row.total_shows,
                boost_clicks=row.boost_clicks,
                total_clicks=row.total_clicks,
                boost_add_to_card=row.boost_add_to_card,
                total_add_to_card=row.total_add_to_card,
                boost_orders_count=row.boost_orders_count,
                total_orders_count=row.total_orders_count,
                boost_orders_delivered_count=row.boost_orders_delivered_count,
                total_orders_delivered_count=row.total_orders_delivered_count,
                cost=row.cost,
                bonus_cost=row.bonus_cost,
                average_cost=row.average_cost,
                boost_revenue_ratio_cost=row.boost_cost_ratio_revenue,
                boost_orders_delivered_sum=row.boost_orders_delivered_sum,
                total_orders_delivered_sum=row.total_orders_delivered_sum,
                revenue_ratio_boost_total=row.boost_revenue_ratio_total,
                advert_id=row.advert_id,
                name_advert=row.name_advert
            ).on_conflict_do_update(
                index_elements=['client_id', 'date', 'vendor_code', 'advert_id'],
                set_={
                    'name_product': row.name_product,
                    'boost_shows': row.boost_shows,
                    'total_shows': row.total_shows,
                    'boost_clicks': row.boost_clicks,
                    'total_clicks': row.total_clicks,
                    'boost_add_to_card': row.boost_add_to_card,
                    'total_add_to_card': row.total_add_to_card,
                    'boost_orders_count': row.boost_orders_count,
                    'total_orders_count': row.total_orders_count,
                    'boost_orders_delivered_count': row.boost_orders_delivered_count,
                    'total_orders_delivered_count': row.total_orders_delivered_count,
                    'cost': row.cost,
                    'bonus_cost': row.bonus_cost,
                    'average_cost': row.average_cost,
                    'boost_revenue_ratio_cost': row.boost_cost_ratio_revenue,
                    'boost_orders_delivered_sum': row.boost_orders_delivered_sum,
                    'total_orders_delivered_sum': row.total_orders_delivered_sum,
                    'revenue_ratio_boost_total': row.boost_revenue_ratio_total,
                    'name_advert': row.name_advert
                }
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_report_shelf(self, list_reports: list[DataYaReportShelf]) -> None:
        """
            Добавление в базу данных записи по бусту продаж.

            Args:
                list_reports (list[DataYaReportShelf]): Список данных об операциях.
        """
        for row in list_reports:
            stmt = insert(YaReportShelf).values(
                client_id=row.client_id,
                date=row.date,
                advert_id=row.advert_id,
                name_advert=row.name_advert,
                category=row.category,
                shows=row.shows,
                coverage=row.coverage,
                clicks=row.clicks,
                ctr=row.ctr,
                shows_frequency=row.shows_frequency,
                add_to_card=row.add_to_card,
                orders_count=row.orders_count,
                orders_conversion=row.orders_conversion,
                order_sum=row.order_sum,
                cpo=row.cpo,
                average_cost_per_mille=row.average_cost_per_mille,
                cost=row.cost,
                cpm=row.cpm,
                cost_ratio_revenue=row.cost_ratio_revenue
            ).on_conflict_do_update(
                index_elements=['client_id', 'date', 'advert_id', 'category'],
                set_={
                    'name_advert': row.name_advert,
                    'shows': row.shows,
                    'coverage': row.coverage,
                    'clicks': row.clicks,
                    'ctr': row.ctr,
                    'shows_frequency': row.shows_frequency,
                    'add_to_card': row.add_to_card,
                    'orders_count': row.orders_count,
                    'orders_conversion': row.orders_conversion,
                    'order_sum': row.order_sum,
                    'cpo': row.cpo,
                    'average_cost_per_mille': row.average_cost_per_mille,
                    'cost': row.cost,
                    'cpm': row.cpm,
                    'cost_ratio_revenue': row.cost_ratio_revenue
                }
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_report_advert_cost(self, list_reports: list[DataYaAdvertCost]) -> None:
        """
            Добавление в базу данных записи по РК.

            Args:
                list_reports (list[DataYaAdvertCost]): Список данных об операциях.
        """
        for row in list_reports:
            stmt = insert(YaAdvertCost).values(
                client_id=row.client_id,
                date=row.date,
                advert_id=row.advert_id,
                name_advert=row.name_advert,
                type_advert=row.type_advert,
                cost=row.cost,
                bonus_deducted=row.bonus_deducted
            ).on_conflict_do_update(
                index_elements=['client_id', 'date', 'advert_id', 'type_advert'],
                set_={
                    'name_advert': row.name_advert,
                    'cost': row.cost,
                    'bonus_deducted': row.bonus_deducted
                }
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_orders(self, list_orders: list[DataYaOrder]) -> None:
        """
            Добавление в базу данных записи о заказах.

            Args:
                list_orders (list[DataYaOrder]): Список данных о заказах.
        """
        for row in list_orders:
            stmt = insert(YaOrders).values(
                order_date=row.order_date,
                client_id=row.client_id,
                sku=row.sku,
                vendor_code=row.vendor_code,
                posting_number=row.posting_number,
                delivery_schema=row.delivery_schema,
                quantities=row.quantities,
                rejected=row.rejected,
                returned=row.returned,
                price=row.price,
                bonus=row.bonus,
                status=row.status,
                update_date=row.update_date
            ).on_conflict_do_update(
                index_elements=['order_date',
                                'sku',
                                'posting_number'],
                set_={'price': row.price,
                      'bonus': row.bonus,
                      'quantities': row.quantities,
                      'rejected': row.rejected,
                      'returned': row.returned,
                      'status': row.status,
                      'update_date': row.update_date,
                      }
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_stock_entry(self, list_stocks: list[DataYaStock]) -> None:
        """
            Добавление в базу данных записи о заказах.

            Args:
                list_stocks (list[DataYaStock]): Список данных о заказах.
        """
        for row in list_stocks:
            stmt = insert(YaStock).values(
                date=row.date,
                client_id=row.client_id,
                campaign_id=row.campaign_id,
                vendor_code=row.vendor_code,
                size=row.size,
                warehouse=row.warehouse,
                quantity=row.quantity,
                type=row.type
            ).on_conflict_do_nothing(
                index_elements=['client_id', 'date', 'campaign_id', 'vendor_code', 'size', 'warehouse', 'type'])
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_cards_products(self, list_card_product: list[DataYaCardProduct]) -> None:
        """
            Обновление информации о карточках товаров.

            Args:
                list_card_product (list[DataYaCardProduct]): Список данных о карточках товаров.
        """
        for row in list_card_product:
            new = YaCardProduct(sku=row.sku,
                                client_id=row.client_id,
                                vendor_code=row.vendor_code,
                                link=row.link,
                                category=row.category,
                                price=row.price,
                                discount_price=row.discount_price,
                                archived=row.archived)

            self.session.merge(new)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")
