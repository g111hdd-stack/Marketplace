import logging

from sqlalchemy.sql import select, delete
from sqlalchemy.dialects.postgresql import insert

from .db import DbConnection, retry_on_exception
from data_classes import DataOperation, DataSbOrders
from .models import SbMain, SbStatusOrder, SbOrders

logger = logging.getLogger(__name__)


class SbDbConnection(DbConnection):

    @retry_on_exception()
    def get_status_orders(self):
        with self.session.begin_nested():
            result = self.session.execute(select(SbStatusOrder)).fetchall()
        return [status[0].field_status for status in result]

    @retry_on_exception()
    def get_not_delivered_orders(self, client_id: str):
        with self.session.begin_nested():
            result = self.session.execute(select(SbOrders).where(SbOrders.client_id == client_id)).fetchall()
        return [order[0].posting_number for order in result]

    @retry_on_exception()
    def add_sb_operation(self, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        for row in list_operations:
            stmt = insert(SbMain).values(
                client_id=row.client_id,
                accrual_date=row.accrual_date,
                type_of_transaction=row.type_of_transaction,
                vendor_code=row.vendor_code,
                posting_number=row.posting_number,
                delivery_schema=row.delivery_schema,
                sku=row.sku,
                sale=row.sale,
                quantities=row.quantities
            ).on_conflict_do_update(
                index_elements=['accrual_date', 'type_of_transaction', 'posting_number', 'sku'],
                set_={'sale': row.sale,
                      'quantities': row.quantities}
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_sb_orders(self, list_operations: list[DataSbOrders]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                list_operations (list[DataSbOrders]): Список данных об операциях.
        """
        for operation in list_operations:
            new_operation = SbOrders(posting_number=operation.posting_number,
                                     client_id=operation.client_id,
                                     field_status=operation.field_status,
                                     date_order=operation.date_order)
            self.session.merge(new_operation)
        self.session.commit()
        logger.info(f"Успешное обновление в базе")

    @retry_on_exception()
    def delete_order_canceled(self, client_id: str):
        self.session.execute(delete(SbOrders).where(SbOrders.client_id == client_id,
                                                    SbOrders.field_status.in_(['CUSTOMER_CANCELED',
                                                                               'MERCHANT_CANCELED',
                                                                               'DELIVERED'])))
        self.session.commit()
