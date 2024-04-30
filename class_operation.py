from datetime import datetime


class Operation:
    """Данные об операции

        Args:
            client_id (str): ID кабинета.
            accrual_date (datetime.date): Дата принятия к учету.
            type_of_transaction (str): Тип операции.
            vendor_cod (str): Корпоративный артикул.
            delivery_schema (str): Схема доставки.
            posting_number (str): Номер отправления.
            sku (str): Артикул внутри системы Ozon.
            sale (float): Стоимость продажи товара.
            quantities (int): Количество.
    """

    def __init__(self, client_id: str, accrual_date: datetime.date, type_of_transaction: str, vendor_cod: str,
                 delivery_schema: str, posting_number: str, sku: str, sale: float, quantities: int):
        self.client_id = client_id
        self.accrual_date = accrual_date
        self.type_of_transaction = type_of_transaction
        self.vendor_cod = vendor_cod
        self.delivery_schema = delivery_schema
        self.posting_number = posting_number
        self.sku = sku
        self.sale = sale
        self.quantities = quantities
