import asyncio
import logging
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.sql import select

from .db import DbConnection
from classes import DataOperation
from .models import Client, YaMain

logger = logging.getLogger(__name__)


class YaDbConnection(DbConnection):
    def add_ya_operation(self, client_id: str, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                client_id (str): ID кабинета.
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = YaMain(client_id=operation.client_id,
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
