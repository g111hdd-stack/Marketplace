import logging
from typing import Type

from sqlalchemy import create_engine, desc
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from data_classes import *
from database.models import *
from config import *

logger = logging.getLogger(__name__)


class DbConnection:

    def __init__(self, echo: bool = False) -> None:
        self.engine = create_engine(url=DB_URL, echo=echo, pool_pre_ping=True)
        self.session = Session(self.engine)

    def start_db(self) -> None:
        """Создание таблиц."""
        with self.session.begin_nested():
            metadata.create_all(self.session.bind)

    def get_clients(self, marketplace: str) -> list[Client]:
        """
            Получает список клиентов, отфильтрованный по заданному рынку.

            Args:
                marketplace (str): Рынок для фильтрации.

            Returns:
                List[Client]: Список клиентов, удовлетворяющих условию фильтрации.
        """
        with self.session.begin_nested():
            result = self.session.execute(select(Client).filter(Client.marketplace == marketplace)).fetchall()
        return [client[0] for client in result]

    def get_client(self, client_id: str) -> Type[Client]:
        client = self.session.query(Client).filter_by(client_id=client_id).first()
        if client:
            return client

    def add_cost_price(self, list_cost_price: list[DataCostPrice]):
        self.session.query(CostPrice).delete()
        for row in list_cost_price:
            new_row = CostPrice(month_date=row.month_date,
                                year_date=row.year_date,
                                vendor_code=row.vendor_code,
                                cost=row.cost)
            self.session.add(new_row)
        try:
            self.session.commit()
            logger.info(f"Успешное добавление в базу")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Ошибка добавления: {e}")
