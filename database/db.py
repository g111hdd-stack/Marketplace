import logging
from typing import Type

from urllib.parse import quote_plus
from sqlalchemy import create_engine, desc
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from data_classes import *
from database.models import *
from config import *

logger = logging.getLogger(__name__)

conn_setting = ConnectionSettings(server=SERVER,
                                  database=DATABASE,
                                  driver=DRIVER,
                                  username=USER,
                                  password=PASSWORD,
                                  timeout=LOGIN_TIMEOUT)

DB_USER = "postgres"
DB_PASS = "216_Bogvina"
DB_HOST = "38.180.101.127:5432"
DB_NAME = "arris"
DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class DbConnection:

    def __init__(self, conn_settings: ConnectionSettings = conn_setting, echo: bool = False, postgres: bool = False) -> None:
        conn_params = quote_plus(
            'Driver=%s;' % conn_settings.driver +
            'Server=tcp:%s.database.windows.net,1433;' % conn_settings.server +
            'Database=%s;' % conn_settings.database +
            'Uid=%s@%s;' % (conn_settings.username, conn_settings.server) +
            'Pwd=%s;' % conn_settings.password +
            'Encrypt=yes;' +
            'TrustServerCertificate=no;' +
            'Connection Timeout=%s;' % conn_settings.timeout)

        conn_string = f'mssql+pyodbc:///?odbc_connect={conn_params}'
        if postgres:
            self.engine = create_engine(url=DB_URL, echo=echo, pool_pre_ping=True)
        else:
            self.engine = create_engine(url=conn_string, echo=echo, pool_pre_ping=True)
        self.session = Session(self.engine)

    def start_db(self) -> None:
        """Создание таблиц. Заполнение таблицы DateList датами от 2024-01-01 до сегодняшней."""
        with self.session.begin_nested():
            metadata.create_all(self.session.bind)

        start_date = datetime.date(year=2024, month=1, day=1)
        existing_start_date = self.session.query(DateList).filter(DateList.date == start_date).first()
        if not existing_start_date:
            self.session.add(DateList(date=start_date))
            self.session.commit()

        last_date = self.session.query(DateList).order_by(desc(DateList.date)).first()
        new_date = last_date.date
        while new_date < datetime.date.today():
            new_date += datetime.timedelta(days=1)
            self.session.add(DateList(date=new_date))
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()

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
