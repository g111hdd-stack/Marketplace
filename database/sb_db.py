import logging

from sqlalchemy.sql import select, delete

from .db import DbConnection
from data_classes import DataOperation, DataSbOrders
from .models import Client, SbMain, SbStatusOrder, SbOrders

logger = logging.getLogger(__name__)


class SbDbConnection(DbConnection):

    def get_status_orders(self):
        with self.session.begin_nested():
            result = self.session.execute(select(SbStatusOrder)).fetchall()
        return [status[0].field_status for status in result]

    def get_not_delivered_orders(self, client_id: str):
        with self.session.begin_nested():
            result = self.session.execute(select(SbOrders).where(SbOrders.client_id == client_id)).fetchall()
        return [order[0].posting_number for order in result]

    def add_sb_operation(self, client_id: str, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                client_id (str): ID кабинета.
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = SbMain(client_id=operation.client_id,
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

    def add_sb_orders(self, client_id: str, list_operations: list[DataSbOrders]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                client_id (str): ID кабинета.
                list_operations (list[DataSbOrders]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = SbOrders(posting_number=operation.posting_number,
                                         client_id=operation.client_id,
                                         field_status=operation.field_status,
                                         date_order=operation.date_order)
                self.session.merge(new_operation)
            try:
                self.session.commit()
                logger.info(f"Успешное обновление в базе")
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка добавления: {e}")

    def delete_order_canceled(self, client_id: str):
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            self.session.execute(delete(SbOrders).where(SbOrders.client_id == client_id,
                                                        SbOrders.field_status.in_(['CUSTOMER_CANCELED',
                                                                                   'MERCHANT_CANCELED',
                                                                                   'DELIVERED'])))
            try:
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                logger.error(f"Ошибка при удалении: {e}")
