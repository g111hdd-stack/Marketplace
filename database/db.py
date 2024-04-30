import urllib

from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from class_operation import Operation
from database.models import Client, OzMain, WBMain


@dataclass(frozen=True)
class ConnectionSettings:

    server: str
    database: str
    username: str
    password: str
    driver: str
    timeout: int


class AzureDbConnection:

    def __init__(self, conn_settings: ConnectionSettings, echo: bool = False) -> None:
        conn_params = urllib.parse.quote_plus(
            'Driver=%s;' % conn_settings.driver +
            'Server=tcp:%s.database.windows.net,1433;' % conn_settings.server +
            'Database=%s;' % conn_settings.database +
            'Uid=%s@%s;' % (conn_settings.username, conn_settings.server) +
            'Pwd=%s;' % conn_settings.password +
            'Encrypt=yes;' +
            'TrustServerCertificate=no;' +
            'Connection Timeout=%s;' % conn_settings.timeout
        )
        conn_string = f'mssql+pyodbc:///?odbc_connect={conn_params}'
        self.engine = create_engine(conn_string, echo=echo, pool_pre_ping=True)
        self.session = Session(self.engine)

    def add_pack_oz_main_entry(self, client_id: str, list_operations: list[Operation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами

            Args:
                client_id (str): ID кабинета.
                list_operations (list[Operation]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = OzMain(client_id=operation.client_id,
                                       accrual_date=operation.accrual_date,
                                       type_of_transaction=operation.type_of_transaction,
                                       vendor_cod=operation.vendor_cod,
                                       posting_number=operation.posting_number,
                                       delivery_schema=operation.delivery_schema,
                                       sku=operation.sku,
                                       sale=operation.sale,
                                       quantities=operation.quantities)
                self.session.add(new_operation)
            try:
                self.session.commit()
                print(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                print(f"Ошибка добавления: {e}")

    def add_pack_wb_main_entry(self, client_id: str, list_operations: list[Operation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами

            Args:
                client_id (str): ID кабинета.
                list_operations (list[Operation]): Список данных об операциях.
        """
        existing_client = self.session.query(Client).filter_by(client_id=client_id).first()
        if existing_client:
            for operation in list_operations:
                new_operation = WBMain(client_id=operation.client_id,
                                       accrual_date=operation.accrual_date,
                                       type_of_transaction=operation.type_of_transaction,
                                       vendor_cod=operation.vendor_cod,
                                       posting_number=operation.posting_number,
                                       delivery_schema=operation.delivery_schema,
                                       sku=operation.sku,
                                       sale=operation.sale,
                                       quantities=operation.quantities)
                self.session.add(new_operation)
            try:
                self.session.commit()
                print(f"Успешное добавление в базу")
            except Exception as e:
                self.session.rollback()
                print(f"Ошибка добавления: {e}")

    def get_select_client(self, marketplace: str) -> list[Client]:
        """
        Получает список клиентов, отфильтрованный по заданному рынку.

        Args:
            marketplace (str, optional): Рынок для фильтрации.. Default to'Ozon'.

        Returns:
            List[Client]: Список клиентов, удовлетворяющих условию фильтрации.
        """
        with self.session.begin():
            result = self.session.execute(select(Client).filter(Client.marketplace == marketplace)).fetchall()
            return [client[0] for client in result]
